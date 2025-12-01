# SIL Website Deployment Workflow

**Complete workflow for deploying website updates**

This document describes the end-to-end process for updating the SIL website with new documentation or code changes.

---

## Quick Reference

```bash
# 1. Update SIL docs (source of truth)
cd /home/scottsen/src/projects/SIL
# ... make doc changes ...
git add docs/
git commit -m "docs: update canonical documents"
git push

# 2. Sync to website
cd /home/scottsen/src/projects/sil-website
./scripts/sync-docs.sh

# 3. Test locally
python src/sil_web/app.py
# Visit http://localhost:8000

# 4. Deploy
git add docs/
git commit -m "sync: update docs from SIL repo"
git push

# GitHub Actions will build and deploy automatically
```

---

## The Two-Repository Pattern

**SIL Repository** (`/home/scottsen/src/projects/SIL/`)
- **Purpose:** Source of truth for documentation
- **Git:** github.com/scottsen/SIL
- **Contents:** Canonical docs, research papers, project index
- **Audience:** Developers, researchers, contributors

**Website Repository** (`/home/scottsen/src/projects/sil-website/`)
- **Purpose:** Public-facing website
- **Git:** github.com/scottsen/sil-website
- **Contents:** FastAPI app + synced docs
- **Audience:** End users, newcomers

**Sync Process:** `scripts/sync-docs.sh` copies SIL docs → website docs

---

## Development Workflow

### Option A: Point at SIL Repo Directly (Recommended for Dev)

**Setup:**
```python
# sil-website/src/sil_web/config/settings.py
import os
from pathlib import Path

# Development: use SIL repo directly (no duplication)
if os.getenv("ENV") != "production":
    DOCS_PATH = Path(__file__).parent.parent.parent.parent / "SIL" / "docs"
else:
    DOCS_PATH = Path(__file__).parent.parent.parent / "docs"
```

**Benefits:**
- No manual sync during development
- Instant updates when editing SIL docs
- Zero duplication

**Drawbacks:**
- Requires SIL repo present
- Can't test production deployment locally

---

### Option B: Manual Sync (Current Approach)

**When you update SIL docs:**
```bash
# 1. Edit docs in SIL repo
cd /home/scottsen/src/projects/SIL
vim docs/canonical/SIL_MANIFESTO.md
git commit -am "docs: update manifesto"

# 2. Sync to website
cd /home/scottsen/src/projects/sil-website
./scripts/sync-docs.sh

# 3. Review changes
git status
git diff docs/

# 4. Commit synced docs
git add docs/
git commit -m "sync: update manifesto from SIL repo"
```

**Benefits:**
- Explicit sync step (intentional)
- Website repo is self-contained
- Matches production deployment

**Drawbacks:**
- Manual step (can forget)
- Docs duplicated locally

---

## Production Deployment

### Automated via GitHub Actions

**Trigger:** Push to `main` branch

**Workflow:**
```yaml
# .github/workflows/deploy.yml
name: Deploy SIL Website

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # Important: Sync docs before building
      - name: Sync documentation
        run: |
          # Fetch SIL repo
          git clone https://github.com/scottsen/SIL.git ../SIL
          ./scripts/sync-docs.sh

      - name: Build Docker image
        run: docker build -t sil-website .

      - name: Deploy to server
        run: |
          # Push to container registry
          # Update production service
```

---

## Validation Checklist

Before deploying, verify:

### 1. Documentation Sync
```bash
./scripts/sync-docs.sh
# Should show:
# ✓ Canonical docs synced (8+ files)
# ✓ Architecture docs synced (2 files)
# ✓ Research docs synced (2+ files)
# ✓ All required files present
```

### 2. Local Testing
```bash
# Start dev server
python src/sil_web/app.py

# Check critical pages:
# - http://localhost:8000/
# - http://localhost:8000/docs/
# - http://localhost:8000/docs/canonical/manifesto
# - http://localhost:8000/research/rag-manifold-transport
# - http://localhost:8000/projects/
```

### 3. Link Validation
```bash
# Check for broken internal links
# (Tool TBD - could use markdown-link-check)
```

### 4. Content Review
- [ ] New docs appear in navigation
- [ ] README files render correctly
- [ ] Code examples format properly
- [ ] Images load (if any)

