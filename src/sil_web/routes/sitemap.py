"""
sitemap.xml endpoint for search engine crawlers.

robots.txt has referenced /sitemap.xml since the site's first commit, but
no route ever served it (SIL-8). Built at request time from the same
docs/ tree the page routes themselves read from -- no separate generated
file to fall out of sync, and no dependency on the SIL source repo (which
isn't present in the deployed container; DOCS_PATH/SIL_DOCS_PATH point
here too, see config/settings.py).

Route slugs use the same lower-hyphenated transform the page routes accept
as their primary match (see routes/pages.py) -- keep this mapping in sync
with CATEGORY routes there and with generate-llms-txt.sh in scripts/,
which derives the same URLs for llms.txt.
"""

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()

SITE_URL = "https://semanticinfrastructurelab.org"

DOCS_ROOT = Path("docs")

# docs/<category>/ -> URL prefix. Kept in sync with CATEGORY_ROUTES in
# scripts/generate-llms-txt.sh and the route handlers in routes/pages.py.
CATEGORY_ROUTES = {
    "foundations": "/foundations",
    "manifesto": "/manifesto",
    "architecture": "/architecture",
    "systems": "/systems",
    "research": "/research",
    "articles": "/articles",
    "essays": "/essays",
}

STATIC_PAGES = [
    "/",
    "/about",
    "/contact",
    "/start",
    "/founders-letter",
    "/foundations",
    "/manifesto",
    "/architecture",
    "/systems",
    "/research",
    "/articles",
    "/essays",
    "/projects",
]


def _slugify(stem: str) -> str:
    return stem.lower().replace("_", "-")


def _collect_urls() -> list[str]:
    urls = list(STATIC_PAGES)

    for category, prefix in CATEGORY_ROUTES.items():
        category_dir = DOCS_ROOT / category
        if not category_dir.is_dir():
            continue
        for md_file in sorted(category_dir.rglob("*.md")):
            if md_file.name == "README.md":
                continue
            urls.append(f"{prefix}/{_slugify(md_file.stem)}")

    # Dedupe while preserving order (e.g. foundations/FOUNDERS_LETTER.md
    # would otherwise also produce /foundations/founders-letter, a URL
    # the foundations route happens to accept too, alongside the
    # dedicated /founders-letter already in STATIC_PAGES).
    seen: set[str] = set()
    deduped = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            deduped.append(url)
    return deduped


@router.get("/sitemap.xml")
async def sitemap_xml() -> Response:
    """Serve sitemap.xml listing all public pages.

    Returns:
        sitemap.xml content as application/xml
    """
    urls = _collect_urls()

    entries = "\n".join(f"  <url><loc>{SITE_URL}{path}</loc></url>" for path in urls)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )

    return Response(content=xml, media_type="application/xml")
