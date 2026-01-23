from sqlalchemy import ForeignKey, Integer, Double, String, Boolean, DateTime, Date, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from enum import Enum as PyEnum

from infra.configs.database import Base


class TicketClasse(PyEnum):
    PROJETO = "projeto"
    RELATORIO = "relatorio"


class TicketTipo(PyEnum):
    ALTERACAO = "alteracao"
    BUG = "bug"
    CORRECAO = "correcao"
    DESENVOLVIMENTO = "desenvolvimento"
    MELHORIA = "melhoria"


class TicketStatus(PyEnum):
    ATIVO = "ativo"
    ABERTO = "aberto"
    PENDENTE = "pendente"
    PAUSADO = "pausado"
    ENCERRADO = "encerrado"
    CANCELADO = "cancelado"


class TicketTags(PyEnum):
    ATRIBUIDO = "atribuido"
    ATRASADO = "atrasado"
    NO_PRAZO = "no_prazo"


class TicketPriority(PyEnum):
    MAXIMA = "maxima"
    URGENTE = "urgente"
    NORMAL = "normal"
    BACKLOG = "backlog"


class TicketImpacto(PyEnum):
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
        ForeignKey("projects.id", ondelete="RESTRICT"),
        nullable=True,
        init=False
    )
    ticket_report_id: Mapped[int | None] = mapped_column(
        ForeignKey("reports.id", ondelete="RESTRICT"),
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

    def __repr__(self) -> str:
        return f"<Ticket(id={self.id}, ticket_title='{self.ticket_title}', ticket_status='{self.ticket_status}')>"
