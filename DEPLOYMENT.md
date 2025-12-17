---
title: "SIL Website - Container Deployment Guide"
id: "sil-website-container-deployment-guide"
uri: "doc://projects/sil-website/DEPLOYMENT.md"
type: "deployment-guide"
status: "production-ready"
version: "1.0"
created: "2025-11-28"
updated: "2025-11-28"
authors:
  - "user:scottsen"
  - "agent:claude"
project: "sil-website"
implements:
  - "doc://infrastructure/DEPLOYMENT_STRATEGY_2025.md"
  - "doc://infrastructure/HYBRID_DEPLOYMENT_ARCHITECTURE_2025.md"
references:
  - "doc://guides/CONTAINERIZATION_USER_GUIDE.md"
  - "doc://infrastructure/STATUS_CURRENT.md"
relates_to:
  - "project://sil-website"
  - "project://SIL"
beth_topics:
  - "sil-website"
  - "container-deployment"
  - "deployment-guide"
  - "registry-workflow"
  - "tia-infrastructure"
  - "staging-production"
  - "podman"
tags:
  - "deployment"
  - "containers"
  - "sil-website"
  - "registry"
  - "staging"
  - "production"
  - "podman"
  - "nginx"
  - "tia-infrastructure"
category: "deployment-documentation"
subcategory: "container-deployment"
priority: "high"
business_impact: "website-deployment"
technical_scope: "sil-website-infrastructure"
infrastructure:
  registry: "registry.mytia.net"
  staging_server: "tia-staging"
  production_server: "tia-apps"
  staging_url: "https://sil-staging.mytia.net"
  production_url: "https://semanticinfrastructurelab.org"
tier: 1
audience: "all"
estimated_read_time: "15 min"
summary: "Complete container-based deployment guide for SIL website following TIA canonical deployment pattern. Covers build, registry push, staging/production deployment, monitoring, and troubleshooting."
---

# SIL Website - Container Deployment Guide

**Last Updated:** 2025-12-08
**Status:** Production Ready ✅

## Overview

This guide follows the **TIA Canonical Deployment Pattern** using container registry workflow.

**Infrastructure:**
- **Registry:** `registry.mytia.net/sil-website`
- **Staging:** `tia-staging` → Port 8080 → https://sil-staging.mytia.net
- **Production:** `tia-apps` → Port 8010 → https://semanticinfrastructurelab.org

---

## Quick Start

```bash
# 1. Pre-deployment checks (recommended)
./scripts/pre-deploy-check.sh staging

# 2. Build, push, and deploy to staging
./deploy/deploy-container.sh staging

# 3. Run smoke tests
./scripts/smoke-test.sh staging

# 4. Deploy to production (after staging verification)
./deploy/deploy-container.sh production
./scripts/smoke-test.sh production
```

---

## Content Management

**SIL uses CONTENT_MANIFEST.yaml to control public vs internal documentation:**

- **Location**: `/projects/SIL/docs/CONTENT_MANIFEST.yaml`
- **Public files**: 58 (synced to website)
- **Internal files**: 13 (protected from publication)
- **Validation**: `./scripts/sync-docs.py --validate`

**Before deploying**, ensure sync is current:
```bash
cd /home/scottsen/src/projects/sil-website
./scripts/sync-docs.py              # Sync public docs from SIL repo
./scripts/sync-docs.py --validate   # Verify no internal files in website
```

**Deployment workflow**:
1. Pre-deploy check validates manifest and sync status
2. Deployment script bakes docs into container
3. Smoke tests verify critical pages load

See `/projects/SIL/docs/CONTENT_MANIFEST.yaml` for complete file list and rationale.

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LOCAL DEVELOPMENT                         │
├─────────────────────────────────────────────────────────────┤
│  1. Build container image with SIL docs baked in            │
│  2. Tag with semantic version                                │
│  3. Test locally on port 8000                                │
│  4. Push to registry.mytia.net                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  CONTAINER REGISTRY                          │
├─────────────────────────────────────────────────────────────┤
│  registry.mytia.net/sil-website:v1.0.0                      │
│  registry.mytia.net/sil-website:staging                     │
│  registry.mytia.net/sil-website:latest                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              tia-proxy (CENTRAL REVERSE PROXY)               │
├─────────────────────────────────────────────────────────────┤
│  nginx (443) routes to backend containers:                   │
│  - sil-staging.mytia.net      → 10.108.0.8:8080 (staging)   │
│  - semanticinfrastructurelab.org → 165.227.98.17:8010 (prod)│
│  Upstreams: /etc/nginx/conf.d/tia-upstreams.conf            │
│  Site config: /etc/nginx/sites-available/                    │
└─────────────────────────────────────────────────────────────┘
                │                           │
                ▼                           ▼
