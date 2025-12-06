"""
Main FastAPI application.

Wires together all layers: services, routes, configuration.
"""

import structlog
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from sil_web.config.settings import DOCS_PATH
from sil_web.routes.health import router as health_router
from sil_web.routes.pages import create_routes
from sil_web.services.content import ContentService, ProjectService
from sil_web.services.github import GitHubService
from sil_web.services.markdown import MarkdownRenderer

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)

log = structlog.get_logger()


def create_app() -> FastAPI:
    """Create and configure FastAPI application.

    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title="Semantic Infrastructure Lab",
        description="Building the semantic substrate for intelligent systems",
        version="0.1.0",
        docs_url=None,  # Disable Swagger UI (not needed for public website)
        redoc_url=None,  # Disable ReDoc (not needed for public website)
    )

    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Initialize services
    content_service = ContentService(docs_path=DOCS_PATH)
    project_service = ProjectService()
    github_service = GitHubService()
    markdown_renderer = MarkdownRenderer(content_service)

    # Mount health check (no dependencies)
    app.include_router(health_router)

    # Create and mount page routes
    routes = create_routes(content_service, project_service, markdown_renderer)
    app.include_router(routes)

    log.info("app_created", docs_path=str(DOCS_PATH))

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    from sil_web.config.settings import DEBUG, HOST, PORT

    uvicorn.run(
        "sil_web.app:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info",
    )
