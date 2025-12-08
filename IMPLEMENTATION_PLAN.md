# SIL Website - Implementation Plan for Document Reorganization

**Goal**: Restructure website to highlight "Lab Founding Documents" and de-emphasize research papers

**Status**: Ready to implement
**Priority**: P0 (Critical for launch)

---

## Phase 1: Add Document Metadata (30 minutes)

### Add `tier` and `order` fields to Document model

**File**: `src/sil_web/domain/models.py`

```python
@dataclass
class Document:
    title: str
    slug: str
    content: str
    category: str
    description: Optional[str] = None
    tier: Optional[int] = None  # NEW: 1=Founding, 2=Architecture, 3=Research
    order: Optional[int] = None  # NEW: Display order within tier
```

### Add tier metadata to ContentService

**File**: `src/sil_web/services/content.py`

Add new constant:

```python
# Document organization: Tier 1 = Founding, 2 = Architecture, 3 = Research
DOCUMENT_TIERS = {
    # Tier 1: Lab Founding Documents (6 docs)
    "start-here": {"tier": 1, "order": 1, "theme": "Entry Point"},
    "founders-letter": {"tier": 1, "order": 2, "theme": "Personal Story"},
    "manifesto": {"tier": 1, "order": 3, "theme": "Core Vision"},
    "principles": {"tier": 1, "order": 4, "theme": "14 Constraints"},
    "stewardship-manifesto": {"tier": 1, "order": 5, "theme": "How We Operate"},
    "founder-profile": {"tier": 1, "order": 6, "theme": "Leadership"},

    # Tier 2: System Architecture (4 docs)
    "semantic-os-architecture": {"tier": 2, "order": 1, "theme": "6-Layer Stack"},
    "technical-charter": {"tier": 2, "order": 2, "theme": "Formal Spec"},
    "design-principles": {"tier": 2, "order": 3, "theme": "How We Build"},
    "glossary": {"tier": 2, "order": 4, "theme": "108 Terms"},

    # Tier 3: Research Output (10 docs, grouped by theme)
    # Theme A: Multi-Agent Systems
    "hierarchical-agency-framework": {"tier": 3, "order": 1, "theme": "Multi-Agent Systems"},
    "multi-agent-protocol-principles": {"tier": 3, "order": 2, "theme": "Multi-Agent Systems"},
    "founders-note-multishot-agent-learning": {"tier": 3, "order": 3, "theme": "Multi-Agent Systems"},

    # Theme B: Observability & Safety
    "semantic-observability": {"tier": 3, "order": 4, "theme": "Observability & Safety"},
    "semantic-feedback-loops": {"tier": 3, "order": 5, "theme": "Observability & Safety"},
    "safety-thresholds": {"tier": 3, "order": 6, "theme": "Observability & Safety"},
    "tool-quality-monitoring": {"tier": 3, "order": 7, "theme": "Observability & Safety"},

    # Theme C: Interface Design
    "progressive-disclosure-guide": {"tier": 3, "order": 8, "theme": "Interface Design"},

    # Theme D: Roadmap
    "research-agenda": {"tier": 3, "order": 9, "theme": "Research Roadmap"},

    # Meta/Overview
    "overview": {"tier": 1, "order": 7, "theme": "Overview"},  # README
}
```

Update `load_document()` to set tier metadata:

```python
def load_document(self, category: str, slug: str) -> Optional[Document]:
    # ... existing code ...

    # Get tier metadata
    tier_info = DOCUMENT_TIERS.get(slug, {"tier": 3, "order": 99, "theme": "Other"})

    doc = Document(
        title=title,
        slug=slug,
        content=post.content,
        category=category,
        description=description,
        tier=tier_info["tier"],
        order=tier_info["order"],
    )

    return doc
```

---

## Phase 2: Create Grouped Docs View (1 hour)

### Add helper method to ContentService

**File**: `src/sil_web/services/content.py`

