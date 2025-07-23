"""
Slack Client Configuration
Handles configuration loading and Slack app initialization
"""
import os
from slack_bolt import App
from dotenv import load_dotenv

class SlackConfig:
    """Configuration manager for Slack bot"""
    
    def __init__(self):
        """Load environment variables and validate configuration"""
        load_dotenv()
        
        self.bot_token = os.environ.get("SLACK_BOT_TOKEN")
        self.app_token = os.environ.get("SLACK_APP_TOKEN")
        self.environment = os.environ.get("ENVIRONMENT", "production")
        
        self._validate_config()
    
    def _validate_config(self):
        """Validate required configuration"""
        if not self.bot_token:
            raise ValueError("SLACK_BOT_TOKEN environment variable is required")
        
        if not self.app_token:
            raise ValueError("SLACK_APP_TOKEN environment variable is required")
        
        if not self.bot_token.startswith("xoxb-"):
            raise ValueError("SLACK_BOT_TOKEN should start with 'xoxb-'")
        
        if not self.app_token.startswith("xapp-"):
            raise ValueError("SLACK_APP_TOKEN should start with 'xapp-'")
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.environment.lower() == "development"

def get_config() -> SlackConfig:
    """Get configuration instance"""
    return SlackConfig()

def initialize_slack_app(config: SlackConfig = None) -> App:
    """Initialize and return Slack app instance"""
    if config is None:
        config = get_config()
    
    # Initialize the Slack app
    app = App(token=config.bot_token)
    
    # Enable debug logging in development
    if config.is_development:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    return app

# Default instance for easy importing
config = get_config()
app = initialize_slack_app(config) 