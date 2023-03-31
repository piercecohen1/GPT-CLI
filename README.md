# GPT-CLI
An interactive CLI for GPT models

[![asciicast](https://asciinema.org/a/gVbepEltW8Gb19NyK3Kzmya4h.svg)](https://asciinema.org/a/gVbepEltW8Gb19NyK3Kzmya4h)

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
1. Clone the repository:
```bash
git clone https://github.com/yourusername/gpt-chat-cli.git
cd gpt-chat-cli
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip3 install -r requirements.txt
```

4. Add your OpenAI API key as an environment variable:
```bash
export OPENAI_API_KEY=your_api_key  # On Windows: set OPENAI_API_KEY=your_api_key
```

Alternatively, you can uncomment and replace the "YOUR_API_KEY" placeholder in the code with your actual API key.

## Usage
Run the chat application:
```bash
python3 chat.py
```

Enter your message and press enter to send it. The AI model will respond accordingly. To use the available commands, type a `/` followed by the command.

Available commands:
```
/paste                    Your clipboard contents will be substituted for the `/paste`

/copy                     Copy the last response to the clipboard

/new                      Start a new chat

/system [SYSTEM PROMPT]   Start a new chat with a custom system message

/model [MODEL]            Switch models and reset the chat

/quit                     Quit the interactive chat

/info                     Display current model and messages

/save [FILENAME]          Save the chat to a file

/load [FILENAME]          Load a chat from a file

/help                     Display help menu
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
