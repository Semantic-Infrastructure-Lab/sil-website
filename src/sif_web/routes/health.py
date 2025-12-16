"""
Health check endpoint for monitoring and deployment validation.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Status information for monitoring systems
    """
    return {
        "status": "healthy",
        "service": "sil-website",
        "version": "0.1.0",
    }
