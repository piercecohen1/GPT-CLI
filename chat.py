#!/usr/bin/env python3
"""
GPT-CLI: An interactive CLI for GPT models

This is the main entry point that maintains backward compatibility
with the original stream.py interface while using the new modular architecture.

Author: Pierce Cohen
Version: 2.0.0
"""

# For backward compatibility, import and run the main function
from src.gpt_cli.cli import main

if __name__ == "__main__":
    main()