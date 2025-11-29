"""
UI components - pure rendering logic.

No business logic, no I/O, no state mutation.
Just pure functions that transform data into HTML strings.
"""

from sil_web.domain.models import Document, Project, ProjectStatus


def project_card(project: Project) -> str:
    """Render a project card.

    Args:
        project: Project to render

    Returns:
        HTML string for project card
    """
    # Status badge
    status_class = "production" if project.is_production else "research"
    status_text = f"✅ {project.status.value.title()}"
    if project.version:
        status_text += f" v{project.version}"

    # Stats badges
    stats_html = ""
    if project.has_stats:
        stats_html = f"""
                <span class="meta-badge">{project.tests} Tests</span>
                <span class="meta-badge">{project.coverage}% Coverage</span>
        """

    # PyPI badge
    pypi_html = ""
    if project.pypi_url:
        stats_html += f"""
                <span class="meta-badge">PyPI</span>
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
            <h3><a href="{project.github_url}" target="_blank">{project.name}</a> — {project.description.split('.')[0]}</h3>
            <div class="meta">
                <span class="meta-badge {status_class}">{status_text}</span>
                {stats_html}
            </div>
            <p><strong>Layer:</strong> {project.layer.value}</p>
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
        <div class="architecture">
            <div class="architecture-title">The Semantic OS</div>
Layer 5: Human Interfaces / SIM       (reveal, browserbridge)
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
