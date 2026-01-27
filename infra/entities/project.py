from sqlalchemy import ForeignKey, Integer, Double, String, Boolean, DateTime, Date, func, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from enum import Enum as PyEnum

from infra.configs.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from infra.entities.team import Team
    from infra.entities.user import User
    from infra.entities.ticket import Ticket
    from infra.entities.associations import (
        ProjectApproval, ProjectAnalyst, ProjectSponsor,
        ProjectOwner, ProjectClient, ProjectAllowedUser, UserProjectFollow
    )


class ProjectStatus(PyEnum):
    """
    Status do ciclo de vida do projeto.

    Workflow: ABERTO → ATIVO → PENDENTE/PAUSADO → ENCERRADO
    - ATIVO: Em execução
    - ABERTO: Aguardando aprovação ou início
    - PENDENTE: Aguardando decisão externa
    - PAUSADO: Temporariamente suspenso
    - ENCERRADO: Finalizado com sucesso
    - CANCELADO: Cancelado sem conclusão
    """
    ATIVO = "ativo"
    ABERTO = "aberto"
    PENDENTE = "pendente"
    PAUSADO = "pausado"
    ENCERRADO = "encerrado"
    CANCELADO = "cancelado"


class ProjectTags(PyEnum):
    """
    Tags de estado do projeto (calculadas automaticamente).

    Indicadores visuais de prazo:
    - ATRIBUIDO: Tem responsáveis designados
    - ATRASADO: Passou da data esperada de término
    - NO_PRAZO: Dentro do cronograma
    """
    ATRIBUIDO = "atribuido"
    ATRASADO = "atrasado"
    NO_PRAZO = "no_prazo"


class ProjectPriority(PyEnum):
    """
    Prioridade de execução do projeto.

    Define a alocação de recursos:
    - MAXIMA: Projeto crítico, prioridade máxima
    - URGENTE: Alta prioridade
    - NORMAL: Prioridade padrão
    - BACKLOG: Baixa prioridade, recursos quando disponíveis
    """
    MAXIMA = "maxima"
    URGENTE = "urgente"
    NORMAL = "normal"
    BACKLOG = "backlog"


class ProjectRiskLevel(PyEnum):
    """
    Nível de risco do projeto.

    Avalia exposição a problemas:
    - MUITO_ALTO: Risco crítico, requer atenção constante
    - ALTO: Risco significativo
    - MEDIO: Risco moderado
    - BAIXO: Risco controlado
    - SEM_RISCO: Projeto de baixa complexidade
    """
    MUITO_ALTO = "muito_alto"
    ALTO = "alto"
    MEDIO = "medio"
    BAIXO = "baixo"
    SEM_RISCO = "sem_risco"


