"""GPT-CLI: An interactive CLI for GPT models.

A modern, modular Python CLI application for interacting with OpenAI's GPT models
with features like conversation management, clipboard integration, and extensible commands.
"""

__version__ = "2.0.0"
__author__ = "Pierce Cohen"
__email__ = "piercecohen1@users.noreply.github.com"

from .chat import ChatApplication
from .cli import main

__all__ = ["ChatApplication", "main"]