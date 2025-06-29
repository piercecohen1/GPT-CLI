"""Configuration management for GPT-CLI."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration class for GPT-CLI application."""
    
    # API Configuration
    openai_api_key: Optional[str] = None
    default_model: str = "gpt-3.5-turbo"
    default_system_message: str = "You are a helpful assistant. Keep your answers concise when possible."
    
    # UI Configuration
    clear_on_init: bool = False
    enable_markdown: bool = True
    enable_syntax_highlighting: bool = True
    
    # File paths
    default_save_directory: str = "."
    
    def __post_init__(self) -> None:
        """Initialize configuration after dataclass creation."""
        if self.openai_api_key is None:
            self.openai_api_key = os.environ.get("OPENAI_API_KEY")
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls(
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            default_model=os.environ.get("GPT_CLI_MODEL", "gpt-3.5-turbo"),
            default_system_message=os.environ.get(
                "GPT_CLI_SYSTEM_MESSAGE", 
                "You are a helpful assistant. Keep your answers concise when possible."
            ),
            clear_on_init=os.environ.get("GPT_CLI_CLEAR_ON_INIT", "false").lower() == "true",
        )
    
    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.openai_api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or provide it in configuration."
            )