"""
Page routes - thin handlers that glue layers together.

No business logic, no formatting, no DB access.
Just: parse input → call service → render response.
"""

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from fastapi.templating import Jinja2Templates

from sil_web.services.content import ContentService, ProjectService
from sil_web.ui.components import (
    architecture_diagram,
    founding_docs_sidebar,
    layer_section,
    nav_bar,
    project_card,
)

if TYPE_CHECKING:
    from sil_web.services.markdown import MarkdownRenderer

router = APIRouter()

# Templates
templates = Jinja2Templates(directory="templates")


def create_routes(
    content_service: ContentService,
    project_service: ProjectService,
    markdown_renderer: "MarkdownRenderer",
):
    """Create routes with injected services."""

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Home page - Founder's Letter."""
        # Load founder's letter
        doc = content_service.load_document_by_slug("founders-letter")
        if not doc:
            raise HTTPException(status_code=404, detail="Founder's letter not found")

        # Get all documents for sidebar
        all_docs = content_service.list_documents()

        # Render markdown to HTML (elegant single-line!)
        html_content = markdown_renderer.render(doc.content)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "content": html_content,
                "nav": nav_bar(""),
                "sidebar": founding_docs_sidebar(all_docs, "founders-letter", ""),
            },
        )

    @router.get("/projects", response_class=HTMLResponse)
    async def projects(request: Request):
        """Projects page - all SIL projects grouped by Semantic OS layer."""
        # Get projects grouped by layer
        by_layer = project_service.get_projects_by_layer()

        # Get all documents for sidebar
        all_docs = content_service.list_documents()

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
                "sidebar": founding_docs_sidebar(all_docs, "", "projects"),
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

        # Get all documents for sidebar
        all_docs = content_service.list_documents()

        # Render markdown to HTML (elegant single-line!)
        html_content = markdown_renderer.render(doc.content)

        return templates.TemplateResponse(
            "document.html",
            {
                "request": request,
                "doc": doc,
                "content": html_content,
                "nav": nav_bar("docs"),
                "sidebar": founding_docs_sidebar(all_docs, slug, ""),
            },
        )

    @router.api_route("/llms.txt", methods=["GET", "HEAD"], response_class=PlainTextResponse)
    async def llms_txt():
        """Serve llms.txt file for LLM consumption (Jeremy Howard standard)."""
        llms_file = Path("static/llms.txt")
        if not llms_file.exists():
            raise HTTPException(status_code=404, detail="llms.txt not found")
        return llms_file.read_text()

    @router.api_route("/llms-full.txt", methods=["GET", "HEAD"], response_class=PlainTextResponse)
    async def llms_full_txt():
        """Serve llms-full.txt file with complete documentation for LLM consumption."""
        llms_full_file = Path("static/llms-full.txt")
        if not llms_full_file.exists():
            raise HTTPException(status_code=404, detail="llms-full.txt not found")
        return llms_full_file.read_text()

    @router.get("/robots.txt", response_class=PlainTextResponse)
    async def robots_txt():
        """Serve robots.txt to guide search engine crawlers."""
        return """User-agent: *
Allow: /
Sitemap: https://semanticinfrastructurelab.org/sitemap.xml

# Allow all ethical AI crawlers
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /
"""

    @router.get("/sitemap.xml", response_class=Response)
    async def sitemap_xml():
        """Generate dynamic sitemap for search engines."""
        # Get all documents for sitemap
        all_docs = content_service.list_documents()

        # Build sitemap
        urls = []

        # Homepage
        urls.append('<url><loc>https://semanticinfrastructurelab.org/</loc><priority>1.0</priority></url>')

        # Projects page
        urls.append('<url><loc>https://semanticinfrastructurelab.org/projects</loc><priority>0.9</priority></url>')

        # Docs index
        urls.append('<url><loc>https://semanticinfrastructurelab.org/docs</loc><priority>0.9</priority></url>')

        # Individual documents
        for doc in all_docs:
            urls.append(f'<url><loc>https://semanticinfrastructurelab.org/docs/{doc.slug}</loc><priority>0.8</priority></url>')

        sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}
</urlset>'''

        return Response(content=sitemap, media_type="application/xml")

    return router