```python
def list_documents_by_tier(self) -> dict[int, list[Document]]:
    """List all documents grouped by tier and sorted by order.

    Returns:
        Dict mapping tier (1, 2, 3) to list of Documents
    """
    all_docs = self.list_documents()

    by_tier = {1: [], 2: [], 3: []}

    for doc in all_docs:
        tier = doc.tier or 3  # Default to tier 3 if not set
        by_tier[tier].append(doc)

    # Sort each tier by order
    for tier in by_tier:
        by_tier[tier].sort(key=lambda d: d.order or 99)

    self.log.info("documents_grouped_by_tier",
                  tier1=len(by_tier[1]),
                  tier2=len(by_tier[2]),
                  tier3=len(by_tier[3]))

    return by_tier

def list_documents_by_theme(self, tier: int = 3) -> dict[str, list[Document]]:
    """List tier 3 documents grouped by theme.

    Returns:
        Dict mapping theme name to list of Documents
    """
    all_docs = self.list_documents()

    by_theme = {}

    for doc in all_docs:
        if doc.tier == tier:
            theme = DOCUMENT_TIERS.get(doc.slug, {}).get("theme", "Other")
            if theme not in by_theme:
                by_theme[theme] = []
            by_theme[theme].append(doc)

    # Sort documents within each theme by order
    for theme in by_theme:
        by_theme[theme].sort(key=lambda d: d.order or 99)

    return by_theme
```

---

## Phase 3: Update Docs Index Route (30 minutes)

### Modify `/docs` route

**File**: `src/sil_web/routes/pages.py`

```python
@router.get("/docs", response_class=HTMLResponse)
async def docs_index(request: Request):
    """Documentation index page with tiered organization."""

    # Get documents grouped by tier
    by_tier = content_service.list_documents_by_tier()

    # Get tier 3 documents grouped by theme
    research_by_theme = content_service.list_documents_by_theme(tier=3)

    return templates.TemplateResponse(
        "docs_index.html",
        {
            "request": request,
            "founding_docs": by_tier[1],  # Tier 1
            "architecture_docs": by_tier[2],  # Tier 2
            "research_by_theme": research_by_theme,  # Tier 3, grouped
            "nav": nav_bar("docs"),
        },
    )
```

---

## Phase 4: Create New Docs Index Template (1 hour)

### Create tiered docs template

**File**: `templates/docs_index.html`

```html
{% extends "base.html" %}

{% block title %}Documentation - Semantic Infrastructure Lab{% endblock %}

{% block description %}Complete documentation for the Semantic Infrastructure Lab including founding documents, system architecture, and research papers.{% endblock %}

{% block content %}
<header class="page-header">
    <h1>SIL Documentation</h1>
    <p class="intro">
        Complete documentation organized by importance and purpose.
        New to SIL? Start with the <strong>Lab Founding Documents</strong> below.
    </p>
</header>

<!-- Tier 1: Lab Founding Documents -->
<section class="doc-tier tier-1">
    <div class="tier-header">
        <h2>Lab Founding Documents</h2>
        <p class="tier-description">
            Essential reading to understand what SIL is, why it matters, and how we operate.
            Start here if you're new to the Semantic Infrastructure Lab.
        </p>
    </div>

    <div class="doc-grid founding">
        {% for doc in founding_docs %}
        <div class="doc-card founding">
            <div class="doc-number">{{ loop.index }}</div>
            <h3><a href="/docs/{{ doc.slug }}">{{ doc.title }}</a></h3>
            <p class="doc-meta">{{ doc.word_count }} words · ~{{ (doc.word_count / 200)|round|int }} min read</p>
            {% if doc.description %}
            <p class="doc-description">{{ doc.description }}</p>
            {% endif %}
            <a href="/docs/{{ doc.slug }}" class="doc-link">Read →</a>
        </div>
        {% endfor %}
    </div>
</section>

<!-- Tier 2: System Architecture -->
<section class="doc-tier tier-2">
    <div class="tier-header">
        <h2>System Architecture & Design</h2>
        <p class="tier-description">
            Technical foundation for builders and researchers.
            The 6-layer Semantic OS, formal specifications, and design principles.
        </p>
    </div>

    <div class="doc-grid architecture">
        {% for doc in architecture_docs %}
        <div class="doc-card architecture">
            <h3><a href="/docs/{{ doc.slug }}">{{ doc.title }}</a></h3>
            <p class="doc-meta">{{ doc.word_count }} words · ~{{ (doc.word_count / 200)|round|int }} min read</p>
            {% if doc.description %}
            <p class="doc-description">{{ doc.description }}</p>
            {% endif %}
            <a href="/docs/{{ doc.slug }}" class="doc-link">Read →</a>
        </div>
        {% endfor %}
    </div>
</section>

<!-- Tier 3: Research Output -->
<section class="doc-tier tier-3">
    <div class="tier-header">
        <h2>Research Output & Technical Papers</h2>
        <p class="tier-description">
            Published research organized by theme. For specialists and deep technical exploration.
        </p>
    </div>

    {% for theme, docs in research_by_theme.items() %}
    <div class="research-theme">
        <h3>{{ theme }}</h3>
        <div class="doc-list">
            {% for doc in docs %}
            <div class="doc-item research">
                <a href="/docs/{{ doc.slug }}">{{ doc.title }}</a>
                <span class="doc-meta">{{ doc.word_count }} words</span>
            </div>
            {% endfor %}
        </div>
    </div>
    {% endfor %}
</section>

{% endblock %}
```

