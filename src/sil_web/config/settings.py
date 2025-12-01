"""
Configuration and settings.

Single source of truth for app configuration.
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent.parent

# DOCS_PATH: Use environment variable if set (for containers),
# otherwise fall back to local development path
DOCS_PATH = Path(os.getenv("SIL_DOCS_PATH", BASE_DIR.parent / "SIL" / "docs"))

# Server
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True

# GitHub (optional)
GITHUB_TOKEN = None  # Set via environment variable if needed
