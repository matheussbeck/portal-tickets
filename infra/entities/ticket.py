from sqlalchemy import ForeignKey, Integer, Double, String, Boolean, DateTime, Date, func, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from enum import Enum as PyEnum

from infra.configs.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from infra.entities.user import User
    from infra.entities.form import Form
    from infra.entities.project import Project
    from infra.entities.report import Report
    from infra.entities.chat import Chat
    from infra.entities.associations import TicketAttendant, TicketTeam, UserTicketFollow


class TicketClasse(PyEnum):
    """
    Classe do ticket - indica a que tipo de entidade se refere.

    Define o contexto do chamado:
    - PROJETO: Chamado relacionado a um projeto
    - RELATORIO: Chamado relacionado a um relatório Power BI
    """
    PROJETO = "projeto"
    RELATORIO = "relatorio"


class TicketTipo(PyEnum):
    """
    Tipo de solicitação do ticket.

    Define a natureza do trabalho:
    - ALTERACAO: Mudança em funcionalidade existente
    - BUG: Correção de erro/defeito
    - CORRECAO: Ajuste de dados ou configuração
    - DESENVOLVIMENTO: Nova funcionalidade
    - MELHORIA: Otimização ou enhancement
    """
    ALTERACAO = "alteracao"
    BUG = "bug"
    CORRECAO = "correcao"
    DESENVOLVIMENTO = "desenvolvimento"
    MELHORIA = "melhoria"


class TicketStatus(PyEnum):
    """
    Status do ciclo de vida do ticket.

    Workflow típico: ABERTO → ATIVO → PENDENTE/PAUSADO → ENCERRADO
    - ATIVO: Em atendimento
    - ABERTO: Aguardando atribuição
    - PENDENTE: Aguardando resposta do cliente
    - PAUSADO: Temporariamente suspenso
    - ENCERRADO: Finalizado com sucesso
    - CANCELADO: Cancelado sem resolução
    """
    ATIVO = "ativo"
    ABERTO = "aberto"
    PENDENTE = "pendente"
    PAUSADO = "pausado"
    ENCERRADO = "encerrado"
    CANCELADO = "cancelado"


class TicketTags(PyEnum):
    """
    Tags de estado do ticket (calculadas automaticamente).

    Indicadores visuais:
    - ATRIBUIDO: Tem atendente designado
    - ATRASADO: Passou do prazo (deadline)
    - NO_PRAZO: Dentro do prazo esperado
    """
    ATRIBUIDO = "atribuido"
    ATRASADO = "atrasado"
    NO_PRAZO = "no_prazo"


class TicketPriority(PyEnum):
    """
    Prioridade de atendimento do ticket.

    Define a ordem de atendimento:
    - MAXIMA: Crítico, atender imediatamente (SLA 4h)
    - URGENTE: Alta prioridade (SLA 8h)
    - NORMAL: Prioridade padrão (SLA 24h)
    - BACKLOG: Baixa prioridade, quando possível
    """
    MAXIMA = "maxima"
    URGENTE = "urgente"
    NORMAL = "normal"
    BACKLOG = "backlog"


class TicketImpacto(PyEnum):
    """
    Nível de impacto do problema/solicitação.

    Avalia consequências:
    - MUITO_ALTO: Parada total de produção
    - ALTO: Processo crítico afetado
    - MEDIO: Processo importante afetado
    - BAIXO: Impacto limitado
    - SEM_IMPACTO: Melhoria, sem urgência
    """
    MUITO_ALTO = "muito_alto"
    ALTO = "alto"
    MEDIO = "medio"
    BAIXO = "baixo"
    SEM_IMPACTO = "sem_impacto"


