"""
Page routes for SIF website - simple markdown pages.
"""

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sif_web.services.content import ContentService

if TYPE_CHECKING:
    from sif_web.services.markdown import MarkdownRenderer

router = APIRouter()

# Templates
templates = Jinja2Templates(directory="templates")


def create_routes(
    content_service: ContentService,
    project_service: None,  # Not used for SIF
    markdown_renderer: "MarkdownRenderer",
):
    """Create routes with injected services."""

    # Navigation items
    nav_items = [
        {"label": "Home", "url": "/"},
        {"label": "About", "url": "/about"},
        {"label": "Research", "url": "/research"},
        {"label": "Funding", "url": "/funding"},
        {"label": "Foundation", "url": "/foundation"},
        {"label": "Contact", "url": "/contact"},
    ]

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Homepage - Timeline A vs B narrative."""
        page_path = Path("docs/pages/index.md")
        if not page_path.exists():
            raise HTTPException(status_code=404, detail="Homepage not found")

        content = page_path.read_text()
        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": "Semantic Infrastructure Foundation",
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/",
            },
        )

    @router.get("/about", response_class=HTMLResponse)
    async def about(request: Request):
        """About page - Vision and current status."""
        page_path = Path("docs/pages/about.md")
        if not page_path.exists():
            raise HTTPException(status_code=404, detail="About page not found")

        content = page_path.read_text()
        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": "About - Semantic Infrastructure Foundation",
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/about",
            },
        )

    @router.get("/research", response_class=HTMLResponse)
    async def research(request: Request):
        """Research page - Production systems and architecture."""
        page_path = Path("docs/pages/research.md")
        if not page_path.exists():
            raise HTTPException(status_code=404, detail="Research page not found")

        content = page_path.read_text()
        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": "Research - Semantic Infrastructure Foundation",
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/research",
            },
        )

    @router.get("/funding", response_class=HTMLResponse)
    async def funding(request: Request):
        """Funding page - Hybrid funding model."""
        page_path = Path("docs/pages/funding.md")
        if not page_path.exists():
            raise HTTPException(status_code=404, detail="Funding page not found")

        content = page_path.read_text()
        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": "Funding Model - Semantic Infrastructure Foundation",
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/funding",
            },
        )

    @router.get("/contact", response_class=HTMLResponse)
    async def contact(request: Request):
        """Contact page - Get involved."""
        page_path = Path("docs/pages/contact.md")
        if not page_path.exists():
            raise HTTPException(status_code=404, detail="Contact page not found")

        content = page_path.read_text()
        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": "Get Involved - Semantic Infrastructure Foundation",
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/contact",
            },
        )

    @router.get("/foundation", response_class=HTMLResponse)
    async def foundation(request: Request):
        """Foundation governance page - Building institutions that last."""
        page_path = Path("docs/pages/foundation/index.md")
        if not page_path.exists():
            raise HTTPException(status_code=404, detail="Foundation page not found")

        content = page_path.read_text()
        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": "Foundation Governance - Semantic Infrastructure Foundation",
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/foundation",
            },
        )

    @router.get("/foundation/chief-steward", response_class=HTMLResponse)
    async def chief_steward(request: Request):
        """Chief Steward role page."""
        page_path = Path("docs/pages/foundation/chief-steward.md")
        if not page_path.exists():
            raise HTTPException(status_code=404, detail="Chief Steward page not found")

        content = page_path.read_text()
        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": "Chief Steward - Semantic Infrastructure Foundation",
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/foundation",
            },
        )

    @router.get("/foundation/executive-director", response_class=HTMLResponse)
    async def executive_director(request: Request):
        """Executive Director role page."""
        page_path = Path("docs/pages/foundation/executive-director.md")
        if not page_path.exists():
            raise HTTPException(
                status_code=404, detail="Executive Director page not found"
            )

        content = page_path.read_text()
        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": "Executive Director - Semantic Infrastructure Foundation",
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/foundation",
            },
        )

    return router
