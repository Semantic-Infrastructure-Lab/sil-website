#!/bin/bash
# SIL Website - Container Registry Deployment Script
# Follows TIA Canonical Deployment Pattern
#
# Usage:
#   ./deploy-container.sh staging           # Normal deploy
#   ./deploy-container.sh staging --fresh   # Force rebuild (use after docs sync)
#   ./deploy-container.sh production
#
# IMPORTANT: Use --fresh flag after running sync-docs.sh to ensure
# docs changes are included (podman caches the COPY docs/ layer)

set -e

# Parse arguments
ENVIRONMENT="${1:-staging}"
FRESH_BUILD=false
if [[ "$2" == "--fresh" ]] || [[ "$2" == "--no-cache" ]]; then
  FRESH_BUILD=true
fi

PROJECT_NAME="sil-website"
REGISTRY="registry.mytia.net"
IMAGE_NAME="${REGISTRY}/${PROJECT_NAME}"

# Get git commit SHA for image labeling
GIT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

# Semantic version (update this for releases)
VERSION="${VERSION:-v1.0.0}"

echo "🚀 SIL Website Container Deployment"
echo "===================================="
echo "Environment: $ENVIRONMENT"
echo "Registry: $REGISTRY"
echo "Image: $IMAGE_NAME"
echo "Version: $VERSION"
echo "Git SHA: $GIT_SHA"
echo "Git Branch: $GIT_BRANCH"
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
  CONTAINER_NAME="${PROJECT_NAME}-staging"
  CONTAINER_TAG="staging"
  SERVICE_PORT="8080"
  # Bind to private IP for tia-proxy access (not 127.0.0.1 or 0.0.0.0)
  BIND_IP="10.108.0.8"
  HEALTH_URL="https://sil-staging.mytia.net/health"
else
  HOST="tia-apps"
  CONTAINER_NAME="$PROJECT_NAME"
  CONTAINER_TAG="latest"
  SERVICE_PORT="8000"
  # Production binds to localhost (nginx on same machine)
  BIND_IP="127.0.0.1"
  HEALTH_URL="https://semanticinfrastructurelab.org/health"
fi

echo "📡 Target server: $HOST"
echo "   Container: $CONTAINER_NAME"
echo "   Tag: $CONTAINER_TAG"
echo "   Port: $SERVICE_PORT"
echo ""

# Step 1: Build container image
echo "🔨 Step 1: Building container image..."
echo "   Building: ${IMAGE_NAME}:${VERSION}"

BUILD_ARGS=(
  --label "git.sha=${GIT_SHA}"
  --label "git.branch=${GIT_BRANCH}"
  --label "build.timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  --label "version=${VERSION}"
  -t "${IMAGE_NAME}:${VERSION}"
)

if [ "$FRESH_BUILD" = true ]; then
  echo "   🔄 Fresh build requested (--no-cache)"
  BUILD_ARGS+=(--no-cache)
fi

podman build "${BUILD_ARGS[@]}" .

echo "✅ Image built successfully"
echo ""

# Step 2: Tag for environment
echo "🏷️  Step 2: Tagging for environment..."
podman tag "${IMAGE_NAME}:${VERSION}" "${IMAGE_NAME}:${CONTAINER_TAG}"
echo "   Tagged: ${IMAGE_NAME}:${CONTAINER_TAG}"
echo "✅ Tagged successfully"
echo ""

# Step 3: Test locally (optional, quick health check)
echo "🧪 Step 3: Testing image locally..."
TEST_CONTAINER="${PROJECT_NAME}-test-$$"

podman run -d \
  --name "$TEST_CONTAINER" \
  -p 127.0.0.1:18000:8000 \
  "${IMAGE_NAME}:${VERSION}"

echo "   Waiting for container to start..."
sleep 5

if podman healthcheck run "$TEST_CONTAINER" >/dev/null 2>&1; then
  echo "✅ Health check passed"
else
  echo "⚠️  Health check failed (container may still be starting)"
  podman logs "$TEST_CONTAINER" | tail -10
fi

# Cleanup test container
podman stop "$TEST_CONTAINER" >/dev/null 2>&1
podman rm "$TEST_CONTAINER" >/dev/null 2>&1
echo ""

# Step 4: Push to registry
echo "📤 Step 4: Pushing to container registry..."
echo "   Pushing: ${IMAGE_NAME}:${VERSION}"
echo "   Pushing: ${IMAGE_NAME}:${CONTAINER_TAG}"

podman push "${IMAGE_NAME}:${VERSION}"
podman push "${IMAGE_NAME}:${CONTAINER_TAG}"

echo "✅ Pushed to registry"
echo ""

# Step 5: Verify registry
echo "🔍 Step 5: Verifying registry..."
if curl -f -s "https://${REGISTRY}/v2/${PROJECT_NAME}/tags/list" | grep -q "${CONTAINER_TAG}"; then
  echo "✅ Tag verified in registry"
else
  echo "⚠️  Tag not found in registry (may need authentication)"
fi
echo ""

# Step 6: Deploy to target server
echo "🚀 Step 6: Deploying to $HOST..."
echo "   Connecting via SSH..."

# Test SSH connection
if ! ssh -q $HOST exit; then
  echo "❌ Cannot connect to $HOST"
  echo "Check your SSH config and keys"
  exit 1
fi

echo "✅ SSH connection successful"
echo ""

# Deploy via SSH
echo "📦 Deploying container on $HOST..."

ssh $HOST bash -s <<EOF
set -e

echo "→ Pulling latest image..."
podman pull ${IMAGE_NAME}:${CONTAINER_TAG}

echo "→ Stopping existing container..."
podman stop $CONTAINER_NAME 2>/dev/null || true
podman rm $CONTAINER_NAME 2>/dev/null || true

echo "→ Starting new container..."
podman run -d \
  --name $CONTAINER_NAME \
  -p ${BIND_IP}:$SERVICE_PORT:8000 \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  --health-timeout=5s \
  --health-retries=3 \
  --restart=unless-stopped \
  ${IMAGE_NAME}:${CONTAINER_TAG}

echo "→ Waiting for container to be healthy..."
for i in {1..10}; do
  if podman healthcheck run $CONTAINER_NAME >/dev/null 2>&1; then
    echo "✅ Container is healthy!"
    break
  fi
  if [ \$i -eq 10 ]; then
    echo "❌ Container health check failed!"
    echo "Logs:"
    podman logs $CONTAINER_NAME | tail -20
    exit 1
  fi
  echo "   Attempt \$i/10..."
  sleep 3
done

echo ""
echo "📊 Container Status:"
podman ps --filter name=$CONTAINER_NAME --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "✅ Deployment complete on $HOST!"
EOF

# Step 7: Verify deployment
echo ""
echo "🔍 Step 7: Verifying deployment..."
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
echo "Image: ${IMAGE_NAME}:${CONTAINER_TAG}"
echo "Version: $VERSION"
echo "Git SHA: $GIT_SHA"
echo "Container: $CONTAINER_NAME"
echo "Health URL: $HEALTH_URL"
echo ""
echo "🔧 Useful commands:"
echo "  ssh $HOST 'podman logs -f $CONTAINER_NAME'     # View logs"
echo "  ssh $HOST 'podman restart $CONTAINER_NAME'     # Restart"
echo "  ssh $HOST 'podman stop $CONTAINER_NAME'        # Stop"
echo "  ssh $HOST 'podman ps --filter name=$CONTAINER_NAME'  # Status"
echo ""
echo "✅ Deployment complete!"
