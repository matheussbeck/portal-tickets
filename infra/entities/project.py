from sqlalchemy import ForeignKey, Integer, Double, String, Boolean, DateTime, Date, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from enum import Enum as PyEnum

from infra.configs.database import Base


class ProjectStatus(PyEnum):
    ATIVO = "ativo"
    ABERTO = "aberto"
    PENDENTE = "pendente"
    PAUSADO = "pausado"
    ENCERRADO = "encerrado"
    CANCELADO = "cancelado"


class ProjectTags(PyEnum):
    ATRIBUIDO = "atribuido"
    ATRASADO = "atrasado"
    NO_PRAZO = "no_prazo"


class ProjectPriority(PyEnum):
    MAXIMA = "maxima"
    URGENTE = "urgente"
    NORMAL = "normal"
    BACKLOG = "backlog"


class ProjectRiskLevel(PyEnum):
    MUITO_ALTO = "muito_alto"
    ALTO = "alto"
    MEDIO = "medio"
    BAIXO = "baixo"
    SEM_RISCO = "sem_risco"


class Project(Base):
    """
    Entidade de Projeto.

    Relacionamentos:
    - N-1: team_responsible (Team), manager (User), status_changed_by (User)
    - 1-N: tickets, approvals
    - N-N: analysts, sponsors, owners, clients, allowed_users, followers
    """
    __tablename__ = "projects"

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    project_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    project_directory: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    project_description: Mapped[str] = mapped_column(String, nullable=False)

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    project_category: Mapped[str | None] = mapped_column(String, nullable=True, init=False)
    project_methodology: Mapped[str | None] = mapped_column(String, nullable=True, init=False)
    project_tags: Mapped[ProjectTags] = mapped_column(Enum(ProjectTags), nullable=False)
    project_priority: Mapped[ProjectPriority | None] = mapped_column(Enum(ProjectPriority), nullable=True, init=False)
    project_risk_level: Mapped[ProjectRiskLevel | None] = mapped_column(Enum(ProjectRiskLevel), nullable=True, init=False)

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    project_team_responsible_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False
    )
    project_manager_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    project_status_changed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        init=False
    )

    # =========================================================================
    # STATUS
    # =========================================================================
    project_status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), nullable=False)
    project_status_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False
    )

    # =========================================================================
    # DATAS
    # =========================================================================
    project_start_date: Mapped[date] = mapped_column(Date, nullable=False)
    project_expected_end_date: Mapped[date] = mapped_column(Date, nullable=False)
    project_approved_at: Mapped[date | None] = mapped_column(Date, nullable=True, init=False)
    project_real_end_date: Mapped[date | None] = mapped_column(Date, nullable=True, init=False)

    # =========================================================================
    # VALORES / ORÇAMENTO
    # =========================================================================
    project_planned_budget: Mapped[float] = mapped_column(Double, nullable=False)
    project_approved_budget: Mapped[float | None] = mapped_column(Double, nullable=True, init=False)
    project_spent_budget: Mapped[float | None] = mapped_column(Double, nullable=True, init=False)
    project_final_budget: Mapped[float | None] = mapped_column(Double, nullable=True, init=False)

    # =========================================================================
    # MÉTRICAS
    # =========================================================================
    project_completion_percentage: Mapped[float | None] = mapped_column(
        Double,
        nullable=True,
        init=False,
        default=0.0
    )
    project_approvers_count: Mapped[int] = mapped_column(Integer, default=0, init=False)

    # =========================================================================
    # CONFIGURAÇÕES
    # =========================================================================
    project_public: Mapped[bool] = mapped_column(Boolean, default=True, init=False)

    # =========================================================================
    # DOCUMENTAÇÃO (JSON)
    # =========================================================================
    project_scope: Mapped[str | None] = mapped_column(String, nullable=True, init=False)
    project_expected_benefits: Mapped[str | None] = mapped_column(String, nullable=True, init=False)
    project_risks: Mapped[str | None] = mapped_column(String, nullable=True, init=False)
    project_assumptions: Mapped[str | None] = mapped_column(String, nullable=True, init=False)
    project_constraints: Mapped[str | None] = mapped_column(String, nullable=True, init=False)
    project_milestones: Mapped[str | None] = mapped_column(String, nullable=True, init=False)
    project_tasks: Mapped[str | None] = mapped_column(String, nullable=True, init=False)

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
