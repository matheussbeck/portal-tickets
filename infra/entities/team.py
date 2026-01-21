from sqlalchemy import ForeignKey, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from infra.configs.database import Base


class Area(enum.Enum):
    EAB = "eab"
    PROJETOS = "projetos"
    CIA = "cia"
    INDICADORES = "indicadores"


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

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    team_manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
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

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'team_name': self.team_name,
            'team_description': self.team_description,
            'team_area': self.team_area.value if self.team_area else None,
            'team_manager_id': self.team_manager_id,
            'team_location': self.team_location,
            'team_cost_center': self.team_cost_center,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'deleted_by': self.deleted_by,
            'active': self.active.value if self.active else None
        }

    def __repr__(self) -> str:
        return f"<Team(id={self.id}, team_name='{self.team_name}', team_area='{self.team_area}')>"
