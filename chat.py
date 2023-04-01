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
from rich.table import Table

if os.name == "nt":
    import pyreadline as readline
else:
    import gnureadline as readline


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

def file_completion(text, state):
    files = [f for f in os.listdir() if f.startswith(text)]
    return files[state] if state < len(files) else None

class ChatApplication:
    def __init__(self, system_message=None, model="gpt-3.5-turbo"):
        self.model = model
        self.system_message = system_message
        self.initialize_messages()
        self.console = Console()
        self.sound = True # Set to False to disable sound

    def initialize_messages(self, system_message=None, model=None):
        if system_message:
            self.system_message = system_message
        else:
            self.system_message = "You are a helpful assistant"
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
        self.console.print(markdown)

    def get_chat_completion(self):
        try:
            # Uncomment if you wish, useful for debugging
            # print("Sent: " + self.messages[-1]["content"])
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages
            )
            assistant_response = response.choices[0].message["content"]
            return assistant_response
        except openai.error.OpenAIError as e:
            if 'maximum context length' in str(e):
                while True:
                    # Remove the oldest message (excluding system message)
                    if len(self.messages) > 1:
                        self.messages.pop(1)
                    else:
                        break

                    # Retry the API call
                    try:
                        response = openai.ChatCompletion.create(
                            model=self.model,
                            messages=self.messages
                        )
                        assistant_response = response.choices[0].message["content"]
                        return assistant_response
                    except openai.error.OpenAIError as retry_e:
                        if 'maximum context length' not in str(retry_e):
                            print(f"An error occurred while processing your request: {retry_e}")
                            break
            else:
                print(f"An error occurred while processing your request: {e}")
            return None

    def save_chat(self, filename):
        try:
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
        clear_terminal()
        try:
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
    args = parser.parse_args()

    if args.version:
        print("GPT-CLI version 1.2.0")
        sys.exit(0)
        
    chat_app = ChatApplication()

    last_response = ""
    print("Model: " + chat_app.model)

    readline.set_completer(file_completion)
    readline.parse_and_bind("tab: complete")

    try:
        while True:
            user_message = input("You: ")

            if "/paste" in user_message:
                user_message = user_message.replace("/paste", pyperclip.paste())

            if user_message.startswith("/"):
                commands = user_message.split("/")

                new_system_message = None
                new_model = None

                for command in commands:
                    command = command.lower().strip()
                    if command.startswith("system"):
                        new_system_message = command[6:].strip()
                        if "/paste" in new_system_message:
                            new_system_message = new_system_message.replace("/paste", pyperclip.paste())
                    elif command.startswith("model"):
                        new_model = command[5:].strip()

                if new_system_message is not None or new_model is not None:
                    clear_terminal()
                    chat_app = ChatApplication(system_message=new_system_message if new_system_message is not None else chat_app.system_message, 
                                            model=new_model if new_model is not None else chat_app.model)
                    chat_app.initialize_messages(system_message=new_system_message if new_system_message is not None else chat_app.system_message, 
                                                model=new_model if new_model is not None else chat_app.model)
                    print("Started a new chat with updated settings.")

                for command in commands:
                    command = command.lower().strip()

                    if command.startswith("system") or command.startswith("model"):
                        continue

                    if command.startswith("help"):
                        print("Available commands:")
                        print("/paste - Paste content from the clipboard")
                        print("/copy - Copy the last response to the clipboard")
                        print("/new - Start a new chat")
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
                        chat_app = ChatApplication()
                        print("Started a new chat.")
                    elif command.startswith("system"):
                        system_message = command[6:].strip()
                        clear_terminal()
                        chat_app = ChatApplication(system_message=system_message)  # Create a new chat with a custom system message
                        print("Started a new chat with a custom system message.")
                    elif command.startswith("model"):
                        model_name = command[5:].strip()
                        if model_name:
                            clear_terminal()
                            chat_app = ChatApplication(model=model_name)  # Create a new chat with the specified model
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
                    elif command.startswith("save"):
                        filename = command[4:].strip()
                        if filename:
                            chat_app.save_chat(filename)
                        else:
                            print("Please specify a filename after the /save command.")
                    elif command.startswith("load"):
                        filename = command[4:].strip()
                        if filename:
                            chat_app.load_chat(filename)
                        else:
                            print("Please specify a filename after the /load command.")

                continue

            chat_app.add_message("user", user_message)
            assistant_response = chat_app.get_chat_completion()
            if assistant_response is not None:
                chat_app.add_message("assistant", assistant_response)
                last_response = assistant_response
                chat_app.display_markdown(f"**Assistant:** {assistant_response}")
                if chat_app.sound:
                    playsound(audio_file_path)
            else:
                print("Assistant: I'm unable to provide a response at the moment.")
    except KeyboardInterrupt:
        print("\n\nExiting the chat application. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()