---

## Phase 5: Add CSS Styling (30 minutes)

### Add tiered document styles

**File**: `static/css/style.css`

```css
/* Document Tier Sections */
.doc-tier {
    margin: 64px 0;
}

.tier-header {
    margin-bottom: 32px;
    border-bottom: 2px solid #e5e5e5;
    padding-bottom: 16px;
}

.tier-header h2 {
    margin: 0 0 12px 0;
}

.tier-description {
    font-size: 17px;
    color: #666;
    line-height: 1.6;
}

/* Document Grid Layouts */
.doc-grid {
    display: grid;
    gap: 24px;
    margin-top: 24px;
}

.doc-grid.founding {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 32px;
}

.doc-grid.architecture {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

/* Document Cards */
.doc-card {
    padding: 24px;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    background: white;
    transition: all 0.2s;
    position: relative;
}

.doc-card:hover {
    border-color: #999;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transform: translateY(-2px);
}

/* Founding Document Cards - Larger, more prominent */
.doc-card.founding {
    padding: 32px;
    border-width: 2px;
    border-color: #4CAF50;
    background: linear-gradient(135deg, #ffffff 0%, #f8fff9 100%);
}

.doc-card.founding:hover {
    border-color: #2e7d32;
}

.doc-number {
    position: absolute;
    top: 16px;
    right: 16px;
    width: 40px;
    height: 40px;
    background: #4CAF50;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 18px;
}

.doc-card h3 {
    margin: 0 60px 12px 0;  /* Space for number badge */
    font-size: 20px;
}

.doc-meta {
    font-size: 13px;
    color: #999;
    margin-bottom: 12px;
}

.doc-description {
    font-size: 15px;
    color: #555;
    line-height: 1.6;
    margin-bottom: 16px;
}

.doc-link {
    display: inline-block;
    color: #0066cc;
    text-decoration: none;
    font-weight: 500;
    font-size: 15px;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;
}

.doc-link:hover {
    border-bottom-color: #0066cc;
}

/* Research Theme Sections */
.research-theme {
    margin: 32px 0;
    padding: 24px;
    background: #fafafa;
    border-radius: 6px;
}

.research-theme h3 {
    margin: 0 0 16px 0;
    font-size: 18px;
    color: #333;
}

.doc-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.doc-item.research {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: white;
    border-radius: 4px;
    border: 1px solid #e5e5e5;
    transition: border-color 0.2s;
}

.doc-item.research:hover {
    border-color: #999;
}

.doc-item.research a {
    color: #333;
    text-decoration: none;
    font-size: 16px;
}

.doc-item.research a:hover {
    color: #0066cc;
}
```

