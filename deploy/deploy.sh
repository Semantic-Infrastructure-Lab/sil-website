#!/bin/bash
# SIL Website Deployment Script
# Usage: ./deploy/deploy.sh [development|staging|production]

set -e

PROFILE="${1:-development}"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🚀 SIL Website Deployment"
echo "=========================="
echo "Profile: $PROFILE"
echo "Project: $PROJECT_DIR"
echo ""

case "$PROFILE" in
  development)
    echo "📦 Development deployment (local, no container)"
    cd "$PROJECT_DIR"

    # Create venv if needed
    if [ ! -d ".venv" ]; then
      echo "Creating virtual environment..."
      uv venv
    fi

    # Activate and install
    source .venv/bin/activate
    echo "Installing dependencies..."
    uv pip install -e ".[dev]"

    echo "✅ Development environment ready"
    echo "Run: python src/sil_web/app.py"
    ;;

  staging)
    echo "📦 Staging deployment (local container)"
    cd "$PROJECT_DIR"

    # Build container
    echo "Building container image..."
    podman build -t sil-website:staging .

    # Stop existing container
    echo "Stopping existing container..."
    podman stop sil-website-staging 2>/dev/null || true
    podman rm sil-website-staging 2>/dev/null || true

    # Run new container
    echo "Starting container..."
    podman run -d \
      --name sil-website-staging \
      -p 8000:8000 \
      -v "${PROJECT_DIR}/../SIL/docs:/app/docs:ro" \
      -v sil-website-staging-logs:/app/logs \
      sil-website:staging

    echo "✅ Staging container deployed"
    echo "URL: http://localhost:8000"
    echo "Logs: podman logs -f sil-website-staging"
    echo "Stop: podman stop sil-website-staging"
    ;;

  production)
    echo "📦 Production deployment (systemd + nginx)"
    cd "$PROJECT_DIR"

    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
      echo "❌ Don't run this script as root!"
      echo "The script will use sudo when needed."
      exit 1
    fi

    # Build container
    echo "Building production container..."
    podman build -t sil-website:latest .

    # Check if systemd service exists
    if [ ! -f "/etc/systemd/system/sil-website.service" ]; then
      echo "Installing systemd service..."
      sudo cp deploy/sil-website.service /etc/systemd/system/
      sudo systemctl daemon-reload
      sudo systemctl enable sil-website
    fi

    # Restart service
    echo "Restarting service..."
    sudo systemctl restart sil-website

    # Wait for health check
    echo "Waiting for service to be healthy..."
    sleep 5

    for i in {1..10}; do
      if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        echo "✅ Service is healthy!"
        break
      fi
      if [ $i -eq 10 ]; then
        echo "❌ Service health check failed!"
        echo "Check logs: sudo journalctl -u sil-website -n 50"
        exit 1
      fi
      sleep 2
    done

    # Check nginx
    if [ ! -L "/etc/nginx/sites-enabled/semanticinfrastructurelab.org" ]; then
      echo ""
      echo "⚠️  Nginx not configured yet!"
      echo "To set up nginx:"
      echo "  sudo cp deploy/nginx.conf /etc/nginx/sites-available/semanticinfrastructurelab.org"
      echo "  sudo ln -s /etc/nginx/sites-available/semanticinfrastructurelab.org /etc/nginx/sites-enabled/"
      echo "  sudo nginx -t"
      echo "  sudo systemctl reload nginx"
    fi

    echo ""
    echo "✅ Production deployment complete!"
    echo "Status: sudo systemctl status sil-website"
    echo "Logs: sudo journalctl -u sil-website -f"
    ;;

  *)
    echo "❌ Invalid profile: $PROFILE"
    echo "Usage: $0 [development|staging|production]"
    exit 1
    ;;
esac
