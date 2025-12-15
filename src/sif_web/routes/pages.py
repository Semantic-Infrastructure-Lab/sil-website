"""
Page routes for SIL website - technical documentation and research.
"""

from pathlib import Path
from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from sif_web.services.content import ContentService

if TYPE_CHECKING:
    from sif_web.services.markdown import MarkdownRenderer

router = APIRouter()

# Templates
templates = Jinja2Templates(directory="templates")


def create_routes(
    content_service: ContentService,
    project_service: None,  # Not used for SIL
    markdown_renderer: "MarkdownRenderer",
) -> APIRouter:
    """Create routes with injected services."""

    # Navigation items for SIL (Lab-focused)
    nav_items = [
        {"label": "Home", "url": "/"},
        {"label": "Tools", "url": "/tools"},
        {"label": "Essays", "url": "/essays"},
        {"label": "Research", "url": "/research"},
        {"label": "About", "url": "/about"},
        {"label": "Contact", "url": "/contact"},
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
    # Tools Section
    # =========================================================================

    @router.get("/tools", response_class=HTMLResponse)
    async def tools_index(request: Request) -> Response:
        """Tools index - List of production tools."""
        return render_markdown_page(
            request,
            Path("docs/tools/README.md"),
            "Tools - Semantic Infrastructure Lab",
            "/tools",
        )

    @router.get("/tools/{name}", response_class=HTMLResponse)
    async def tool_page(request: Request, name: str) -> Response:
        """Individual tool documentation."""
        # Map URL name to filename (reveal -> REVEAL.md)
        filename = name.upper() + ".md"
        tool_path = Path("docs/tools") / filename

        if not tool_path.exists():
            raise HTTPException(status_code=404, detail=f"Tool not found: {name}")

        content = tool_path.read_text()

        # Extract title from first H1
        title = f"{name.title()} - Semantic Infrastructure Lab"
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
                "current_page": "/tools",
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
        """Individual research paper."""
        # Map URL name to filename
        filename = name.upper().replace("-", "_") + ".md"
        paper_path = Path("docs/research") / filename

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
    # Canonical Documents Section
    # =========================================================================

    @router.get("/canonical", response_class=HTMLResponse)
    async def canonical_index(request: Request) -> Response:
        """Canonical documents index - Manifesto, principles, charter."""
        return render_markdown_page(
            request,
            Path("docs/canonical/README.md"),
            "Canonical Documents - Semantic Infrastructure Lab",
            "/canonical",
        )

    @router.get("/canonical/{name}", response_class=HTMLResponse)
    async def canonical_doc(request: Request, name: str) -> Response:
        """Individual canonical document."""
        # Map URL name to filename
        filename = name.upper().replace("-", "_") + ".md"
        doc_path = Path("docs/canonical") / filename

        # Also try with SIL_ prefix
        if not doc_path.exists():
            doc_path = Path("docs/canonical") / f"SIL_{filename}"

        if not doc_path.exists():
            raise HTTPException(status_code=404, detail=f"Document not found: {name}")

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
                "current_page": "/canonical",
            },
        )

    # =========================================================================
    # Innovations Section
    # =========================================================================

    @router.get("/innovations", response_class=HTMLResponse)
    async def innovations_index(request: Request) -> Response:
        """Innovations index - Major projects and systems."""
        return render_markdown_page(
            request,
            Path("docs/innovations/README.md"),
            "Innovations - Semantic Infrastructure Lab",
            "/innovations",
        )

    @router.get("/innovations/{name}", response_class=HTMLResponse)
    async def innovation_page(request: Request, name: str) -> Response:
        """Individual innovation/project page."""
        # Map URL name to filename
        filename = name.upper().replace("-", "_") + ".md"
        doc_path = Path("docs/innovations") / filename

        if not doc_path.exists():
            raise HTTPException(status_code=404, detail=f"Innovation not found: {name}")

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
                "current_page": "/innovations",
            },
        )

    # =========================================================================
    # Founder's Letter (Legacy URL support)
    # =========================================================================

    @router.get("/founders-letter", response_class=HTMLResponse)
    async def founders_letter(request: Request) -> Response:
        """Founder's Letter - direct access."""
        return render_markdown_page(
            request,
            Path("docs/canonical/FOUNDERS_LETTER.md"),
            "Founder's Letter - Semantic Infrastructure Lab",
            "/",
        )

    return router
