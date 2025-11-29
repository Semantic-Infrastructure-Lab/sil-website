"""
Configuration and settings.

Single source of truth for app configuration.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent.parent
SIL_REPO_PATH = BASE_DIR.parent / "SIL"
DOCS_PATH = SIL_REPO_PATH / "docs"

# Server
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True

# GitHub (optional)
GITHUB_TOKEN = None  # Set via environment variable if needed
