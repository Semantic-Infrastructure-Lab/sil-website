# SIL Website Changelog

## [Unreleased]

### Deployed - 2025-12-05

#### Staging Deployment with Launch-Ready Documentation (shimmering-palette-1205)
- **40 files synced from official SIL repo** (commit 1929d8d)
  - 15 canonical documents (including all hakami-1205 and infernal-flame-1205 fixes)
  - 2 architecture documents
  - 7 research documents
  - 5 meta documents
  - 3 tools documents
  - 6 root-level guides
  - llms-full.txt regenerated (11,311 lines, 368KB)

**Critical Fixes Deployed:**
- **$470K economic correction** - Fixed 10x error in MANIFESTO, FAQ, QUICKSTART (was incorrectly $47K per 1000 agents)
- **v0.16.0 version updates** - Updated from v0.13.x across 5 locations (MANIFESTO, PRINCIPLES, FAQ)
- **Pantheon IR definition** - Added to GLOSSARY with complete description
- **Accessibility improvements** - Fixed 26 alphabetical headings + 9 section headings for screen readers
- **Timestamp additions** - Added "as of Dec 2025" to download statistics

**Scout P1 High-Impact Fixes:**
- Expanded acronyms on first use (USIR, SIM, Pantheon IR)
- Fixed heading structure for accessibility compliance
- Updated credibility markers (current versions, dated statistics)

**Deployment Architecture:**
- Container: sil-website-staging (registry.mytia.net/sil-website:staging)
- Deployed to: tia-staging
- Health: ✅ Healthy (16/17 validation tests passing)
- Live: https://sil-staging.mytia.net

**Status:** ✅ Production-ready - All P0 blockers resolved, staging validated

### Added - 2025-12-01

#### License & Citation Metadata (blessed-sea-1201)
- **LICENSE** - Apache 2.0 license file (was previously missing!)
- **CONTENT_LICENSE.md** - Dual licensing guide (code vs documentation)
- **CITATION.cff** - Academic citation metadata for research use
- **pyproject.toml** - Updated license field from MIT to Apache-2.0
- **README.md** - Updated license badge and section

**Critical Fix:**
- Production website was operating without a license file
- Now properly licensed: Code (Apache 2.0) + Content (CC BY 4.0)

**SIL Ecosystem Integration:**
- Unified licensing with all SIL ecosystem projects
- Copyright: Semantic Infrastructure Lab Contributors

### Added - 2025-11-30

#### Slug Auto-Discovery (b032349)
- **filename_to_slug()** helper function for automatic slug generation
- **ContentService._discover_slugs()** method with caching
- **SLUG_OVERRIDES** dict for backward compatibility with existing short URLs
- Auto-discovered 7+ new documents not in old hardcoded mappings:
  - canonical/SIL_CIVILIZATIONAL_SYSTEMS_ENGINEERING.md
  - canonical/SIL_FOUNDING_TEAM_ARCHETYPES.md
  - canonical/SIL_MORPHOGEN_PROJECT.md
  - canonical/SIL_PHYSICAL_LAB_DESIGN.md
  - canonical/SIL_SEMANTIC_OS_ARCHITECTURE.md
  - canonical/SIL_STEWARDSHIP_MANIFESTO.md
  - canonical/SIL_TWO_DIVISION_STRUCTURE.md
  - meta/DOC_CONSOLIDATION_PLAN.md
  - Plus README.md files in multiple categories

**Benefits:**
- New docs automatically get routes (zero code changes needed)
- Backward compatible with existing URLs
- Cached for performance
- Reduces manual work from 5 steps to 1

**Testing:**
- ✅ Old slugs with overrides work (e.g., /docs/manifesto)
- ✅ Auto-discovered docs work (e.g., /docs/founders-letter)
- ✅ New docs work (e.g., /docs/civilizational-systems-engineering)
- ✅ Zero-fuckitude workflow tested and working

#### llms.txt Implementation (f940618, clever-god-1130)
- `/llms.txt` - Navigation file (7KB) for LLM-friendly documentation access
- `/llms-full.txt` - Complete documentation (436KB, 13,377 lines)
- `scripts/generate-llms-full.sh` - Auto-generation script
- `scripts/auto-deploy-docs.sh` - Single-command deployment workflow
- Implements Jeremy Howard's llms.txt standard (September 2024)

**URLs:**
- Staging: https://sil-staging.mytia.net/llms.txt
- Staging: https://sil-staging.mytia.net/llms-full.txt
- Reference: https://llmstxt.org

### Fixed - 2025-11-30 (clever-god-1130)

#### Staging URL Corrections (5bf7c68)
- Fixed incorrect staging URL references from `staging.semanticinfrastructurelab.org` to `sil-staging.mytia.net`
- Updated 11 files (5 in sil-website repo, 6 session READMEs)
- Affected files:
  - README.md, DEPLOYMENT.md
  - deploy/deploy-container.sh, deploy/deploy-remote.sh
  - docs/operations/DEPLOYMENT_STANDARDS.md
  - 6 session README files

### Removed
- Hardcoded slug_mappings dict (83 lines) - replaced with auto-discovery
- Hardcoded all_slugs dict in list_documents() - replaced with auto-discovery

## [v1.0.0] - 2025-11-28

Initial production release of SIL website.

### Architecture
- FastAPI backend with Jinja2 templates
- Markdown content with frontmatter
- Content service for document/project management
- Containerized deployment (Podman)
- Nginx reverse proxy with SSL

### Features
- 34+ SIL documentation files organized by category
- 11 SIL projects (5 production, 6 research/alpha/planned)
- Semantic OS 6-layer architecture visualization
- Reading guides and navigation
- Health check endpoints
- Structured logging with structlog

### Deployment
- Staging: https://sil-staging.mytia.net
- Production: https://semanticinfrastructurelab.org
- Container registry: registry.mytia.net/sil-website

### Infrastructure
- Built on tia-staging (staging) and tia-production (production)
- Automated container deployment via deploy scripts
- Health checks and monitoring
- Zero-downtime deployments

---

## Notes

### Versioning
We follow [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes to API or deployment
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Links
- Repository: https://github.com/scottsen/sil-website
- Documentation: /docs
- Projects: /projects
- llms.txt spec: https://llmstxt.org

### Session References
- clever-god-1130: llms.txt implementation + staging URL fixes
- safuculi-1130: slug auto-discovery implementation