┌──────────────────────────┐  ┌──────────────────────────────┐
│   STAGING (tia-staging)  │  │  PRODUCTION (tia-apps)       │
├──────────────────────────┤  ├──────────────────────────────┤
│  IP: 10.108.0.8          │  │  IP: 165.227.98.17           │
│  Container: 8080→8000    │  │  Container: 8010→8000        │
│  Bind: 10.108.0.8:8080   │  │  Bind: 0.0.0.0:8010          │
│  Health: /health         │  │  Health: /health             │
└──────────────────────────┘  └──────────────────────────────┘
```

**Key Architecture Points:**
- **tia-proxy** handles ALL nginx/SSL termination (not tia-apps or tia-staging)
- Containers bind to IPs accessible from tia-proxy
- Staging uses private IP (10.108.0.8), production uses public (0.0.0.0)

---

## Step-by-Step Deployment

### Step 1: Build Container Image

```bash
# Navigate to project directory
cd /home/scottsen/src/projects/sil-website

# Build with version tag
VERSION="v1.0.0"  # Use semantic versioning
podman build -t registry.mytia.net/sil-website:$VERSION .

# Tag for environments
podman tag registry.mytia.net/sil-website:$VERSION registry.mytia.net/sil-website:staging
podman tag registry.mytia.net/sil-website:$VERSION registry.mytia.net/sil-website:latest
```

**What gets baked into the container:**
- ✅ Python application code
- ✅ SIL docs from `/home/scottsen/src/projects/SIL/docs`
- ✅ All dependencies (FastHTML, Markdown, etc.)
- ✅ Health check endpoint
- ❌ No secrets (use environment variables)

### Step 2: Test Locally

```bash
# Run container locally
podman run -p 8000:8000 \
  --name sil-website-test \
  registry.mytia.net/sil-website:$VERSION

# Test health endpoint
curl http://localhost:8000/health

# Test main page
curl http://localhost:8000/

# View logs
podman logs -f sil-website-test

# Cleanup
podman stop sil-website-test
podman rm sil-website-test
```

### Step 3: Push to Registry

```bash
# Login to registry (first time only)
podman login registry.mytia.net

# Push all tags
podman push registry.mytia.net/sil-website:$VERSION
podman push registry.mytia.net/sil-website:staging
podman push registry.mytia.net/sil-website:latest

# Verify push
curl https://registry.mytia.net/v2/sil-website/tags/list
```

### Step 4: Deploy to Staging

```bash
# SSH to staging server
ssh tia-staging

# Pull latest staging image
podman pull registry.mytia.net/sil-website:staging

# Stop existing container
podman stop sil-website-staging || true
podman rm sil-website-staging || true

# Run new container
podman run -d \
  --name sil-website-staging \
  -p 127.0.0.1:8080:8000 \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  --health-timeout=5s \
  --health-retries=3 \
  registry.mytia.net/sil-website:staging

# Check health
podman healthcheck run sil-website-staging

# Check logs
podman logs -f sil-website-staging
```

### Step 5: Verify Staging

```bash
# From local machine
curl -f https://sil-staging.mytia.net/health
curl -f https://sil-staging.mytia.net/ | head -20

# Check nginx is proxying correctly
ssh tia-staging 'curl -f http://localhost:8080/health'
```

### Step 6: Deploy to Production

```bash
# SSH to production server
ssh tia-apps

# Pull latest production image
podman pull registry.mytia.net/sil-website:latest

# Stop existing container
podman stop sil-website || true
podman rm sil-website || true

# Run new container
podman run -d \
  --name sil-website \
  -p 0.0.0.0:8010:8000 \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  --health-timeout=5s \
  --health-retries=3 \
  registry.mytia.net/sil-website:latest

# Check health
podman healthcheck run sil-website

# Monitor startup
podman logs -f sil-website
```

### Step 7: Verify Production

```bash
# From local machine
curl -f https://semanticinfrastructurelab.org/health
curl -f https://semanticinfrastructurelab.org/ | head -20

# Verify all pages load
curl -f https://semanticinfrastructurelab.org/projects
curl -f https://semanticinfrastructurelab.org/docs/manifesto
```

---

## Automated Deployment Script

Use `deploy/deploy-container.sh` for automated deployments:

```bash
# Deploy to staging
./deploy/deploy-container.sh staging

# Deploy to production
./deploy/deploy-container.sh production
```

**What the script does:**
1. Builds container with current git commit SHA as label
2. Tags with environment-specific tag
3. Pushes to registry.mytia.net
4. SSHs to target server
5. Pulls latest image
6. Stops old container
7. Starts new container
8. Waits for health check
9. Verifies deployment

---

## Systemd Service (Optional - For Auto-Restart)

To run sil-website as a systemd service on production:

```bash
# Copy service file
sudo cp deploy/sil-website.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable sil-website

