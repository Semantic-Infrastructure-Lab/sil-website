---
title: "SIL Deployment Standards"
id: sil-deployment-standards
uri: doc://operations/DEPLOYMENT_STANDARDS.md
type: standard
status: active
version: '1.0'
created: '2025-11-28'
authors:
  - scottsen
  - agent:claude-sonnet-4.5
related:
  - uri: /home/scottsen/src/tia/commands/container/README.md
    type: extends
    description: TIA container orchestration patterns
tags:
  - deployment
  - containers
  - podman
  - systemd
  - nginx
  - infrastructure
category: operations
priority: high
tier: 1
audience: platform-engineers
summary: Comprehensive deployment standards for all SIL production projects - containers, systemd, nginx, and CI/CD.
---

# SIL Deployment Standards

**Unified deployment patterns for the Semantic Infrastructure Lab ecosystem.**

---

## Philosophy

SIL deployment follows these principles:
1. **Container-first** - All services run in containers (Podman)
2. **Systemd-managed** - Production services managed by systemd
3. **Nginx-proxied** - Web apps behind reverse proxy
4. **Profile-based** - Consistent dev/staging/prod profiles
5. **Observable** - Structured logging, health checks, metrics
6. **Reproducible** - Infrastructure as code, documented procedures

---

## Infrastructure Environments

### Environment Overview

| Environment | Host | Alias | IP | Purpose |
|------------|------|-------|----|---------|
| **Local** | localhost | - | 127.0.0.1 | Development |
| **Staging** | tia-dev | tia-staging | 167.71.107.249 | Pre-production testing |
| **Production** | tia-apps | - | 165.227.98.17 | Live services |

### Environment Details

#### Local Development
- **Purpose:** Active development, rapid iteration
- **Access:** Direct (no SSH needed)
- **Containers:** Optional (can run natively)
- **Deployment:** `./deploy/deploy.sh development`
- **URL:** `http://localhost:PORT`

#### Staging (tia-dev / tia-staging)
- **Purpose:** Pre-production validation, integration testing
- **Access:** `ssh tia-staging` (alias for tia-dev)
- **Containers:** Required (Podman)
- **Deployment:** `./deploy/deploy.sh staging` (remote)
- **URL:** `https://sil-staging.mytia.net`
- **Features:**
  - Production-like environment
  - Safe testing of deployment procedures
  - Integration testing
  - Performance validation

#### Production (tia-apps)
- **Purpose:** Live public services
- **Access:** `ssh tia-apps` (limited, automated deployments preferred)
- **Containers:** Required (Podman + systemd)
- **Deployment:** Automated via GitHub Actions
- **URL:** `https://semanticinfrastructurelab.org`
- **Features:**
  - High availability
  - Monitoring & alerting
  - Automated backups
  - TLS/HTTPS required

### SSH Configuration

Add to `~/.ssh/config`:

```ssh-config
# Development staging environment
Host tia-dev
    HostName 167.71.107.249
    User scottsen

# Staging alias (same as tia-dev)
Host tia-staging
    HostName 167.71.107.249
    User scottsen

# Production environment
Host tia-apps
    HostName 165.227.98.17
    User scottsen
```

### Deployment Flow

```
Local Development
  ↓ (git push to feature branch)
Pull Request Created
  ↓ (CI tests pass)
Merge to main
  ↓ (automatic)
Deploy to Staging (tia-staging)
  ↓ (manual approval or time-based)
Deploy to Production (tia-apps)
```

---

## Deployment Tiers

### Tier 1: CLI Tools (PyPI-Distributed)
**Examples:** reveal, tiacad (CLI mode)

**Deployment:**
```bash
# Development
uv venv && uv pip install -e ".[dev]"

# Production
pip install reveal-cli
pipx install reveal-cli  # Isolated install
```

**No containerization needed** - Users install directly.

---

### Tier 2: Web Applications (Containerized + Systemd)
**Examples:** sil-website, morphogen-server, pantheon-api

**Stack:**
- **Container:** Podman (following TIA patterns)
- **Process:** Systemd service
- **Proxy:** Nginx reverse proxy
- **TLS:** Let's Encrypt (certbot)

**Full deployment pattern below.**

---

### Tier 3: Background Services (Containerized)
**Examples:** semantic-memory-daemon, agent-ether-coordinator

**Stack:**
- **Container:** Podman
- **Process:** Systemd service
- **No proxy** (internal only)

---

## Standard Deployment Stack

### 1. Containerization (Podman)

**Why Podman over Docker?**
- Rootless containers (better security)
- No daemon required
- Compatible with Docker images
- systemd integration
- TIA uses it (consistency)

#### Standard Dockerfile

```dockerfile
# Multi-stage build for production
FROM python:3.11-slim AS builder

WORKDIR /build
COPY pyproject.toml README.md ./
COPY src/ src/

# Install build dependencies
RUN pip install --no-cache-dir build && \
    python -m build

# Production stage
FROM python:3.11-slim

# Non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy wheel from builder
COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm /tmp/*.whl

# Copy static assets if web app
COPY static/ static/
COPY templates/ templates/

USER appuser
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "sil_web.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Build and Tag

```bash
# Local build
podman build -t sil-website:latest .