---

## Phase 6: Update Sidebar (30 minutes)

### Simplify sidebar to reflect new hierarchy

**File**: `src/sil_web/ui/components.py`

Find the `founding_docs_sidebar()` function and update it:

```python
def founding_docs_sidebar(all_docs: list[Document], current_slug: str = "", current_page: str = "") -> str:
    """Render sidebar with tiered document organization."""

    # Group docs by tier
    tier1 = [d for d in all_docs if d.tier == 1]
    tier2 = [d for d in all_docs if d.tier == 2]
    tier3 = [d for d in all_docs if d.tier == 3]

    # Sort by order
    tier1.sort(key=lambda d: d.order or 99)
    tier2.sort(key=lambda d: d.order or 99)

    sidebar_html = '<aside class="sidebar">'

    # Founding Documents section
    sidebar_html += '<div class="sidebar-section">'
    sidebar_html += '<h3 class="sidebar-title">Founding Documents</h3>'
    sidebar_html += '<ul class="sidebar-list">'
    for doc in tier1:
        active = "active" if doc.slug == current_slug else ""
        sidebar_html += f'<li><a href="/docs/{doc.slug}" class="{active}">{doc.title}</a></li>'
    sidebar_html += '</ul></div>'

    # Architecture section
    sidebar_html += '<div class="sidebar-section">'
    sidebar_html += '<h3 class="sidebar-title">System Architecture</h3>'
    sidebar_html += '<ul class="sidebar-list">'
    for doc in tier2:
        active = "active" if doc.slug == current_slug else ""
        sidebar_html += f'<li><a href="/docs/{doc.slug}" class="{active}">{doc.title}</a></li>'
    sidebar_html += '</ul></div>'

    # Research (collapsed)
    sidebar_html += '<div class="sidebar-section">'
    sidebar_html += '<h3 class="sidebar-title">Research Papers</h3>'
    sidebar_html += '<p class="sidebar-note">See <a href="/docs">documentation index</a> for all research papers</p>'
    sidebar_html += '</div>'

    # Projects
    sidebar_html += '<div class="sidebar-section">'
    sidebar_html += '<h3 class="sidebar-title">Projects & Tools</h3>'
    sidebar_html += '<ul class="sidebar-list">'
    sidebar_html += '<li><a href="/projects">All Projects</a></li>'
    sidebar_html += '<li><a href="https://github.com/scottsen/sil" target="_blank">GitHub →</a></li>'
    sidebar_html += '</ul></div>'

    sidebar_html += '</aside>'

    return sidebar_html
```

---

## Summary: Implementation Checklist

**Files to Modify**:
- [ ] `src/sil_web/domain/models.py` - Add tier/order fields
- [ ] `src/sil_web/services/content.py` - Add DOCUMENT_TIERS, update load_document(), add grouping methods
- [ ] `src/sil_web/routes/pages.py` - Update /docs route
- [ ] `templates/docs_index.html` - Create new tiered template
- [ ] `static/css/style.css` - Add tier styling
- [ ] `src/sil_web/ui/components.py` - Update sidebar

**Testing**:
- [ ] Run local server: `python src/sil_web/app.py`
- [ ] Visit http://localhost:8000/docs
- [ ] Verify 3-tier hierarchy displays
- [ ] Check all 20 documents are present
- [ ] Verify sidebar shows simplified navigation
- [ ] Test responsive layout

**Deployment**:
- [ ] Build container: `./deploy/deploy-container.sh staging`
- [ ] Verify on staging: https://sil-staging.mytia.net/docs
- [ ] Deploy to production: `./deploy/deploy-container.sh production`

**Estimated Total Time**: 4 hours

---

## Questions Before Implementation

1. **Founding doc set approved?** Are these the right 6 documents?
2. **README redundant?** Should we merge README into START_HERE?
3. **Tier placement correct?** Any research papers that should be Tier 2?
4. **Visual hierarchy sufficient?** Numbered badges, larger cards for Tier 1?
5. **Implement now or later?** Ready to proceed or review first?
