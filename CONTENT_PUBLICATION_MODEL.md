# SIL Website Content Publication Model

**Status:** Canonical Reference
**Last Updated:** 2025-12-21
**Owner:** Scott Senkeresty

---

## TL;DR

- **URL Structure:** `/{category}/{slug}`
- **Content Location:** `docs/{category}/*.md` (flat, no subdirectories)
- **Slug Conversion:** Lowercase, underscores→hyphens, `SIL_` prefix removed, `README.md` → `overview`
- **Category Index:** `/{category}` → `docs/{category}/README.md` (requires explicit route)
- **Link Format:** Always use `/category/slug`, never filename or legacy paths

---

## Architecture: Two Discovery Mechanisms

### 1. ContentService Discovery (Dynamic)

**How it works:**
```python
# content.py:102-150
for md_file in category_path.glob('*.md'):  # Only immediate children!
    slug = filename_to_slug(md_file.name)
    slug_map[slug] = filename
```

**Key Constraints:**
- **Flat structure only:** No subdirectories discovered
- **Auto-slugging:** Filenames converted to URL slugs
- **No recursion:** `docs/architecture/models/` files are invisible

**Example:**
```
File: docs/foundations/SIL_GLOSSARY.md
Slug: glossary (SIL_ removed, lowercase, _ → -)
URL:  /foundations/glossary
```

### 2. Hardcoded Routes (Explicit)

**How it works:**
```python
# pages.py
@router.get("/foundations")
async def foundations_index(request: Request) -> Response:
    return render_markdown_page(..., Path("docs/foundations/README.md"), ...)
```

**Categories with index routes:**
- `/manifesto` → `docs/manifesto/README.md`
- `/foundations` → `docs/foundations/README.md`
- `/systems` → `docs/systems/README.md`
- `/research` → `docs/research/README.md`
- `/architecture` → `docs/architecture/README.md`
- `/projects` → `docs/projects/README.md`
- `/articles` → `docs/articles/README.md`
- `/essays` → `docs/essays/README.md`

**Legacy category redirects (301):**
- `/canonical/*` → `/foundations/*`
- `/tools/*` → `/systems/*`
- `/innovations/*` → `/systems/*`

---

## File Organization Rules

### ✅ Correct Structure

```
docs/
├── foundations/
│   ├── README.md           # /foundations (index route)
│   ├── SIL_GLOSSARY.md     # /foundations/glossary
│   ├── quickstart.md       # /foundations/quickstart
│   └── start-here.md       # /foundations/start-here
├── research/
│   ├── README.md           # /research (index route)
│   ├── AI_DOCUMENTATION.md # /research/ai-documentation
│   └── IDENTITY_MAPPING.md # /research/identity-mapping
└── architecture/
    ├── README.md           # /architecture (index route)
    ├── UNIFIED_GUIDE.md    # /architecture/unified-guide
    └── SYNTHESIS_MAP.md    # /architecture/synthesis-map
```

###❌ Incorrect Structure (Undiscoverable)

```
docs/
├── architecture/
│   ├── models/              # ❌ Subdirectory - files invisible!
│   │   └── LAYER_MODELS.md  # 404 - not discovered
│   └── decisions/           # ❌ Subdirectory - files invisible!
│       └── ADR_001.md       # 404 - not discovered
```

**Fix:** Move files to category root
```bash
mv docs/architecture/models/*.md docs/architecture/
mv docs/architecture/decisions/*.md docs/architecture/
```

---

## Slug Conversion Reference

**Function:** `filename_to_slug()` (content.py:19-47)

| Filename | Slug | URL |
|----------|------|-----|
| `README.md` | `overview` | `/{category}/overview` |
| `SIL_GLOSSARY.md` | `glossary` | `/foundations/glossary` |
| `RAG_AS_MANIFOLD.md` | `rag-as-manifold` | `/research/rag-as-manifold` |
| `quickstart.md` | `quickstart` | `/foundations/quickstart` |
| `UNIFIED_ARCHITECTURE_GUIDE.md` | `unified-architecture-guide` | `/architecture/unified-architecture-guide` |

**Rules:**
1. Remove `.md` extension
2. `README` → `overview`
3. Remove `SIL_` prefix
4. Lowercase
5. Underscores → hyphens

---

## Linking Standards

### Internal Links

**✅ Correct:**
```markdown
[Glossary](/foundations/glossary)
[Research Agenda](/research/research-agenda-year-1)
[Architecture Guide](/architecture/unified-architecture-guide)
[Projects](/projects/project-index)
```

**❌ Incorrect:**
```markdown
[Glossary](/foundations/SIL_GLOSSARY)          # Use slug, not filename!
[Glossary](/canonical/glossary)                # Use current category, not legacy!
[Projects](/projects)                          # Use /projects/overview or full page
[Guide](../architecture/UNIFIED_GUIDE.md)      # Use absolute /category/slug paths!
```

### Category-Only Links

**Prefer specific pages over category-only:**
```markdown
✅ [See all projects](/projects/overview)      # Explicit
⚠️  [See all projects](/projects)              # Works but ambiguous
```

### External Links

```markdown
✅ [Email](mailto:scott@semanticinfrastructurelab.org)
✅ [GitHub](https://github.com/Semantic-Infrastructure-Lab)
```

---

## Adding New Content

### 1. Create the File

```bash
# Place in appropriate category directory (flat, no subdirs)
vim docs/foundations/NEW_DOCUMENT.md
```

### 2. Add Frontmatter

```yaml
---
title: "My New Document"
tier: 2
order: 10
private: false
beth_topics:
  - topic1
  - topic2
---
```

### 3. Verify Slug

