from sqlalchemy import ForeignKey, Integer, Double, String, Boolean, DateTime, Date, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
import enum

from infra.configs.database import Base


class TicketClasse(enum.Enum):
    PROJETO = "projeto"
    RELATORIO = "relatorio"


class TicketTipo(enum.Enum):
    ALTERACAO = "alteracao"
    BUG = "bug"
    CORRECAO = "correcao"
    DESENVOLVIMENTO = "desenvolvimento"
    MELHORIA = "melhoria"


class TicketStatus(enum.Enum):
    ATIVO = "ativo"
    ABERTO = "aberto"
    PENDENTE = "pendente"
    PAUSADO = "pausado"
    ENCERRADO = "encerrado"
    CANCELADO = "cancelado"


class TicketTags(enum.Enum):
    ATRIBUIDO = "atribuido"
    ATRASADO = "atrasado"
    NO_PRAZO = "no_prazo"


class TicketPriority(enum.Enum):
    MAXIMA = "maxima"
    URGENTE = "urgente"
    NORMAL = "normal"
    BACKLOG = "backlog"


class TicketImpacto(enum.Enum):
    MUITO_ALTO = "muito_alto"
    ALTO = "alto"
    MEDIO = "medio"
    BAIXO = "baixo"
    SEM_IMPACTO = "sem_impacto"


class Ticket(Base):
    """
    Entidade de Ticket (Chamado).

    Relacionamentos:
    - N-1: client (User), form (Form), project (Project), report (Report),
           status_changed_by (User), closed_by (User)
    - 1-N: chat, messages (via chat)
    - N-N: attendants (User), teams (Team), followers (User)
    """
    __tablename__ = "tickets"

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    ticket_title: Mapped[str] = mapped_column(String, nullable=False)
    ticket_description: Mapped[str] = mapped_column(String, nullable=False)

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    ticket_class: Mapped[TicketClasse] = mapped_column(Enum(TicketClasse), nullable=False)
    ticket_type: Mapped[TicketTipo] = mapped_column(Enum(TicketTipo), nullable=False)
    ticket_priority: Mapped[TicketPriority | None] = mapped_column(
        Enum(TicketPriority),
        nullable=True,
        init=False
    )
    ticket_impact: Mapped[TicketImpacto | None] = mapped_column(
        Enum(TicketImpacto),
        nullable=True,
        init=False
    )

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    ticket_client_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    ticket_form_id: Mapped[int] = mapped_column(
        ForeignKey("forms.id", ondelete="RESTRICT"),
        nullable=False
    )
    # Relacionamento polimórfico: ticket pode ser de projeto OU relatório
    ticket_project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=True,
        init=False
    )
    ticket_report_id: Mapped[int | None] = mapped_column(
        ForeignKey("reports.id", ondelete="CASCADE"),
        nullable=True,
        init=False
    )
    ticket_status_changed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        init=False
    )
    ticket_closed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        init=False
    )

    # =========================================================================
    # STATUS
    # =========================================================================
    ticket_status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus), nullable=False)
    ticket_status_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False
    )

    # =========================================================================
    # DATAS
    # =========================================================================
    ticket_deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False
    )
    ticket_closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False
    )
    ticket_mail_sent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False
    )

    # =========================================================================
    # MÉTRICAS
    # =========================================================================
    ticket_estimated_hours: Mapped[float | None] = mapped_column(Double, nullable=True, init=False)
    ticket_actual_hours: Mapped[float | None] = mapped_column(Double, nullable=True, init=False)
    ticket_satisfaction_rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        init=False
    )  # escala de 1 a 10

    # =========================================================================
    # EXTRAS
    # =========================================================================
    ticket_attachments: Mapped[str | None] = mapped_column(String, nullable=True, init=False)  # JSON array
    ticket_resolution_notes: Mapped[str | None] = mapped_column(String, nullable=True, init=False)

    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================

    # N - 1 (Ticket pertence a User/Form/Project/Report)
    client: Mapped["User"] = relationship(
        back_populates="tickets_created",
        lazy="raise",
        foreign_keys=[ticket_client_id],
        init=False
    )
    form: Mapped["Form"] = relationship(
        back_populates="tickets",
        lazy="raise",
        foreign_keys=[ticket_form_id],
        init=False
    )
    project: Mapped["Project | None"] = relationship(
        back_populates="tickets",
        lazy="raise",
        foreign_keys=[ticket_project_id],
        init=False
    )
    report: Mapped["Report | None"] = relationship(
        back_populates="report_tickets",
        lazy="raise",
        foreign_keys=[ticket_report_id],
        init=False
    )
    status_changed_by: Mapped["User | None"] = relationship(
        back_populates="tickets_status_changed",
        lazy="raise",
        foreign_keys=[ticket_status_changed_by_id],
        init=False
    )
    closed_by: Mapped["User | None"] = relationship(
        back_populates="tickets_closed",
        lazy="raise",
        foreign_keys=[ticket_closed_by_id],
        init=False
    )

    # 1 - 1 (Ticket tem um Chat)
    chat: Mapped["Chat | None"] = relationship(
        back_populates="ticket",
        lazy="raise",
        uselist=False,
        init=False
    )

    # N - N (via tabelas de associação)
    attendants: Mapped[list["TicketAttendant"]] = relationship(
        back_populates="ticket",
        lazy="raise",
        init=False,
        default_factory=list
    )
    teams: Mapped[list["TicketTeam"]] = relationship(
        back_populates="ticket",
        lazy="raise",
        init=False,
        default_factory=list
    )
    followers: Mapped[list["UserTicketFollow"]] = relationship(
        back_populates="ticket",
        lazy="raise",
        init=False,
        default_factory=list
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'ticket_title': self.ticket_title,
            'ticket_description': self.ticket_description,
            'ticket_class': self.ticket_class.value if self.ticket_class else None,
            'ticket_type': self.ticket_type.value if self.ticket_type else None,
            'ticket_priority': self.ticket_priority.value if self.ticket_priority else None,
            'ticket_impact': self.ticket_impact.value if self.ticket_impact else None,
            'ticket_client_id': self.ticket_client_id,
            'ticket_form_id': self.ticket_form_id,
            'ticket_project_id': self.ticket_project_id,
            'ticket_report_id': self.ticket_report_id,
            'ticket_status': self.ticket_status.value if self.ticket_status else None,
            'ticket_status_changed_at': self.ticket_status_changed_at.isoformat() if self.ticket_status_changed_at else None,
            'ticket_status_changed_by_id': self.ticket_status_changed_by_id,
            'ticket_deadline': self.ticket_deadline.isoformat() if self.ticket_deadline else None,
            'ticket_closed_at': self.ticket_closed_at.isoformat() if self.ticket_closed_at else None,
            'ticket_closed_by_id': self.ticket_closed_by_id,
            'ticket_mail_sent_at': self.ticket_mail_sent_at.isoformat() if self.ticket_mail_sent_at else None,
            'ticket_estimated_hours': self.ticket_estimated_hours,
            'ticket_actual_hours': self.ticket_actual_hours,
            'ticket_satisfaction_rating': self.ticket_satisfaction_rating,
            'ticket_attachments': self.ticket_attachments,
            'ticket_resolution_notes': self.ticket_resolution_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'deleted_by': self.deleted_by,
            'active': self.active.value if self.active else None
        }

    def __repr__(self) -> str:
        return f"<Ticket(id={self.id}, ticket_title='{self.ticket_title}', ticket_status='{self.ticket_status}')>"
