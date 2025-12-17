"""
Page routes for SIL website - technical documentation and research.
"""

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from sil_web.services.content import ContentService

if TYPE_CHECKING:
    from sil_web.services.markdown import MarkdownRenderer

router = APIRouter()

# Templates
templates = Jinja2Templates(directory="templates")


def create_routes(
    content_service: ContentService,
    project_service: None,  # Not used for SIL
    markdown_renderer: "MarkdownRenderer",
) -> APIRouter:
    """Create routes with injected services."""

    # Navigation items for SIL (Lab-focused, Bell Labs structure)
    nav_items = [
        {"label": "Home", "url": "/"},
        {"label": "Manifesto", "url": "/manifesto"},
        {"label": "Research", "url": "/research"},
        {"label": "Systems", "url": "/systems"},
        {"label": "Foundations", "url": "/foundations"},
        {"label": "About", "url": "/about"},
    ]

    def render_markdown_page(
        request: Request,
        page_path: Path,
        title: str,
        current_page: str,
    ) -> Response:
        """Helper to render a markdown page."""
        if not page_path.exists():
            raise HTTPException(status_code=404, detail=f"Page not found: {page_path}")

        content = page_path.read_text()
        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": title,
                "content": html_content,
                "nav_items": nav_items,
                "current_page": current_page,
            },
        )

    # =========================================================================
    # Core Pages
    # =========================================================================

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request) -> Response:
        """Homepage - Technical lab landing."""
        return render_markdown_page(
            request,
            Path("docs/pages/index.md"),
            "Semantic Infrastructure Lab",
            "/",
        )

    @router.get("/about", response_class=HTMLResponse)
    async def about(request: Request) -> Response:
        """About page - The lab and team."""
        return render_markdown_page(
            request,
            Path("docs/pages/about.md"),
            "About - Semantic Infrastructure Lab",
            "/about",
        )

    @router.get("/contact", response_class=HTMLResponse)
    async def contact(request: Request) -> Response:
        """Contact page - Collaboration and inquiries."""
        return render_markdown_page(
            request,
            Path("docs/pages/contact.md"),
            "Contact - Semantic Infrastructure Lab",
            "/contact",
        )

    # =========================================================================
    # Manifesto Section
    # =========================================================================

    @router.get("/manifesto", response_class=HTMLResponse)
    async def manifesto_index(request: Request) -> Response:
        """Manifesto - YOLO and soul documents."""
        return render_markdown_page(
            request,
            Path("docs/manifesto/README.md"),
            "Manifesto - Semantic Infrastructure Lab",
            "/manifesto",
        )

    @router.get("/manifesto/{name}", response_class=HTMLResponse)
    async def manifesto_doc(request: Request, name: str) -> Response:
        """Individual manifesto document."""
        filename = name.upper() + ".md"
        doc_path = Path("docs/manifesto") / filename

        if not doc_path.exists():
            raise HTTPException(status_code=404, detail=f"Manifesto document not found: {name}")

        content = doc_path.read_text()
        title = f"{name.title()} - SIL"
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip() + " - SIL"
                break

        html_content = markdown_renderer.render(content)
        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": title,
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/manifesto",
            },
        )

    # =========================================================================
    # Foundations Section
    # =========================================================================

    @router.get("/foundations", response_class=HTMLResponse)
    async def foundations_index(request: Request) -> Response:
        """Foundations - Core principles and architecture."""
        return render_markdown_page(
            request,
            Path("docs/foundations/README.md"),
            "Foundations - Semantic Infrastructure Lab",
            "/foundations",
        )

    @router.get("/foundations/{name}", response_class=HTMLResponse)
    async def foundations_doc(request: Request, name: str) -> Response:
        """Individual foundations document."""
        # Try lowercase with hyphens first
        filename = name + ".md"
        doc_path = Path("docs/foundations") / filename

        # Try with SIL_ prefix and underscores
        if not doc_path.exists():
            filename = "SIL_" + name.upper().replace("-", "_") + ".md"
            doc_path = Path("docs/foundations") / filename

        # Try uppercase with underscores (no SIL_ prefix)
        if not doc_path.exists():
            filename = name.upper().replace("-", "_") + ".md"
            doc_path = Path("docs/foundations") / filename

        if not doc_path.exists():
            raise HTTPException(status_code=404, detail=f"Foundations document not found: {name}")

        content = doc_path.read_text()
        title = f"{name.replace('-', ' ').title()} - SIL"
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip() + " - SIL"
                break

        html_content = markdown_renderer.render(content)
        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": title,
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/foundations",
            },
        )

    # =========================================================================
    # Systems Section (Production Tools)
    # =========================================================================

    @router.get("/systems", response_class=HTMLResponse)
    async def systems_index(request: Request) -> Response:
        """Systems index - Production tools and implementations."""
        return render_markdown_page(
            request,
            Path("docs/systems/README.md"),
            "Systems - Semantic Infrastructure Lab",
            "/systems",
        )

    @router.get("/systems/{name}", response_class=HTMLResponse)
    async def system_page(request: Request, name: str) -> Response:
        """Individual system documentation."""
        # Try lowercase with hyphens first (agent-ether.md)
        filename = name + ".md"
        system_path = Path("docs/systems") / filename

        # Try uppercase (REVEAL.md)
        if not system_path.exists():
            filename = name.upper() + ".md"
            system_path = Path("docs/systems") / filename

        if not system_path.exists():
            raise HTTPException(status_code=404, detail=f"System not found: {name}")

        content = system_path.read_text()
        title = f"{name.title()} - SIL"
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip() + " - SIL"
                break

        html_content = markdown_renderer.render(content)
        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": title,
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/systems",
            },
        )

    # =========================================================================
    # Articles Section
    # =========================================================================

    @router.get("/articles", response_class=HTMLResponse)
    async def articles_index(request: Request) -> Response:
        """Articles index - Technical articles and tutorials."""
        return render_markdown_page(
            request,
            Path("docs/articles/README.md"),
            "Articles - Semantic Infrastructure Lab",
            "/articles",
        )

    @router.get("/articles/{slug}", response_class=HTMLResponse)
    async def article(request: Request, slug: str) -> Response:
        """Serve articles by slug."""
        articles_dir = Path("docs/articles")

        # Map slug to filename (reveal-introduction -> reveal-introduction.md)
        filename = slug + ".md"
        article_path = articles_dir / filename

        # Try uppercase with underscores if not found
        if not article_path.exists():
            filename = slug.upper().replace("-", "_") + ".md"
            article_path = articles_dir / filename

        if not article_path.exists():
            raise HTTPException(status_code=404, detail=f"Article not found: {slug}")

        content = article_path.read_text()

        # Extract title from first H1 if present
        title = "Article - Semantic Infrastructure Lab"
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip() + " - SIL"
                break

        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": title,
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/articles",
            },
        )

    # =========================================================================
    # Essays Section
    # =========================================================================

    @router.get("/essays", response_class=HTMLResponse)
    async def essays_index(request: Request) -> Response:
        """Essays index - List all technical essays."""
        essays_dir = Path("docs/essays")

        # Build dynamic essay list
        essays = []
        if essays_dir.exists():
            for essay_file in sorted(essays_dir.glob("*.md")):
                if essay_file.name == "README.md":
                    continue
                # Convert filename to slug and title
                slug = essay_file.stem.lower().replace("_", "-")
                # Read first H1 for title
                content = essay_file.read_text()
                title = essay_file.stem.replace("_", " ").title()
                for line in content.split("\n"):
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
                essays.append({"slug": slug, "title": title})

        # Generate markdown content for essay list
        md_content = "# Essays\n\nTechnical essays on semantic infrastructure.\n\n"
        for essay in essays:
            md_content += f"- [{essay['title']}](/essays/{essay['slug']})\n"

        if not essays:
            md_content += "*No essays published yet.*\n"

        html_content = markdown_renderer.render(md_content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": "Essays - Semantic Infrastructure Lab",
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/essays",
            },
        )

    @router.get("/essays/{slug}", response_class=HTMLResponse)
    async def essay(request: Request, slug: str) -> Response:
        """Serve essays by slug. Maps slug to filename in docs/essays/."""
        essays_dir = Path("docs/essays")

        # Map slug back to filename (progressive-disclosure-for-ai-agents -> PROGRESSIVE_DISCLOSURE_FOR_AI_AGENTS.md)
        filename = slug.upper().replace("-", "_") + ".md"
        essay_path = essays_dir / filename

        if not essay_path.exists():
            raise HTTPException(status_code=404, detail=f"Essay not found: {slug}")

        content = essay_path.read_text()

        # Extract title from first H1 if present
        title = "Essay - Semantic Infrastructure Lab"
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip() + " - SIL"
                break

        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": title,
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/essays",
            },
        )

    # =========================================================================
    # Research Section
    # =========================================================================

    @router.get("/research", response_class=HTMLResponse)
    async def research(request: Request) -> Response:
        """Research page - Deep technical papers."""
        return render_markdown_page(
            request,
            Path("docs/research/README.md"),
            "Research - Semantic Infrastructure Lab",
            "/research",
        )

    @router.get("/research/{name}", response_class=HTMLResponse)
    async def research_paper(request: Request, name: str) -> Response:
        """Individual research paper - handles both flat and subdirectory structure."""
        # Map URL name to filename
        filename = name.upper().replace("-", "_") + ".md"

        # Try root level first
        paper_path = Path("docs/research") / filename

        # If not found, search in subdirectories
        if not paper_path.exists():
            research_dir = Path("docs/research")
            for subdir in research_dir.iterdir():
                if subdir.is_dir():
                    candidate = subdir / filename
                    if candidate.exists():
                        paper_path = candidate
                        break

        if not paper_path.exists():
            raise HTTPException(status_code=404, detail=f"Research paper not found: {name}")

        content = paper_path.read_text()

        # Extract title from first H1
        title = f"{name.replace('-', ' ').title()} - SIL Research"
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip() + " - SIL"
                break

        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": title,
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/research",
            },
        )

    # =========================================================================
    # Architecture Section
    # =========================================================================

    @router.get("/architecture/{name}", response_class=HTMLResponse)
    async def architecture_doc(request: Request, name: str) -> Response:
        """Individual architecture document."""
        # Try uppercase with underscores first (UNIFIED_ARCHITECTURE_GUIDE.md)
        filename = name.upper().replace("-", "_") + ".md"
        doc_path = Path("docs/architecture") / filename

        # Try lowercase with hyphens
        if not doc_path.exists():
            filename = name + ".md"
            doc_path = Path("docs/architecture") / filename

        if not doc_path.exists():
            raise HTTPException(status_code=404, detail=f"Architecture document not found: {name}")

        content = doc_path.read_text()
        title = f"{name.replace('-', ' ').title()} - SIL Architecture"
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip() + " - SIL"
                break

        html_content = markdown_renderer.render(content)
        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": title,
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/architecture",
            },
        )

    # =========================================================================
    # Projects Section
    # =========================================================================

    @router.get("/projects/{name}", response_class=HTMLResponse)
    async def project_doc(request: Request, name: str) -> Response:
        """Individual project document."""
        # Try uppercase with underscores first (PROJECT_INDEX.md)
        filename = name.upper().replace("-", "_") + ".md"
        doc_path = Path("docs/projects") / filename

        # Try lowercase with hyphens
        if not doc_path.exists():
            filename = name + ".md"
            doc_path = Path("docs/projects") / filename

        if not doc_path.exists():
            raise HTTPException(status_code=404, detail=f"Project document not found: {name}")

        content = doc_path.read_text()
        title = f"{name.replace('-', ' ').title()} - SIL Projects"
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip() + " - SIL"
                break

        html_content = markdown_renderer.render(content)
        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": title,
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/projects",
            },
        )

    # =========================================================================
    # Legacy Redirects (Old structure -> New structure)
    # =========================================================================

    @router.get("/tools", response_class=HTMLResponse)
    async def tools_redirect(request: Request) -> Response:
        """Redirect /tools to /systems."""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/systems", status_code=301)

    @router.get("/tools/{name}", response_class=HTMLResponse)
    async def tool_redirect(request: Request, name: str) -> Response:
        """Redirect /tools/{name} to /systems/{name}."""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=f"/systems/{name}", status_code=301)

    @router.get("/canonical", response_class=HTMLResponse)
    async def canonical_redirect(request: Request) -> Response:
        """Redirect /canonical to /foundations."""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/foundations", status_code=301)

    @router.get("/canonical/{name}", response_class=HTMLResponse)
    async def canonical_doc_redirect(request: Request, name: str) -> Response:
        """Redirect /canonical/{name} to appropriate new location."""
        from fastapi.responses import RedirectResponse
        # Map common canonical docs to new structure
        if name in ["manifesto", "yolo"]:
            return RedirectResponse(url=f"/manifesto/{name}", status_code=301)
        else:
            return RedirectResponse(url=f"/foundations/{name}", status_code=301)

    # =========================================================================
    # Quick Start & Getting Started Pages
    # =========================================================================

    @router.get("/start", response_class=HTMLResponse)
    async def start_here(request: Request) -> Response:
        """Start Here - Getting started guide."""
        return render_markdown_page(
            request,
            Path("docs/START_HERE.md"),
            "Start Here - Semantic Infrastructure Lab",
            "/",
        )

    # =========================================================================
    # Founder's Letter (Legacy URL support)
    # =========================================================================

    @router.get("/founders-letter", response_class=HTMLResponse)
    async def founders_letter(request: Request) -> Response:
        """Founder's Letter - direct access."""
        return render_markdown_page(
            request,
            Path("docs/foundations/FOUNDERS_LETTER.md"),
            "Founder's Letter - Semantic Infrastructure Lab",
            "/",
        )

    # =========================================================================
    # Meta Section (FAQ, Founder, Influences)
    # =========================================================================

    @router.get("/meta/{name}", response_class=HTMLResponse)
    async def meta_page(request: Request, name: str) -> Response:
        """Meta pages - FAQ, founder background, influences."""
        # Map URL name to filename
        filename = name.upper().replace("-", "_") + ".md"
        doc_path = Path("docs/meta") / filename

        if not doc_path.exists():
            raise HTTPException(status_code=404, detail=f"Page not found: {name}")

        content = doc_path.read_text()

        # Extract title from first H1
        title = f"{name.replace('-', ' ').title()} - SIL"
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip() + " - SIL"
                break

        html_content = markdown_renderer.render(content)

        return templates.TemplateResponse(
            "page.html",
            {
                "request": request,
                "title": title,
                "content": html_content,
                "nav_items": nav_items,
                "current_page": "/about",
            },
        )

    return router
