# SIL Website - Deployment Runbook

**Quick reference checklist for deploying SIL website to staging or production**

---

## Pre-Deployment (5 minutes)

```bash
cd /home/scottsen/src/projects/sil-website
```

### 1. Sync Content
```bash
./scripts/sync-docs.py              # Sync public docs from SIL repo
./scripts/sync-docs.py --validate   # Verify no internal files leaked
```

**Expected**: ✅ No internal files found in website repo

### 2. Run Pre-Deployment Checks
```bash
./scripts/pre-deploy-check.sh staging
```

**Expected**: All checks pass (or warnings only)

**Critical checks**:
- □ Content manifest validated (58 public, 13 internal)
- □ Sync status clean
- □ No broken links detected
- □ Git status clean (or changes committed)
- □ Target environment healthy
- □ **Nginx NOT in maintenance mode** ← Prevents earthly-wizard-1216 issue

**If maintenance mode detected**:
```bash
# Find latest backup
ssh tia-proxy 'ls -lt /etc/nginx/sites-available/semanticinfrastructurelab.org.backup-* | head -1'

# Restore (replace TIMESTAMP)
ssh tia-proxy 'sudo cp /etc/nginx/sites-available/semanticinfrastructurelab.org.backup-TIMESTAMP \
                          /etc/nginx/sites-available/semanticinfrastructurelab.org'

# Reload nginx
ssh tia-proxy 'sudo nginx -t && sudo systemctl reload nginx'
```

---

## Staging Deployment (10 minutes)

### 1. Deploy to Staging
```bash
./deploy/deploy-container.sh staging --fresh
```

**What happens**:
1. Builds container with current docs
2. Tags and pushes to registry
3. Deploys to tia-staging:8080
4. Waits for health check

**Expected**: ✅ Deployment complete! Health check passed

### 2. Run Smoke Tests
```bash
./scripts/smoke-test.sh staging
```

**Tests 9 critical pages**:
- /health, /, /manifesto/YOLO, /foundations/FOUNDERS_LETTER
- /foundations/design-principles, /systems/beth, /systems/reveal
- /systems/tia, /research

**Expected**: ✅ ALL SMOKE TESTS PASSED

### 3. Manual Verification
```bash
# Open in browser
open https://sil-staging.mytia.net

# Or curl test
curl -s https://sil-staging.mytia.net/ | grep '<title>'
```

**Verify**:
- □ Homepage loads
- □ Navigation works
- □ Content looks correct
- □ No obvious errors

### 4. Check Logs
```bash
ssh tia-staging 'podman logs sil-website-staging --tail 20'
```

**Expected**: No errors, normal startup messages

---

## Production Deployment (10 minutes)

⚠️ **Only deploy to production after staging is verified**

### 1. Deploy to Production
```bash
./deploy/deploy-container.sh production
```

**What happens**:
1. Pulls latest image from registry
2. Deploys to tia-apps:8010
3. Waits for health check

**Expected**: ✅ Deployment complete! Health check passed

### 2. Run Smoke Tests
```bash
./scripts/smoke-test.sh production
```

**Expected**: ✅ ALL SMOKE TESTS PASSED

### 3. Monitor for 5 Minutes
```bash
# Watch logs
ssh tia-apps 'podman logs -f sil-website --tail 20'

# In another terminal, test pages
curl -s https://semanticinfrastructurelab.org/health | jq .
curl -s https://semanticinfrastructurelab.org/ | grep '<title>'
```

**Watch for**:
- No error spikes
- Normal request patterns
- Healthy responses

### 4. Final Verification
```bash
# Check critical pages
open https://semanticinfrastructurelab.org/manifesto/YOLO
open https://semanticinfrastructurelab.org/foundations/FOUNDERS_LETTER
open https://semanticinfrastructurelab.org/systems/beth
```

**Verify**:
- □ All pages load correctly
- □ Links work (especially after link architecture fix)
- □ No 404 errors
- □ Content is current

---

## Post-Deployment

### 1. Update Documentation (if infrastructure changed)
```bash
# If containers, ports, or config changed
cd /home/scottsen/src/tia
tia infrastructure validate --update
```

### 2. Commit Any Changes
```bash
cd /home/scottsen/src/projects/sil-website
git status
# If changes exist, commit them
```

### 3. Tag Release (optional, for significant changes)
```bash
git tag -a v1.0.x -m "Release notes here"
git push --tags
```

---

## Rollback Procedure

If production deployment fails or has issues:

### Quick Rollback
```bash
# List available versions
curl https://registry.mytia.net/v2/sil-website/tags/list

# Deploy previous version
ssh tia-apps
podman pull registry.mytia.net/sil-website:v0.9.0
podman stop sil-website
podman rm sil-website
podman run -d --name sil-website \
  -p 0.0.0.0:8010:8000 \
  --health-cmd="curl -f http://localhost:8000/health || exit 1" \
  --health-interval=30s \
  --restart=unless-stopped \
  registry.mytia.net/sil-website:v0.9.0
```

### Verify Rollback
```bash
./scripts/smoke-test.sh production
```

---

## Common Issues

### Container won't start
```bash
# Check logs
ssh tia-apps 'podman logs sil-website'

# Check image
ssh tia-apps 'podman images | grep sil-website'
```

### Health check failing
```bash
# Test health endpoint directly
ssh tia-apps 'curl http://localhost:8010/health'

# Check if container is running
ssh tia-apps 'podman ps | grep sil-website'
```

### Site shows old content
**Cause**: Podman cached the `COPY docs/` layer

**Fix**: Use `--fresh` flag
```bash
./deploy/deploy-container.sh staging --fresh
```

### 502 Bad Gateway
**Cause**: Nginx in maintenance mode or container not accessible

**Check**:
```bash
# Verify nginx config
ssh tia-proxy 'sudo nginx -t'

# Check if proxying (not serving static)
ssh tia-proxy 'grep -v "^#" /etc/nginx/sites-available/semanticinfrastructurelab.org | grep proxy_pass'
```

---

## Time Estimates

- **Pre-deployment checks**: 5 minutes
- **Staging deployment**: 10 minutes (build + test)
- **Production deployment**: 10 minutes (deploy + verify)
- **Total**: ~25 minutes for full staging → production cycle

---

## See Also

- **DEPLOYMENT.md**: Complete deployment guide (architecture, troubleshooting)
- **scripts/pre-deploy-check.sh**: Automated pre-deployment validation
- **scripts/smoke-test.sh**: Post-deployment smoke tests
- **CONTENT_MANIFEST.yaml**: Public vs internal file list
