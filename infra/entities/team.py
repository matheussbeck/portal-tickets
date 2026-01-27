from sqlalchemy import ForeignKey, Integer, String, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

from infra.configs.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from infra.entities.user import User
    from infra.entities.report import Report
    from infra.entities.project import Project
    from infra.entities.associations import TicketTeam


class Area(PyEnum):
    """
    Área de atuação do time.

    Define o departamento/setor:
    - EAB: Escritório de Análise de Business
    - PROJETOS: Gestão de Projetos
    - CIA: Central de Inteligência e Analytics
    - INDICADORES: Indicadores e Métricas
    """
    EAB = "eab"
    PROJETOS = "projetos"
    CIA = "cia"
    INDICADORES = "indicadores"


class TeamStatus(PyEnum):
    """
    Status operacional do time (diferente de active que é soft delete).

    Indica a situação do time para atribuição de trabalho:
    - ATIVO: Operando normalmente, pode receber demandas
    - SUSPENSO: Temporariamente sem receber demandas
    - REESTRUTURACAO: Em processo de reorganização
    """
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    REESTRUTURACAO = "reestruturacao"


class Team(Base):
    """
    Entidade de Time/Equipe.

    Agrupa usuários por área de atuação e responsabilidades.
    Cada time tem um gerente opcional e pode ser responsável por
    projetos, relatórios e tickets.

    Relacionamentos:
        N-1 (Team pertence a):
            - manager: Usuário que gerencia o time (opcional)

        1-N (Team possui muitos):
            - team_members: Usuários que pertencem ao time
            - team_reports: Relatórios sob responsabilidade do time
            - team_projects: Projetos do time

        N-N (via tabelas de associação):
            - assigned_tickets: Tickets atribuídos ao time (via TicketTeam)

    Índices:
        - ix_teams_name: Nome do time (único)
        - ix_teams_area_status: Filtro por área + status operacional

    Exemplo de Instanciação (Template Construtor):
        ```python
        # Campos OBRIGATÓRIOS no construtor:
        team = Team(
            team_name="Analytics BI",      # Nome único do time
            team_area=Area.CIA             # Área de atuação
        )

        # Campos OPCIONAIS (têm init=False):
        # - id: autoincrement
        # - team_description: None por padrão
        # - team_status: TeamStatus.ATIVO por padrão
        # - team_manager_id: None por padrão (definido depois)
        # - team_location: None
        # - team_cost_center: None
        # - created_at, updated_at: preenchidos pelo banco
        # - active: Status.ATIVO por padrão (da Base)
        ```
    """
    __tablename__ = "teams"

    # Índices compostos para queries frequentes
    __table_args__ = (
        Index('ix_teams_area_status', 'team_area', 'team_status'),
    )

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    team_name: Mapped[str] = mapped_column(
        String, unique=True, nullable=False,
        doc="Nome único do time (ex: 'Analytics BI', 'Projetos TI')"
    )
    team_description: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="Descrição das responsabilidades e escopo do time"
    )

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    team_area: Mapped[Area] = mapped_column(
        Enum(Area), nullable=False,
        doc="Área/departamento do time (EAB, PROJETOS, CIA, INDICADORES)"
    )
    team_status: Mapped[TeamStatus] = mapped_column(
        Enum(TeamStatus),
        default=TeamStatus.ATIVO,
        init=False,
        doc="Status operacional. Diferente de 'active' (soft delete)"
    )

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    team_manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", use_alter=True, name="fk_team_manager", ondelete="RESTRICT"),
        nullable=True,
        init=False,
        doc="FK para User (gerente). use_alter evita dependência circular"
    )

    # =========================================================================
    # EXTRAS
    # =========================================================================
    team_location: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="Localização física do time (prédio, andar)"
    )
    team_cost_center: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="Centro de custo para alocação financeira"
    )

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
