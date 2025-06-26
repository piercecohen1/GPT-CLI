# GPT-CLI
An interactive CLI for GPT models

**Click below to see a short demo!**

[![asciicast](https://asciinema.org/a/572801.svg)](https://asciinema.org/a/572801)

## Features
* Simple and intuitive command-line interface
* Supports Markdown with syntax-highlighting for code
* Work with all OpenAI GPT models
* Customize system message
* Supports clipboard operations
* Play sounds on response
* Model switching on the fly
* Chat commands to manage the chat and settings
* Save and Restore chat conversations

## Installation

#### Make sure you have Python 3.10 or higher installed on your system. You can check your Python version by running `python --version` or `python3 --version` in your terminal. Older version may work but have not been tested.

1. Clone the repository:
```bash
git clone https://github.com/piercecohen1/GPT-CLI.git
cd GPT-CLI
```

2. Create a virtual environment and activate it (optional):
```bash
python3 -m venv gpt-venv
source gpt-venv/bin/activate  # On Windows: gpt-venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip3 install -r requirements.txt
```

4. Add your OpenAI API key as an environment variable (replace your_api_key with your actual API key):

For Zsh:
```bash
echo "export OPENAI_API_KEY=your_api_key" >> ~/.zshrc
source ~/.zshrc
```

For Bash:
```bash
echo "export OPENAI_API_KEY=your_api_key" >> ~/.bashrc
source ~/.bashrc
```

Or, to set temporarily:
```bash
export OPENAI_API_KEY=your_api_key  # On Windows: set OPENAI_API_KEY=your_api_key
```


Alternatively, you can uncomment and replace the "YOUR_API_KEY" placeholder in the code with your actual API key.

## Usage
Run the chat application:
```bash
python3 stream.py
```

Enter your message and press enter to send it. The AI model will respond accordingly. To use the available commands, type a `/` followed by the command.

Available commands:
```
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
```


## Examples


### Customize system messages to "jailbreak" models

[![asciicast](https://asciinema.org/a/iQHmpE9qKKeJ0lWphlwUEI4VE.svg)](https://asciinema.org/a/iQHmpE9qKKeJ0lWphlwUEI4VE)


### Paste easily from the command-line

[![asciicast](https://asciinema.org/a/GQPq0nWtGyF9uXGiJ6MMGhQMX.svg)](https://asciinema.org/a/GQPq0nWtGyF9uXGiJ6MMGhQMX)

### Quickly copy responses

[![asciicast](https://asciinema.org/a/SHTVLa7xUjF94kTpTJPAochG2.svg)](https://asciinema.org/a/SHTVLa7xUjF94kTpTJPAochG2)

## License
This project is released under the MIT License.
