"""Command handling for GPT-CLI."""

import logging
from typing import Dict, Callable, Any, Optional
import pyperclip
from rich.table import Table

from .utils import clear_terminal, count_messages_by_role

logger = logging.getLogger(__name__)


class CommandHandler:
    """Handles all CLI commands for the GPT application."""
    
    def __init__(self, chat_app: Any) -> None:
        """Initialize command handler.
        
        Args:
            chat_app: ChatApplication instance
        """
        self.chat_app = chat_app
        self.commands: Dict[str, Callable[[str], None]] = {
            '/save': self._save_command,
            '/load': self._load_command,
            '/quit': self._quit_command,
            '/exit': self._quit_command,
            '/info': self._info_command,
            '/clear': self._clear_command,
            '/new': self._new_command,
            '/system': self._system_command,
            '/model': self._model_command,
            '/copy': self._copy_command,
            '/paste': self._paste_command,
            '/help': self._help_command,
        }
    
    def handle_command(self, user_input: str) -> bool:
        """Handle a command input.
        
        Args:
            user_input: Full user input starting with '/'
            
        Returns:
            True if should exit, False otherwise
        """
        parts = user_input.split(' ', 1)
        command = parts[0].lower()
        argument = parts[1].strip() if len(parts) > 1 else ""
        
        if command in self.commands:
            try:
                result = self.commands[command](argument)
                if command in ['/quit', '/exit']:
                    return True
            except Exception as e:
                logger.error(f"Error executing command {command}: {e}")
                print(f"Error executing command: {e}")
        else:
            print(f"Unknown command: {command}")
            print("Type /help to see available commands.")
        
        return False
    
    def _save_command(self, filename: str) -> None:
        """Save chat to file."""
        if not filename:
            print("Please specify a filename after the /save command.")
            return
        self.chat_app.save_chat(filename)
    
    def _load_command(self, filename: str) -> None:
        """Load chat from file."""
        if not filename:
            print("Please specify a filename after the /load command.")
            return
        self.chat_app.load_chat(filename)
    
    def _quit_command(self, _: str) -> None:
        """Quit the application."""
        print("Exiting the GPT-CLI.")
    
    def _info_command(self, _: str) -> None:
        """Display chat information."""
        messages = self.chat_app.messages
        user_count = count_messages_by_role(messages, 'user')
        assistant_count = count_messages_by_role(messages, 'assistant')
        
        table = Table(title="Chat Information", show_header=True, header_style="bold magenta")
        table.add_column("Attribute", style="dim", width=20)
        table.add_column("Value")
        table.add_row("Model", self.chat_app.model)
        table.add_row("System Message", self.chat_app.system_message)
        table.add_row("User Messages", str(user_count))
        table.add_row("Assistant Messages", str(assistant_count))
        
        self.chat_app.console.print(table)
    
    def _clear_command(self, _: str) -> None:
        """Clear the terminal."""
        clear_terminal()
    
    def _new_command(self, _: str) -> None:
        """Start a new chat session."""
        self.chat_app.initialize_messages()
        print("Started a new chat session.")
    
    def _system_command(self, system_message: str) -> None:
        """Start new chat with custom system message."""
        if not system_message:
            print("Please provide a system message after the /system command.")
            return
        
        clear_terminal()
        self.chat_app.initialize_messages(system_message=system_message)
        print("Started a new chat with a custom system message.")
    
    def _model_command(self, model: str) -> None:
        """Switch to a different model."""
        if not model:
            print("Please specify a model name after the /model command.")
            return
        
        clear_terminal()
        self.chat_app.model = model
        self.chat_app.initialize_messages()
        print(f"Switched model to {model} and started a new chat session.")
    
    def _copy_command(self, _: str) -> None:
        """Copy last response to clipboard."""
        if not self.chat_app.messages:
            print("No messages to copy.")
            return
        
        last_message = self.chat_app.messages[-1]['content']
        try:
            pyperclip.copy(last_message)
            print("Copied the last message to the clipboard.")
        except Exception as e:
            logger.error(f"Failed to copy to clipboard: {e}")
            print(f"Failed to copy to clipboard: {e}")
    
    def _paste_command(self, _: str) -> None:
        """Paste content from clipboard and send as message."""
        try:
            pasted_content = pyperclip.paste()
            if not pasted_content.strip():
                print("Clipboard is empty.")
                return
            
            self.chat_app.add_message("user", pasted_content)
            response = self.chat_app.try_chat_completion()
            if response:
                self.chat_app.add_message("assistant", response)
        except Exception as e:
            logger.error(f"Failed to paste from clipboard: {e}")
            print(f"Failed to paste from clipboard: {e}")
    
    def _help_command(self, _: str) -> None:
        """Display help message."""
        help_text = """
Available commands:
/paste                    Paste clipboard content
/copy                     Copy the last response to the clipboard
/new                      Start a new chat
/clear                    Clear terminal window
/system [SYSTEM PROMPT]   Start a new chat with a custom system message
/model [MODEL]            Start a new chat with the specified model
/quit                     Exit the program
/info                     Display info about the current chat session
/save [FILENAME]          Save the chat to a file
/load [FILENAME]          Load a chat from a file
/help                     Display this help message
        """
        print(help_text.strip())