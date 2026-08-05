"""
Page routes for SIL website - technical documentation and research.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import frontmatter
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from sil_web.services.content import ContentService

if TYPE_CHECKING:
    from sil_web.services.markdown import MarkdownRenderer
    from sil_web.services.metrics import MetricsService

router = APIRouter()

# Templates
templates = Jinja2Templates(directory="templates")


# =============================================================================
# Per-category filename resolvers
#
# Each mirrors the exact pattern order its HTML route has always used, so
# extracting them here changes nothing about what the HTML routes serve.
# Shared by the HTML routes below AND the raw-markdown (`/{path}.md`) route,
# so both always agree on which file a URL maps to.
# =============================================================================


def _resolve_manifesto(name: str) -> Path | None:
    candidate = Path("docs/manifesto") / f"{name.upper()}.md"
    return candidate if candidate.exists() else None


def _resolve_foundations(name: str) -> Path | None:
    for candidate in (
        Path("docs/foundations") / f"{name}.md",
        Path("docs/foundations") / f"SIL_{name.upper().replace('-', '_')}.md",
        Path("docs/foundations") / f"{name.upper().replace('-', '_')}.md",
    ):
        if candidate.exists():
            return candidate
    return None


def _resolve_systems(name: str) -> Path | None:
    for pattern in (name, name.lower().replace("_", "-"), name.upper(), name.lower()):
        candidate = Path("docs/systems") / f"{pattern}.md"
        if candidate.exists():
            return candidate
    return None


def is_draft_article(path: Path) -> bool:
    """True if an article's frontmatter reads status: draft (SIL-16).

    Draft articles are allowed to sit in docs/articles/ (and even carry a
    CONTENT_MANIFEST.yaml visibility: public entry, so sync-docs.py can bring
    them into the website repo ahead of time) -- this is the actual publish
    gate that keeps them off every public surface until flipped to
    "published". Checked here (shared by the HTML and raw-markdown article
    routes) and independently in routes/sitemap.py and the llms.txt/
    llms-full.txt generators in scripts/, since none of those share this
    module.
    """
    try:
        post = frontmatter.load(path)
    except (OSError, ValueError):
        return False
    return str(post.metadata.get("status", "")).lower() == "draft"


def _resolve_articles(slug: str) -> Path | None:
    for candidate in (
        Path("docs/articles") / f"{slug}.md",
        Path("docs/articles") / f"{slug.upper().replace('-', '_')}.md",
    ):
        if candidate.exists() and not is_draft_article(candidate):
            return candidate
    return None


def _resolve_research(name: str) -> Path | None:
    filename = f"{name.upper().replace('-', '_')}.md"
    root_candidate = Path("docs/research") / filename
    if root_candidate.exists():
        return root_candidate
    research_dir = Path("docs/research")
    for subdir in research_dir.iterdir():
        if subdir.is_dir():
            candidate = subdir / filename
            if candidate.exists():
                return candidate
    return None


def _resolve_architecture(name: str) -> Path | None:
    for candidate in (
        Path("docs/architecture") / f"{name.upper().replace('-', '_')}.md",
        Path("docs/architecture") / f"{name}.md",
    ):
        if candidate.exists():
            return candidate
    return None


def _resolve_projects(name: str) -> Path | None:
    for candidate in (
        Path("docs/projects") / f"{name.upper().replace('-', '_')}.md",
        Path("docs/projects") / f"{name}.md",
    ):
        if candidate.exists():
            return candidate
    return None


def _resolve_meta(name: str) -> Path | None:
    candidate = Path("docs/meta") / f"{name.upper().replace('-', '_')}.md"
    return candidate if candidate.exists() else None


# category -> resolver, for the /{category}/{name}.md dispatch below.
# "essays" is handled separately (goes through ContentService for privacy filtering).
CATEGORY_RESOLVERS = {
    "manifesto": _resolve_manifesto,
    "foundations": _resolve_foundations,
    "systems": _resolve_systems,
    "articles": _resolve_articles,
    "research": _resolve_research,
    "architecture": _resolve_architecture,
    "projects": _resolve_projects,
    "meta": _resolve_meta,
}

# category -> index doc, for /{category}.md
CATEGORY_INDEX_DOCS = {
    "manifesto": Path("docs/manifesto/README.md"),
    "foundations": Path("docs/foundations/README.md"),
    "systems": Path("docs/systems/README.md"),
    "articles": Path("docs/articles/README.md"),
    "research": Path("docs/research/README.md"),
    "architecture": Path("docs/architecture/README.md"),
    "projects": Path("docs/projects/README.md"),
}

# top-level slug -> doc, for root-level /{slug}.md
ROOT_PAGE_DOCS = {
    "": Path("docs/pages/index.md"),
    "about": Path("docs/pages/about.md"),
    "contact": Path("docs/pages/contact.md"),
    "start": Path("docs/START_HERE.md"),
    "founders-letter": Path("docs/foundations/FOUNDERS_LETTER.md"),
}


def create_routes(
    content_service: ContentService,
    project_service: None,  # Not used for SIL
    markdown_renderer: "MarkdownRenderer",
    metrics_service: "MetricsService | None" = None,
) -> APIRouter:
    """Create routes with injected services.

    Args:
        content_service: Content management service
        project_service: Not used for SIL (kept for compatibility)
        markdown_renderer: Markdown rendering service
        metrics_service: Metrics service (optional, for canonical metrics)
    """

    # Navigation items for SIL (Lab-focused, Bell Labs structure)
    nav_items = [
        {"label": "Home", "url": "/"},
        {"label": "Manifesto", "url": "/manifesto"},
        {"label": "Research", "url": "/research"},
        {"label": "Systems", "url": "/systems"},
        {"label": "Articles", "url": "/articles"},
        {"label": "Foundations", "url": "/foundations"},
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

        # Build template context
        context = {
            "request": request,
            "title": title,
            "content": html_content,
            "nav_items": nav_items,
            "current_page": current_page,
        }

        # Add metrics if service is available
        if metrics_service is not None:
            context["metrics"] = metrics_service.metrics

        return templates.TemplateResponse("page.html", context)

    # =========================================================================
    # Raw Markdown Source (per-page llms.txt convention: /{page}.md)
    #
    # Registered before every {name}-style route below on purpose: Starlette's
    # default path converter matches dots, so "/systems/{name}" would otherwise
    # swallow "/systems/reveal.md" (name="reveal.md") before this route ever
    # got a chance. Route matching is first-match-wins in registration order.
    # =========================================================================

    @router.get("/{full_path:path}.md", include_in_schema=False)
    async def raw_markdown(request: Request, full_path: str) -> Response:
        """Serve a page's raw markdown source, matching the llms-full.txt convention
        of unrendered content (frontmatter included, as written)."""
        full_path = full_path.strip("/")

        if full_path in ROOT_PAGE_DOCS:
            doc_path = ROOT_PAGE_DOCS[full_path]
            if doc_path.exists():
                return Response(doc_path.read_text(), media_type="text/markdown; charset=utf-8")
            raise HTTPException(status_code=404, detail=f"Page not found: {full_path}")

        if full_path in CATEGORY_INDEX_DOCS:
            doc_path = CATEGORY_INDEX_DOCS[full_path]
            if doc_path.exists():
                return Response(doc_path.read_text(), media_type="text/markdown; charset=utf-8")
            raise HTTPException(status_code=404, detail=f"Page not found: {full_path}")

        if full_path == "essays":
            essay_docs = content_service.list_documents(category="essays", include_private=False)
            md_content = "# Essays\n\nTechnical essays on semantic infrastructure.\n\n"
            for doc in sorted(essay_docs, key=lambda d: d.order):
                md_content += f"- [{doc.title}](/essays/{doc.slug})\n"
            if not essay_docs:
                md_content += "*No essays published yet.*\n"
            return Response(md_content, media_type="text/markdown; charset=utf-8")

        if "/" not in full_path:
            raise HTTPException(status_code=404, detail=f"Page not found: {full_path}")

        category, name = full_path.split("/", 1)

        if category == "essays":
            doc = content_service.load_document("essays", name, include_private=False)
            if not doc or doc.private:
                raise HTTPException(status_code=404, detail=f"Essay not found: {name}")
            return Response(doc.content, media_type="text/markdown; charset=utf-8")

        resolver = CATEGORY_RESOLVERS.get(category)
        if resolver is None:
            raise HTTPException(status_code=404, detail=f"Page not found: {full_path}")

        doc_path = resolver(name)
        if doc_path is None:
            raise HTTPException(status_code=404, detail=f"Document not found: {full_path}")

        return Response(doc_path.read_text(), media_type="text/markdown; charset=utf-8")

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
        doc_path = _resolve_manifesto(name)

        if doc_path is None:
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
        doc_path = _resolve_foundations(name)

        if doc_path is None:
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
        system_path = _resolve_systems(name)

        if system_path is None:
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
        article_path = _resolve_articles(slug)

        if article_path is None:
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
        # Use content_service to load essays with privacy filtering
        essay_docs = content_service.list_documents(category="essays", include_private=False)

        # Generate markdown content for essay list
        md_content = "# Essays\n\nTechnical essays on semantic infrastructure.\n\n"
        for doc in sorted(essay_docs, key=lambda d: d.order):
            md_content += f"- [{doc.title}](/essays/{doc.slug})\n"

        if not essay_docs:
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
        """Serve essays by slug with privacy filtering."""
        # Use content_service to load essay with privacy filtering (Layer 2: Service)
        doc = content_service.load_document("essays", slug, include_private=False)

        # Layer 3: Route safety check - 404 for private or non-existent documents
        if not doc:
            raise HTTPException(status_code=404, detail=f"Essay not found: {slug}")

        # Additional safety: Check if document is private (defense-in-depth)
        if doc.private:
            raise HTTPException(status_code=404, detail=f"Essay not found: {slug}")

        title = doc.title + " - SIL"
        html_content = markdown_renderer.render(doc.content)

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
        paper_path = _resolve_research(name)

        if paper_path is None:
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

    @router.get("/architecture", response_class=HTMLResponse)
    async def architecture_index(request: Request) -> Response:
        """Architecture - System design and technical architecture."""
        return render_markdown_page(
            request,
            Path("docs/architecture/README.md"),
            "Architecture - Semantic Infrastructure Lab",
            "/architecture",
        )

    @router.get("/architecture/{name}", response_class=HTMLResponse)
    async def architecture_doc(request: Request, name: str) -> Response:
        """Individual architecture document."""
        doc_path = _resolve_architecture(name)

        if doc_path is None:
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

    @router.get("/projects", response_class=HTMLResponse)
    async def projects_index(request: Request) -> Response:
        """Projects - SIL project catalog and documentation."""
        return render_markdown_page(
            request,
            Path("docs/projects/README.md"),
            "Projects - Semantic Infrastructure Lab",
            "/projects",
        )

    @router.get("/projects/{name}", response_class=HTMLResponse)
    async def project_doc(request: Request, name: str) -> Response:
        """Individual project document."""
        doc_path = _resolve_projects(name)

        if doc_path is None:
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

    @router.get("/innovations", response_class=HTMLResponse)
    async def innovations_redirect(request: Request) -> Response:
        """Redirect /innovations to /systems."""
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/systems", status_code=301)

    @router.get("/innovations/{name}", response_class=HTMLResponse)
    async def innovation_redirect(request: Request, name: str) -> Response:
        """Redirect /innovations/{name} to /systems/{name}."""
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
        if name == "manifesto":
            # Redirect to manifesto index page
            return RedirectResponse(url="/manifesto", status_code=301)
        elif name == "yolo":
            return RedirectResponse(url="/manifesto/yolo", status_code=301)
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
        doc_path = _resolve_meta(name)

        if doc_path is None:
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
