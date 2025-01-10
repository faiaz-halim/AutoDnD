"""
AI companion behavior and response generation system
"""
from .companion import AICompanion
from .responses import CLASS_RESPONSES, GENERAL_RESPONSES, SUPPORT_RESPONSES, CONCERN_RESPONSES
from .actions import CLASS_ACTIONS, CONTEXT_ADDONS, ENVIRONMENT_ACTIONS

__all__ = [
    'AICompanion',
    'CLASS_RESPONSES',
    'GENERAL_RESPONSES',
    'SUPPORT_RESPONSES',
    'CONCERN_RESPONSES',
    'CLASS_ACTIONS',
    'CONTEXT_ADDONS',
    'ENVIRONMENT_ACTIONS'
]