"""Handle Anthropic API credentials and authentication."""

import os

from dotenv import load_dotenv


def load_api_credentials():
    """
    Load API credentials from environment variables.

    Returns:
        dict: A dictionary containing API credentials
    """
    # Try to load from .env file
    load_dotenv()

    # Get API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found in environment. "
            "Please set it in your .env file or environment variables."
        )

    return {
        "api_key": api_key,
    }


def get_api_key():
    """
    Get the Anthropic API key.

    Returns:
        str: The API key

    Raises:
        ValueError: If API key is not found
    """
    return load_api_credentials()["api_key"]