# With registry (future)
podman build -t registry.semanticinfrastructurelab.org/sil-website:v0.1.0 .
podman push registry.semanticinfrastructurelab.org/sil-website:v0.1.0
```

---

### 2. Systemd Service Management

#### Service File Template

```ini
[Unit]
Description=SIL Website - Semantic Infrastructure Lab public site
Documentation=https://github.com/semantic-infrastructure-lab/sil-website
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=scottsen
Group=scottsen
WorkingDirectory=/home/scottsen/src/projects/sil-website

# Container management
ExecStartPre=/usr/bin/podman pull localhost/sil-website:latest
ExecStart=/usr/bin/podman run \
  --rm \
  --name sil-website \
  -p 127.0.0.1:8000:8000 \
  -v /home/scottsen/src/projects/SIL/docs:/app/docs:ro \
  -v sil-website-logs:/app/logs \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  localhost/sil-website:latest

ExecStop=/usr/bin/podman stop -t 10 sil-website
ExecStopPost=/usr/bin/podman rm -f sil-website

Restart=on-failure
RestartSec=10s

# Resource limits
MemoryMax=512M
CPUQuota=50%

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=sil-website

[Install]
WantedBy=multi-user.target
```

#### Service Management

```bash
# Install service
sudo cp sil-website.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sil-website
sudo systemctl start sil-website

# Check status
sudo systemctl status sil-website
sudo journalctl -u sil-website -f

# Updates
podman build -t sil-website:latest .
sudo systemctl restart sil-website
```

---

### 3. Nginx Reverse Proxy

#### Site Configuration

```nginx
# /etc/nginx/sites-available/semanticinfrastructurelab.org

upstream sil_website {
    server 127.0.0.1:8000 fail_timeout=0;
}

server {
    listen 80;
    listen [::]:80;
    server_name semanticinfrastructurelab.org www.semanticinfrastructurelab.org;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name semanticinfrastructurelab.org www.semanticinfrastructurelab.org;

    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/semanticinfrastructurelab.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/semanticinfrastructurelab.org/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/semanticinfrastructurelab.org/chain.pem;

    # SSL settings (Mozilla Intermediate)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files
    location /static {
        alias /var/www/sil-website/static;
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # Proxy to application
    location / {
        proxy_pass http://sil_website;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://sil_website/health;
        access_log off;
    }

    # Logging
    access_log /var/log/nginx/sil-website-access.log;
    error_log /var/log/nginx/sil-website-error.log;
}
```

#### Enable Site

```bash
# Enable configuration
sudo ln -s /etc/nginx/sites-available/semanticinfrastructurelab.org \
            /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload
sudo systemctl reload nginx
```

---

### 4. TLS Certificates (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d semanticinfrastructurelab.org \
                     -d www.semanticinfrastructurelab.org

# Auto-renewal (certbot sets this up automatically)
sudo systemctl status certbot.timer

# Manual renewal test
sudo certbot renew --dry-run
```

---

## Deployment Profiles

### Development (Local)

```bash
# No container, direct execution
cd sil-website
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
python src/sil_web/app.py
# http://localhost:8000
```

### Staging (tia-staging / tia-dev)

**Local staging (testing container):**
```bash
# Build and run container locally
podman build -t sil-website:staging .
podman run -p 8000:8000 \
  -v $(pwd)/../SIL/docs:/app/docs:ro \
  sil-website:staging
```

**Remote staging (tia-staging server):**
```bash
# Deploy to staging server
./deploy/deploy-remote.sh staging

# Or manually:
ssh tia-staging << 'EOF'
  cd /var/www/sil-website
  git pull
  podman build -t sil-website:staging .
  podman stop sil-website-staging 2>/dev/null || true
  podman run -d --name sil-website-staging \
    -p 8080:8000 \
    -v /var/www/SIL/docs:/app/docs:ro \
    sil-website:staging
EOF

# Check health
curl https://sil-staging.mytia.net/health
```

### Production (Systemd + Nginx)

```bash
# Build production image
podman build -t sil-website:latest .

# Deploy service
sudo systemctl start sil-website

# Check health
curl https://semanticinfrastructurelab.org/health
```

---

## Registry Strategy

### Current State (Transitional)
All repos on `github.com/scottsen/*` (personal account).

### Target State (Q1 2025)
All production repos on `github.com/semantic-infrastructure-lab/*`.

### Container Registry Options

**Option 1: GitHub Container Registry (ghcr.io)**
```bash
# Free for public repos, integrated with GitHub
podman login ghcr.io
podman tag sil-website:latest ghcr.io/semantic-infrastructure-lab/sil-website:v0.1.0
podman push ghcr.io/semantic-infrastructure-lab/sil-website:v0.1.0
```

**Option 2: Self-Hosted (registry.semanticinfrastructurelab.org)**
```bash
# Full control, requires infrastructure
# Deploy registry container with TLS
podman run -d -p 5000:5000 --restart=always \
  -v registry-data:/var/lib/registry \
  --name registry \
  registry:2
```

**Recommendation:** Start with GitHub Container Registry (ghcr.io), migrate to self-hosted when traffic justifies.

---

## Health Checks & Monitoring

### Application Health Endpoint

```python
# src/sil_web/routes/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "sil-website",
        "version": "0.1.0",
    }
```

### Systemd Health Monitoring

```ini
# In service file
ExecStartPost=/bin/sleep 5
ExecStartPost=/usr/bin/curl -f http://localhost:8000/health

# Restart on failure
Restart=on-failure
RestartSec=10s
StartLimitBurst=3
StartLimitIntervalSec=60s
```

### External Monitoring

```bash
# Uptime monitoring (UptimeRobot, StatusCake, etc.)
# Check every 5 minutes:
# https://semanticinfrastructurelab.org/health
```

---

## Logging Standards

### Structured Logging (All SIL Projects)

```python
import structlog

log = structlog.get_logger()

# Always include context
log.info("request_received",
         method="GET",
         path="/projects",
         user_agent="Mozilla/5.0")

log.error("database_error",
          query="SELECT * FROM projects",
          error="Connection timeout",
          duration_ms=5000)
```

### Log Aggregation

**Local Development:**
```bash
# View logs
sudo journalctl -u sil-website -f --output json-pretty
```

**Production:**
```bash
# Forward to centralized logging (future)
# Options: Loki, Elasticsearch, CloudWatch
```

---

## CI/CD Pipeline (GitHub Actions)

### `.github/workflows/deploy.yml`

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build container
        run: |
          podman build -t sil-website:${{ github.sha }} .
          podman tag sil-website:${{ github.sha }} \
                     ghcr.io/semantic-infrastructure-lab/sil-website:latest

      - name: Push to registry
        run: |
          echo "${{ secrets.GITHUB_TOKEN }}" | \
            podman login ghcr.io -u ${{ github.actor }} --password-stdin
          podman push ghcr.io/semantic-infrastructure-lab/sil-website:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_KEY }}
          script: |
            podman pull ghcr.io/semantic-infrastructure-lab/sil-website:latest
            sudo systemctl restart sil-website
            sleep 5
            curl -f https://semanticinfrastructurelab.org/health
