# SYNCED CONTENT - DO NOT EDIT DIRECTLY

⚠️ **This directory contains synced documentation from /projects/SIL/docs/**

## 🆕 Manifest-Aware Sync System (2025-12-16)

**All syncing is now controlled by CONTENT_MANIFEST.yaml**

- Only files marked `visibility: public` in the manifest are synced
- Internal docs (`visibility: internal`) are kept in SIL repo only
- Glass-box transparency: Every decision documented with rationale
- See `/projects/SIL/docs/CONTENT_MANIFEST.yaml` for complete list

**Current stats:**
- 57 public docs synced from SIL repo
- 13 internal docs kept in SIL repo only
- ~9 website-specific files (pages/, guides/, etc.)

## Content Ownership

### Synced from SIL Repo (PUBLIC ONLY)
**Source:** `/projects/SIL/docs/` (filtered by CONTENT_MANIFEST.yaml)

These directories contain ONLY public docs:
- `foundations/` ← Public SIL foundations (8 files)
- `architecture/` ← Public architecture docs (10 files, some under review)
- `research/` ← Public research papers (15 files)
- `systems/` ← Public system docs (9 files)
- `essays/` ← Public essays (1 file)
- `meta/` ← Public meta docs (5 files: FAQ, influences, stewardship, founder)
- `articles/` ← Public articles (2 files)
- `vision/` ← Public vision docs (1 file)
- `manifesto/` ← Public manifesto (2 files)
- Top-level guides (START_HERE, QUICKSTART, READING_GUIDE, etc.)

**⚠️ DO NOT EDIT** - Changes will be overwritten on next sync

### Internal Docs NOT Synced
These exist in `/projects/SIL/docs/` but are NOT synced here:
- `meta/MARKDOWN_STYLE_GUIDE.md` - Internal writing standards
- `meta/SIL_TOOL_QUALITY_MONITORING.md` - Internal operations (618 lines)
- `meta/FOUNDERS_NOTE_*.md` - Work-in-progress notes
- `meta/SIL_RESEARCH_AGENDA_YEAR1.md` - Internal strategy
- `meta/SIL_SAFETY_THRESHOLDS.md` - Operational standards
- `operations/*` - All deployment and operations docs
- Various WIP and planning documents

**See:** `/projects/SIL/docs/CONTENT_MANIFEST.yaml` for complete list with rationale

### Website-Specific Content (✅ VERSION CONTROLLED)
**Managed in this repo** - NOT synced from SIL

- `pages/` ← Website pages (about, contact, index)
- `guides/` ← Website-specific guides
- `projects/` ← Project documentation (PRISM, PROJECT_INDEX)
- `semantic-os/` ← Semantic OS documentation
- `README_SYNCED_CONTENT.md` ← This file

## How to Update Content

### Updating Public SIL Documentation

```bash
# 1. Edit source in SIL repo
cd /home/scottsen/src/projects/SIL
vim docs/systems/reveal.md

# 2. Verify it's public in manifest
grep -A3 "reveal.md" docs/CONTENT_MANIFEST.yaml
# Should show: visibility: public

# 3. Commit to SIL repo
git commit -am "docs: Update Reveal documentation"

# 4. Sync to website (manifest-aware)
cd /home/scottsen/src/projects/sil-website
./scripts/sync-docs.py
# Or use: ./scripts/sync-docs.sh (backward compatible)

# 5. Verify and commit
git add docs/
git commit -m "docs: Sync Reveal updates from SIL repo"

# 6. Deploy
./deploy/deploy-container.sh staging
```

### Adding New Documentation

```bash
# 1. Create file in SIL repo
cd /home/scottsen/src/projects/SIL
vim docs/research/NEW_PAPER.md

# 2. Add to CONTENT_MANIFEST.yaml with visibility
vim docs/CONTENT_MANIFEST.yaml
# Add entry with visibility: public or internal

# 3. If public, sync to website
cd /home/scottsen/src/projects/sil-website
./scripts/sync-docs.py
```

**See:** `/projects/SIL/docs/operations/CONTENT_MANIFEST_GUIDE.md` for complete workflow

### Updating Website-Specific Content

```bash
# Edit directly (version controlled in this repo)
cd /home/scottsen/src/projects/sil-website
vim docs/pages/about.md

# Commit changes
git add docs/pages/about.md
git commit -m "docs: Update about page"

# Deploy
./deploy/deploy-container.sh staging
```

## Validation

### Check Sync Health

```bash
# Validate manifest and check for internal files
./scripts/sync-docs.py --validate

# Expected output:
# ✓ No internal files found in website repo
# ✓ Validation passed
```

### Preview Changes Before Sync

```bash
./scripts/sync-docs.py --dry-run
```

### Clean Internal Files (if accidentally synced)

```bash
./scripts/sync-docs.py --clean
```

## Version Control Strategy

### What's Git Tracked

✅ **Tracked in this repo:**
- Website-specific content (pages/, guides/, projects/, semantic-os/)
- This README file
- Build artifacts and deployment configs

🚫 **NOT tracked (synced from SIL):**
- All public SIL documentation
- Managed by manifest, regenerated on sync

### .gitignore Strategy

Pattern-based .gitignore ignores synced content while tracking website-specific content.

See `.gitignore` for specific patterns.

## Documentation Reference

- **CONTENT_MANIFEST.yaml** - Source of truth for what's public/internal
- **CONTENT_MANIFEST_GUIDE.md** - How to maintain the manifest
- **WEBSITE_DEPLOYMENT_GUIDE.md** - Complete deployment workflow
- **sync-docs.py** - Manifest-aware sync script

## Session History

- **2025-12-16** (charcoal-jewel-1216) - Implemented manifest-aware sync system
- **2025-12-16** (bronze-spark-1216) - Created CONTENT_MANIFEST.yaml
- **2025-12-16** (chrome-hue-1216) - Identified 10 internal docs being exposed
- **2025-12-15** (celestial-champion-1215) - Added essays to synced content
- **2025-12-13** (ethereal-helm-1213) - Fixed gitignore strategy
