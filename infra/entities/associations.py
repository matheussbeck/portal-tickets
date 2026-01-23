"""
Tabelas de Associação N-N para o Portal de Chamados

Este arquivo contém todas as tabelas de associação para relacionamentos N-N.
Algumas são tabelas simples (apenas FKs), outras têm atributos extras.

Organização:
1. Enums para status de aprovação
2. ProjectApproval - Sistema de aprovação com workflow
3. Associações Project ↔ User (analysts, sponsors, owners, clients, allowed_users)
4. Associações Ticket ↔ User/Team (attendants, teams)
5. Associações Report ↔ User (allowed_users)
6. Tabelas de Follow (user follows report/project/ticket)
"""

from sqlalchemy import ForeignKey, Integer, String, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum as PyEnum

from infra.configs.database import Base


# =============================================================================
# ENUMS
# =============================================================================

class ApprovalStatus(PyEnum):
    """Status de aprovação individual de um aprovador"""
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"


# =============================================================================
# SISTEMA DE APROVAÇÃO DE PROJETOS
# =============================================================================

class ProjectApproval(Base):
    """
    Sistema de aprovação de projetos com workflow.
    Permite múltiplos aprovadores em sequência, cada um com seu próprio status.

    Exemplo de uso:
        - Projeto precisa de 3 aprovações: Gerente -> Diretor -> VP
        - Cada um aprova em ordem (approval_order: 1, 2, 3)
        - Aprovação do próximo só é liberada após anterior aprovar
    """
    __tablename__ = "project_approvals"

    # Identificação do projeto e aprovador
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="RESTRICT"),
        nullable=False
    )
    approver_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Ordem na sequência de aprovação (1 = primeiro aprovador)
    approval_order: Mapped[int] = mapped_column(Integer, nullable=False)

    # Status individual deste aprovador
    status: Mapped[ApprovalStatus] = mapped_column(
        Enum(ApprovalStatus),
        default=ApprovalStatus.PENDENTE
    )

    # Data/hora da aprovação/rejeição (preenchido quando status muda)
    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False
    )

    # Comentários do aprovador (obrigatório em caso de rejeição)
    comments: Mapped[str | None] = mapped_column(String, nullable=True, init=False)

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="approvals", lazy="raise", init=False)
    approver: Mapped["User"] = relationship(back_populates="project_approvals", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'project_id': self.project_id,
            'approver_id': self.approver_id,
            'approval_order': self.approval_order,
            'status': self.status.value if self.status else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'comments': self.comments,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<ProjectApproval(project_id={self.project_id}, approver_id={self.approver_id}, order={self.approval_order}, status={self.status})>"


# =============================================================================
# ASSOCIAÇÕES PROJECT ↔ USER
# =============================================================================

class ProjectAnalyst(Base):
    """Analistas atribuídos a um projeto"""
    __tablename__ = "project_analysts"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="RESTRICT"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="analysts", lazy="raise", init=False)
    user: Mapped["User"] = relationship(back_populates="analyst_projects", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None
        }

    def __repr__(self) -> str:
        return f"<ProjectAnalyst(project_id={self.project_id}, user_id={self.user_id})>"


class ProjectSponsor(Base):
    """Patrocinadores de um projeto"""
    __tablename__ = "project_sponsors"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="RESTRICT"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="sponsors", lazy="raise", init=False)
    user: Mapped["User"] = relationship(back_populates="sponsored_projects", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id
        }

    def __repr__(self) -> str:
        return f"<ProjectSponsor(project_id={self.project_id}, user_id={self.user_id})>"


class ProjectOwner(Base):
    """Donos/responsáveis de um projeto"""
    __tablename__ = "project_owners"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="RESTRICT"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="owners", lazy="raise", init=False)
    user: Mapped["User"] = relationship(back_populates="owned_projects", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id
        }

    def __repr__(self) -> str:
        return f"<ProjectOwner(project_id={self.project_id}, user_id={self.user_id})>"


class ProjectClient(Base):
    """Clientes de um projeto"""
    __tablename__ = "project_clients"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="RESTRICT"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="clients", lazy="raise", init=False)
    user: Mapped["User"] = relationship(back_populates="client_projects", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id
        }

    def __repr__(self) -> str:
        return f"<ProjectClient(project_id={self.project_id}, user_id={self.user_id})>"


