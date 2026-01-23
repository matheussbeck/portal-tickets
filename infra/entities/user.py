from sqlalchemy import ForeignKey, Integer, String, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

from infra.configs.database import Base, Status

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from infra.entities.team import Team
    from infra.entities.message import Message
    from infra.entities.ticket import Ticket
    from infra.entities.report import Report

class UserRole(PyEnum):
    ADMINISTRADOR = "administrador"
    GESTOR = "gestor"
    N2 = "especialista"
    N1 = "atendente"  
    USER = "user"


class UserTipo(PyEnum):
    ATENDENTE = "atendente"
    SOLICITANTE = "solicitante"
    ADMINISTRADOR = "administrador"


class UserStatus(PyEnum):
    """Status operacional do usuário (diferente de active que é soft delete)"""
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    BLOQUEADO = "bloqueado"
    FERIAS = "ferias"
    AFASTADO = "afastado"


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
    user_role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False)
    user_tipo: Mapped[UserTipo] = mapped_column(
        Enum(UserTipo), nullable=False)
    user_status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus),
        default=UserStatus.ATIVO,
        init=False
    )

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
    team: Mapped["Team"] = relationship(
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
        init=False,
        default=None
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

    # 1 - N (Usuário envio mensagens)
    messages_sent: Mapped[list["Message"]] = relationship(
        foreign_keys="[Message.message_user_id]",
        back_populates="user",
        lazy="raise",
        init=False,
        default_factory=list
    )

    report_status_changed: Mapped[list["Report"]] = relationship(
        foreign_keys="[Report.report_status_changed_by_id]",
        back_populates="status_changed_by",
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

    def __repr__(self) -> str:
        return f"<User(id={self.id}, user_full_name='{self.user_full_name}', user_email='{self.user_email}')>"

    @property
    def is_admin(self) -> bool:
        """Verifica se usuario e admin."""
        return self.user_role == UserRole.ADMIN

    @property
    def is_active_and_available(self) -> bool:
        """Verifica se usuario esta ativo E disponivel para trabalho."""
        return (
            self.active == Status.ATIVO and
            self.user_status == UserStatus.ATIVO
        )

    @property
    def display_name(self) -> str:
        """Retorna primeiro nome para exibicao."""
        full_name = self.user_full_name.split()
        first_last_name = f"{full_name[0]} {full_name[-1]}"
        return first_last_name if self.user_full_name else ""