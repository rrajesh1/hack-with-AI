"""
Pytest configuration and fixtures for Slack bot tests.
"""
import pytest
from unittest.mock import Mock
import os

@pytest.fixture
def mock_slack_app():
    """Mock Slack app for testing."""
    app = Mock()
    app.message = Mock()
    app.command = Mock()
    app.event = Mock()
    app.error = Mock()
    return app

@pytest.fixture
def mock_say():
    """Mock say function for testing."""
    return Mock()

@pytest.fixture
def mock_ack():
    """Mock ack function for testing."""
    return Mock()

@pytest.fixture
def mock_respond():
    """Mock respond function for testing."""
    return Mock()

@pytest.fixture
def sample_message():
    """Sample message event for testing."""
    return {
        'user': 'U123456789',
        'text': 'Hello bot!',
        'channel': 'C123456789',
        'ts': '1234567890.123456'
    }

@pytest.fixture
def sample_command():
    """Sample slash command for testing."""
    return {
        'command': '/test',
        'text': 'test argument',
        'user_id': 'U123456789',
        'channel_id': 'C123456789'
    }

@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing."""
    return {
        'SLACK_BOT_TOKEN': 'xoxb-test-bot-token-123',
        'SLACK_APP_TOKEN': 'xapp-test-app-token-123',
        'ENVIRONMENT': 'development'
    }

@pytest.fixture(autouse=True)
def setup_test_env(mock_env_vars):
    """Automatically set up test environment variables."""
    original_env = dict(os.environ)
    os.environ.update(mock_env_vars)
    yield
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env) 