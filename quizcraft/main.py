#!/usr/bin/env python3
"""
QuizCraft - Main entry point
"""
import sys

from .ui.cli import main as cli_main


def main():
    """Main entry point for the application"""
    return cli_main()


if __name__ == "__main__":
    sys.exit(main())
