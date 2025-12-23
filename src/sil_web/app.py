"""
Main FastAPI application.

Wires together all layers: services, routes, configuration.
"""

import structlog
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from sil_web.config.settings import DOCS_PATH
from sil_web.routes.health import router as health_router
from sil_web.routes.llms import router as llms_router
from sil_web.routes.pages import create_routes
from sil_web.routes.robots import router as robots_router
from sil_web.services.content import ContentService
from sil_web.services.markdown import MarkdownRenderer
from sil_web.services.metrics import MetricsService

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)

log = structlog.get_logger()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)

        # Security headers
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://analytics.semanticinfrastructurelab.org; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self' https://analytics.semanticinfrastructurelab.org; "
            "frame-ancestors 'self';"
        )

        # HSTS (only in production - nginx should handle this)
        # Uncommented for defense in depth
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

        return response


def create_app() -> FastAPI:
    """Create and configure FastAPI application.

    Returns:
        Configured FastAPI app
    """
    app = FastAPI(
        title="Semantic Infrastructure Lab",
        description="Building the semantic substrate for trustworthy AI",
        version="0.1.0",
        docs_url=None,  # Disable Swagger UI (not needed for public website)
        redoc_url=None,  # Disable ReDoc (not needed for public website)
    )

    # Add security headers middleware
    app.add_middleware(SecurityHeadersMiddleware)

    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Initialize services
    content_service = ContentService(docs_path=DOCS_PATH)
    markdown_renderer = MarkdownRenderer(content_service)
    metrics_service = MetricsService()  # Uses canonical TIA metrics by default

    # Mount health check (no dependencies)
    app.include_router(health_router)

    # Mount robots.txt (no dependencies)
    app.include_router(robots_router)

    # Mount llms.txt endpoints (no dependencies)
    app.include_router(llms_router)

    # Create and mount page routes (SIF doesn't use project_service)
    routes = create_routes(content_service, None, markdown_renderer, metrics_service)
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
