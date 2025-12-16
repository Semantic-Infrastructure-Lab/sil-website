#!/bin/bash
# SIL Website - Documentation Sync Script
# Wrapper for sync-docs.py (Python implementation)
#
# This bash script exists for backward compatibility.
# The actual implementation is in sync-docs.py
#
# SESSION: bronze-spark-1216

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Call Python implementation
exec "$SCRIPT_DIR/sync-docs.py" "$@"
