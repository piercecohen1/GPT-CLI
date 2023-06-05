#!/usr/bin/env python3

# Author: Pierce Cohen
# Description: An interactive CLI for GPT models

import openai
import os
import sys
from rich.console import Console
from rich.markdown import Markdown
import pyperclip
from playsound import playsound
import argparse
import json
import time
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import PathCompleter, Completer, Completion
from prompt_toolkit.document import Document
from rich.live import Live
from urllib3.exceptions import InvalidChunkLength

class CustomPathCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        if text.startswith("/save ") or text.startswith("/load "):
            command, partial_path = text.split(" ", 1)
            path_completer = PathCompleter()
            path_document = Document(partial_path, len(partial_path))
            for completion in path_completer.get_completions(path_document, complete_event):
                yield Completion(completion.text, completion.start_position, completion.display, completion.display_meta)

# OpenAI API key, stored as an environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Uncomment the following line if you wish to hardcode your API key
# openai.api_key = "YOUR_API_KEY"

if not openai.api_key:
    print("Error: OPENAI_API_KEY not found.")
    print("Please set the OPENAI_API_KEY environment variable or hardcode your API key.")
    sys.exit(1)

homebrew_prefix = os.environ.get("HOMEBREW_PREFIX", "/usr/local")
homebrew_audio_file_path = os.path.join(homebrew_prefix, "share", "gpt-cli", "resources", "alert.wav")
repo_audio_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "alert.wav")

audio_file_path = homebrew_audio_file_path if os.path.exists(homebrew_audio_file_path) else repo_audio_file_path

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

class ChatApplication:
    def __init__(self, system_message=None, model="gpt-4", clear_on_init=False):
        self.model = model
        self.system_message = system_message
        self.initialize_messages()
        self.console = Console()
        self.sound = True # Set to False to disable sound
        if clear_on_init:
            clear_terminal()

    def initialize_messages(self, system_message=None, model=None):
        if system_message:
            self.system_message = system_message
        else:
            self.system_message = "You are a helpful assistant. Keep your answers concise when possible."
        if model:
            self.model = model
        self.messages = [{"role": "system", "content": self.system_message}]


    def add_message(self, role, content):
        message = {
            "role": role,
            "content": content
        }
        self.messages.append(message)

    def display_markdown(self, text):
        markdown = Markdown(text)
        self.console.print(markdown, end="")

    def try_chat_completion(self):
        full_content = ""
        with Live(auto_refresh=False) as live:
            markdown_text = f"**Assistant:** "
            live.update(Markdown(markdown_text))
            for chunk in openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages,
                stream=True,
            ):
                content = chunk["choices"][0].get("delta", {}).get("content")
                if content:
                    markdown_text += content
                    full_content += content
                    live.update(Markdown(markdown_text))
                    live.refresh()
        return full_content


    def get_chat_completion(self):
        try:
            return self.try_chat_completion()
        
        except InvalidChunkLength as e:
            print(f"An error occurred while processing the response: {e}")
            return None

        except openai.error.OpenAIError as e:
            if 'maximum context length' in str(e):
                retry_limit = 25  # Set a limit for the number of retries
                retry_count = 0

                while retry_count < retry_limit:
                    retry_count += 1
                    # Remove the oldest two messages (excluding system message)
                    if len(self.messages) > 4:
                        for _ in range(4):
                            self.messages.pop(1)

                    time.sleep(0.1) 
                    # Retry the API call
                    # TODO: Make separate function for this
                    try:
                        return self.try_chat_completion()
                    except openai.error.OpenAIError as retry_e:
                        if 'maximum context length' not in str(retry_e):
                            print(f"An error occurred while processing your request: {retry_e}")
                            break
            else:
                print(f"An error occurred while processing your request: {e}")
            return None

    def save_chat(self, filename):
        try:
            abs_path = os.path.abspath(filename)
            if os.path.isdir(abs_path):
                print("Error: The specified path is a directory, please provide a valid file name.")
                return

            base_path = os.path.dirname(abs_path)
            if not os.path.exists(base_path):
                os.makedirs(base_path)

            # Remove the model information from the messages
            for message in self.messages:
                if "model" in message:
                    del message["model"]

            chat_data = {
                "model": self.model,
                "messages": self.messages
            }

            with open(filename, "w") as outfile:
                json.dump(chat_data, outfile)

            print(f"Chat saved to '{filename}'.")
        except Exception as e:
            print(f"An error occurred while saving the chat: {e}")

    def load_chat(self, filename):
        try:
            filename = os.path.abspath(filename)
            with open(filename, "r") as infile:
                chat_data = json.load(infile)

            loaded_messages = chat_data["messages"]
            
            system_message = None
            model = chat_data["model"] if "model" in chat_data else None
            for message in loaded_messages:
                if message["role"] == "system":
                    system_message = message["content"]

            if model:
                self.model = model

            self.initialize_messages(system_message, model)
            self.messages = loaded_messages
            print(f"Chat loaded from '{filename}'.")
            
            for message in loaded_messages:
                role = message["role"].capitalize()
                content = message["content"]
                if role == "Assistant":
                    self.display_markdown(f"**{role}:** {content}")
                else:
                    print(f"{role}: {content}")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred while loading the chat: {e}")

    def format_messages(self):
        formatted_messages = ""
        for message in self.messages:
            role = message["role"].capitalize()
            content = message["content"]
            formatted_messages += f"{role}: {content}\n"
        return formatted_messages


