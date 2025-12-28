# Archived Templates

**Date archived:** 2024-12-28
**Reason:** These templates represent the old architecture and are no longer used.

## Architecture Change

The SIL website was refactored from a template inheritance model to a simpler standalone template model.

### Old Architecture (Archived)
- **Base template:** `base.html` - Master layout with blocks
- **Child templates:** Extended `base.html` with content blocks
  - `index.html` - Homepage
  - `document.html` - Document wrapper
  - `docs_index.html` - Documentation index
  - `projects.html` - Projects page

### Current Architecture (Production)
- **Single template:** `page.html` - Standalone template with Jinja2 rendering
- **Used by:** All routes in `src/sil_web/routes/pages.py`
- **Navigation:** Hardcoded header with `nav_items` context variable

## Why These Were Archived

**Code audit (2024-12-28):**
- ✅ Verified: No routes reference these templates
- ✅ Verified: No Python code imports these templates
- ✅ Navigation CSS mismatch: These templates would have used `.nav-bar`, but current CSS uses `.site-header`/`.main-nav`

**Last modified:** Dec 14-20, 2024 (2+ weeks unused)

## If You Need to Restore

If the architecture needs to revert to template inheritance:

1. Move desired templates back to `/templates/`
2. Update CSS to match template classes
3. Update routes in `pages.py` to reference correct templates
4. Test thoroughly before deploying

## Related Changes

Same session that archived these templates also:
- Added proper CSS for `.site-header`, `.main-nav`, `.header-content`, `.site-title`, `.nav-link`
- Removed orphaned `.nav-bar` CSS styles
- Cleaned up navigation technical debt

**Session:** contracting-galaxy-1227 (2024-12-28)
