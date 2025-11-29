#!/bin/bash
# SIL Website Remote Deployment Script
# Usage: ./deploy/deploy-remote.sh [staging|production]

set -e

ENVIRONMENT="${1:-staging}"
PROJECT_NAME="sil-website"

echo "🚀 SIL Website Remote Deployment"
echo "================================="
echo "Environment: $ENVIRONMENT"
echo ""

# Validate environment
case "$ENVIRONMENT" in
  staging|production)
    ;;
  *)
    echo "❌ Invalid environment: $ENVIRONMENT"
    echo "Usage: $0 [staging|production]"
    exit 1
    ;;
esac

# Set environment-specific variables
if [ "$ENVIRONMENT" == "staging" ]; then
  HOST="tia-staging"
  DEPLOY_PATH="/var/www/$PROJECT_NAME"
  CONTAINER_NAME="${PROJECT_NAME}-staging"
  CONTAINER_TAG="staging"
  SERVICE_PORT="8080"
  HEALTH_URL="https://staging.semanticinfrastructurelab.org/health"
else
  HOST="tia-apps"
  DEPLOY_PATH="/var/www/$PROJECT_NAME"
  CONTAINER_NAME="$PROJECT_NAME"
  CONTAINER_TAG="latest"
  SERVICE_PORT="8000"
  HEALTH_URL="https://semanticinfrastructurelab.org/health"
fi

echo "📡 Deploying to $HOST ($ENVIRONMENT)"
echo "   Path: $DEPLOY_PATH"
echo "   Container: $CONTAINER_NAME"
echo ""

# Test SSH connection
echo "🔐 Testing SSH connection..."
if ! ssh -q $HOST exit; then
  echo "❌ Cannot connect to $HOST"
  echo "Check your SSH config and keys"
  exit 1
fi
echo "✅ SSH connection successful"
echo ""

# Deploy
echo "📦 Deploying to remote server..."

ssh $HOST bash -s << EOF
set -e

echo "→ Navigating to project directory..."
cd $DEPLOY_PATH || {
  echo "❌ Project directory not found: $DEPLOY_PATH"
  echo "Create it first: mkdir -p $DEPLOY_PATH"
  exit 1
}

echo "→ Pulling latest code..."
git pull origin main

echo "→ Building container image..."
podman build -t $PROJECT_NAME:$CONTAINER_TAG .

echo "→ Stopping existing container..."
podman stop $CONTAINER_NAME 2>/dev/null || true
podman rm $CONTAINER_NAME 2>/dev/null || true

echo "→ Starting new container..."
podman run -d \
  --name $CONTAINER_NAME \
  -p 127.0.0.1:$SERVICE_PORT:8000 \
  -v /var/www/SIL/docs:/app/docs:ro \
  -v ${PROJECT_NAME}-logs:/app/logs \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  $PROJECT_NAME:$CONTAINER_TAG

echo "→ Waiting for container to be healthy..."
for i in {1..10}; do
  if podman healthcheck run $CONTAINER_NAME >/dev/null 2>&1; then
    echo "✅ Container is healthy!"
    break
  fi
  if [ \$i -eq 10 ]; then
    echo "❌ Container health check failed!"
    podman logs $CONTAINER_NAME
    exit 1
  fi
  sleep 2
done

echo "✅ Deployment complete!"
EOF

# Verify deployment
echo ""
echo "🔍 Verifying deployment..."
sleep 2

if curl -f -s -o /dev/null "$HEALTH_URL"; then
  echo "✅ Health check passed: $HEALTH_URL"
else
  echo "⚠️  Health check failed (might need DNS/nginx setup)"
  echo "   Try: ssh $HOST 'curl -f http://localhost:$SERVICE_PORT/health'"
fi

echo ""
echo "📊 Deployment Summary"
echo "===================="
echo "Environment: $ENVIRONMENT"
echo "Host: $HOST"
echo "Container: $CONTAINER_NAME"
echo "Health URL: $HEALTH_URL"
echo ""
echo "🔧 Useful commands:"
echo "  ssh $HOST 'podman logs -f $CONTAINER_NAME'  # View logs"
echo "  ssh $HOST 'podman restart $CONTAINER_NAME'  # Restart"
echo "  ssh $HOST 'podman stop $CONTAINER_NAME'     # Stop"
echo ""
echo "✅ Deployment complete!"
