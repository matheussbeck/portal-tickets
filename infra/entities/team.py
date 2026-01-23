from sqlalchemy import ForeignKey, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

from infra.configs.database import Base


class Area(PyEnum):
    EAB = "eab"
    PROJETOS = "projetos"
    CIA = "cia"
    INDICADORES = "indicadores"


class TeamStatus(PyEnum):
    """Status operacional do time (diferente de active que é soft delete)"""
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    REESTRUTURACAO = "reestruturacao"


class Team(Base):
    """
    Entidade de Time/Equipe.

    Relacionamentos:
    - N-1: manager (User) - gerente do time
    - 1-N: team_members (User), team_reports (Report), team_projects (Project)
    - N-N: assigned_tickets (Ticket via TicketTeam)
    """
    __tablename__ = "teams"

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    team_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    team_description: Mapped[str | None] = mapped_column(String, nullable=True, init=False)

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    team_area: Mapped[Area] = mapped_column(Enum(Area), nullable=False)
    team_status: Mapped[TeamStatus] = mapped_column(
        Enum(TeamStatus),
        default=TeamStatus.ATIVO,
        init=False
    )

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    team_manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", use_alter=True, name="fk_team_manager", ondelete="RESTRICT"),
        nullable=True,
        init=False
    )

    # =========================================================================
    # EXTRAS
    # =========================================================================
    team_location: Mapped[str | None] = mapped_column(String, nullable=True, init=False)
    team_cost_center: Mapped[str | None] = mapped_column(String, nullable=True, init=False)

    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================

    # N - 1 (Time tem um gerente)
    manager: Mapped["User | None"] = relationship(
        foreign_keys=[team_manager_id],
        back_populates="managed_team",
        lazy="raise",
        init=False
    )
    # 1 - N (Time tem muitos membros/reports/projects)
    team_members: Mapped[list["User"]] = relationship(
        foreign_keys="[User.user_team_id]",
        back_populates="team",
        lazy="raise",
        init=False,
        default_factory=list
    )
    team_reports: Mapped[list["Report"]] = relationship(
        back_populates="team",
        lazy="raise",
        init=False,
        default_factory=list
    )
    team_projects: Mapped[list["Project"]] = relationship(
        back_populates="team_responsible",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # N - N (via tabelas de associação)
    assigned_tickets: Mapped[list["TicketTeam"]] = relationship(
        back_populates="team",
        lazy="raise",
        init=False,
        default_factory=list
    )

    def __repr__(self) -> str:
        return f"<Team(id={self.id}, team_name='{self.team_name}', team_area='{self.team_area}')>"