```

---

## Quick Reference

### Deployment Checklist

**Pre-Deployment:**
- [ ] Tests passing (`pytest`)
- [ ] Linting clean (`ruff check`)
- [ ] Type checking (`mypy src/`)
- [ ] Dockerfile builds
- [ ] Health endpoint working
- [ ] Documentation updated

**Deployment:**
- [ ] Build container image
- [ ] Push to registry (if applicable)
- [ ] Update systemd service
- [ ] Restart service
- [ ] Verify health endpoint
- [ ] Check logs
- [ ] Test public URL

**Post-Deployment:**
- [ ] Monitor error logs (24h)
- [ ] Check resource usage
- [ ] Verify TLS certificate
- [ ] Update deployment docs

---

## Project-Specific Standards

### SIL Website
- **Container:** Yes
- **Systemd:** Yes
- **Nginx:** Yes (HTTPS required)
- **Port:** 8000 (internal)
- **Domain:** semanticinfrastructurelab.org

### Morphogen (Future Web API)
- **Container:** Yes
- **Systemd:** Yes
- **Nginx:** Yes
- **Port:** 8001 (internal)
- **Domain:** api.morphogen.dev

### Reveal CLI
- **Container:** No (PyPI package)
- **Deployment:** `pip install reveal-cli`

---

## Migration Path

### Phase 1: Immediate (Q4 2024)
- [x] Document deployment standards (this document)
- [ ] Create Dockerfile for sil-website
- [ ] Create systemd service template
- [ ] Deploy sil-website to production

### Phase 2: Short-term (Q1 2025)
- [ ] Transfer repos to semantic-infrastructure-lab org
- [ ] Set up GitHub Container Registry
- [ ] Create deployment automation (GitHub Actions)
- [ ] Add health checks to all web services

### Phase 3: Medium-term (Q2 2025)
- [ ] Self-hosted container registry
- [ ] Centralized logging (Loki)
- [ ] Metrics (Prometheus)
- [ ] Alerting (Alertmanager)

---

## Resources

**TIA Documentation:**
- [TIA Container Commands](/home/scottsen/src/tia/commands/container/README.md)
- [TIA Boot System Architecture](/home/scottsen/src/tia/docs/boot/BOOT_SYSTEM_ARCHITECTURE.md)

**External:**
- [Podman Documentation](https://docs.podman.io/)
- [Systemd Service Files](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [Nginx Reverse Proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/)
- [Let's Encrypt](https://letsencrypt.org/getting-started/)

---

**Version:** 1.0
**Last Updated:** 2025-11-28
**Status:** Active
**Maintainer:** Scott + SIL Core Team
