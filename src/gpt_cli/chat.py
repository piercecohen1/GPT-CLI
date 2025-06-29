"""Chat application for GPT-CLI."""

import logging
from typing import List, Dict, Optional, Any
import openai
from rich.console import Console
from rich.markdown import Markdown

from .config import Config
from .utils import save_json, load_json, clear_terminal

logger = logging.getLogger(__name__)


class ChatApplication:
    """Main chat application class for interacting with GPT models."""
    
    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialize the chat application.
        
        Args:
            config: Configuration object, defaults to Config.from_env()
        """
        self.config = config or Config.from_env()
        self.config.validate()
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.config.openai_api_key)
        
        # Chat state
        self.model = self.config.default_model
        self.system_message = self.config.default_system_message
        self.messages: List[Dict[str, str]] = []
        
        # UI components
        self.console = Console()
        
        # Initialize messages
        self.initialize_messages()
        
        if self.config.clear_on_init:
            clear_terminal()
    
    def initialize_messages(self, system_message: Optional[str] = None, model: Optional[str] = None) -> None:
        """Initialize or reset the conversation messages.
        
        Args:
            system_message: Custom system message, defaults to config default
            model: Model to use, defaults to current model
        """
        if system_message is not None:
            self.system_message = system_message
        else:
            self.system_message = self.config.default_system_message
            
        if model is not None:
            self.model = model
            
        self.messages = [{"role": "system", "content": self.system_message}]
        logger.info(f"Initialized chat with model: {self.model}")
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation.
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
        """
        message = {"role": role, "content": content}
        self.messages.append(message)
        logger.debug(f"Added {role} message: {content[:100]}...")
    
    def display_markdown(self, text: str) -> None:
        """Display text as markdown if enabled.
        
        Args:
            text: Text to display
        """
        if self.config.enable_markdown:
            markdown = Markdown(text)
            self.console.print(markdown, end="")
        else:
            print(text, end="")
    
    def try_chat_completion(self) -> str:
        """Attempt to get a chat completion from the API.
        
        Returns:
            The assistant's response content, or empty string if failed
        """
        response_content = ""
        
        try:
            logger.info(f"Requesting completion from {self.model}")
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=True
            )
            
            for part in stream:
                if part.choices[0].delta.content is not None:
                    content = part.choices[0].delta.content
                    print(content, end='', flush=True)
                    response_content += content
                
                # Check if the response is complete
                if (hasattr(part.choices[0], 'finish_reason') and 
                    part.choices[0].finish_reason == 'stop'):
                    print()  # Add newline after response
                    break
                    
        except openai.APIConnectionError as e:
            error_msg = "Could not reach OpenAI servers"
            logger.error(f"{error_msg}: {e}")
            print(f"Error: {error_msg}")
            if e.__cause__:
                print(f"Cause: {e.__cause__}")
                
        except openai.RateLimitError as e:
            error_msg = "Rate limit exceeded. Please wait and try again."
            logger.error(f"Rate limit error: {e}")
            print(f"Error: {error_msg}")
            
        except openai.APIStatusError as e:
            error_msg = f"API error with status code {e.status_code}"
            logger.error(f"{error_msg}: {e}")
            print(f"Error: {error_msg}")
            print(f"Response: {e.response}")
            
        except Exception as e:
            error_msg = f"Unexpected error occurred: {e}"
            logger.error(error_msg)
            print(f"Error: {error_msg}")
        
        return response_content.strip()
    
    def save_chat(self, filename: str) -> None:
        """Save the current chat to a file.
        
        Args:
            filename: Name of the file to save to
        """
        try:
            chat_data = {
                "model": self.model,
                "system_message": self.system_message,
                "messages": self.messages,
                "version": "2.0.0"
            }
            save_json(chat_data, filename)
            print(f"Chat saved to '{filename}'.")
            
        except Exception as e:
            logger.error(f"Failed to save chat to '{filename}': {e}")
            print(f"An error occurred while saving the chat: {e}")
    
    def load_chat(self, filename: str) -> None:
        """Load a chat from a file.
        
        Args:
            filename: Name of the file to load from
        """
        try:
            chat_data = load_json(filename)
            
            # Handle both old and new format
            self.model = chat_data.get("model", self.config.default_model)
            self.system_message = chat_data.get(
                "system_message", 
                self.config.default_system_message
            )
            self.messages = chat_data.get("messages", [])
            
            # Ensure system message is first if messages exist
            if self.messages and self.messages[0].get("role") != "system":
                self.messages.insert(0, {"role": "system", "content": self.system_message})
            
            print(f"Chat loaded from '{filename}'.")
            logger.info(f"Loaded chat from '{filename}' with {len(self.messages)} messages")
            
        except FileNotFoundError:
            error_msg = f"File '{filename}' not found."
            logger.error(error_msg)
            print(error_msg)
            
        except Exception as e:
            error_msg = f"An error occurred while loading the chat: {e}"
            logger.error(error_msg)
            print(error_msg)