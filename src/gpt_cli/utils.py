"""Utility functions for GPT-CLI."""

import os
from typing import Any, Dict, List
import json
import logging

logger = logging.getLogger(__name__)


def clear_terminal() -> None:
    """Clear the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ]
    )


def save_json(data: Dict[str, Any], filepath: str) -> None:
    """Save data to JSON file.
    
    Args:
        data: Data to save
        filepath: Path to save the file
        
    Raises:
        IOError: If file cannot be written
    """
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        logger.info(f"Data saved to '{filepath}'")
    except IOError as e:
        logger.error(f"Failed to save data to '{filepath}': {e}")
        raise


def load_json(filepath: str) -> Dict[str, Any]:
    """Load data from JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Loaded data dictionary
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file contains invalid JSON
    """
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        logger.info(f"Data loaded from '{filepath}'")
        return data
    except FileNotFoundError:
        logger.error(f"File '{filepath}' not found")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in '{filepath}': {e}")
        raise


def format_messages(messages: List[Dict[str, str]]) -> str:
    """Format messages for display.
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        Formatted string representation of messages
    """
    return "\n".join(
        f"{message['role'].capitalize()}: {message['content']}"
        for message in messages
    )


def count_messages_by_role(messages: List[Dict[str, str]], role: str) -> int:
    """Count messages by role.
    
    Args:
        messages: List of message dictionaries
        role: Role to count (user, assistant, system)
        
    Returns:
        Number of messages with the specified role
    """
    return sum(1 for message in messages if message.get('role') == role)