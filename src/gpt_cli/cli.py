"""Command-line interface for GPT-CLI."""

import argparse
import sys
import logging
from typing import Optional
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter, Completer, Completion
from prompt_toolkit.document import Document

from . import __version__
from .config import Config
from .chat import ChatApplication
from .commands import CommandHandler
from .utils import setup_logging

logger = logging.getLogger(__name__)


class CustomPathCompleter(Completer):
    """Custom completer for file paths in save/load commands."""
    
    def get_completions(self, document: Document, complete_event) -> Completion:
        """Get completions for file paths.
        
        Args:
            document: Current document
            complete_event: Completion event
            
        Yields:
            Path completions
        """
        text = document.text_before_cursor
        if text.startswith("/save ") or text.startswith("/load "):
            try:
                command, partial_path = text.split(" ", 1)
                path_completer = PathCompleter()
                path_document = Document(partial_path, len(partial_path))
                for completion in path_completer.get_completions(path_document, complete_event):
                    yield Completion(completion.text, completion.start_position,
                                   completion.display, completion.display_meta)
            except ValueError:
                # Handle case where no space after command
                pass


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.
    
    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="An interactive CLI for GPT models",
        prog="gpt-cli"
    )
    
    parser.add_argument(
        "-v", "--version", 
        action="version", 
        version=f"GPT-CLI version {__version__}"
    )
    
    parser.add_argument(
        "--load", 
        type=str, 
        help="Load a chat from a file immediately upon launching the program"
    )
    
    parser.add_argument(
        "-q", "--query", 
        type=str, 
        help="Execute a query immediately upon launch"
    )
    
    parser.add_argument(
        "--model", 
        type=str,
        default="gpt-3.5-turbo",
        help="Specify the GPT model to use (default: gpt-3.5-turbo)"
    )
    
    parser.add_argument(
        "--system", 
        type=str,
        help="Set a custom system message"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="WARNING",
        help="Set the logging level (default: WARNING)"
    )
    
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="Don't clear terminal on startup"
    )
    
    return parser


def run_interactive_session(chat_app: ChatApplication) -> None:
    """Run the interactive chat session.
    
    Args:
        chat_app: Initialized ChatApplication instance
    """
    command_handler = CommandHandler(chat_app)
    session = PromptSession(completer=CustomPathCompleter())
    
    print(f"Model: {chat_app.model}")
    print("Type /help for available commands.")
    
    try:
        while True:
            try:
                user_input = session.prompt("You: ")
                
                if not user_input.strip():
                    continue
                
                if user_input.startswith('/'):
                    should_exit = command_handler.handle_command(user_input)
                    if should_exit:
                        break
                else:
                    # Regular chat message
                    chat_app.add_message("user", user_input)
                    assistant_response = chat_app.try_chat_completion()
                    if assistant_response:
                        chat_app.add_message("assistant", assistant_response)
                    print()  # Add blank line after response
                    
            except KeyboardInterrupt:
                print("\nUse /quit to exit or Ctrl+C again to force quit.")
                try:
                    # Give user a chance to quit gracefully
                    user_input = session.prompt("You: ")
                    if user_input.lower() in ['/quit', '/exit', 'quit', 'exit']:
                        break
                except KeyboardInterrupt:
                    print("\nForce quit detected. Exiting...")
                    break
                    
    except Exception as e:
        logger.error(f"Unexpected error in interactive session: {e}")
        print(f"An unexpected error occurred: {e}")


def main() -> None:
    """Main entry point for the GPT-CLI application."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    
    try:
        # Create configuration
        config = Config.from_env()
        config.default_model = args.model
        config.clear_on_init = not args.no_clear
        
        if args.system:
            config.default_system_message = args.system
        
        # Initialize chat application
        chat_app = ChatApplication(config)
        
        # Load chat if specified
        if args.load:
            chat_app.load_chat(args.load)
        
        # Execute query if specified
        if args.query:
            chat_app.add_message("user", args.query)
            response = chat_app.try_chat_completion()
            if response:
                chat_app.add_message("assistant", response)
            print()
            
            # If only query was specified, exit after response
            if not sys.stdin.isatty():
                return
        
        # Start interactive session
        run_interactive_session(chat_app)
        
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()