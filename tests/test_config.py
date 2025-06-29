"""Tests for configuration management."""

import os
import pytest
from unittest.mock import patch

from src.gpt_cli.config import Config


class TestConfig:
    """Test configuration management."""
    
    def test_config_defaults(self) -> None:
        """Test default configuration values."""
        config = Config()
        assert config.default_model == "gpt-3.5-turbo"
        assert config.clear_on_init is False
        assert config.enable_markdown is True
        assert config.default_save_directory == "."
    
    def test_config_from_env(self) -> None:
        """Test configuration from environment variables."""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'GPT_CLI_MODEL': 'gpt-4',
            'GPT_CLI_CLEAR_ON_INIT': 'true'
        }):
            config = Config.from_env()
            assert config.openai_api_key == 'test-key'
            assert config.default_model == 'gpt-4'
            assert config.clear_on_init is True
    
    def test_config_validation_missing_api_key(self) -> None:
        """Test configuration validation with missing API key."""
        config = Config(openai_api_key=None)
        with pytest.raises(ValueError, match="OpenAI API key is required"):
            config.validate()
    
    def test_config_validation_with_api_key(self) -> None:
        """Test configuration validation with API key."""
        config = Config(openai_api_key="test-key")
        config.validate()  # Should not raise