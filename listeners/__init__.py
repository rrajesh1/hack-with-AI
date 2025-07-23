"""
Listeners package for organizing Slack event handlers.
"""

from .messages import register_message_listeners
from .commands import register_command_listeners
from .events import register_event_listeners

def register_all_listeners(app):
    """Register all listeners with the Slack app."""
    register_message_listeners(app)
    register_command_listeners(app)
    register_event_listeners(app) 