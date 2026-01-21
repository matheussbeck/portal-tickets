# Entidades principais
from .team import Team
from .user import User
from .report import Report
from .project import Project
from .ticket import Ticket
from .form import Form
from .chat import Chat
from .message import Message

# Tabelas de associação N-N
from .associations import (
    ApprovalStatus,
    ProjectApproval,
    ProjectAnalyst,
    ProjectSponsor,
    ProjectOwner,
    ProjectClient,
    ProjectAllowedUser,
    TicketAttendant,
    TicketTeam,
    ReportAllowedUser,
    UserReportFollow,
    UserProjectFollow,
    UserTicketFollow,
)

__all__ = [
    # Entidades principais
    'Team',
    'User',
    'Report',
    'Project',
    'Ticket',
    'Form',
    'Chat',
    'Message',
    # Enums de associação
    'ApprovalStatus',
    # Tabelas de associação
    'ProjectApproval',
    'ProjectAnalyst',
    'ProjectSponsor',
    'ProjectOwner',
    'ProjectClient',
    'ProjectAllowedUser',
    'TicketAttendant',
    'TicketTeam',
    'ReportAllowedUser',
    'UserReportFollow',
    'UserProjectFollow',
    'UserTicketFollow',
]
