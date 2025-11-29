"""
Page routes - thin handlers that glue layers together.

No business logic, no formatting, no DB access.
Just: parse input → call service → render response.
"""

from pathlib import Path

import markdown
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sil_web.services.content import ContentService, ProjectService
from sil_web.ui.components import architecture_diagram, nav_bar, project_card

router = APIRouter()

# Templates
templates = Jinja2Templates(directory="templates")


def create_routes(content_service: ContentService, project_service: ProjectService):
    """Create routes with injected services."""

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Home page - Founder's Letter."""
        # Load founder's letter
        doc = content_service.load_document("founders-letter")
        if not doc:
            raise HTTPException(status_code=404, detail="Founder's letter not found")

        # Convert markdown to HTML
        html_content = markdown.markdown(doc.content)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "content": html_content,
                "nav": nav_bar(""),
            },
        )

    @router.get("/projects", response_class=HTMLResponse)
    async def projects(request: Request):
        """Projects page - all production systems."""
        # Get all production projects
        all_projects = project_service.get_production_projects()

        # Render each project as HTML
        project_cards = [project_card(p) for p in all_projects]

        return templates.TemplateResponse(
            "projects.html",
            {
                "request": request,
                "projects": project_cards,
                "architecture": architecture_diagram(),
                "nav": nav_bar("projects"),
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
        doc = content_service.load_document(slug)
        if not doc:
            raise HTTPException(status_code=404, detail=f"Document '{slug}' not found")

        # Convert markdown to HTML
        html_content = markdown.markdown(doc.content)

        return templates.TemplateResponse(
            "document.html",
            {
                "request": request,
                "doc": doc,
                "content": html_content,
                "nav": nav_bar("docs"),
            },
        )

    return router
