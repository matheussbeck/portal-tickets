from sqlalchemy import Integer, String, Boolean, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

from infra.configs.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from infra.entities.ticket import Ticket


class FormClasse(PyEnum):
    """
    Classe do formulário - define para qual tipo de entidade.

    - PROJETO: Formulário para tickets de projetos
    - RELATORIO: Formulário para tickets de relatórios
    """
    PROJETO = "projeto"
    RELATORIO = "relatorio"


class FormTipo(PyEnum):
    """
    Tipo de solicitação que o formulário atende.

    Define a natureza do trabalho:
    - ALTERACAO: Mudança em funcionalidade
    - BUG: Correção de erro
    - CORRECAO: Ajuste de dados
    - DESENVOLVIMENTO: Nova funcionalidade
    - MELHORIA: Otimização
    """
    ALTERACAO = "alteracao"
    BUG = "bug"
    CORRECAO = "correcao"
    DESENVOLVIMENTO = "desenvolvimento"
    MELHORIA = "melhoria"


class Form(Base):
    """
    Template de formulário para criação de tickets.

    Define a estrutura de campos e validações para abertura
    de tickets de um tipo específico.

    Relacionamentos:
        1-N (Form possui muitos):
            - tickets: Tickets criados usando este template

    Índices:
        - ix_forms_class_type: Busca por classe e tipo

    Exemplo de Instanciação (Template Construtor):
        ```python
        # Campos OBRIGATÓRIOS no construtor:
        form = Form(
            form_name="Bug em Relatório",
            form_ticket_class=FormClasse.RELATORIO,
            form_type=FormTipo.BUG,
            form_fields='{"campos": [...]}'  # JSON com definição
        )

        # Campos OPCIONAIS (têm init=False):
        # - form_description: Descrição do uso
        # - form_is_default: Se é o formulário padrão
        # - form_version: Versão (começa em 1)
        ```
    """
    __tablename__ = "forms"

    # Índices compostos para queries frequentes
    __table_args__ = (
        Index('ix_forms_class_type', 'form_ticket_class', 'form_type'),
    )

    # =========================================================================
    # IDENTIFICAÇÃO
    # =========================================================================
    form_name: Mapped[str] = mapped_column(
        String, nullable=False,
        doc="Nome do formulário (ex: 'Bug em Relatório')"
    )
    form_description: Mapped[str | None] = mapped_column(
        String, nullable=True, init=False,
        doc="Descrição de quando usar este formulário"
    )

    # =========================================================================
    # CLASSIFICAÇÃO
    # =========================================================================
    form_ticket_class: Mapped[FormClasse] = mapped_column(
        Enum(FormClasse),
        nullable=False,
        doc="Classe do ticket (PROJETO ou RELATORIO)"
    )
    form_type: Mapped[FormTipo] = mapped_column(
        Enum(FormTipo),
        nullable=False,
        doc="Tipo de solicitação (BUG, MELHORIA, etc.)"
    )

    # =========================================================================
    # CONFIGURAÇÕES
    # =========================================================================
    form_fields: Mapped[str] = mapped_column(
        String, nullable=False,
        doc="JSON com definição dos campos do formulário"
    )
    form_is_default: Mapped[bool] = mapped_column(
        Boolean, default=False, init=False,
        doc="Se True, é o formulário padrão para esta classe+tipo"
    )
    form_version: Mapped[int] = mapped_column(
        Integer, default=1, init=False,
        doc="Versão do formulário (incrementa em alterações)"
    )

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
