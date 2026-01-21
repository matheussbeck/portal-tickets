from infra.configs.database import Base
from infra.configs.connection import DBConnectionHandler
from infra.repositories import TeamRepository, UserRepository, ReportRepository, ProjectRepository, TicketRepository, FormRepository, ChatRepository, MessageRepository
from infra.entities.team import Area
from infra.entities.user import UserRoles, UserTipo
from infra.entities.report import ReportFrequency, ReportStatus, ReportTags
from infra.entities.project import ProjectStatus, ProjectTags
from infra.entities.ticket import TicketClasse, TicketTipo, TicketStatus
from infra.entities.form import FormClasse, FormTipo
from datetime import date

# Criar instância do handler e tabelas
db_handler = DBConnectionHandler()
engine = db_handler.get_engine()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Instanciar repositories
team_repo = TeamRepository()
user_repo = UserRepository()
report_repo = ReportRepository()
project_repo = ProjectRepository()
form_repo = FormRepository()
ticket_repo = TicketRepository()
chat_repo = ChatRepository()
message_repo = MessageRepository()

# ========================================
# TEAMS
# ========================================
# insert(team_name, team_area) -> retorna ID
team1_id = team_repo.insert(
    team_name="Performance Agricola",
    team_area=Area.EAB
)
team2_id = team_repo.insert(
    team_name="Planejamento Agricola",
    team_area=Area.PROJETOS
)

# ========================================
# USERS
# ========================================
# insert(user_corporative_id, user_full_name, user_email, user_password, user_team_id, user_role, user_tipo) -> retorna ID
user1_id = user_repo.insert(
    user_corporative_id=416149,
    user_full_name='Matheus Beck',
    user_email='matheus@raizen.com',
    user_password='senhaSegura123',
    user_team_id=team1_id,
    user_role=UserRoles.N1,
    user_tipo=UserTipo.ATENDENTE
)
user2_id = user_repo.insert(
    user_corporative_id=123456,
    user_full_name='Ana Silva',
    user_email='ana.silva@raizen.com',
    user_password='senhaSegura123',
    user_team_id=team2_id,
    user_role=UserRoles.N2,
    user_tipo=UserTipo.ATENDENTE
)
user3_id = user_repo.insert(
    user_corporative_id=789012,
    user_full_name='Carlos Santos',
    user_email='carlos.santos@raizen.com',
    user_password='senhaSegura123',
    user_team_id=team1_id,
    user_role=UserRoles.GESTOR,
    user_tipo=UserTipo.SOLICITANTE
)

# Definir gerentes dos times (após criar os usuários)
team_repo.set_manager(team1_id, user3_id)  # Carlos é gestor do time 1
team_repo.set_manager(team2_id, user2_id)  # Ana é gestora do time 2

# ========================================
# REPORTS
# ========================================
# insert(report_name, report_link, report_description, report_frequency,
#        report_team_responsible_id, report_owner_id, report_status, report_tags, report_public) -> retorna ID
report1_id = report_repo.insert(
    report_name='Projecao CCT',
    report_link='https://powerbi.com/cct',
    report_description='Relatorio hora a hora de Corte, Carregamento e Transporte de cana',
    report_frequency=ReportFrequency.HORARIO,
    report_team_responsible_id=team1_id,
    report_owner_id=user1_id,
    report_status=ReportStatus.ATIVO,
    report_tags=ReportTags.CCT,
    report_public=True
)
report2_id = report_repo.insert(
    report_name='Produtividade Agricola',
    report_link='https://powerbi.com/produtividade',
    report_description='Dashboard de produtividade de colheita por talhao e frente de trabalho',
    report_frequency=ReportFrequency.DIARIO,
    report_team_responsible_id=team1_id,
    report_owner_id=user3_id,
    report_status=ReportStatus.ATIVO,
    report_tags=ReportTags.PRODUCAO,
    report_public=False
)
report3_id = report_repo.insert(
    report_name='Qualidade da Cana',
    report_link='https://powerbi.com/qualidade-cana',
    report_description='Analise de ATR, pureza e fibra da cana colhida por regiao',
    report_frequency=ReportFrequency.DIARIO,
    report_team_responsible_id=team2_id,
    report_owner_id=user2_id,
    report_status=ReportStatus.ATIVO,
    report_tags=ReportTags.QUALIDADE,
    report_public=True
)

# ========================================
# PROJECTS
# ========================================
# insert(project_name, project_directory, project_description, project_team_responsible_id,
#        project_manager_id, project_tags, project_status, project_start_date,
#        project_expected_end_date, project_planned_budget, project_public) -> retorna ID
project1_id = project_repo.insert(
    project_name='Otimizacao Rotas Transporte',
    project_directory='/projects/otimizacao-rotas',
    project_description='Projeto de otimizacao de rotas de transporte de cana para reduzir custos e tempo',
    project_team_responsible_id=team1_id,
    project_manager_id=user3_id,
    project_tags=ProjectTags.ATRIBUIDO,
    project_status=ProjectStatus.ATIVO,
    project_start_date=date(2024, 1, 15),
    project_expected_end_date=date(2024, 6, 30),
    project_planned_budget=150000.0,
    project_public=True
)

project2_id = project_repo.insert(
    project_name='Telemetria Colhedoras',
    project_directory='/projects/telemetria-colhedoras',
    project_description='Implementacao de sistema de telemetria em tempo real para monitoramento de colhedoras',
    project_team_responsible_id=team2_id,
    project_manager_id=user2_id,
    project_tags=ProjectTags.NO_PRAZO,
    project_status=ProjectStatus.PENDENTE,
    project_start_date=date(2024, 3, 1),
    project_expected_end_date=date(2024, 12, 31),
    project_planned_budget=280000.0,
    project_public=True
)