# Start service
sudo systemctl start sil-website

# Check status
sudo systemctl status sil-website

# View logs
sudo journalctl -u sil-website -f
```

**Service features:**
- Auto-restart on failure
- Resource limits (512MB RAM, 50% CPU)
- Health checks every 30s
- Graceful shutdown

---

## Nginx Configuration

**All nginx configuration is on tia-proxy** (not on tia-apps or tia-staging).

**Traffic Flow:**
```
User → tia-proxy (nginx/SSL) → backend container
```

**Staging:**
```
https://sil-staging.mytia.net
  → tia-proxy nginx (443)
  → upstream sil_website_staging (10.108.0.8:8080)
  → container:8000
```

**Production:**
```
https://semanticinfrastructurelab.org
  → tia-proxy nginx (443)
  → upstream sil_website_production (165.227.98.17:8010)
  → container:8000
```

**Configuration files (on tia-proxy):**
- Upstreams: `/etc/nginx/conf.d/tia-upstreams.conf`
- Site config: `/etc/nginx/sites-available/semanticinfrastructurelab.org`

**Useful commands (on tia-proxy):**
```bash
# View upstreams
cat /etc/nginx/conf.d/tia-upstreams.conf | grep sil

# Test config
sudo nginx -t

# Reload after changes
sudo systemctl reload nginx
```

---

## Rollback Procedure

If deployment fails:

```bash
# List previous images
curl https://registry.mytia.net/v2/sil-website/tags/list

# Pull specific version
podman pull registry.mytia.net/sil-website:v0.9.0

# Run previous version
podman run -d --name sil-website \
  -p 0.0.0.0:8010:8000 \
  registry.mytia.net/sil-website:v0.9.0
```

**Or tag previous version as latest:**

```bash
# Locally, tag old version as latest
podman pull registry.mytia.net/sil-website:v0.9.0
podman tag registry.mytia.net/sil-website:v0.9.0 registry.mytia.net/sil-website:latest
podman push registry.mytia.net/sil-website:latest

# Then redeploy using standard workflow
```

---

## Troubleshooting

### Container won't start

```bash
# Check container logs
podman logs sil-website

# Check container inspect
podman inspect sil-website

# Test image locally
podman run -it --rm registry.mytia.net/sil-website:latest /bin/bash
```

### Health check failing

```bash
# Test health endpoint manually
podman exec sil-website curl -f http://localhost:8000/health

# Check application logs
podman logs -f sil-website

# Verify port binding
podman port sil-website
```

### Registry push fails

```bash
# Re-authenticate
podman login registry.mytia.net

# Check registry connectivity
curl https://registry.mytia.net/v2/

# Check image size
podman images | grep sil-website
```

### Site not accessible via HTTPS

```bash
# Check nginx is running
ssh tia-apps 'sudo systemctl status nginx'

# Check nginx config
ssh tia-apps 'sudo nginx -t'

# Check nginx logs
ssh tia-apps 'sudo tail -f /var/log/nginx/sil-website-error.log'

# Verify container is listening
ssh tia-apps 'curl http://localhost:8010/health'
```

### Docs not updating after sync (IMPORTANT)

**Symptom:** You ran `sync-docs.sh` and `generate-llms-full.sh`, deployed, but the site shows old content.

**Cause:** Podman caches the `COPY docs/ docs/` layer. If file timestamps don't change enough, it reuses the cached layer.

**Fix:** Force a no-cache build:

```bash
# Option 1: Build with --no-cache
podman build --no-cache -t registry.mytia.net/sil-website:v1.0.x .

# Option 2: Touch docs to bust cache (less reliable)
touch docs/.cache-bust
```

**Verification:**
```bash
# Check build output - should NOT say "Using cache" for docs step
# Look for: [2/2] STEP 9/15: COPY --chown=appuser:appuser docs/ docs/
# Should show: --> abc123def (new hash, not "Using cache")
```

### 502 Bad Gateway on staging

**Symptom:** Container is running, `curl localhost:8080` works on tia-staging, but https://sil-staging.mytia.net returns 502.

**Cause:** Container bound to `127.0.0.1:8080` but nginx proxy on tia-proxy reaches `10.108.0.8:8080` (private IP).

**Architecture:**
```
tia-proxy (nginx) → 10.108.0.8:8080 → tia-staging container
```

**Fix:** Bind to private IP, not localhost:

```bash
# Wrong (localhost only):
podman run -d -p 127.0.0.1:8080:8000 ...

