"""
UI components - pure rendering logic.

No business logic, no I/O, no state mutation.
Just pure functions that transform data into HTML strings.
"""

from sil_web.domain.models import Document, Project, ProjectStatus


def project_card(project: Project) -> str:
    """Render a project card with maturity indicators.

    Args:
        project: Project to render

    Returns:
        HTML string for project card
    """
    # Status badge with emoji indicators
    status_emoji = {
        "production": "✅",
        "research": "🔬",
        "alpha": "🚧",
        "specification": "📋",
        "planned": "💭",
    }
    emoji = status_emoji.get(project.status.value, "")
    status_class = project.status.value
    status_text = f"{emoji} {project.status.value.title()}"
    if project.version:
        status_text += f" v{project.version}"

    # Private indicator
    privacy_html = ""
    if project.is_private:
        privacy_html = '<span class="meta-badge private">🔒 Private</span>'

    # Maturity note
    maturity_html = ""
    if project.maturity_note:
        maturity_html = f'<span class="maturity-note">{project.maturity_note}</span>'

    # Stats badges
    stats_html = ""
    if project.has_stats:
        stats_html = f"""
                <span class="meta-badge">{project.tests} Tests</span>
                <span class="meta-badge">{project.coverage}% Coverage</span>
        """

    # PyPI badge
    if project.pypi_url:
        stats_html += f"""
                <span class="meta-badge pypi">PyPI</span>
        """

    # Innovations list
    innovations_html = ""
    if project.innovations:
        items = "\n".join(f"<li>{item}</li>" for item in project.innovations)
        innovations_html = f"""
            <p><strong>Key innovations:</strong></p>
            <ul>
                {items}
            </ul>
        """

    # Use cases
    use_cases_html = ""
    if project.use_cases:
        cases_str = ", ".join(project.use_cases)
        use_cases_html = f"""
            <p><strong>Use cases:</strong> {cases_str}</p>
        """

    # Links
    links_html = f"""
        <a href="{project.github_url}" target="_blank">Repository →</a>
    """
    if project.pypi_url:
        links_html += f"""
        <a href="{project.pypi_url}" target="_blank">PyPI Package →</a>
    """

    return f"""
        <div class="project">
            <h3><a href="{project.github_url}" target="_blank">{project.name}</a></h3>
            <div class="meta">
                <span class="meta-badge {status_class}">{status_text}</span>
                {privacy_html}
                {stats_html}
            </div>
            {maturity_html}
            <p>{project.description}</p>
            {innovations_html}
            {use_cases_html}
            <div class="links">
                {links_html}
            </div>
        </div>
    """


def document_preview(doc: Document) -> str:
    """Render a document preview card.

    Args:
        doc: Document to preview

    Returns:
        HTML string for document preview
    """
    desc = doc.description or f"{doc.word_count} words"

    return f"""
        <div class="doc-preview">
            <h3><a href="/docs/{doc.slug}">{doc.title}</a></h3>
            <p>{desc}</p>
        </div>
    """


def architecture_diagram() -> str:
    """Render the 6-layer architecture diagram.

    Returns:
        HTML string for architecture diagram
    """
    return """
        <div class="architecture"><div class="architecture-title">The Semantic OS</div>
Layer 5: Human Interfaces / SIM        (reveal, browserbridge)
Layer 4: Deterministic Engines         (morphogen, riffstack)
Layer 3: Multi-Agent Orchestration     (agent-ether)
Layer 2: Domain Modules                (morphogen, tiacad, riffstack, sup)
Layer 1: Universal Semantic IR         (pantheon)
Layer 0: Semantic Memory               (semantic-memory)

Cross-Cutting: Provenance              (genesisgraph, prism)
        </div>
    """


def nav_bar(current_page: str = "") -> str:
    """Render navigation bar.

    Args:
        current_page: Current page slug for highlighting

    Returns:
        HTML string for navigation
    """
    pages = [
        ("", "Home"),
        ("projects", "Projects"),
        ("docs", "Documentation"),
    ]

    links = []
    for slug, title in pages:
        url = f"/{slug}" if slug else "/"
        active = "active" if slug == current_page else ""
        links.append(f'<a href="{url}" class="{active}">{title}</a>')

    links_html = " ".join(links)

    return f"""
        <nav class="nav-bar">
            {links_html}
            <a href="https://github.com/scottsen/sil" target="_blank">GitHub</a>
        </nav>
    """


