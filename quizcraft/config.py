"""
Configuration settings for QuizCraft
"""

import os

from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

# Default configuration
DEFAULT_CONFIG = {
    "pdf": {
        "ocr_fallback": os.environ.get("OCR_ENABLED", "true").lower()
        == "true",
        "tesseract_path": os.environ.get(
            "TESSERACT_PATH", "/usr/local/bin/tesseract"
        ),
    },
    "api": {
        "max_retries": 3,
        "backoff_factor": 2,
    },
    "cache": {
        "max_size_mb": int(os.environ.get("CACHE_SIZE_LIMIT", "100")),
        "ttl_days": 7,
        "db_path": os.environ.get("CACHE_DB_PATH", ".cache/cache.db"),
    },
    "log": {
        "level": os.environ.get("LOG_LEVEL", "INFO"),
    },
}


def get_config():
    """Returns the current configuration"""
    # Create cache directory if it doesn't exist
    os.makedirs(
        os.path.dirname(DEFAULT_CONFIG["cache"]["db_path"]), exist_ok=True
    )
    return DEFAULT_CONFIG.copy()