# Correct (accessible from proxy):
podman run -d -p 10.108.0.8:8080:8000 ...
```

**Verification:**
```bash
# Check binding
ssh tia-staging 'podman port sil-website-staging'
# Should show: 8000/tcp -> 10.108.0.8:8080

# Test from proxy
ssh tia-proxy 'curl http://10.108.0.8:8080/health'
```

---

## Deploying Essays

Essays are published content pieces served from `/essays/{slug}`. The source lives in TIA SIL project (`/home/scottsen/src/tia/projects/SIL/lab/products/essays/`).

### Quick Deploy

```bash
cd /home/scottsen/src/projects/sil-website

# 1. Sync essays from TIA SIL
./scripts/sync-docs.sh

# 2. Deploy with fresh build (required for content changes)
./deploy/deploy-container.sh staging --fresh

# 3. Verify
curl https://sif-staging.mytia.net/essays/progressive-disclosure-for-ai-agents
```

### URL Mapping

Essay filenames map to URLs:

| Source File | URL |
|------------|-----|
| `PROGRESSIVE_DISCLOSURE_FOR_AI_AGENTS.md` | `/essays/progressive-disclosure-for-ai-agents` |
| `NEW_ESSAY_TITLE.md` | `/essays/new-essay-title` |

**Pattern:** `UPPER_SNAKE_CASE.md` → `/essays/lower-kebab-case`

### Adding New Essays

1. Create essay in TIA SIL: `/home/scottsen/src/tia/projects/SIL/lab/products/essays/NEW_ESSAY.md`
2. Run `./scripts/sync-docs.sh` to sync to website
3. Deploy with `--fresh` flag to include new content
4. Access at `https://sif-staging.mytia.net/essays/new-essay`

### Important Notes

- **Always use `--fresh` flag** when deploying content changes (podman caches the COPY layer)
- Essays are synced from TIA SIL lab, not the main SIL repo
- The essay route extracts the title from the first `# H1` in the markdown

---

## Best Practices

### Version Tagging

✅ **DO:**
- Use semantic versioning: `v1.0.0`, `v1.0.1`, `v1.1.0`
- Tag git commits when deploying: `git tag v1.0.0`
- Include git SHA in image labels
- Keep staging/production tags updated

❌ **DON'T:**
- Use generic tags like `v1` or `test`
- Skip version tags (always version!)
- Forget to push tags: `git push --tags`

### Container Images

✅ **DO:**
- Bake docs into container (no volume mounts)
- Use multi-stage builds to reduce size
- Test locally before pushing
- Use health checks
- Set resource limits

❌ **DON'T:**
- Mount volumes in production (breaks portability)
- Include secrets in image (use env vars)
- Skip health checks
- Use `:latest` tag in production (use versioned tags)

### Deployment Workflow

✅ **DO:**
- Always deploy to staging first
- Verify staging before production
- Use automated script for consistency
- Monitor logs during deployment
- Keep previous version available for rollback

❌ **DON'T:**
- Deploy directly to production
- Skip health checks
- Deploy without testing
- Delete old images immediately

---

## Monitoring

### Container Health

```bash
# Check container status
podman ps -a --filter name=sil-website

# Check health
podman healthcheck run sil-website

# View logs
podman logs -f sil-website --since 5m

# Check resource usage
podman stats sil-website
```

### Application Health

```bash
# Health endpoint (staging)
curl -f https://sil-staging.mytia.net/health

# Health endpoint (production)
curl -f https://semanticinfrastructurelab.org/health

# Check response time
time curl -f https://semanticinfrastructurelab.org/
```

---

## Infrastructure Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **registry.mytia.net** | Container registry | TIA infrastructure |
| **tia-staging** | Staging server | SSH host |
| **tia-apps** | Production server | SSH host |
| **tia-proxy** | Reverse proxy / Load balancer | TIA infrastructure |
| **GitHub** | Source code | https://github.com/scottsen/sil-website |

---

## Related Documentation

- **TIA Deployment Strategy:** `~/src/tia/docs/infrastructure/DEPLOYMENT_STRATEGY_2025.md`
- **TIA Container Guide:** `~/src/tia/docs/guides/CONTAINERIZATION_USER_GUIDE.md`
- **TIA Infrastructure Status:** `~/src/tia/docs/infrastructure/STATUS_CURRENT.md`
- **Hybrid Deployment Architecture:** `~/src/tia/docs/infrastructure/HYBRID_DEPLOYMENT_ARCHITECTURE_2025.md`

---

## Contact

**Issues:** Report at https://github.com/scottsen/sil-website/issues
**TIA Infrastructure:** See TIA docs at `~/src/tia/docs/infrastructure/`
