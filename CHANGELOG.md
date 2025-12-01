# SIL Website Changelog

## [Unreleased]

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
