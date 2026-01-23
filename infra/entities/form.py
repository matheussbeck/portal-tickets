from sqlalchemy import Integer, String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

from infra.configs.database import Base


class FormClasse(PyEnum):
    PROJETO = "projeto"
    RELATORIO = "relatorio"


class FormTipo(PyEnum):
    ALTERACAO = "alteracao"
    BUG = "bug"
    CORRECAO = "correcao"
    DESENVOLVIMENTO = "desenvolvimento"
    MELHORIA = "melhoria"


class Form(Base):
    """
    Template de formulário para criação de tickets.

    Relacionamentos:
    - 1-N: tickets (Ticket) - formulário é usado por muitos tickets
    """
    __tablename__ = "forms"

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    form_name: Mapped[str] = mapped_column(String, nullable=False)
    form_description: Mapped[str | None] = mapped_column(String, nullable=True, init=False)

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    form_ticket_class: Mapped[FormClasse] = mapped_column(
        Enum(FormClasse),
        nullable=False
    )  # project or report
    form_type: Mapped[FormTipo] = mapped_column(
        Enum(FormTipo),
        nullable=False
    )  # enum do tipo de ticket

    # =========================================================================
    # CONFIGURAÇÕES
    # =========================================================================
    form_fields: Mapped[str] = mapped_column(String, nullable=False)  # JSON com definição dos campos
    form_is_default: Mapped[bool] = mapped_column(Boolean, default=False, init=False)
    form_version: Mapped[int] = mapped_column(Integer, default=1, init=False)

    # =========================================================================
    # RELATIONSHIPS
    # =========================================================================

    # 1 - N (Form é usado por muitos tickets)
    tickets: Mapped[list["Ticket"]] = relationship(
        back_populates="form",
        lazy="raise",
        init=False,
        default_factory=list
    )

    

    def __repr__(self) -> str:
        return f"<Form(id={self.id}, form_name='{self.form_name}', form_type='{self.form_type}')>"
