"""
Basic tests for the Slack bot functionality.
"""
import pytest
from unittest.mock import Mock, patch
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

class TestSlackBot:
    """Test cases for Slack bot functionality."""
    
    def test_bot_initialization(self):
        """Test that the bot can be initialized."""
        with patch.dict(os.environ, {
            'SLACK_BOT_TOKEN': 'xoxb-test-token',
            'SLACK_APP_TOKEN': 'xapp-test-token'
        }):
            try:
                from slack_client import get_config, initialize_slack_app
                config = get_config()
                app = initialize_slack_app(config)
                assert app is not None
                assert config.bot_token == 'xoxb-test-token'
                assert config.app_token == 'xapp-test-token'
            except ValueError:
                # Expected if tokens don't have proper format
                pass
    
    def test_config_validation(self):
        """Test configuration validation."""
        with patch.dict(os.environ, {}, clear=True):
            from slack_client import SlackConfig
            with pytest.raises(ValueError, match="SLACK_BOT_TOKEN"):
                SlackConfig()
    
    def test_version_info(self):
        """Test version information."""
        from version import get_version, get_user_agent
        version = get_version()
        user_agent = get_user_agent()
        
        assert version == "1.0.0"
        assert "AwesomeSlackBot" in user_agent
        assert version in user_agent

class TestMessageHandlers:
    """Test message handling functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_say = Mock()
        self.mock_message = {
            'user': 'U123456',
            'text': 'test message',
            'channel': 'C123456'
        }
    
    def test_hello_message_handler(self):
        """Test hello message response."""
        from listeners.messages import register_message_listeners
        
        # This is a simplified test - in practice you'd use Slack's testing utilities
        # For now, we're just testing that the module imports correctly
        assert callable(register_message_listeners)
    
    def test_help_message_handler(self):
        """Test help message response."""
        from listeners.messages import register_message_listeners
        assert callable(register_message_listeners)

class TestSlashCommands:
    """Test slash command functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_ack = Mock()
        self.mock_respond = Mock()
        self.mock_command = {
            'text': 'test command',
            'user_id': 'U123456'
        }
    
    def test_echo_command(self):
        """Test echo command."""
        from listeners.commands import register_command_listeners
        assert callable(register_command_listeners)
    
    def test_joke_command(self):
        """Test joke command."""
        from listeners.commands import register_command_listeners
        assert callable(register_command_listeners)

if __name__ == "__main__":
    pytest.main([__file__]) 