---

## Common Scenarios

### Scenario 1: New Research Paper

**SIL Repo:**
```bash
cd /home/scottsen/src/projects/SIL
# Create paper
vim docs/research/NEW_PAPER.md
# Update research README
vim docs/research/README.md
git add docs/research/
git commit -m "research: add new paper on topic X"
git push
```

**Website:**
```bash
cd /home/scottsen/src/projects/sil-website
# Sync docs
./scripts/sync-docs.sh
# Update ContentService slug mappings
vim src/sil_web/services/content.py
# Add "new-paper": "NEW_PAPER.md" to research category
# Commit and deploy
git add .
git commit -m "feat: add new research paper page"
git push
```

---

### Scenario 2: Documentation Reorganization

**SIL Repo:**
```bash
cd /home/scottsen/src/projects/SIL
# Move docs
mv docs/canonical/OLD.md docs/vision/OLD.md
# Update references
grep -r "canonical/OLD" docs/ # Find references
# ... update links ...
git commit -am "refactor: move OLD to vision category"
git push
```

**Website:**
```bash
cd /home/scottsen/src/projects/sil-website
# Sync docs
./scripts/sync-docs.sh
# Update slug mappings
vim src/sil_web/services/content.py
# Move "old" from canonical to vision category
# Add URL redirect (if needed)
git add .
git commit -m "refactor: update doc category mappings"
git push
```

---

### Scenario 3: New Canonical Document

**SIL Repo:**
```bash
cd /home/scottsen/src/projects/SIL
# Create doc
vim docs/canonical/NEW_GUIDE.md
# Add to README
vim docs/canonical/README.md
# Update READING_GUIDE
vim docs/READING_GUIDE.md
git add docs/
git commit -m "docs: add new canonical guide"
git push
```

**Website:**
```bash
cd /home/scottsen/src/projects/sil-website
./scripts/sync-docs.sh
# Update ContentService
vim src/sil_web/services/content.py
# Add to canonical slug_mappings and all_slugs
# Test
python src/sil_web/app.py
curl http://localhost:8000/docs/canonical/new-guide
# Deploy
git add .
git commit -m "feat: add new canonical guide"
git push
```

---

## Troubleshooting

### Docs not appearing on website

**Check:**
1. Did you run `sync-docs.sh`?
2. Is the file in the right category directory?
3. Is the slug mapping correct in `content.py`?
4. Does the markdown parse correctly? (frontmatter issues?)

**Debug:**
```bash
# Check synced files
ls -la docs/canonical/
# Check ContentService can load
python -c "
from pathlib import Path
from sil_web.services.content import ContentService
service = ContentService(Path('docs'))
doc = service.load_document('canonical', 'your-slug')
print(doc)
"
```

---

### Sync script fails

**Check:**
1. Is SIL repo at `../SIL/` relative to website?
2. Do you have read permissions?
3. Are there uncommitted changes blocking?

**Fix:**
```bash
# Verify SIL location
ls ../SIL/docs/
# Check permissions
ls -la ../SIL/docs/
# Run with debug
bash -x scripts/sync-docs.sh
```

---

## Best Practices

### 1. Always Edit in SIL Repo
**Never edit docs directly in website repo.** They'll be overwritten on next sync.

### 2. Commit Sync Changes
After running `sync-docs.sh`, always commit the result:
```bash
git add docs/
git commit -m "sync: update docs from SIL repo (commit SHA)"
```

### 3. Reference SIL Commits
In sync commits, reference the SIL commit:
```bash
git commit -m "sync: update research docs (SIL@abc1234)"
```

### 4. Test Before Deploy
Always test locally after sync:
```bash
./scripts/sync-docs.sh
python src/sil_web/app.py
# Manual smoke test
git push
```

---

## Future Improvements

### Automated Sync
Add GitHub webhook: SIL repo push → trigger website sync job

### Pre-commit Validation
Lint markdown, check links, validate frontmatter before allowing commits

### Preview Deployments
Automatic staging deployment for PRs

---

**Last Updated:** 2025-11-30
**Sync Script:** `scripts/sync-docs.sh`
**ContentService:** `src/sil_web/services/content.py`
