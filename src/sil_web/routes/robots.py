"""
Robots.txt endpoint for search engine crawler control.

Staging: Disallow all (prevent indexing of staging site)
Production: Allow all with sitemap reference
"""

import os

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt() -> str:
    """Serve robots.txt based on environment.

    Returns:
        robots.txt content as plain text
    """
    # Check environment (default to production for safety)
    environment = os.getenv("ENVIRONMENT", "production").lower()

    if environment == "staging":
        # Staging: Prevent all indexing
        return """User-agent: *
Disallow: /
"""
    else:
        # Production: Allow indexing with sitemap
        return """User-agent: *
Allow: /

Sitemap: https://semanticinfrastructurelab.org/sitemap.xml
"""
