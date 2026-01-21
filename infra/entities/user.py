from sqlalchemy import ForeignKey, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from infra.configs.database import Base


class UserRoles(enum.Enum):
    N1 = "atendente"
    N2 = "solicitante"
    GESTOR = "gestor"
    ADMINISTRADOR = "administrador"


class UserTipo(enum.Enum):
    ATENDENTE = "atendente"
    SOLICITANTE = "solicitante"
    ADMINISTRADOR = "administrador"


class User(Base):
    """
    Entidade de Usuário.

    Relacionamentos:
    - N-1: team (Team)
    - 1-N: user_reports (Report como owner), managed_team (Team como gerente),
           managed_projects (Project), tickets_created, etc.
    - N-N: via tabelas de associação (analyst_projects, attended_tickets, etc.)
    """
    __tablename__ = "users"

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    user_corporative_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    user_full_name: Mapped[str] = mapped_column(String, nullable=False)
    user_email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    user_password: Mapped[str] = mapped_column(String, nullable=False)
    user_photo: Mapped[str | None] = mapped_column(String, nullable=True, init=False)

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    user_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False
    )

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    user_role: Mapped[UserRoles] = mapped_column(Enum(UserRoles), nullable=False)
    user_tipo: Mapped[UserTipo] = mapped_column(Enum(UserTipo), nullable=False)

    # =========================================================================
    # CONFIGURAÇÕES
    # =========================================================================
    user_notification_preferences: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        init=False
    )  # JSON

    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================

    # N - 1 (Usuário pertence a um time)
    team: Mapped["Team | None"] = relationship(
        foreign_keys=[user_team_id],
        back_populates="team_members",
        lazy="raise",
        init=False
    )

    # 1 - N (Usuário gerencia um time)
    managed_team: Mapped["Team | None"] = relationship(
        foreign_keys="[Team.team_manager_id]",
        back_populates="manager",
        uselist=False,
        lazy="raise",
        init=False
    )

    # 1 - N (Usuário é dono de reports)
    user_reports: Mapped[list["Report"]] = relationship(
        foreign_keys="[Report.report_owner_id]",
        back_populates="owner",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # 1 - N (Usuário é gerente de projetos)
    managed_projects: Mapped[list["Project"]] = relationship(
        foreign_keys="[Project.project_manager_id]",
        back_populates="manager",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # 1 - N (Usuário alterou status de projetos)
    projects_status_changed: Mapped[list["Project"]] = relationship(
        foreign_keys="[Project.project_status_changed_by_id]",
        back_populates="status_changed_by",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # 1 - N (Usuário criou tickets)
    tickets_created: Mapped[list["Ticket"]] = relationship(
        foreign_keys="[Ticket.ticket_client_id]",
        back_populates="client",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # 1 - N (Usuário alterou status de tickets)
    tickets_status_changed: Mapped[list["Ticket"]] = relationship(
        foreign_keys="[Ticket.ticket_status_changed_by_id]",
        back_populates="status_changed_by",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # 1 - N (Usuário fechou tickets)
    tickets_closed: Mapped[list["Ticket"]] = relationship(
        foreign_keys="[Ticket.ticket_closed_by_id]",
        back_populates="closed_by",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # N - N (via tabelas de associação - Project)
    project_approvals: Mapped[list["ProjectApproval"]] = relationship(
        back_populates="approver",
        lazy="raise",
        init=False,
        default_factory=list
    )
    analyst_projects: Mapped[list["ProjectAnalyst"]] = relationship(
        back_populates="user",
        lazy="raise",
        init=False,
        default_factory=list
    )
    sponsored_projects: Mapped[list["ProjectSponsor"]] = relationship(
        back_populates="user",
        lazy="raise",
        init=False,
        default_factory=list
    )
    owned_projects: Mapped[list["ProjectOwner"]] = relationship(
        back_populates="user",
        lazy="raise",
        init=False,
        default_factory=list
    )
    client_projects: Mapped[list["ProjectClient"]] = relationship(
        back_populates="user",
        lazy="raise",
        init=False,
        default_factory=list
    )
    allowed_projects: Mapped[list["ProjectAllowedUser"]] = relationship(
        back_populates="user",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # N - N (via tabelas de associação - Ticket)
    attended_tickets: Mapped[list["TicketAttendant"]] = relationship(
        back_populates="user",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # N - N (via tabelas de associação - Report)
    allowed_reports: Mapped[list["ReportAllowedUser"]] = relationship(
        back_populates="user",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # N - N (via tabelas de follow)
    followed_reports: Mapped[list["UserReportFollow"]] = relationship(
        back_populates="user",
        lazy="raise",
        init=False,
        default_factory=list
    )
    followed_projects: Mapped[list["UserProjectFollow"]] = relationship(
        back_populates="user",
        lazy="raise",
        init=False,
        default_factory=list
    )
    followed_tickets: Mapped[list["UserTicketFollow"]] = relationship(
        back_populates="user",
        lazy="raise",
        init=False,
        default_factory=list
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_corporative_id': self.user_corporative_id,
            'user_full_name': self.user_full_name,
            'user_email': self.user_email,
            'user_photo': self.user_photo,
            'user_team_id': self.user_team_id,
            'user_role': self.user_role.value if self.user_role else None,
            'user_tipo': self.user_tipo.value if self.user_tipo else None,
            'user_notification_preferences': self.user_notification_preferences,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'deleted_by': self.deleted_by,
            'active': self.active.value if self.active else None
        }

    def __repr__(self) -> str:
        return f"<User(id={self.id}, user_full_name='{self.user_full_name}', user_email='{self.user_email}')>"

