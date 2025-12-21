"""
llms.txt and llms-full.txt endpoints for LLM crawlers.

Provides structured navigation for LLM crawlers following the llms.txt spec:
https://llmstxt.org/
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

router = APIRouter()

# Path to static files
STATIC_DIR = Path("static")


@router.get("/llms.txt", response_class=PlainTextResponse)
async def llms_txt() -> str:
    """Serve llms.txt navigation file for LLM crawlers.

    Returns:
        llms.txt content as plain text
    """
    llms_file = STATIC_DIR / "llms.txt"

    if not llms_file.exists():
        raise HTTPException(status_code=404, detail="llms.txt not found")

    return llms_file.read_text()


@router.get("/llms-full.txt", response_class=PlainTextResponse)
async def llms_full_txt() -> str:
    """Serve llms-full.txt with complete documentation for LLM crawlers.

    Returns:
        llms-full.txt content as plain text
    """
    llms_full_file = STATIC_DIR / "llms-full.txt"

    if not llms_full_file.exists():
        raise HTTPException(status_code=404, detail="llms-full.txt not found")

    return llms_full_file.read_text()
