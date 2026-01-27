from sqlalchemy import ForeignKey, String, Boolean, DateTime, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum as PyEnum

from infra.configs.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from infra.entities.team import Team
    from infra.entities.user import User
    from infra.entities.ticket import Ticket
    from infra.entities.associations import ReportAllowedUser, UserReportFollow


class ReportFrequency(PyEnum):
    """
    Frequência de atualização dos dados do relatório.

    Define quando os dados são atualizados:
    - DIARIO: Atualização diária (geralmente de madrugada)
    - HORARIO: Atualização a cada hora
    - AGENDADO: Atualização em horários específicos
    - SOB_DEMANDA: Atualização manual quando necessário
    """
    DIARIO = "diario"
    HORARIO = "horario"
    AGENDADO = "agendado"
    SOB_DEMANDA = "sob_demanda"


class ReportStatus(PyEnum):
    """
    Status operacional do relatório.

    Indica a situação para os usuários:
    - ATIVO: Funcionando normalmente, dados confiáveis
    - MANUTENCAO: Em manutenção programada
    - DESATUALIZADO: Dados podem estar defasados
    - TESTE: Em fase de testes, não usar em produção
    - INATIVO: Desativado, não utilizar
    - DESENVOLVIMENTO: Sendo desenvolvido
    - DIAGNOSTICO: Em análise de problemas
    """
    ATIVO = "ativo"
    MANUTENCAO = "manutencao"
    DESATUALIZADO = "desatualizado"
    TESTE = "teste"
    INATIVO = "inativo"
    DESENVOLVIMENTO = "desenvolvimento"
    DIAGNOSTICO = "diagnostico"


class ReportTags(PyEnum):
    """
    Tags de classificação por área/departamento.

    Define o público-alvo principal:
    - CIA: Central de Inteligência e Analytics
    - CCT: Centro de Controle Técnico
    - PRODUCAO: Área de Produção
    - SSMA: Segurança, Saúde e Meio Ambiente
    - CCO: Centro de Controle Operacional
    - MANUTENCAO: Área de Manutenção
    - QUALIDADE: Área de Qualidade
    """
    CIA = "cia"
    CCT = "cct"
    PRODUCAO = "producao"
    SSMA = "ssma"
    CCO = "cco"
    MANUTENCAO = "manutencao"
    QUALIDADE = "qualidade"


class Report(Base):
    """
    Entidade de Relatório (Power BI).

    Representa um relatório/dashboard do Power BI com metadados,
    responsáveis e controle de acesso.

    Relacionamentos:
        N-1 (Report pertence a):
            - team: Time responsável pelo relatório
            - owner: Usuário dono/responsável principal
            - status_changed_by: Último usuário que alterou status

        1-N (Report possui muitos):
            - report_tickets: Tickets relacionados ao relatório

        N-N (via tabelas de associação):
            - allowed_users: Usuários com acesso (se não público)
            - followers: Usuários seguindo o relatório

    Índices:
        - ix_reports_team_status: Relatórios por time e status
        - ix_reports_owner: Relatórios de um dono
        - ix_reports_tags: Relatórios por tag/área

    Exemplo de Instanciação (Template Construtor):
        ```python
        # Campos OBRIGATÓRIOS no construtor:
        report = Report(
            report_name="Dashboard de Vendas",
            report_link="https://app.powerbi.com/...",
            report_description="Análise diária de vendas...",
            report_frequency=ReportFrequency.DIARIO,
            report_tags=ReportTags.CIA,
            report_status=ReportStatus.ATIVO,
            report_team_responsible_id=1,    # FK para Team
            report_owner_id=1,               # FK para User
            report_public=True               # Visível para todos
        )

        # Campos OPCIONAIS (têm init=False):
        # - report_status_changed_by_id: Preenchido no workflow
        # - report_status_changed_at: Data da última alteração
        # - report_data_last_update: Última atualização dos dados
        # - report_pbix_last_update: Última publicação do arquivo
        # - report_dataset_source: Fonte de dados
        ```
    """
    __tablename__ = "reports"

    # Índices compostos para queries frequentes
    __table_args__ = (
        Index('ix_reports_team_status', 'report_team_responsible_id', 'report_status'),
        Index('ix_reports_owner', 'report_owner_id'),
        Index('ix_reports_tags', 'report_tags'),
    )

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    report_name: Mapped[str] = mapped_column(
        String, unique=True, nullable=False,
        doc="Nome único do relatório"
    )
    report_link: Mapped[str] = mapped_column(
        String, unique=True, nullable=False,
        doc="URL do relatório no Power BI Service"
    )
    report_description: Mapped[str] = mapped_column(
        String, nullable=False,
        doc="Descrição do propósito e conteúdo do relatório"
    )

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    report_frequency: Mapped[ReportFrequency] = mapped_column(
        Enum(ReportFrequency),
        nullable=False,
        doc="Frequência de atualização dos dados (DIARIO, HORARIO, etc.)"
    )
    report_tags: Mapped[ReportTags] = mapped_column(
        Enum(ReportTags),
        doc="Tag de área/departamento (CIA, CCT, PRODUCAO, etc.)"
    )

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    report_team_responsible_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False,
        doc="FK para Team responsável pelo relatório"
    )
    report_owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        doc="FK para User dono/responsável principal"
    )
    report_status_changed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        init=False,
        doc="FK para User que fez última alteração de status"
    )

    # =========================================================================
    # STATUS
    # =========================================================================
    report_status: Mapped[ReportStatus] = mapped_column(
        Enum(ReportStatus), nullable=False,
        doc="Status operacional do relatório"
    )
    report_status_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False,
        doc="Data/hora da última alteração de status"
    )

    # =========================================================================
    # DATAS
    # =========================================================================
    report_data_last_update: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        init=False,
        doc="Data/hora da última atualização dos dados (refresh)"
    )
    report_pbix_last_update: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        init=False,
        doc="Data/hora da última publicação do arquivo .pbix"
    )

    # =========================================================================
    # CONFIGURAÇÕES
    # =========================================================================
    report_public: Mapped[bool] = mapped_column(
        Boolean, default=True,
        doc="Se True, visível para todos. Se False, apenas allowed_users"
    )

    # =========================================================================
    # EXTRAS
    # =========================================================================
    report_dataset_source: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        init=False,
        doc="Fonte de dados principal (ex: 'SAP', 'Oracle', 'SQL Server')"
    )

    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================

    # N - 1 (Report pertence a Team/User)
    team: Mapped["Team"] = relationship(
        foreign_keys=[report_team_responsible_id],
        back_populates="team_reports",
        lazy="raise",
        init=False
    )
    owner: Mapped["User"] = relationship(
        foreign_keys=[report_owner_id],
        back_populates="user_reports",
        lazy="raise",
        init=False
    )
    status_changed_by: Mapped["User | None"] = relationship(
        foreign_keys=[report_status_changed_by_id],
        back_populates= "report_status_changed",
        lazy="raise",
        init=False
    )

    # 1 - N (Report tem muitos tickets)
    report_tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="report",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # N - N (via tabelas de associação)
    allowed_users: Mapped[list["ReportAllowedUser"]] = relationship(
        back_populates="report",
        lazy="raise",
        init=False,
        default_factory=list
    )
    followers: Mapped[list["UserReportFollow"]] = relationship(
        back_populates="report",
        lazy="raise",
        init=False,
        default_factory=list
    )

    def __repr__(self) -> str:
        return f"<Report(id={self.id}, report_name='{self.report_name}', report_status='{self.report_status}')>"