class Project(Base):
    """
    Entidade de Projeto.

    Representa uma iniciativa com escopo, cronograma, orçamento e
    sistema de aprovação por múltiplos níveis hierárquicos.

    Relacionamentos:
        N-1 (Project pertence a):
            - team_responsible: Time responsável pela execução
            - manager: Usuário gerente do projeto
            - status_changed_by: Último usuário que alterou status

        1-N (Project possui muitos):
            - tickets: Chamados relacionados ao projeto
            - approvals: Aprovações de múltiplos níveis

        N-N (via tabelas de associação):
            - analysts: Analistas do projeto
            - sponsors: Patrocinadores
            - owners: Donos do produto
            - clients: Clientes internos
            - allowed_users: Usuários com acesso (se não público)
            - followers: Usuários seguindo o projeto

    Índices:
        - ix_projects_team_status: Projetos por time e status
        - ix_projects_manager: Projetos de um gerente
        - ix_projects_dates: Projetos por período

    Exemplo de Instanciação (Template Construtor):
        ```python
        # Campos OBRIGATÓRIOS no construtor:
        project = Project(
            project_name="Portal de Chamados v2",
            project_directory="/projetos/portal-chamados",
            project_description="Modernização do sistema...",
            project_tags=ProjectTags.NO_PRAZO,
            project_status=ProjectStatus.ABERTO,
            project_team_responsible_id=1,   # FK para Team
            project_manager_id=1,            # FK para User
            project_start_date=date(2024, 1, 1),
            project_expected_end_date=date(2024, 6, 30),
            project_planned_budget=50000.00
        )

        # Campos OPCIONAIS (têm init=False):
        # - project_category, project_methodology: Classificação adicional
        # - project_priority, project_risk_level: Definidos na análise
        # - project_approved_at, project_real_end_date: Preenchidos no workflow
        # - project_approved_budget, project_spent_budget, project_final_budget
        # - project_completion_percentage: Atualizado durante execução
        # - project_public: True por padrão
        # - project_scope, project_risks, etc.: Documentação JSON
        ```
    """
    __tablename__ = "projects"

    # Índices compostos para queries frequentes
    __table_args__ = (
        Index('ix_projects_team_status', 'project_team_responsible_id', 'project_status'),
        Index('ix_projects_manager', 'project_manager_id'),
        Index('ix_projects_dates', 'project_start_date', 'project_expected_end_date'),
    )

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    project_name: Mapped[str] = mapped_column(
        String, nullable=False, unique=True,
        doc="Nome único do projeto"
    )
    project_directory: Mapped[str] = mapped_column(
        String, nullable=False, unique=True,
        doc="Caminho único para armazenamento de arquivos"
    )
    project_description: Mapped[str] = mapped_column(
        String, nullable=False,
        doc="Descrição detalhada do projeto e objetivos"
    )

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    project_category: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="Categoria do projeto (ex: 'Infraestrutura', 'Analytics')"
    )
    project_methodology: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="Metodologia de gestão (ex: 'Scrum', 'Kanban', 'Waterfall')"
    )
    project_tags: Mapped[ProjectTags] = mapped_column(
        Enum(ProjectTags), nullable=False,
        doc="Tag de estado do prazo (ATRIBUIDO, ATRASADO, NO_PRAZO)"
    )
    project_priority: Mapped[ProjectPriority | None] = mapped_column(
        Enum(ProjectPriority), nullable=True, init=False,
        doc="Prioridade de execução (definida na análise inicial)"
    )
    project_risk_level: Mapped[ProjectRiskLevel | None] = mapped_column(
        Enum(ProjectRiskLevel), nullable=True, init=False,
        doc="Nível de risco avaliado (definido na análise)"
    )

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    project_team_responsible_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False,
        doc="FK para Team responsável pela execução"
    )
    project_manager_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        doc="FK para User gerente do projeto"
    )
    project_status_changed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        init=False,
        doc="FK para User que fez última alteração de status"
    )

    # =========================================================================
    # STATUS
    # =========================================================================
    project_status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), nullable=False,
        doc="Status atual do ciclo de vida do projeto"
    )
    project_status_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False,
        doc="Data/hora da última alteração de status"
    )

    # =========================================================================
    # DATAS
    # =========================================================================
    project_start_date: Mapped[date] = mapped_column(
        Date, nullable=False,
        doc="Data de início planejada"
    )
    project_expected_end_date: Mapped[date] = mapped_column(
        Date, nullable=False,
        doc="Data de término esperada (baseline)"
    )
    project_approved_at: Mapped[date | None] = mapped_column(
        Date, nullable=True, init=False,
        doc="Data em que todas as aprovações foram concluídas"
    )
    project_real_end_date: Mapped[date | None] = mapped_column(
        Date, nullable=True, init=False,
        doc="Data real de término (preenchida no encerramento)"
    )

    # =========================================================================
    # VALORES / ORÇAMENTO
    # =========================================================================
    project_planned_budget: Mapped[float] = mapped_column(
        Double, nullable=False,
        doc="Orçamento planejado inicial (em R$)"
    )
    project_approved_budget: Mapped[float | None] = mapped_column(
        Double, nullable=True, init=False,
        doc="Orçamento aprovado após análise (em R$)"
    )
    project_spent_budget: Mapped[float | None] = mapped_column(
        Double, nullable=True, init=False,
        doc="Valor gasto até o momento (atualizado periodicamente)"
    )
    project_final_budget: Mapped[float | None] = mapped_column(
        Double, nullable=True, init=False,
        doc="Custo final realizado (preenchido no encerramento)"
    )

    # =========================================================================
    # MÉTRICAS
    # =========================================================================
    project_completion_percentage: Mapped[float | None] = mapped_column(
        Double,
        nullable=True,
        init=False,
        default=0.0,
        doc="Percentual de conclusão (0.0 a 100.0)"
    )
    project_approvers_count: Mapped[int] = mapped_column(
        Integer, default=0, init=False,
        doc="Número de aprovadores necessários (calculado)"
    )

    # =========================================================================
    # CONFIGURAÇÕES
    # =========================================================================
    project_public: Mapped[bool] = mapped_column(
        Boolean, default=True, init=False,
        doc="Se True, visível para todos. Se False, apenas allowed_users"
    )

    # =========================================================================
    # DOCUMENTAÇÃO (JSON)
    # =========================================================================
    project_scope: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="JSON com definição de escopo (incluído/excluído)"
    )
    project_expected_benefits: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="JSON com benefícios esperados"
    )
    project_risks: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="JSON com riscos identificados e mitigações"
    )
    project_assumptions: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="JSON com premissas do projeto"
    )
    project_constraints: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="JSON com restrições e limitações"
    )
    project_milestones: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="JSON com marcos/entregas principais"
    )
    project_tasks: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="JSON com lista de tarefas/atividades"
    )

    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================

    # N - 1 (Projeto pertence a um Team/User)
    team_responsible: Mapped["Team"] = relationship(
        back_populates="team_projects",
        lazy="raise",
        foreign_keys=[project_team_responsible_id],
        init=False
    )
    manager: Mapped["User"] = relationship(
        back_populates="managed_projects",
        lazy="raise",
        foreign_keys=[project_manager_id],
        init=False
    )
    status_changed_by: Mapped["User | None"] = relationship(
        back_populates="projects_status_changed",
        lazy="raise",
        foreign_keys=[project_status_changed_by_id],
        init=False
    )

    # 1 - N (Projeto tem muitos tickets/approvals)
    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="project",
        lazy="raise",
        init=False,
        default_factory=list
    )
    approvals: Mapped[list["ProjectApproval"]] = relationship(
        back_populates="project",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # N - N (via tabelas de associação)
    analysts: Mapped[list["ProjectAnalyst"]] = relationship(
        back_populates="project",
        lazy="raise",
        init=False,
        default_factory=list
    )
    sponsors: Mapped[list["ProjectSponsor"]] = relationship(
        back_populates="project",
        lazy="raise",
        init=False,
        default_factory=list
    )
    owners: Mapped[list["ProjectOwner"]] = relationship(
        back_populates="project",
        lazy="raise",
        init=False,
        default_factory=list
    )
    clients: Mapped[list["ProjectClient"]] = relationship(
        back_populates="project",
        lazy="raise",
        init=False,
        default_factory=list
    )
    allowed_users: Mapped[list["ProjectAllowedUser"]] = relationship(
        back_populates="project",
        lazy="raise",
        init=False,
        default_factory=list
    )
    followers: Mapped[list["UserProjectFollow"]] = relationship(
        back_populates="project",
        lazy="raise",
        init=False,
        default_factory=list
    )


    def __repr__(self) -> str:
        return f"<Project(id={self.id}, project_name='{self.project_name}', project_status='{self.project_status}')>"
