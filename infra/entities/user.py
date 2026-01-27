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
    from infra.entities.project import Project
    from infra.entities.associations import (
        ProjectApproval, ProjectAnalyst, ProjectSponsor, ProjectOwner,
        ProjectClient, ProjectAllowedUser, TicketAttendant,
        ReportAllowedUser, UserReportFollow, UserProjectFollow, UserTicketFollow
    )


class UserRole(PyEnum):
    """
    Papel/cargo do usuário no sistema.

    Define o nível de acesso e responsabilidades:
    - ADMINISTRADOR: Acesso total ao sistema
    - GESTOR: Gerencia equipes e projetos
    - N2: Especialista técnico (segundo nível)
    - N1: Atendente de primeiro nível
    - USER: Usuário comum (solicitante)
    """
    ADMINISTRADOR = "administrador"
    GESTOR = "gestor"
    N2 = "especialista"
    N1 = "atendente"
    USER = "user"


class UserTipo(PyEnum):
    """
    Tipo de perfil do usuário.

    Define como o usuário interage com o sistema:
    - ATENDENTE: Recebe e processa tickets
    - SOLICITANTE: Abre tickets (cliente interno)
    - ADMINISTRADOR: Configura e gerencia o sistema
    """
    ATENDENTE = "atendente"
    SOLICITANTE = "solicitante"
    ADMINISTRADOR = "administrador"


class UserStatus(PyEnum):
    """
    Status operacional do usuário (diferente de active que é soft delete).

    Indica a disponibilidade do usuário para trabalho:
    - ATIVO: Disponível para receber atribuições
    - SUSPENSO: Temporariamente impedido (disciplinar)
    - BLOQUEADO: Acesso bloqueado (segurança)
    - FERIAS: Em período de férias
    - AFASTADO: Licença médica ou outras ausências
    """
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    BLOQUEADO = "bloqueado"
    FERIAS = "ferias"
    AFASTADO = "afastado"


class User(Base):
    """
    Entidade de Usuário - Central do sistema.

    Esta é a entidade mais conectada do sistema, relacionando-se com
    praticamente todas as outras entidades direta ou indiretamente.

    Relacionamentos:
        N-1 (User pertence a):
            - team: Time ao qual o usuário pertence

        1-N (User possui muitos):
            - managed_team: Time que o usuário gerencia (se for gestor)
            - user_reports: Relatórios que o usuário é dono
            - managed_projects: Projetos que o usuário gerencia
            - tickets_created: Tickets abertos pelo usuário
            - messages_sent: Mensagens enviadas pelo usuário

        N-N (via tabelas de associação):
            - analyst_projects: Projetos onde atua como analista
            - attended_tickets: Tickets atendidos
            - followed_reports/projects/tickets: Entidades seguidas

    Índices:
        - ix_users_email: Busca por email (único)
        - ix_users_corporative_id: Busca por ID corporativo (único)
        - ix_users_team_role: Busca por time + papel (listagem de equipe)
        - ix_users_status_active: Filtro por status operacional + soft delete

    Exemplo de Instanciação (Template Construtor):
        ```python
        # Campos OBRIGATÓRIOS no construtor (não têm init=False):
        user = User(
            user_corporative_id=12345,       # ID do sistema corporativo
            user_full_name="João Silva",     # Nome completo
            user_email="joao@empresa.com",   # Email único
            user_password="hash_senha",      # Senha (já hasheada!)
            user_team_id=1,                  # FK para Team
            user_role=UserRole.N1,           # Papel no sistema
            user_tipo=UserTipo.ATENDENTE     # Tipo de perfil
        )

        # Campos OPCIONAIS (têm init=False, preenchidos automaticamente ou depois):
        # - id: autoincrement
        # - user_photo: None por padrão
        # - user_status: UserStatus.ATIVO por padrão
        # - user_notification_preferences: None por padrão
        # - created_at, updated_at: preenchidos pelo banco
        # - active: Status.ATIVO por padrão (da Base)
        ```
    """
    __tablename__ = "users"

    # Índices compostos para queries frequentes
    __table_args__ = (
        Index('ix_users_team_role', 'user_team_id', 'user_role'),
        Index('ix_users_status_active', 'user_status', 'active'),
    )

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    user_corporative_id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False,
        doc="ID único do sistema corporativo (integração RH)"
    )
    user_full_name: Mapped[str] = mapped_column(
        String, nullable=False,
        doc="Nome completo do usuário"
    )
    user_email: Mapped[str] = mapped_column(
        String, unique=True, nullable=False,
        doc="Email corporativo (usado para login)"
    )
    user_password: Mapped[str] = mapped_column(
        String, nullable=False,
        doc="Hash da senha (bcrypt). NUNCA armazenar texto plano!"
    )
    user_photo: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="URL ou path da foto de perfil"
    )

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    user_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False,
        doc="FK para Team. RESTRICT impede deletar time com usuários"
    )

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    user_role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), nullable=False,
        doc="Papel/cargo que define nível de acesso (ADMIN, GESTOR, N2, N1, USER)"
    )
    user_tipo: Mapped[UserTipo] = mapped_column(
        Enum(UserTipo), nullable=False,
        doc="Tipo de perfil: ATENDENTE (processa), SOLICITANTE (abre), ADMINISTRADOR"
    )
    user_status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus),
        default=UserStatus.ATIVO,
        init=False,
        doc="Status operacional (disponibilidade). Diferente de 'active' (soft delete)"
    )

    # =========================================================================
    # CONFIGURAÇÕES
    # =========================================================================
    user_notification_preferences: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        init=False,
        doc="JSON com preferências de notificação (email, push, etc.)"
    )

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
        """Verifica se usuário é administrador."""
        return self.user_role == UserRole.ADMINISTRADOR

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