class Ticket(Base):
    """
    Entidade de Ticket (Chamado).

    Representa uma solicitação de trabalho, podendo ser relacionada
    a um projeto ou relatório. Tem ciclo de vida com status,
    prioridade, atendentes e comunicação via chat.

    Relacionamentos:
        N-1 (Ticket pertence a):
            - client: Usuário que abriu o ticket
            - form: Template de formulário usado
            - project: Projeto relacionado (se ticket_class=PROJETO)
            - report: Relatório relacionado (se ticket_class=RELATORIO)
            - status_changed_by: Último usuário que alterou status
            - closed_by: Usuário que encerrou o ticket

        1-1 (Ticket possui um):
            - chat: Container de mensagens do ticket

        N-N (via tabelas de associação):
            - attendants: Atendentes designados (via TicketAttendant)
            - teams: Times responsáveis (via TicketTeam)
            - followers: Usuários seguindo (via UserTicketFollow)

    Índices:
        - ix_tickets_client_status: Busca tickets de um cliente por status
        - ix_tickets_project: Tickets de um projeto
        - ix_tickets_report: Tickets de um relatório
        - ix_tickets_status_priority: Fila de atendimento (status + prioridade)

    Exemplo de Instanciação (Template Construtor):
        ```python
        # Campos OBRIGATÓRIOS no construtor:
        ticket = Ticket(
            ticket_title="Erro no relatório de vendas",
            ticket_description="O filtro de data não está funcionando...",
            ticket_class=TicketClasse.RELATORIO,
            ticket_type=TicketTipo.BUG,
            ticket_status=TicketStatus.ABERTO,
            ticket_client_id=1,        # FK para User (quem abriu)
            ticket_form_id=1           # FK para Form (template usado)
        )

        # Campos OPCIONAIS (têm init=False):
        # - ticket_project_id / ticket_report_id: Definir um deles conforme ticket_class
        # - ticket_priority, ticket_impact: Definidos na triagem
        # - ticket_deadline: Calculado baseado em prioridade/SLA
        # - ticket_status_changed_by_id, ticket_closed_by_id: Preenchidos no workflow
        # - ticket_estimated_hours, ticket_actual_hours: Para métricas
        # - ticket_satisfaction_rating: Avaliação do cliente (1-10)
        ```
    """
    __tablename__ = "tickets"

    # Índices compostos para queries frequentes
    __table_args__ = (
        Index('ix_tickets_client_status', 'ticket_client_id', 'ticket_status'),
        Index('ix_tickets_project', 'ticket_project_id'),
        Index('ix_tickets_report', 'ticket_report_id'),
        Index('ix_tickets_status_priority', 'ticket_status', 'ticket_priority'),
    )

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    ticket_title: Mapped[str] = mapped_column(
        String, nullable=False,
        doc="Título resumido do ticket (máx 200 caracteres recomendado)"
    )
    ticket_description: Mapped[str] = mapped_column(
        String, nullable=False,
        doc="Descrição detalhada do problema ou solicitação"
    )

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    ticket_class: Mapped[TicketClasse] = mapped_column(
        Enum(TicketClasse), nullable=False,
        doc="Classe: PROJETO ou RELATORIO (define o contexto)"
    )
    ticket_type: Mapped[TicketTipo] = mapped_column(
        Enum(TicketTipo), nullable=False,
        doc="Tipo de solicitação (BUG, MELHORIA, ALTERACAO, etc.)"
    )
    ticket_priority: Mapped[TicketPriority | None] = mapped_column(
        Enum(TicketPriority),
        nullable=True,
        init=False,
        doc="Prioridade de atendimento (definida na triagem)"
    )
    ticket_impact: Mapped[TicketImpacto | None] = mapped_column(
        Enum(TicketImpacto),
        nullable=True,
        init=False,
        doc="Nível de impacto no negócio (definido na triagem)"
    )

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    ticket_client_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        doc="FK para User que abriu o ticket (solicitante)"
    )
    ticket_form_id: Mapped[int] = mapped_column(
        ForeignKey("forms.id", ondelete="RESTRICT"),
        nullable=False,
        doc="FK para Form (template de formulário usado)"
    )
    # Relacionamento polimórfico: ticket pode ser de projeto OU relatório
    ticket_project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="RESTRICT"),
        nullable=True,
        init=False,
        doc="FK para Project (se ticket_class=PROJETO)"
    )
    ticket_report_id: Mapped[int | None] = mapped_column(
        ForeignKey("reports.id", ondelete="RESTRICT"),
        nullable=True,
        init=False,
        doc="FK para Report (se ticket_class=RELATORIO)"
    )
    ticket_status_changed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        init=False,
        doc="FK para User que fez última alteração de status"
    )
    ticket_closed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        init=False,
        doc="FK para User que encerrou o ticket"
    )

    # =========================================================================
    # STATUS
    # =========================================================================
    ticket_status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus), nullable=False,
        doc="Status atual do ciclo de vida do ticket"
    )
    ticket_status_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False,
        doc="Data/hora da última alteração de status"
    )

    # =========================================================================
    # DATAS
    # =========================================================================
    ticket_deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False,
        doc="Prazo para conclusão (calculado baseado em SLA)"
    )
    ticket_closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False,
        doc="Data/hora do encerramento do ticket"
    )
    ticket_mail_sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False,
        doc="Data/hora do último email de notificação enviado"
    )

    # =========================================================================
    # MÉTRICAS
    # =========================================================================
    ticket_estimated_hours: Mapped[float | None] = mapped_column(
        Double, nullable=True, init=False,
        doc="Horas estimadas para conclusão (estimativa inicial)"
    )
    ticket_actual_hours: Mapped[float | None] = mapped_column(
        Double, nullable=True, init=False,
        doc="Horas reais gastas (preenchido no encerramento)"
    )
    ticket_satisfaction_rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        init=False,
        doc="Avaliação de satisfação do cliente (escala 1-10)"
    )

    # =========================================================================
    # EXTRAS
    # =========================================================================
    ticket_attachments: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="JSON array com URLs/paths dos anexos"
    )
    ticket_resolution_notes: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="Notas de resolução (preenchido pelo atendente no encerramento)"
    )

    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================

    # N - 1 (Ticket pertence a User/Form/Project/Report)
    client: Mapped["User"] = relationship(
        back_populates="tickets_created",
        lazy="raise",
        foreign_keys=[ticket_client_id],
        init=False
    )
    form: Mapped["Form"] = relationship(
        back_populates="tickets",
        lazy="raise",
        foreign_keys=[ticket_form_id],
        init=False
    )
    project: Mapped["Project | None"] = relationship(
        back_populates="tickets",
        lazy="raise",
        foreign_keys=[ticket_project_id],
        init=False
    )
    report: Mapped["Report | None"] = relationship(
        back_populates="report_tickets",
        lazy="raise",
        foreign_keys=[ticket_report_id],
        init=False
    )
    status_changed_by: Mapped["User | None"] = relationship(
        back_populates="tickets_status_changed",
        lazy="raise",
        foreign_keys=[ticket_status_changed_by_id],
        init=False
    )
    closed_by: Mapped["User | None"] = relationship(
        back_populates="tickets_closed",
        lazy="raise",
        foreign_keys=[ticket_closed_by_id],
        init=False
    )

    # 1 - 1 (Ticket tem um Chat)
    chat: Mapped["Chat | None"] = relationship(
        back_populates="ticket",
        lazy="raise",
        uselist=False,
        init=False
    )

    # N - N (via tabelas de associação)
    attendants: Mapped[list["TicketAttendant"]] = relationship(
        back_populates="ticket",
        lazy="raise",
        init=False,
        default_factory=list
    )
    teams: Mapped[list["TicketTeam"]] = relationship(
        back_populates="ticket",
        lazy="raise",
        init=False,
        default_factory=list
    )
    followers: Mapped[list["UserTicketFollow"]] = relationship(
        back_populates="ticket",
        lazy="raise",
        init=False,
        default_factory=list
    )

    def __repr__(self) -> str:
        return f"<Ticket(id={self.id}, ticket_title='{self.ticket_title}', ticket_status='{self.ticket_status}')>"