# ========================================
# FORMS
# ========================================
# insert(form_name, form_ticket_class, form_type, form_fields) -> retorna ID
form1_id = form_repo.insert(
    form_name='Formulario Correcao Report',
    form_ticket_class=FormClasse.RELATORIO,
    form_type=FormTipo.CORRECAO,
    form_fields='{"fields":[{"name":"erro_descricao","type":"textarea","required":true},{"name":"print_tela","type":"file","required":true},{"name":"talhao_afetado","type":"text","required":false}]}'
)

form2_id = form_repo.insert(
    form_name='Formulario Melhoria Operacional',
    form_ticket_class=FormClasse.PROJETO,
    form_type=FormTipo.MELHORIA,
    form_fields='{"fields":[{"name":"justificativa","type":"textarea","required":true},{"name":"beneficios_esperados","type":"textarea","required":true},{"name":"areas_impactadas","type":"text","required":true},{"name":"prazo_desejado":"date","required":true}]}'
)

# ========================================
# TICKETS
# ========================================
# insert(ticket_title, ticket_class, ticket_type, ticket_client_id,
#        ticket_description, ticket_form_id, ticket_status) -> retorna ID
ticket1_id = ticket_repo.insert(
    ticket_title='Divergencia valores CCT Talhao 45A',
    ticket_class=TicketClasse.RELATORIO,
    ticket_type=TicketTipo.CORRECAO,
    ticket_client_id=user3_id,
    ticket_description='Relatorio CCT apresentando tonelagem divergente no talhao 45A. Valor reportado: 850t, valor real: 920t',
    ticket_form_id=form1_id,
    ticket_status=TicketStatus.ABERTO
)

ticket2_id = ticket_repo.insert(
    ticket_title='Adicionar filtro por variedade de cana',
    ticket_class=TicketClasse.RELATORIO,
    ticket_type=TicketTipo.MELHORIA,
    ticket_client_id=user3_id,
    ticket_description='Incluir filtro por variedade de cana (SP, RB, etc) no dashboard de Produtividade Agricola',
    ticket_form_id=form2_id,
    ticket_status=TicketStatus.PENDENTE
)

ticket3_id = ticket_repo.insert(
    ticket_title='Falha atualizacao dados ATR',
    ticket_class=TicketClasse.RELATORIO,
    ticket_type=TicketTipo.CORRECAO,
    ticket_client_id=user2_id,
    ticket_description='Relatorio Qualidade da Cana nao atualizou dados de ATR desde 15/12',
    ticket_form_id=form1_id,
    ticket_status=TicketStatus.ATIVO
)

# Associar tickets a reports
ticket_repo.assign_to_report(ticket1_id, report1_id)
ticket_repo.assign_to_report(ticket2_id, report2_id)
ticket_repo.assign_to_report(ticket3_id, report3_id)

# ========================================
# CHATS
# ========================================
# insert(chat_ticket_id) -> retorna ID
chat1_id = chat_repo.insert(chat_ticket_id=ticket1_id)
chat2_id = chat_repo.insert(chat_ticket_id=ticket2_id)
chat3_id = chat_repo.insert(chat_ticket_id=ticket3_id)

# ========================================
# MESSAGES
# ========================================
# insert(message_chat_id, message_user_id, message_content, message_type, message_is_internal) -> retorna ID
message_repo.insert(
    message_chat_id=chat1_id,
    message_user_id=user3_id,
    message_content='Boa tarde, identifiquei divergencia nos valores de tonelagem do talhao 45A no relatorio CCT. O sistema mostra 850t mas conferimos e foram 920t colhidas.',
    message_type='text',
    message_is_internal=False
)

message_repo.insert(
    message_chat_id=chat1_id,
    message_user_id=user1_id,
    message_content='Obrigado pelo reporte Carlos. Vou verificar a integracao com o sistema de pesagem e retorno em breve.',
    message_type='text',
    message_is_internal=False
)

message_repo.insert(
    message_chat_id=chat1_id,
    message_user_id=user1_id,
    message_content='Chamado encaminhado para equipe de integracao. Possivel falha na captura de tickets de pesagem.',
    message_type='system',
    message_is_internal=True
)

message_repo.insert(
    message_chat_id=chat2_id,
    message_user_id=user2_id,
    message_content='Otima sugestao! O filtro por variedade vai ajudar muito na analise comparativa. Vou incluir no backlog da proxima sprint.',
    message_type='text',
    message_is_internal=False
)

message_repo.insert(
    message_chat_id=chat3_id,
    message_user_id=user1_id,
    message_content='Ana, verificamos que o job de carga do ATR falhou no dia 15/12. Vou reprocessar os dados agora.',
    message_type='text',
    message_is_internal=False
)

message_repo.insert(
    message_chat_id=chat3_id,
    message_user_id=user2_id,
    message_content='Perfeito Matheus! Por favor me avise quando estiver atualizado para validarmos os numeros.',
    message_type='text',
    message_is_internal=False
)

print("Database criado e populado com sucesso!")
print(f"Teams criados: {team1_id}, {team2_id}")
print(f"Users criados: {user1_id}, {user2_id}, {user3_id}")
print(f"Reports criados: {report1_id}, {report2_id}, {report3_id}")
print(f"Projects criados: {project1_id}, {project2_id}")
print(f"Forms criados: {form1_id}, {form2_id}")
print(f"Tickets criados: {ticket1_id}, {ticket2_id}, {ticket3_id}")
print(f"Chats criados: {chat1_id}, {chat2_id}, {chat3_id}")
