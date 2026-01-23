"""
Teste de Entidades e Relacionamentos ORM SQLAlchemy

Este script:
1. Cria as tabelas no banco
2. Popula com dados de teste
3. Testa relacionamentos ORM (navegação entre entidades)
4. Testa soft delete
5. Valida consistência dos relationships
"""
from datetime import date

from sqlalchemy.orm import selectinload

from infra.configs.database import Base, Status
from infra.configs.connection import DBConnectionHandler

# Entities
from infra.entities.team import Team, Area, TeamStatus
from infra.entities.user import User, UserRoles, UserTipo, UserStatus
from infra.entities.report import Report, ReportFrequency, ReportStatus, ReportTags
from infra.entities.project import Project, ProjectStatus, ProjectTags
from infra.entities.ticket import Ticket, TicketClasse, TicketTipo, TicketStatus
from infra.entities.form import Form, FormClasse, FormTipo
from infra.entities.chat import Chat
from infra.entities.message import Message

# Repositories
from infra.repositories import (
    TeamRepository, UserRepository, ReportRepository,
    ProjectRepository, TicketRepository, FormRepository,
    ChatRepository, MessageRepository
)


def print_section(title: str):
    """Helper para imprimir seções"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print('='*60)


def print_test(name: str, passed: bool):
    """Helper para imprimir resultado de teste"""
    status = "PASSOU" if passed else "FALHOU"
    symbol = "[OK]" if passed else "[X]"
    print(f"  {symbol} {name}: {status}")


# =============================================================================
# SETUP: Criar tabelas
# =============================================================================
print_section("SETUP: Criando banco de dados")

db_handler = DBConnectionHandler()
engine = db_handler.get_engine()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
print("  Tabelas criadas com sucesso!")

# =============================================================================
# PARTE 1: Criar dados usando Repositories
# =============================================================================
print_section("PARTE 1: Populando banco de dados")

# Instanciar repositories
team_repo = TeamRepository()
user_repo = UserRepository()
report_repo = ReportRepository()
project_repo = ProjectRepository()
form_repo = FormRepository()
ticket_repo = TicketRepository()
chat_repo = ChatRepository()
message_repo = MessageRepository()

# TEAMS
team1_id = team_repo.create(team_name="Performance Agricola", team_area=Area.EAB)
team2_id = team_repo.create(team_name="Planejamento Agricola", team_area=Area.PROJETOS)
print(f"  Teams criados: {team1_id}, {team2_id}")

# USERS
user1_id = user_repo.create(
    user_corporative_id=416149,
    user_full_name='Matheus Beck',
    user_email='matheus@raizen.com',
    user_password='senhaSegura123',
    user_team_id=team1_id,
    user_role=UserRoles.N1,
    user_tipo=UserTipo.ATENDENTE
)
user2_id = user_repo.create(
    user_corporative_id=123456,
    user_full_name='Ana Silva',
    user_email='ana.silva@raizen.com',
    user_password='senhaSegura123',
    user_team_id=team2_id,
    user_role=UserRoles.N2,
    user_tipo=UserTipo.ATENDENTE
)
user3_id = user_repo.create(
    user_corporative_id=789012,
    user_full_name='Carlos Santos',
    user_email='carlos.santos@raizen.com',
    user_password='senhaSegura123',
    user_team_id=team1_id,
    user_role=UserRoles.GESTOR,
    user_tipo=UserTipo.SOLICITANTE
)
print(f"  Users criados: {user1_id}, {user2_id}, {user3_id}")

# Definir gerentes dos times
team_repo.set_manager(team1_id, user3_id)
team_repo.set_manager(team2_id, user2_id)
print("  Gerentes definidos")

# REPORTS
report1_id = report_repo.create(
    report_name='Projecao CCT',
    report_link='https://powerbi.com/cct',
    report_description='Relatorio hora a hora de CCT',
    report_frequency=ReportFrequency.HORARIO,
    report_team_responsible_id=team1_id,
    report_owner_id=user1_id,
    report_status=ReportStatus.ATIVO,
    report_tags=ReportTags.CCT,
    report_public=True
)
report2_id = report_repo.create(
    report_name='Produtividade Agricola',
    report_link='https://powerbi.com/produtividade',
    report_description='Dashboard de produtividade',
    report_frequency=ReportFrequency.DIARIO,
    report_team_responsible_id=team1_id,
    report_owner_id=user3_id,
    report_status=ReportStatus.ATIVO,
    report_tags=ReportTags.PRODUCAO,
    report_public=False
)
print(f"  Reports criados: {report1_id}, {report2_id}")

# PROJECTS
project1_id = project_repo.create(
    project_name='Otimizacao Rotas',
    project_directory='/projects/rotas',
    project_description='Projeto de otimizacao',
    project_team_responsible_id=team1_id,
    project_manager_id=user3_id,
    project_tags=ProjectTags.ATRIBUIDO,
    project_status=ProjectStatus.ATIVO,
    project_start_date=date(2024, 1, 15),
    project_expected_end_date=date(2024, 6, 30),
    project_planned_budget=150000.0
)
print(f"  Projects criados: {project1_id}")

# FORMS
form1_id = form_repo.create(
    form_name='Form Correcao',
    form_ticket_class=FormClasse.RELATORIO,
    form_type=FormTipo.CORRECAO,
    form_fields='{"fields":[]}'
)
print(f"  Forms criados: {form1_id}")

# TICKETS
ticket1_id = ticket_repo.create(
    ticket_title='Divergencia CCT',
    ticket_class=TicketClasse.RELATORIO,
    ticket_type=TicketTipo.CORRECAO,
    ticket_client_id=user3_id,
    ticket_description='Valores divergentes',
    ticket_form_id=form1_id,
    ticket_status=TicketStatus.ABERTO
)
ticket_repo.assign_to_report(ticket1_id, report1_id)
print(f"  Tickets criados: {ticket1_id}")

# CHATS
chat1_id = chat_repo.create(chat_ticket_id=ticket1_id)
print(f"  Chats criados: {chat1_id}")

# MESSAGES
msg1_id = message_repo.create(
    message_chat_id=chat1_id,
    message_user_id=user3_id,
    message_content='Primeira mensagem do ticket'
)
msg2_id = message_repo.create(
    message_chat_id=chat1_id,
    message_user_id=user1_id,
    message_content='Resposta do atendente',
    message_is_internal=False
)
print(f"  Messages criadas: {msg1_id}, {msg2_id}")


# =============================================================================
# PARTE 2: Testar Relacionamentos ORM
# =============================================================================
print_section("PARTE 2: Testando Relacionamentos ORM")

with DBConnectionHandler() as db:
    # -------------------------------------------------------------------------
    # Teste 1: User -> Team (N-1)
    # -------------------------------------------------------------------------
    user = db.session.query(User).options(
        selectinload(User.team)
    ).filter(User.id == user1_id).first()

    test_passed = user.team is not None and user.team.team_name == "Performance Agricola"
    print_test("User -> Team (N-1)", test_passed)

    # -------------------------------------------------------------------------
    # Teste 2: Team -> Users (1-N)
    # -------------------------------------------------------------------------
    team = db.session.query(Team).options(
        selectinload(Team.team_members)
    ).filter(Team.id == team1_id).first()

    test_passed = len(team.team_members) == 2  # user1 e user3
    print_test(f"Team -> Users (1-N): {len(team.team_members)} membros", test_passed)

    # -------------------------------------------------------------------------
    # Teste 3: Team -> Manager (N-1)
    # -------------------------------------------------------------------------
    team = db.session.query(Team).options(
        selectinload(Team.manager)
    ).filter(Team.id == team1_id).first()

    test_passed = team.manager is not None and team.manager.user_full_name == "Carlos Santos"
    print_test("Team -> Manager (N-1)", test_passed)

    # -------------------------------------------------------------------------
    # Teste 4: User -> Managed Team (1-1)
    # -------------------------------------------------------------------------
    user = db.session.query(User).options(
        selectinload(User.managed_team)
    ).filter(User.id == user3_id).first()

    test_passed = user.managed_team is not None and user.managed_team.team_name == "Performance Agricola"
    print_test("User -> Managed Team (1-1)", test_passed)

    # -------------------------------------------------------------------------
    # Teste 5: Report -> Team (N-1)
    # -------------------------------------------------------------------------
    report = db.session.query(Report).options(
        selectinload(Report.team)
    ).filter(Report.id == report1_id).first()

    test_passed = report.team is not None and report.team.team_name == "Performance Agricola"
    print_test("Report -> Team (N-1)", test_passed)

    # -------------------------------------------------------------------------
    # Teste 6: Report -> Owner (N-1)
    # -------------------------------------------------------------------------
    report = db.session.query(Report).options(
        selectinload(Report.owner)
    ).filter(Report.id == report1_id).first()

    test_passed = report.owner is not None and report.owner.user_full_name == "Matheus Beck"
    print_test("Report -> Owner (N-1)", test_passed)

    # -------------------------------------------------------------------------
    # Teste 7: User -> Reports (1-N)
    # -------------------------------------------------------------------------
    user = db.session.query(User).options(
        selectinload(User.user_reports)
    ).filter(User.id == user1_id).first()

    test_passed = len(user.user_reports) == 1
    print_test(f"User -> Reports (1-N): {len(user.user_reports)} reports", test_passed)

    # -------------------------------------------------------------------------
    # Teste 8: Project -> Manager (N-1)
    # -------------------------------------------------------------------------
    project = db.session.query(Project).options(
        selectinload(Project.manager)
    ).filter(Project.id == project1_id).first()

    test_passed = project.manager is not None and project.manager.user_full_name == "Carlos Santos"
    print_test("Project -> Manager (N-1)", test_passed)

    # -------------------------------------------------------------------------
    # Teste 9: Ticket -> Client (N-1)
    # -------------------------------------------------------------------------
    ticket = db.session.query(Ticket).options(
        selectinload(Ticket.client)
    ).filter(Ticket.id == ticket1_id).first()

    test_passed = ticket.client is not None and ticket.client.user_full_name == "Carlos Santos"
    print_test("Ticket -> Client (N-1)", test_passed)

    # -------------------------------------------------------------------------
    # Teste 10: Ticket -> Report (N-1)
    # -------------------------------------------------------------------------
    ticket = db.session.query(Ticket).options(
        selectinload(Ticket.report)
    ).filter(Ticket.id == ticket1_id).first()

    test_passed = ticket.report is not None and ticket.report.report_name == "Projecao CCT"
    print_test("Ticket -> Report (N-1)", test_passed)

    # -------------------------------------------------------------------------
    # Teste 11: Ticket -> Chat (1-1)
    # -------------------------------------------------------------------------
    ticket = db.session.query(Ticket).options(
        selectinload(Ticket.chat)
    ).filter(Ticket.id == ticket1_id).first()

    test_passed = ticket.chat is not None
    print_test("Ticket -> Chat (1-1)", test_passed)

    # -------------------------------------------------------------------------
    # Teste 12: Chat -> Ticket (N-1)
    # -------------------------------------------------------------------------
    chat = db.session.query(Chat).options(
        selectinload(Chat.ticket)
    ).filter(Chat.id == chat1_id).first()

    test_passed = chat.ticket is not None and chat.ticket.ticket_title == "Divergencia CCT"
    print_test("Chat -> Ticket (N-1)", test_passed)

    # -------------------------------------------------------------------------
    # Teste 13: Chat -> Messages (1-N)
    # -------------------------------------------------------------------------
    chat = db.session.query(Chat).options(
        selectinload(Chat.messages)
    ).filter(Chat.id == chat1_id).first()

    test_passed = len(chat.messages) == 2
    print_test(f"Chat -> Messages (1-N): {len(chat.messages)} mensagens", test_passed)

    # -------------------------------------------------------------------------
    # Teste 14: Message -> User (N-1)
    # -------------------------------------------------------------------------
    message = db.session.query(Message).options(
        selectinload(Message.user)
    ).filter(Message.id == msg1_id).first()

    test_passed = message.user is not None and message.user.user_full_name == "Carlos Santos"
    print_test("Message -> User (N-1)", test_passed)

    # -------------------------------------------------------------------------
    # Teste 15: Message -> Chat (N-1)
    # -------------------------------------------------------------------------
    message = db.session.query(Message).options(
        selectinload(Message.chat)
    ).filter(Message.id == msg1_id).first()

    test_passed = message.chat is not None
    print_test("Message -> Chat (N-1)", test_passed)


# =============================================================================
# PARTE 3: Testar Soft Delete
# =============================================================================
print_section("PARTE 3: Testando Soft Delete")

# Criar um user temporário para testar soft delete
temp_user_id = user_repo.create(
    user_corporative_id=999999,
    user_full_name='Usuario Temporario',
    user_email='temp@raizen.com',
    user_password='senha123',
    user_team_id=team1_id,
    user_role=UserRoles.N1,
    user_tipo=UserTipo.ATENDENTE
)
print(f"  Usuario temporario criado: ID {temp_user_id}")

# Verificar que existe
exists_before = user_repo.exists(temp_user_id)
print_test("Usuario existe antes do soft delete", exists_before)

# Soft delete
user_repo.soft_delete(temp_user_id, deleted_by=user1_id)
print("  Soft delete executado")

# Verificar que NÃO aparece mais em queries normais
exists_after = user_repo.exists(temp_user_id)
print_test("Usuario NAO aparece em queries normais", not exists_after)

# Verificar que AINDA existe se incluir inativos
user_data = user_repo.select_by_id(temp_user_id, include_inactive=True)
print_test("Usuario AINDA existe com include_inactive=True", user_data is not None)

# Verificar campos de soft delete
print_test("Campo 'active' = INATIVO", user_data['active'] == 'inativo')
print_test("Campo 'deleted_at' preenchido", user_data['deleted_at'] is not None)
print_test("Campo 'deleted_by' preenchido", user_data['deleted_by'] == user1_id)

# Restaurar
user_repo.restore(temp_user_id)
print("  Restore executado")

# Verificar que voltou a aparecer
exists_restored = user_repo.exists(temp_user_id)
print_test("Usuario aparece novamente apos restore", exists_restored)


# =============================================================================
# PARTE 4: Testar to_dict()
# =============================================================================
print_section("PARTE 4: Testando to_dict()")

with DBConnectionHandler() as db:
    user = db.session.query(User).filter(User.id == user1_id).first()
    user_dict = user.to_dict()

    print_test("to_dict() retorna dict", isinstance(user_dict, dict))
    print_test("Contém 'id'", 'id' in user_dict)
    print_test("Contém 'user_full_name'", 'user_full_name' in user_dict)
    print_test("Contém 'created_at'", 'created_at' in user_dict)
    print_test("Enum convertido para string", isinstance(user_dict.get('user_role'), str))
    print_test("Datetime convertido para ISO", isinstance(user_dict.get('created_at'), str))


# =============================================================================
# PARTE 5: Navegação Completa (Exemplo End-to-End)
# =============================================================================
print_section("PARTE 5: Navegacao Completa")

with DBConnectionHandler() as db:
    # Partindo de uma Message, navegar até o Team responsável pelo Report do Ticket
    message = db.session.query(Message).options(
        selectinload(Message.chat)
        .selectinload(Chat.ticket)
        .selectinload(Ticket.report)
        .selectinload(Report.team)
    ).filter(Message.id == msg1_id).first()

    # Navegação: Message -> Chat -> Ticket -> Report -> Team
    team_name = message.chat.ticket.report.team.team_name

    print(f"  Message ID: {message.id}")
    print(f"  -> Chat ID: {message.chat.id}")
    print(f"  -> Ticket: {message.chat.ticket.ticket_title}")
    print(f"  -> Report: {message.chat.ticket.report.report_name}")
    print(f"  -> Team: {team_name}")

    test_passed = team_name == "Performance Agricola"
    print_test("Navegacao Message->Chat->Ticket->Report->Team", test_passed)


# =============================================================================
# RESUMO
# =============================================================================
print_section("RESUMO")
print("""
  Banco de dados criado e populado com sucesso!

  Entidades criadas:
  - 2 Teams
  - 4 Users (incluindo 1 temporario para teste)
  - 2 Reports
  - 1 Project
  - 1 Form
  - 1 Ticket
  - 1 Chat
  - 2 Messages

  Testes executados:
  - Relacionamentos N-1 (belongs_to)
  - Relacionamentos 1-N (has_many)
  - Relacionamentos 1-1 (has_one)
  - Soft Delete (delete, restore)
  - to_dict() conversion
  - Navegacao completa entre entidades
""")
