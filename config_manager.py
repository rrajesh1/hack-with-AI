"""
Configuration Manager for Slack Bot
Supports JSON, YAML, and environment variable configuration
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path

class ConfigManager:
    """Manages configuration loading from various sources"""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration manager"""
        self.config_file = config_file or self._find_config_file()
        self._config = {}
        self._load_config()
    
    def _find_config_file(self) -> Optional[str]:
        """Find configuration file in common locations"""
        possible_files = [
            'config.json',
            'config.yaml', 
            'config.yml',
            'settings.json',
            '.config.json'
        ]
        
        for filename in possible_files:
            if Path(filename).exists():
                return filename
        
        return None
    
    def _load_config(self):
        """Load configuration from file or environment variables"""
        if self.config_file and Path(self.config_file).exists():
            self._load_from_file()
        else:
            print(f"⚠️  Config file not found, falling back to environment variables")
            self._load_from_env()
    
    def _load_from_file(self):
        """Load configuration from JSON or YAML file"""
        try:
            with open(self.config_file, 'r') as f:
                if self.config_file.endswith(('.yaml', '.yml')):
                    try:
                        import yaml
                        self._config = yaml.safe_load(f)
                    except ImportError:
                        raise ImportError("PyYAML required for YAML config files. Install with: pip install pyyaml")
                else:
                    self._config = json.load(f)
            
            print(f"✅ Loaded configuration from {self.config_file}")
            
        except Exception as e:
            print(f"❌ Error loading config file {self.config_file}: {e}")
            print("Falling back to environment variables...")
            self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        from dotenv import load_dotenv
        load_dotenv()
        
        self._config = {
            'slack': {
                'bot_token': os.environ.get('SLACK_BOT_TOKEN'),
                'app_token': os.environ.get('SLACK_APP_TOKEN')
            },
            'environment': os.environ.get('ENVIRONMENT', 'production'),
            'bot': {
                'name': os.environ.get('BOT_NAME', 'Slackbot'),
                'version': '1.0.0',
                'debug': os.environ.get('DEBUG', 'false').lower() == 'true'
            },
            'features': {
                'welcome_messages': True,
                'reaction_responses': True,
                'joke_commands': True
            },
            'logging': {
                'level': os.environ.get('LOG_LEVEL', 'INFO'),
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'slack.bot_token')"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_slack_config(self) -> Dict[str, str]:
        """Get Slack-specific configuration"""
        return {
            'bot_token': self.get('slack.bot_token'),
            'app_token': self.get('slack.app_token')
        }
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.get('environment', 'production').lower() == 'development'
    
    def is_debug_enabled(self) -> bool:
        """Check if debug mode is enabled"""
        return self.get('bot.debug', False)
    
    def validate_required_settings(self):
        """Validate that required settings are present"""
        slack_config = self.get_slack_config()
        
        if not slack_config['bot_token']:
            raise ValueError("Missing required setting: slack.bot_token")
        
        if not slack_config['app_token']:
            raise ValueError("Missing required setting: slack.app_token")
        
        if not slack_config['bot_token'].startswith('xoxb-'):
            raise ValueError("Invalid bot_token format. Should start with 'xoxb-'")
        
        if not slack_config['app_token'].startswith('xapp-'):
            raise ValueError("Invalid app_token format. Should start with 'xapp-'")
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self._config.copy()
    
    def update_config(self, updates: Dict[str, Any]):
        """Update configuration values"""
        def deep_update(base: Dict, updates: Dict):
            for key, value in updates.items():
                if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                    deep_update(base[key], value)
                else:
                    base[key] = value
        
        deep_update(self._config, updates)
    
    def save_config(self, filename: Optional[str] = None):
        """Save current configuration to file"""
        save_file = filename or self.config_file or 'config.json'
        
        try:
            with open(save_file, 'w') as f:
                if save_file.endswith(('.yaml', '.yml')):
                    try:
                        import yaml
                        yaml.dump(self._config, f, default_flow_style=False)
                    except ImportError:
                        raise ImportError("PyYAML required for YAML config files. Install with: pip install pyyaml")
                else:
                    json.dump(self._config, f, indent=2)
            
            print(f"✅ Configuration saved to {save_file}")
            
        except Exception as e:
            print(f"❌ Error saving config: {e}")

# Convenience functions
def load_config(config_file: Optional[str] = None) -> ConfigManager:
    """Load configuration from file or environment"""
    return ConfigManager(config_file)

def get_config() -> ConfigManager:
    """Get default configuration instance"""
    return ConfigManager()

# Global config instance
config = get_config() 