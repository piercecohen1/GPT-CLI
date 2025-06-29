"""Tests for utility functions."""

import json
import tempfile
import os
from unittest.mock import patch

from src.gpt_cli.utils import (
    save_json, load_json, format_messages, count_messages_by_role
)


class TestUtils:
    """Test utility functions."""
    
    def test_save_and_load_json(self) -> None:
        """Test JSON save and load functionality."""
        test_data = {"key": "value", "number": 42}
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = f.name
        
        try:
            # Test save
            save_json(test_data, temp_path)
            assert os.path.exists(temp_path)
            
            # Test load
            loaded_data = load_json(temp_path)
            assert loaded_data == test_data
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_format_messages(self) -> None:
        """Test message formatting."""
        messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        
        formatted = format_messages(messages)
        expected = "User: Hello\nAssistant: Hi there!"
        assert formatted == expected
    
    def test_count_messages_by_role(self) -> None:
        """Test message counting by role."""
        messages = [
            {"role": "system", "content": "System message"},
            {"role": "user", "content": "User message 1"},
            {"role": "assistant", "content": "Assistant response"},
            {"role": "user", "content": "User message 2"}
        ]
        
        assert count_messages_by_role(messages, "user") == 2
        assert count_messages_by_role(messages, "assistant") == 1
        assert count_messages_by_role(messages, "system") == 1
        assert count_messages_by_role(messages, "nonexistent") == 0
    
    def test_load_json_file_not_found(self) -> None:
        """Test loading JSON from non-existent file."""
        import pytest
        with pytest.raises(FileNotFoundError):
            load_json("nonexistent_file.json")