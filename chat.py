# Author: Pierce Cohen
# Description: An interactive CLI for GPT models

import openai
import os
import sys
from rich.console import Console
from rich.markdown import Markdown
import pyperclip
from playsound import playsound
import readline

# OpenAI API key, stored as an environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Uncomment the following line if you wish to hardcode your API key
# openai.api_key = "YOUR_API_KEY"


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


class ChatApplication:
    def __init__(self, system_message=None, model="gpt-3.5-turbo"):
        self.model = model
        self.system_message = system_message
        self.initialize_messages()
        self.console = Console()
        self.sound = True # Set to False to disable sound

    def initialize_messages(self):
        if self.system_message:
            self.messages = [{"role": "system", "content": self.system_message}]
        else:
            self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

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
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.messages
            )
            assistant_response = response.choices[0].message["content"]
            return assistant_response
        except Exception as e:
            print(f"An error occurred while processing your request: {e}")
            return None

def main():
    chat_app = ChatApplication()
    last_response = ""
    print("Model: " + chat_app.model)
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
                        print(f"Model: {chat_app.model}")
                        print(f"Messages: {chat_app.messages}")

                continue

            chat_app.add_message("user", user_message)
            assistant_response = chat_app.get_chat_completion()
            if assistant_response is not None:
                chat_app.add_message("assistant", assistant_response)
                last_response = assistant_response
                chat_app.display_markdown(f"**Assistant:** {assistant_response}")
                if chat_app.sound:
                    playsound("alert.wav")
            else:
                print("Assistant: I'm unable to provide a response at the moment.")
    except KeyboardInterrupt:
        print("\n\nExiting the chat application. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()