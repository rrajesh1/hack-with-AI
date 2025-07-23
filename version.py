"""
Version information for the Slack bot application.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__license__ = "MIT"

def get_version():
    """Return the current version of the application."""
    return __version__

def get_user_agent():
    """Return a user agent string for the application."""
    return f"AwesomeSlackBot/{__version__}" 