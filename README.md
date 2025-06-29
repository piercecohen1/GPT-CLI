# GPT-CLI

A modern, modular Python CLI application for interacting with OpenAI's GPT models.

**Click below to see a short demo!**

[![asciicast](https://asciinema.org/a/572801.svg)](https://asciinema.org/a/572801)

## Features

### Core Functionality
* **Interactive CLI**: Simple and intuitive command-line interface
* **Multiple Models**: Support for all OpenAI GPT models (GPT-3.5, GPT-4, etc.)
* **Rich Text**: Markdown rendering with syntax highlighting for code blocks
* **Conversation Management**: Save and restore chat conversations
* **System Messages**: Customize system prompts for different use cases

### User Experience
* **Clipboard Integration**: Easy copy/paste operations
* **Model Switching**: Change models on the fly without losing context
* **Command System**: Powerful slash commands for chat management
* **Configuration**: Environment-based configuration with sensible defaults
* **Logging**: Comprehensive logging for debugging and monitoring

### Developer Features  
* **Modern Python**: Type hints, dataclasses, and modern Python practices
* **Modular Architecture**: Clean separation of concerns across modules
* **Comprehensive Testing**: Unit tests with pytest
* **Code Quality**: Linting with ruff, formatting with black
* **Development Tools**: Pre-commit hooks, mypy type checking

## Installation

### Requirements
- Python 3.8 or higher (Python 3.10+ recommended)
- OpenAI API key

### Quick Install

1. **Clone the repository:**
```bash
git clone https://github.com/piercecohen1/GPT-CLI.git
cd GPT-CLI
```

2. **Create a virtual environment** (recommended):
```bash
python3 -m venv gpt-venv
source gpt-venv/bin/activate  # On Windows: gpt-venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
# Or for development:
pip install -e ".[dev]"
```

4. **Set up your OpenAI API key:**

```bash
# For Zsh:
echo "export OPENAI_API_KEY=your_api_key" >> ~/.zshrc && source ~/.zshrc

# For Bash:
echo "export OPENAI_API_KEY=your_api_key" >> ~/.bashrc && source ~/.bashrc

# Or set temporarily:
export OPENAI_API_KEY=your_api_key
```

### Package Installation (Future)
```bash
pip install gpt-cli  # Coming soon
```

## Usage

### Basic Usage
```bash
# Run the interactive chat
python3 chat.py

# Or use as a module
python3 -m gpt_cli

# Quick query
python3 chat.py --query "Explain Python decorators"

# Use different model
python3 chat.py --model gpt-4

# Custom system message
python3 chat.py --system "You are a helpful coding assistant"
```

### Command Line Options
```bash
python3 chat.py --help
```

### Interactive Commands
Once running, use these commands in the chat interface:

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

## Development

### Project Structure
```
GPT-CLI/
├── src/gpt_cli/           # Main package
│   ├── __init__.py        # Package initialization
│   ├── __main__.py        # Module entry point
│   ├── cli.py             # CLI interface and argument parsing
│   ├── chat.py            # ChatApplication class
│   ├── commands.py        # Command handling logic
│   ├── config.py          # Configuration management
│   └── utils.py           # Utility functions
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_config.py
│   └── test_utils.py
├── chat.py                # Backward compatibility entry point
├── pyproject.toml         # Modern Python packaging
├── requirements.txt       # Dependencies
├── .pre-commit-config.yaml # Pre-commit hooks
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

### Development Setup

1. **Clone and set up development environment:**
```bash
git clone https://github.com/piercecohen1/GPT-CLI.git
cd GPT-CLI
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

2. **Install pre-commit hooks:**
```bash
pre-commit install
```

3. **Run tests:**
```bash
pytest
pytest --cov=src/gpt_cli  # With coverage
```

4. **Code quality checks:**
```bash
ruff check src/              # Linting
black src/ tests/            # Formatting
mypy src/                    # Type checking
```

### Architecture Improvements (v2.0.0)

This version represents a major refactor from the original single-file implementation:

**✅ Improvements Made:**
- **Modular Architecture**: Split monolithic code into logical modules
- **Type Safety**: Added comprehensive type hints throughout
- **Modern Python**: Leveraged dataclasses, pathlib, and Python 3.8+ features  
- **Error Handling**: Improved error handling and user feedback
- **Configuration**: Environment-based configuration management
- **Testing**: Added unit tests with pytest
- **Documentation**: Comprehensive docstrings and improved README
- **Code Quality**: Integrated ruff, black, mypy, and pre-commit hooks
- **Packaging**: Modern pyproject.toml-based packaging
- **Logging**: Structured logging for debugging and monitoring

**🔧 Technical Debt Resolved:**
- Fixed file naming inconsistency (stream.py → chat.py)
- Removed unused resources (alert.wav)
- Eliminated hard-coded configuration values
- Separated concerns (CLI, chat logic, commands, utilities)
- Added proper entry points and import structure

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is released under the MIT License.