**Filename:** `NEW_DOCUMENT.md`
**Expected slug:** `new-document`
**Expected URL:** `/foundations/new-document`

### 4. Link to It

```markdown
[Check out my new doc](/foundations/new-document)
```

### 5. Validate

```bash
# Run audit (will show as orphaned if not linked from anywhere)
cd /home/scottsen/src/tia/sessions/jacked-legion-1221
python audit_links.py
```

---

## Adding a New Category

### 1. Create Directory

```bash
mkdir docs/new-category
```

### 2. Create README.md

```bash
cat > docs/new-category/README.md <<'EOF'
---
title: "New Category"
tier: 2
order: 50
private: false
---

# New Category

Overview of this category.
EOF
```

### 3. Add Route Handlers

Edit `src/sil_web/routes/pages.py`:

```python
# Add index route
@router.get("/new-category", response_class=HTMLResponse)
async def new_category_index(request: Request) -> Response:
    """New Category - Description."""
    return render_markdown_page(
        request,
        Path("docs/new-category/README.md"),
        "New Category - Semantic Infrastructure Lab",
        "/new-category",
    )

# Add document handler
@router.get("/new-category/{name}", response_class=HTMLResponse)
async def new_category_doc(request: Request, name: str) -> Response:
    """Individual new category document."""
    filename = name.upper().replace("-", "_") + ".md"
    doc_path = Path("docs/new-category") / filename

    if not doc_path.exists():
        filename = name + ".md"
        doc_path = Path("docs/new-category") / filename

    if not doc_path.exists():
        raise HTTPException(404, f"Document not found: {name}")

    content = doc_path.read_text()
    title = f"{name.replace('-', ' ').title()} - SIL"

    html_content = markdown_renderer.render(content)
    return templates.TemplateResponse("page.html", {
        "request": request,
        "title": title,
        "content": html_content,
        "nav_items": nav_items,
        "current_page": "/new-category",
    })
```

### 4. Update Navigation (if needed)

Edit templates to add category to nav.

### 5. Update Audit Script

Add category to `SIL_CATEGORIES` list in `audit_links.py`.

---

## Common Issues & Fixes

### Issue: File Returns 404

**Cause:** File in subdirectory (not discovered)

**Fix:**
```bash
# Move to category root
mv docs/category/subdir/file.md docs/category/
```

### Issue: Link Broken Despite File Existing

**Cause 1:** Using filename instead of slug
```markdown
❌ /foundations/SIL_GLOSSARY
✅ /foundations/glossary
```

**Cause 2:** Using legacy category
```markdown
❌ /canonical/glossary
✅ /foundations/glossary
```

**Cause 3:** Using relative path
```markdown
❌ ../research/paper.md
✅ /research/paper
```

### Issue: Category-Only URL Returns 404

**Cause:** No index route defined

**Fix:** Add `@router.get("/{category}")` route (see "Adding a New Category")

### Issue: Audit Script Reports False Positives

**Known false positives:**
- SIF website links (hardcoded routes, not ContentService-discovered)
- `mailto:` links (valid external links)
- Category-only URLs with index routes

**Workaround:** Manually verify reported "broken" links before fixing.

---

## SIF Website (Different Model)

**Architecture:** Hardcoded routes only (no ContentService discovery)

```python
# sif-website pages.py
@router.get("/funding")
async def funding(request: Request) -> Response:
    doc = content_service.load_document("pages", "funding")
    ...
```

**File structure:**
```
docs/
└── pages/
    ├── index.md         # /
    ├── about.md         # /about
    ├── funding.md       # /funding
    ├── contact.md       # /contact
    └── foundation/
        ├── index.md            # /foundation
        ├── chief-steward.md    # /foundation/chief-steward
        └── executive-director.md # /foundation/executive-director
```

**Linking in SIF:**
```markdown
[About](/about)
[Funding](/funding)
[Contact](/contact)
[Foundation](/foundation)
```

---

## Validation Tools

### Audit Script

```bash
cd /home/scottsen/src/tia/sessions/jacked-legion-1221
python audit_links.py
```

**Output:**
- Broken links (includes false positives)
- Orphaned files (no incoming links)
- Undiscoverable files (in subdirectories)

**Note:** Manually verify "broken" links - script has false positive rate of ~53%.

### Manual Testing

```bash
# Test locally
cd /home/scottsen/src/projects/sil-website
python src/sil_web/app.py

# Test in browser
open http://localhost:8000/foundations/glossary
```

### Production Testing

```bash
# Test live site
curl -I https://semanticinfrastructurelab.org/foundations/glossary
curl -I https://semanticinfrastructurelab.org/architecture
```

---

## Migration Checklist

When reorganizing content:

- [ ] Move subdirectory files to category root
- [ ] Update internal links to use correct slugs
- [ ] Update legacy category references (`/canonical/` → `/foundations/`)
- [ ] Ensure all categories have README.md
- [ ] Ensure all categories have index routes in pages.py
- [ ] Run audit script and validate results
- [ ] Test locally
- [ ] Deploy to staging
- [ ] Verify staging
- [ ] Deploy to production
- [ ] Verify production

---

## See Also

- `src/sil_web/services/content.py:19-47` - `filename_to_slug()` implementation
- `src/sil_web/services/content.py:102-150` - `_discover_slugs()` implementation
- `src/sil_web/routes/pages.py` - Route definitions
- `sessions/jacked-legion-1221/audit_links.py` - Link validation tool
- `sessions/jacked-legion-1221/COMPREHENSIVE_WEBSITE_AUDIT_REPORT.md` - Audit findings

---

**Questions?** Contact scott@semanticinfrastructurelab.org
