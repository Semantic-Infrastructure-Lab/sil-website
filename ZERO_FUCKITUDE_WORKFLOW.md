# Zero-Fuckitude Documentation Workflow

**TL;DR:** Add markdown to SIL repo, run one script, done.

---

## The Goal

**Add a new research paper with ZERO manual fuckitude:**

1. Write `MY_PAPER.md` in `/SIL/docs/research/`
2. Run **ONE SCRIPT**
3. Paper appears on website + llms.txt automatically

---

## Current Status: ZERO FUCKITUDE ACHIEVED ✅

**What's automated:**
✅ Markdown sync from SIL → website (`sync-docs.sh`)
✅ llms-full.txt regeneration (`generate-llms-full.sh`)
✅ Single deployment script (`deploy-container.sh`)
✅ **NEW:** Slug auto-discovery in `content.py` (b032349)
✅ One-command workflow (`auto-deploy-docs.sh`)

**What's manual:**
Nothing! Just run the script and answer prompts.

---

## The One-Script Solution

### NEW: `./scripts/auto-deploy-docs.sh`

**What it does:**
1. Syncs docs from SIL repo
2. Regenerates llms-full.txt
3. Shows git diff
4. Commits changes (with your approval)
5. Deploys to staging (optional)

**Usage:**

```bash
# After adding/editing docs in SIL repo:
cd /home/scottsen/src/projects/sil-website
./scripts/auto-deploy-docs.sh
```

That's it. ONE COMMAND.

---

## Complete Workflow Example

### Adding a New Research Paper

```bash
# 1. Add paper to SIL repo
cd /home/scottsen/src/projects/SIL
vim docs/research/SEMANTIC_VERSIONING_AS_TYPE_THEORY.md
git add docs/research/
git commit -m "docs: add semantic versioning paper"
git push

# 2. Deploy to website (ONE COMMAND)
cd /home/scottsen/src/projects/sil-website
./scripts/auto-deploy-docs.sh

# Script will:
# - Sync the new paper
# - Add it to llms-full.txt automatically
# - Show you the diff
# - Ask if you want to commit
# - Ask if you want to deploy to staging

# 3. Done! Check staging:
curl https://sil-staging.mytia.net/llms-full.txt | grep -i "semantic versioning"
```

**Paper is now:**
✅ Synced to website repo
✅ Included in llms-full.txt
✅ Deployed to staging
✅ **Automatically routed** at `/docs/semantic-versioning-as-type-theory` (no code changes needed!)
✅ Auto-discovered by ContentService

---

## ✅ IMPLEMENTED: Auto-Discovery (b032349, safuculi-1130)

**Auto-discovery is NOW LIVE in content.py!**

**How it works:**
- `filename_to_slug()` generates slugs automatically from filenames
  - `RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md` → `rag-manifold-transport`
  - `layer-0-semantic-memory.md` → `layer-0-semantic-memory`
  - `README.md` → `overview` (special case)
- `ContentService._discover_slugs()` scans `docs/*/` at runtime
- Results are cached for performance
- `SLUG_OVERRIDES` dict for backward compatibility with existing short URLs

**Benefits achieved:**
✅ Add paper to SIL repo
✅ Run `auto-deploy-docs.sh`
✅ **ZERO manual mapping updates** - auto-discovered automatically!
✅ Discovered 7+ new documents not in old hardcoded mappings
✅ Backward compatible with all existing URLs

**Test script:** `./scripts/test-auto-discovery.py`
**Commit:** b032349 (2025-11-30)

---

## Manual Override (For Special Cases)

If you need custom slugs or special handling:

1. **Option A**: Add frontmatter to the markdown
   ```yaml
   ---
   slug: custom-slug-name
   ---
   ```

2. **Option B**: Override in `content.py` slug_overrides dict
   ```python
   slug_overrides = {
       "research": {
           "rag": "RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md"  # Short slug
       }
   }
   ```

---

## Deployment Targets

**Staging (automated):**
```bash
./scripts/auto-deploy-docs.sh
# Deploys to: https://sil-staging.mytia.net
```

**Production (manual approval):**
```bash
# After staging verification
git push origin master
./deploy/deploy-container.sh production
# Deploys to: https://semanticinfrastructurelab.org
```

---

## File Locations

- **SIL repo (source):** `/home/scottsen/src/projects/SIL/docs/`
- **Website repo (deployed):** `/home/scottsen/src/projects/sil-website/`
- **Scripts:** `sil-website/scripts/`
  - `sync-docs.sh` - Sync markdown from SIL
  - `generate-llms-full.sh` - Rebuild llms-full.txt
  - `auto-deploy-docs.sh` - **THE ONE SCRIPT** ⭐

---

## Summary

**Before (Pre-clever-god-1130):**
- 5 manual steps
- Hardcoded slug mappings in code
- Easy to forget regenerating llms-full.txt
- Need to edit code to add new docs

**After (clever-god-1130 + safuculi-1130):**
1. Run `./scripts/auto-deploy-docs.sh`
2. Answer Y/N prompts
3. **Done!** New docs automatically routed with zero code changes

**ZERO FUCKITUDE ACHIEVED ✅**

---

## Session Credits

- **clever-god-1130** (2025-11-30): llms.txt implementation + auto-deploy workflow
- **safuculi-1130** (2025-11-30): Slug auto-discovery implementation