class ProjectAllowedUser(Base):
    """Usuários com permissão de acesso a um projeto (além dos públicos)"""
    __tablename__ = "project_allowed_users"

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="RESTRICT"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="allowed_users", lazy="raise", init=False)
    user: Mapped["User"] = relationship(back_populates="allowed_projects", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id
        }

    def __repr__(self) -> str:
        return f"<ProjectAllowedUser(project_id={self.project_id}, user_id={self.user_id})>"


# =============================================================================
# ASSOCIAÇÕES TICKET ↔ USER/TEAM
# =============================================================================

class TicketAttendant(Base):
    """Atendentes/responsáveis atribuídos a um ticket"""
    __tablename__ = "ticket_attendants"

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="RESTRICT"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )

    # Relationships
    ticket: Mapped["Ticket"] = relationship(back_populates="attendants", lazy="raise", init=False)
    user: Mapped["User"] = relationship(back_populates="attended_tickets", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'user_id': self.user_id,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None
        }

    def __repr__(self) -> str:
        return f"<TicketAttendant(ticket_id={self.ticket_id}, user_id={self.user_id})>"


class TicketTeam(Base):
    """Times atribuídos a um ticket"""
    __tablename__ = "ticket_teams"

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="RESTRICT"),
        nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )

    # Relationships
    ticket: Mapped["Ticket"] = relationship(back_populates="teams", lazy="raise", init=False)
    team: Mapped["Team"] = relationship(back_populates="assigned_tickets", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'ticket_id': self.ticket_id,
            'team_id': self.team_id,
            'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None
        }

    def __repr__(self) -> str:
        return f"<TicketTeam(ticket_id={self.ticket_id}, team_id={self.team_id})>"


# =============================================================================
# ASSOCIAÇÕES REPORT ↔ USER
# =============================================================================

class ReportAllowedUser(Base):
    """Usuários com permissão de acesso a um relatório (além dos públicos)"""
    __tablename__ = "report_allowed_users"

    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id", ondelete="RESTRICT"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Relationships
    report: Mapped["Report"] = relationship(back_populates="allowed_users", lazy="raise", init=False)
    user: Mapped["User"] = relationship(back_populates="allowed_reports", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'report_id': self.report_id,
            'user_id': self.user_id
        }

    def __repr__(self) -> str:
        return f"<ReportAllowedUser(report_id={self.report_id}, user_id={self.user_id})>"


# =============================================================================
# TABELAS DE FOLLOW (Usuário segue entidades)
# =============================================================================

class UserReportFollow(Base):
    """Usuário segue um relatório para receber notificações"""
    __tablename__ = "user_report_follows"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    report_id: Mapped[int] = mapped_column(
        ForeignKey("reports.id", ondelete="RESTRICT"),
        nullable=False
    )
    followed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="followed_reports", lazy="raise", init=False)
    report: Mapped["Report"] = relationship(back_populates="followers", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'report_id': self.report_id,
            'followed_at': self.followed_at.isoformat() if self.followed_at else None
        }

    def __repr__(self) -> str:
        return f"<UserReportFollow(user_id={self.user_id}, report_id={self.report_id})>"


class UserProjectFollow(Base):
    """Usuário segue um projeto para receber notificações"""
    __tablename__ = "user_project_follows"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="RESTRICT"),
        nullable=False
    )
    followed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="followed_projects", lazy="raise", init=False)
    project: Mapped["Project"] = relationship(back_populates="followers", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'followed_at': self.followed_at.isoformat() if self.followed_at else None
        }

    def __repr__(self) -> str:
        return f"<UserProjectFollow(user_id={self.user_id}, project_id={self.project_id})>"


class UserTicketFollow(Base):
    """Usuário segue um ticket para receber notificações"""
    __tablename__ = "user_ticket_follows"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="RESTRICT"),
        nullable=False
    )
    followed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="followed_tickets", lazy="raise", init=False)
    ticket: Mapped["Ticket"] = relationship(back_populates="followers", lazy="raise", init=False)

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'ticket_id': self.ticket_id,
            'followed_at': self.followed_at.isoformat() if self.followed_at else None
        }

    def __repr__(self) -> str:
        return f"<UserTicketFollow(user_id={self.user_id}, ticket_id={self.ticket_id})>"
