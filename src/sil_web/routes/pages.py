"""
Page routes - thin handlers that glue layers together.

No business logic, no formatting, no DB access.
Just: parse input → call service → render response.
"""

import re
from pathlib import Path

import markdown
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates

from sil_web.services.content import ContentService, ProjectService
from sil_web.ui.components import (
    architecture_diagram,
    founding_docs_sidebar,
    layer_section,
    nav_bar,
    project_card,
)

router = APIRouter()

# Templates
templates = Jinja2Templates(directory="templates")


def strip_first_h1(markdown_text: str) -> str:
    """Remove first h1 heading from markdown to avoid duplicate h1 tags.

    Templates provide page headers with h1, so strip any h1 from
    markdown content to maintain semantic HTML structure.
    """
    # Match first h1 (# Title) and any following blank lines
    pattern = r'^#\s+.*?\n(\n)*'
    return re.sub(pattern, '', markdown_text, count=1, flags=re.MULTILINE)


def create_routes(content_service: ContentService, project_service: ProjectService):
    """Create routes with injected services."""

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Home page - Founder's Letter."""
        # Load founder's letter
        doc = content_service.load_document_by_slug("founders-letter")
        if not doc:
            raise HTTPException(status_code=404, detail="Founder's letter not found")

        # Get all canonical documents for sidebar
        all_docs = content_service.list_documents()
        canonical_docs = [d for d in all_docs if d.category == "canonical"]

        # Strip first h1 (template provides page header) and convert to HTML
        content_without_h1 = strip_first_h1(doc.content)
        html_content = markdown.markdown(content_without_h1)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "content": html_content,
                "nav": nav_bar(""),
                "sidebar": founding_docs_sidebar(canonical_docs, "founders-letter", ""),
            },
        )

    @router.get("/projects", response_class=HTMLResponse)
    async def projects(request: Request):
        """Projects page - all SIL projects grouped by Semantic OS layer."""
        # Get projects grouped by layer
        by_layer = project_service.get_projects_by_layer()

        # Get all canonical documents for sidebar
        all_docs = content_service.list_documents()
        canonical_docs = [d for d in all_docs if d.category == "canonical"]

        # Render layer sections in order (5 → 0 + cross-cutting)
        from sil_web.domain.models import Layer

        layer_order = [
            Layer.LAYER_5,
            Layer.LAYER_4,
            Layer.LAYER_3,
            Layer.LAYER_2,
            Layer.LAYER_1,
            Layer.LAYER_0,
            Layer.CROSS_CUTTING,
        ]

        layer_sections = [
            layer_section(layer, by_layer[layer]) for layer in layer_order
        ]

        return templates.TemplateResponse(
            "projects.html",
            {
                "request": request,
                "layer_sections": layer_sections,
                "architecture": architecture_diagram(),
                "nav": nav_bar("projects"),
                "sidebar": founding_docs_sidebar(canonical_docs, "", "projects"),
            },
        )

    @router.get("/docs", response_class=HTMLResponse)
    async def docs_index(request: Request):
        """Documentation index page."""
        # List all canonical documents
        documents = content_service.list_documents()

        # Group by category
        canonical = [d for d in documents if d.category == "canonical"]

        return templates.TemplateResponse(
            "docs_index.html",
            {
                "request": request,
                "canonical": canonical,
                "nav": nav_bar("docs"),
            },
        )

    @router.get("/docs/{slug}", response_class=HTMLResponse)
    async def doc_page(request: Request, slug: str):
        """Individual document page."""
        doc = content_service.load_document_by_slug(slug)
        if not doc:
            raise HTTPException(status_code=404, detail=f"Document '{slug}' not found")

        # Get all canonical documents for sidebar
        all_docs = content_service.list_documents()
        canonical_docs = [d for d in all_docs if d.category == "canonical"]

        # Strip first h1 (template provides page header) and convert to HTML
        content_without_h1 = strip_first_h1(doc.content)
        html_content = markdown.markdown(content_without_h1)

        return templates.TemplateResponse(
            "document.html",
            {
                "request": request,
                "doc": doc,
                "content": html_content,
                "nav": nav_bar("docs"),
                "sidebar": founding_docs_sidebar(canonical_docs, slug, ""),
            },
        )

    @router.get("/llms.txt", response_class=PlainTextResponse)
    async def llms_txt():
        """Serve llms.txt file for LLM consumption (Jeremy Howard standard)."""
        llms_file = Path("static/llms.txt")
        if not llms_file.exists():
            raise HTTPException(status_code=404, detail="llms.txt not found")
        return llms_file.read_text()

    @router.get("/llms-full.txt", response_class=PlainTextResponse)
    async def llms_full_txt():
        """Serve llms-full.txt file with complete documentation for LLM consumption."""
        llms_full_file = Path("static/llms-full.txt")
        if not llms_full_file.exists():
            raise HTTPException(status_code=404, detail="llms-full.txt not found")
        return llms_full_file.read_text()

    return router