def founding_docs_sidebar(documents: list[Document], current_slug: str = "", current_page: str = "") -> str:
    """Render left sidebar navigation with tiered document organization.

    Args:
        documents: List of all documents (will be grouped by tier)
        current_slug: Currently active document slug
        current_page: Currently active page (e.g., 'projects')

    Returns:
        HTML string for sidebar navigation with 3-tier hierarchy
    """
    # Organize by tier: 1=Founding, 2=Architecture, 3=Research
    # Sort documents by tier and order
    sorted_docs = sorted(documents, key=lambda d: (d.tier, d.order))

    # Group by tier
    tier1_docs = [d for d in sorted_docs if d.tier == 1]
    tier2_docs = [d for d in sorted_docs if d.tier == 2]
    tier3_docs = [d for d in sorted_docs if d.tier == 3]

    def render_doc_links(docs: list[Document]) -> str:
        """Render list of document links."""
        links = []
        for doc in docs:
            active = "active" if doc.slug == current_slug else ""
            links.append(f'<a href="/docs/{doc.slug}" class="{active}">{doc.title}</a>')
        return "\n                    ".join(links)

    # Build sections
    sections_html = []

    # Tier 1: Founding Documents
    if tier1_docs:
        sections_html.append(f"""
            <h3>Founding Documents</h3>
            <nav class="sidebar-nav">
                {render_doc_links(tier1_docs)}
            </nav>
        """)

    # Tier 2: Architecture
    if tier2_docs:
        sections_html.append(f"""
            <h3 class="sidebar-section-header">Architecture</h3>
            <nav class="sidebar-nav">
                {render_doc_links(tier2_docs)}
            </nav>
        """)

    # Tier 3: Research (show only key papers to keep sidebar clean)
    if tier3_docs:
        # Show top 5 research papers
        key_research = tier3_docs[:5]
        sections_html.append(f"""
            <h3 class="sidebar-section-header">Key Research</h3>
            <nav class="sidebar-nav">
                {render_doc_links(key_research)}
                <a href="/docs" class="">All Research →</a>
            </nav>
        """)

    sections = "\n".join(sections_html)

    # Projects link
    projects_active = "active" if current_page == "projects" else ""
    projects_link = f'<a href="/projects" class="{projects_active}">All Projects</a>'

    return f"""
        <aside class="sidebar">
            {sections}

            <div class="sidebar-links">
                {projects_link}
                <a href="https://github.com/scottsen/sil" target="_blank" class="">GitHub →</a>
            </div>
        </aside>
    """


def layer_section(layer, projects: list[Project]) -> str:
    """Render a layer section with all its projects.

    Args:
        layer: The Layer enum value
        projects: List of projects in this layer

    Returns:
        HTML string for layer section
    """
    if not projects:
        return ""

    # Layer number and name
    layer_map = {
        "Semantic Memory": ("Layer 0", "semantic-memory"),
        "Universal Semantic IR": ("Layer 1", "usir"),
        "Domain Modules": ("Layer 2", "domain-modules"),
        "Multi-Agent Orchestration": ("Layer 3", "multi-agent"),
        "Deterministic Engines": ("Layer 4", "engines"),
        "Human Interfaces / SIM": ("Layer 5", "interfaces"),
        "Cross-Cutting Infrastructure": ("Cross-Cutting", "cross-cutting"),
    }

    layer_num, layer_id = layer_map.get(layer.value, ("", ""))

    # Render project cards
    project_cards = "\n".join(project_card(p) for p in projects)

    return f"""
        <section class="layer-section" id="{layer_id}">
            <div class="layer-header">
                <span class="layer-number">{layer_num}</span>
                <h2>{layer.value}</h2>
            </div>
            <div class="layer-projects">
                {project_cards}
            </div>
        </section>
    """
