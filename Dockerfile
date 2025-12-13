# Multi-stage Dockerfile for SIF Website
# Following SIF Deployment Standards v1.0

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Copy project files
COPY pyproject.toml README.md ./
COPY src/ src/

# Install build dependencies and build wheel
RUN pip install --no-cache-dir build && \
    python -m build

# Stage 2: Production
FROM python:3.11-slim

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash appuser

WORKDIR /app

# Copy wheel from builder and install
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm /tmp/*.whl

# Copy static assets and templates
COPY --chown=appuser:appuser static/ static/
COPY --chown=appuser:appuser templates/ templates/

# Copy SIF docs (baked into container - no volume mounts needed)
# These are the SIF Foundation content pages (about, research, contact)
COPY --chown=appuser:appuser docs/ docs/

# Set docs path environment variable
ENV SIL_DOCS_PATH=/app/docs

# Create logs directory
RUN mkdir -p /app/logs && chown appuser:appuser /app/logs

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "sif_web.app:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
