from sqlalchemy import ForeignKey, Integer, Double, String, Boolean, DateTime, Date, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
import enum

from infra.configs.database import Base


class ProjectStatus(enum.Enum):
    ATIVO = "ativo"
    ABERTO = "aberto"
    PENDENTE = "pendente"
    PAUSADO = "pausado"
    ENCERRADO = "encerrado"
    CANCELADO = "cancelado"


class ProjectTags(enum.Enum):
    ATRIBUIDO = "atribuido"
    ATRASADO = "atrasado"
    NO_PRAZO = "no_prazo"


class ProjectPriority(enum.Enum):
    MAXIMA = "maxima"
    URGENTE = "urgente"
    NORMAL = "normal"
    BACKLOG = "backlog"


class ProjectRiskLevel(enum.Enum):
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
    project_approvers_count: Mapped[int] = mapped_column(Integer, default=0)

    # =========================================================================
    # CONFIGURAÇÕES
    # =========================================================================
    project_public: Mapped[bool] = mapped_column(Boolean, default=True)

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

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'project_name': self.project_name,
            'project_directory': self.project_directory,
            'project_description': self.project_description,
            'project_category': self.project_category,
            'project_methodology': self.project_methodology,
            'project_tags': self.project_tags.value if self.project_tags else None,
            'project_priority': self.project_priority.value if self.project_priority else None,
            'project_risk_level': self.project_risk_level.value if self.project_risk_level else None,
            'project_team_responsible_id': self.project_team_responsible_id,
            'project_manager_id': self.project_manager_id,
            'project_status': self.project_status.value if self.project_status else None,
            'project_status_changed_at': self.project_status_changed_at.isoformat() if self.project_status_changed_at else None,
            'project_status_changed_by_id': self.project_status_changed_by_id,
            'project_start_date': self.project_start_date.isoformat() if self.project_start_date else None,
            'project_expected_end_date': self.project_expected_end_date.isoformat() if self.project_expected_end_date else None,
            'project_approved_at': self.project_approved_at.isoformat() if self.project_approved_at else None,
            'project_real_end_date': self.project_real_end_date.isoformat() if self.project_real_end_date else None,
            'project_planned_budget': self.project_planned_budget,
            'project_approved_budget': self.project_approved_budget,
            'project_spent_budget': self.project_spent_budget,
            'project_final_budget': self.project_final_budget,
            'project_completion_percentage': self.project_completion_percentage,
            'project_approvers_count': self.project_approvers_count,
            'project_public': self.project_public,
            'project_scope': self.project_scope,
            'project_expected_benefits': self.project_expected_benefits,
            'project_risks': self.project_risks,
            'project_assumptions': self.project_assumptions,
            'project_constraints': self.project_constraints,
            'project_milestones': self.project_milestones,
            'project_tasks': self.project_tasks,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'deleted_by': self.deleted_by,
            'active': self.active.value if self.active else None
        }

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, project_name='{self.project_name}', project_status='{self.project_status}')>"