def main():
    parser = argparse.ArgumentParser(description="An interactive CLI for GPT models")
    parser.add_argument("-v", "--version", action="store_true", help="Show the version number and exit")
    parser.add_argument("--load", type=str, help="Load a chat from a file immediately upon launching the program")
    parser.add_argument("-q", "--query", type=str, help="Execute a query immediately upon launch")
    args = parser.parse_args()

    if args.version:
        print("GPT-CLI version 1.2.5")
        sys.exit(0)
        
    chat_app = ChatApplication(clear_on_init=False)

    if args.load:
        chat_app.load_chat(args.load)

    if args.query:
        print()
        chat_app.add_message("user", args.query)
        assistant_response = chat_app.get_chat_completion()
        if assistant_response is not None:
            chat_app.add_message("assistant", assistant_response)
            if chat_app.sound:
                playsound(audio_file_path)
        else:
            print("Assistant: I'm unable to provide a response at the moment.")

    last_response = ""
    print("Model: " + chat_app.model)

    session = PromptSession(completer=CustomPathCompleter())

    try:
        while True:
            user_message = session.prompt("You: ")
            if "/paste" in user_message:
                clipboard_content = pyperclip.paste()
                if clipboard_content is None:
                    print("Clipboard is empty.")
                    continue
                user_message = user_message.replace("/paste", clipboard_content)

            if user_message.startswith("/"):
                if user_message.startswith("/save ") or user_message.startswith("/load "):
                    commands = [user_message[1:]]
                else:
                    commands = user_message.split("/")

                new_system_message = None
                new_model = None

                # TODO: Handle commands with a dictionary and separate functions for each command
                for command in commands:
                    command = command.lower().strip()
                    if command.startswith("system"):
                        new_system_message = command[6:].strip()
                        if "/paste" in new_system_message:
                            new_system_message = new_system_message.replace("/paste", pyperclip.paste())
                    elif command.startswith("model"):
                        new_model = command[5:].strip()

                if new_system_message is not None or new_model is not None:
                    chat_app = ChatApplication(clear_on_init=True,system_message=new_system_message if new_system_message is not None else chat_app.system_message, 
                                            model=new_model if new_model is not None else chat_app.model)
                    chat_app.initialize_messages(system_message=new_system_message if new_system_message is not None else chat_app.system_message, 
                                                model=new_model if new_model is not None else chat_app.model)
                    print("\n\nStarted a new chat with updated settings.")

                for command in commands:
                    command = command.lower().strip()

                    if command.startswith("system") or command.startswith("model"):
                        continue

                    if command.startswith("help"):
                        print("Available commands:")
                        print("/paste - Paste content from the clipboard")
                        print("/copy - Copy the last response to the clipboard")
                        print("/new - Start a new chat")
                        print("/clear - Clear terminal window")
                        print("/system - Start a new chat with a custom system message")
                        print("/model - Switch models and reset the chat")
                        print("/quit - Quit the interactive chat")
                        print("/info - Display current model and messages")
                        print("/save [FILENAME] - Save the chat to a file")
                        print("/load [FILENAME] - Load a chat from a file")
                    if command.startswith("copy"):
                        pyperclip.copy(last_response)
                        print("Assistant's response copied to clipboard.")
                    elif command.startswith("new"):
                        clear_terminal()
                        chat_app = ChatApplication(clear_on_init=True)
                        print("\n\nStarted a new chat.")
                    elif command.startswith("system"):
                        system_message = command[6:].strip()
                        clear_terminal()
                        chat_app = ChatApplication(clear_on_init=True,system_message=system_message)  # Create a new chat with a custom system message
                        print("Started a new chat with a custom system message.")
                    elif command.startswith("model"):
                        model_name = command[5:].strip()
                        if model_name:
                            clear_terminal()
                            chat_app = ChatApplication(clear_on_init=True,model=model_name)  # Create a new chat with the specified model
                            print(f"Switched to model '{model_name}' and started a new chat.")
                        else:
                            print("Please specify a model name after the /model command.")
                    elif command.startswith("quit") or command.startswith("exit"):
                        print("Exiting the chat application. Goodbye!")
                        sys.exit(0)
                    elif command.startswith("info"):
                        user_messages = sum(1 for message in chat_app.messages if message["role"] == "user")
                        assistant_messages = sum(1 for message in chat_app.messages if message["role"] == "assistant")
                        system_message = chat_app.system_message

                        table = Table(show_header=True, header_style="bold magenta")
                        table.add_column("Attribute")
                        table.add_column("Value")

                        table.add_row("Model", chat_app.model)
                        table.add_row("System Message", system_message)
                        table.add_row("User Messages", str(user_messages))
                        table.add_row("Assistant Messages", str(assistant_messages))

                        chat_app.console.print(table)
                    elif user_message.startswith("/save "):
                        filename = user_message[5:].strip()
                        if filename:
                            if not os.path.dirname(filename):
                                filename = os.path.join(os.getcwd(), filename)
                            if os.path.isdir(filename):
                                print("Error: The specified path is a directory, please provide a valid file name.")
                            else:
                                chat_app.save_chat(filename)
                        else:
                            print("Please specify a filename after the /save command.")
                    elif user_message.startswith("/load "):
                        filename = user_message[5:].strip()
                        if filename:
                            if not os.path.dirname(filename):
                                filename = os.path.join(os.getcwd(), filename)
                            chat_app.load_chat(filename)
                        else:
                            print("Please specify a filename after the /load command.")
                    elif command.startswith("clear"):
                        clear_terminal()
                        print("\n")

                continue

            chat_app.add_message("user", user_message)
            assistant_response = chat_app.get_chat_completion()
            if assistant_response is not None:
                chat_app.add_message("assistant", assistant_response)
                last_response = assistant_response
                if chat_app.sound:
                    playsound(audio_file_path)
            else:
                print("Assistant: I'm unable to provide a response at the moment.")
    except KeyboardInterrupt:
        print("\n\nExiting the chat application. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()