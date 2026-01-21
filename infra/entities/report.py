from sqlalchemy import ForeignKey, String, Boolean, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum

from infra.configs.database import Base


class ReportFrequency(enum.Enum):
    DIARIO = "diario"
    HORARIO = "horario"
    AGENDADO = "agendado"
    SOB_DEMANDA = "sob_demanda"


class ReportStatus(enum.Enum):
    ATIVO = "ativo"
    MANUTENCAO = "manutencao"
    DESATUALIZADO = "desatualizado"
    TESTE = "teste"
    INATIVO = "inativo"
    DESENVOLVIMENTO = "desenvolvimento"
    DIAGNOSTICO = "diagnostico"


class ReportTags(enum.Enum):
    CIA = "cia"
    CCT = "cct"
    PRODUCAO = "producao"
    SSMA = "ssma"
    CCO = "cco"
    MANUTENCAO = "manutencao"
    QUALIDADE = "qualidade"


class Report(Base):
    """
    Entidade de Relatório (Power BI).

    Relacionamentos:
    - N-1: team (Team), owner (User), status_changed_by (User)
    - 1-N: report_tickets (Ticket)
    - N-N: allowed_users (User), followers (User)
    """
    __tablename__ = "reports"

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    report_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    report_link: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    report_description: Mapped[str] = mapped_column(String, nullable=False)

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    report_frequency: Mapped[ReportFrequency] = mapped_column(
        Enum(ReportFrequency),
        nullable=False
    )
    report_tags: Mapped[ReportTags] = mapped_column(Enum(ReportTags))

    # =========================================================================
    # FOREIGN KEYS
    # =========================================================================
    report_team_responsible_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="RESTRICT"),
        nullable=False
    )
    report_owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    report_status_changed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        init=False
    )

    # =========================================================================
    # STATUS
    # =========================================================================
    report_status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus), nullable=False)
    report_status_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        init=False
    )

    # =========================================================================
    # DATAS
    # =========================================================================
    report_data_last_update: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        init=False
    )
    report_pbix_last_update: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        init=False
    )

    # =========================================================================
    # CONFIGURAÇÕES
    # =========================================================================
    report_public: Mapped[bool] = mapped_column(Boolean, default=True)

    # =========================================================================
    # EXTRAS
    # =========================================================================
    report_dataset_source: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
        init=False
    )

    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================

    # N - 1 (Report pertence a Team/User)
    team: Mapped["Team"] = relationship(
        back_populates="team_reports",
        lazy="raise",
        init=False
    )
    owner: Mapped["User"] = relationship(
        foreign_keys=[report_owner_id],
        back_populates="user_reports",
        lazy="raise",
        init=False
    )
    status_changed_by: Mapped["User | None"] = relationship(
        foreign_keys=[report_status_changed_by_id],
        lazy="raise",
        init=False
    )

    # 1 - N (Report tem muitos tickets)
    report_tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="report",
        lazy="raise",
        init=False,
        default_factory=list
    )

    # N - N (via tabelas de associação)
    allowed_users: Mapped[list["ReportAllowedUser"]] = relationship(
        back_populates="report",
        lazy="raise",
        init=False,
        default_factory=list
    )
    followers: Mapped[list["UserReportFollow"]] = relationship(
        back_populates="report",
        lazy="raise",
        init=False,
        default_factory=list
    )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'report_name': self.report_name,
            'report_link': self.report_link,
            'report_description': self.report_description,
            'report_frequency': self.report_frequency.value if self.report_frequency else None,
            'report_tags': self.report_tags.value if self.report_tags else None,
            'report_team_responsible_id': self.report_team_responsible_id,
            'report_owner_id': self.report_owner_id,
            'report_status': self.report_status.value if self.report_status else None,
            'report_status_changed_at': self.report_status_changed_at.isoformat() if self.report_status_changed_at else None,
            'report_status_changed_by_id': self.report_status_changed_by_id,
            'report_data_last_update': self.report_data_last_update.isoformat() if self.report_data_last_update else None,
            'report_pbix_last_update': self.report_pbix_last_update.isoformat() if self.report_pbix_last_update else None,
            'report_public': self.report_public,
            'report_dataset_source': self.report_dataset_source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'updated_by': self.updated_by,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'deleted_by': self.deleted_by,
            'active': self.active.value if self.active else None
        }

    def __repr__(self) -> str:
        return f"<Report(id={self.id}, report_name='{self.report_name}', report_status='{self.report_status}')>"
