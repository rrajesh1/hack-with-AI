"""
Slack Client Configuration
Handles configuration loading and Slack app initialization
"""
from slack_bolt import App
from config_manager import ConfigManager

class SlackConfig:
    """Configuration manager for Slack bot using config files"""
    
    def __init__(self, config_file: str = None):
        """Load configuration from file or environment variables"""
        self.config_manager = ConfigManager(config_file)
        self.config_manager.validate_required_settings()
        
        slack_config = self.config_manager.get_slack_config()
        self.bot_token = slack_config['bot_token']
        self.app_token = slack_config['app_token']
        self.environment = self.config_manager.get('environment', 'production')
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.config_manager.is_development()
    
    @property
    def is_debug_enabled(self) -> bool:
        """Check if debug mode is enabled"""
        return self.config_manager.is_debug_enabled()
    
    def get_feature_setting(self, feature: str) -> bool:
        """Get feature setting"""
        return self.config_manager.get(f'features.{feature}', True)
    
    def get_bot_name(self) -> str:
        """Get bot name"""
        return self.config_manager.get('bot.name', 'Slackbot')

def get_config(config_file: str = None) -> SlackConfig:
    """Get configuration instance"""
    return SlackConfig(config_file)

def initialize_slack_app(config: SlackConfig = None) -> App:
    """Initialize and return Slack app instance"""
    if config is None:
        config = get_config()
    
    # Initialize the Slack app
    app = App(token=config.bot_token)
    
    # Configure logging based on config
    if config.is_development or config.is_debug_enabled:
        import logging
        log_level = config.config_manager.get('logging.level', 'INFO')
        log_format = config.config_manager.get('logging.format', 
                                               '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        logging.basicConfig(
            level=getattr(logging, log_level.upper(), logging.INFO),
            format=log_format
        )
        
        print(f"🔧 Debug logging enabled (level: {log_level})")
    
    return app

# Default instance for easy importing
config = get_config()
app = initialize_slack_app(config) 