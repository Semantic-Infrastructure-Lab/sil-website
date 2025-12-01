"""
Content service - loads SIL documents and project data.

This service handles I/O: reading files, parsing markdown, loading YAML.
"""

import re
from pathlib import Path
from typing import Optional

import frontmatter
import structlog

from sil_web.domain.models import Document, Layer, Project, ProjectStatus

log = structlog.get_logger()


def filename_to_slug(filename: str) -> str:
    """Convert filename to URL-friendly slug.

    Examples:
        RAG_AS_SEMANTIC_MANIFOLD_TRANSPORT.md -> rag-manifold-transport
        UNIFIED_ARCHITECTURE_GUIDE.md -> unified-architecture-guide
        layer-0-semantic-memory.md -> layer-0-semantic-memory
        README.md -> overview (special case for semantic-os)

    Args:
        filename: The markdown filename to convert

    Returns:
        URL-friendly slug
    """
    # Remove .md extension
    name = filename.replace('.md', '')

    # Special case: README becomes 'overview'
    if name == 'README':
        return 'overview'

    # Remove common prefixes
    name = re.sub(r'^SIL_', '', name)

    # Convert to lowercase and replace underscores with hyphens
    slug = name.lower().replace('_', '-')

    return slug


class ContentService:
    """Service for loading SIL content (docs, projects)."""

    # Slug overrides for special cases (slug -> filename)
    # Only needed when auto-discovery would produce wrong slug
    SLUG_OVERRIDES = {
        "canonical": {
            "manifesto": "SIL_MANIFESTO.md",
            "principles": "SIL_PRINCIPLES.md",
            # Removed "charter" override - auto-discovers as "technical-charter" (clearer)
            "glossary": "SIL_GLOSSARY.md",
            "research-agenda": "SIL_RESEARCH_AGENDA_YEAR1.md",
            # These auto-discover correctly: founders-letter, founder-profile, tia-profile, technical-charter
        },
        "architecture": {
            # All auto-discover correctly
        },
        "guides": {
            "optimization": "OPTIMIZATION_IN_SIL.md",
            "ecosystem-layout": "SIL_ECOSYSTEM_PROJECT_LAYOUT.md",
        },
        "vision": {
            # All auto-discover correctly
        },
        "research": {
            # All auto-discover correctly
        },
        "meta": {
            # All auto-discover correctly
        },
        "semantic-os": {
            # All auto-discover correctly (README -> overview handled by filename_to_slug)
        },
    }

    def __init__(self, docs_path: Path) -> None:
        """Initialize content service.

        Args:
            docs_path: Path to SIL repository docs directory
        """
        self.docs_path = docs_path
        self.log = log.bind(service="content")
        self._slug_cache: dict[str, dict[str, str]] = {}  # category -> {slug: filename}

    def _discover_slugs(self, category: str) -> dict[str, str]:
        """Auto-discover all markdown files in a category and map slugs to filenames.

        Uses SLUG_OVERRIDES for special cases, then auto-discovers remaining files.

        Args:
            category: Document category (canonical, architecture, etc.)

        Returns:
            Dict mapping slug -> filename
        """
        # Return cached result if available
        if category in self._slug_cache:
            return self._slug_cache[category]

        category_path = self.docs_path / category

        if not category_path.exists():
            self.log.warning("category_path_not_found", category=category, path=str(category_path))
            return {}

        slug_map = {}

        # Start with overrides for this category
        if category in self.SLUG_OVERRIDES:
            slug_map.update(self.SLUG_OVERRIDES[category])

        # Auto-discover all markdown files
        for md_file in sorted(category_path.glob('*.md')):
            filename = md_file.name
            slug = filename_to_slug(filename)

            # Only add if not already in overrides
            if slug not in slug_map:
                slug_map[slug] = filename

        # Cache the result
        self._slug_cache[category] = slug_map

        self.log.debug("slugs_discovered", category=category, count=len(slug_map))
        return slug_map

    def load_document(self, category: str, slug: str) -> Optional[Document]:
        """Load a document from any category by slug.

        Args:
            category: Document category (canonical, architecture, guides, vision, research, meta)
            slug: Document slug (e.g., 'manifesto', 'unified-architecture-guide')

        Returns:
            Document instance or None if not found
        """
        # Auto-discover slugs for this category
        slug_map = self._discover_slugs(category)

        if not slug_map:
            self.log.warning("invalid_category_or_empty", category=category)
            return None

        if slug not in slug_map:
            self.log.warning("document_not_found", category=category, slug=slug)
            return None

        filename = slug_map[slug]
        doc_path = self.docs_path / category / filename

        if not doc_path.exists():
            self.log.error("document_file_missing", category=category, slug=slug, path=str(doc_path))
            return None

        # Parse frontmatter and content
        with open(doc_path, encoding="utf-8") as f:
            post = frontmatter.load(f)

        title = post.get("title", slug.replace("-", " ").title())
        description = post.get("description")

        doc = Document(
            title=title,
            slug=slug,
            content=post.content,
            category=category,
            description=description,
        )

        self.log.info("document_loaded", category=category, slug=slug, word_count=doc.word_count)
        return doc

    def load_document_by_slug(self, slug: str) -> Optional[Document]:
        """Load a document by slug, searching across all categories.

        This is a convenience method for backward compatibility with routes
        that only provide a slug.

        Args:
            slug: Document slug (e.g., 'manifesto', 'rag-manifold-transport')

        Returns:
            Document instance or None if not found
        """
        # Try each category until we find the slug
        categories = ["canonical", "architecture", "guides", "vision", "research", "meta", "semantic-os"]

        for category in categories:
            doc = self.load_document(category, slug)
            if doc:
                return doc

        self.log.warning("document_not_found_any_category", slug=slug)
        return None

    def list_documents(self, category: Optional[str] = None) -> list[Document]:
        """List all available documents, optionally filtered by category.

        Args:
            category: Optional category to filter by (canonical, architecture, etc.)

        Returns:
            List of Document instances
        """
        # Auto-discover all categories or just the requested one
        all_categories = ["canonical", "architecture", "guides", "vision", "research", "meta", "semantic-os"]
        categories_to_list = [category] if category else all_categories

        docs = []
        for cat in categories_to_list:
            # Discover all slugs in this category
            slug_map = self._discover_slugs(cat)

            # Load each document
            for slug in slug_map.keys():
                doc = self.load_document(cat, slug)
                if doc:
                    docs.append(doc)

        self.log.info("documents_listed", category=category, count=len(docs))
        return docs


class ProjectService:
    """Service for loading SIL project data."""

    def __init__(self) -> None:
        """Initialize project service."""
        self.log = log.bind(service="projects")

    def get_all_projects(self) -> list[Project]:
        """Get ALL SIL projects across all maturity levels.

        Returns:
            List of all Project instances
        """
        projects = [
            # ===== PRODUCTION PROJECTS =====
            Project(
                name="Morphogen",
                slug="morphogen",
                description="Universal, deterministic computation platform unifying audio synthesis, physics simulation, circuit design, geometry, and optimization in one type system, scheduler, and language.",
                status=ProjectStatus.PRODUCTION,
                layer=Layer.LAYER_4,
                github_url="https://github.com/scottsen/morphogen",
                version="0.11.0",
                tests=900,
                coverage=85,
                innovations=[
                    "Cross-domain composition (audio + physics + circuits in same program)",
                    "Deterministic execution (bitwise-identical results)",
                    "MLIR-based compilation",
                    "Multirate scheduling (audio @ 48kHz, physics @ 240Hz)",
                ],
                use_cases=[
                    "Audio synthesis",
                    "Physical modeling",
                    "Multi-domain simulation",
                    "Generative art",
                ],
            ),
            Project(
                name="TiaCAD",
                slug="tiacad",
                description="Declarative parametric CAD system using YAML instead of code. Reference-based composition model for explicit, verifiable geometry.",
                status=ProjectStatus.PRODUCTION,
                layer=Layer.LAYER_2,
                github_url="https://github.com/scottsen/tiacad",
                version="3.1.1",
                tests=1027,
                coverage=92,
                innovations=[
                    "YAML-based declarative syntax (no programming required)",
                    "Reference-based composition (parts as peers, not hierarchy)",
                    "Auto-generated spatial anchors",
                    "Comprehensive schema validation",
                ],
                use_cases=[
                    "Parametric 3D modeling",
                    "Manufacturing",
                    "Design automation",
                    "CAD workflows",
                ],
            ),
            Project(
                name="GenesisGraph",
                slug="genesisgraph",
                description="Open standard for cryptographically verifiable process provenance. Three-level selective disclosure (A/B/C) enables proving compliance without revealing trade secrets.",
                status=ProjectStatus.PRODUCTION,
                layer=Layer.CROSS_CUTTING,
                github_url="https://github.com/scottsen/genesisgraph",
                version="0.3.0",
                tests=363,
                coverage=63,
                innovations=[
                    "Selective disclosure (prove compliance without revealing IP)",
                    "DID-based identity (did:web, did:ion, did:ethr)",
                    "Zero-knowledge proof templates",
                    "Transparency log anchoring",
                ],
                use_cases=[
                    "AI pipeline verification",
                    "Manufacturing compliance",
                    "Scientific reproducibility",
                    "Healthcare audit trails",
                ],
            ),
            Project(
                name="reveal",
                slug="reveal",
                description="Semantic exploration tool for codebases. Smart, progressive disclosure of code structure without reading entire files. Optimized for AI agents and developers.",
                status=ProjectStatus.PRODUCTION,
                layer=Layer.LAYER_5,
                github_url="https://github.com/scottsen/reveal",
                version="0.11.0",
                pypi_url="https://pypi.org/project/reveal-cli/",
                innovations=[
                    "Progressive disclosure (structure → elements → implementation)",
                    "Zero configuration (smart defaults)",
                    "15+ file types supported (Python, JS, TS, Rust, Go, etc.)",
                    "Perfect Unix integration (filename:line format)",
                ],
                use_cases=[
                    "Codebase exploration",
                    "AI agent context optimization",
                    "Rapid code understanding",
                    "Token-efficient file reading",
                ],
            ),
            Project(
                name="SIL",
                slug="sil",
                description="The Semantic Infrastructure Lab itself—vision, principles, research agenda, and unified architecture for the entire ecosystem.",
                status=ProjectStatus.PRODUCTION,
                layer=Layer.CROSS_CUTTING,
                github_url="https://github.com/scottsen/sil",
                version="1.0.0",
                innovations=[
                    "Manifesto — Why SIL exists",
                    "Technical Charter — System specification",
                    "Principles — The 14 principles",
                    "Unified Architecture Guide — The framework",
                ],
                use_cases=["Research foundation", "Architectural guidance"],
            ),
            # ===== RESEARCH / ALPHA PROJECTS =====
            Project(
                name="Pantheon",
                slug="pantheon",
                description="Universal semantic IR enabling cross-domain composition. Adapters translate domain languages (audio, CAD, UI) into common semantic graph for interoperability.",
                status=ProjectStatus.RESEARCH,
                layer=Layer.LAYER_1,
                github_url="https://github.com/scottsen/pantheon",
                is_private=True,
                maturity_note="Working prototype, API evolving",
                innovations=[
                    "Universal graph representation",
                    "Domain adapters (audio, CAD, UI, geometry)",
                    "Semantic type system",
                    "Cross-domain operators",
                ],
                use_cases=["Cross-domain composition", "Semantic transformation", "Universal representation layer"],
            ),
            Project(
                name="RiffStack",
                slug="riffstack",
                description="Stack-based live looping and audio synthesis with YAML-driven patch configuration. Real-time performance environment for musical expression.",
                status=ProjectStatus.ALPHA,
                layer=Layer.LAYER_4,
                github_url="https://github.com/scottsen/riffstack",
                maturity_note="MVP - basic features working, needs stability",
                innovations=[
                    "Stack-based composition",
                    "Live looping",
                    "MLIR compilation for performance",
                    "YAML patch description",
                ],
                use_cases=["Live musical performance", "Audio patching", "Real-time synthesis"],
            ),
            Project(
                name="SUP",
                slug="sup",
                description="Semantic UI platform translating intent into reactive UI components. Declarative UI description with multiple backend targets (React, Vue, native).",
                status=ProjectStatus.ALPHA,
                layer=Layer.LAYER_2,
                github_url="https://github.com/scottsen/sup",
                is_private=True,
                maturity_note="Early development, API unstable",
                innovations=[
                    "Intent → UI compilation",
                    "Backend-agnostic (React, Vue, native)",
                    "Semantic layout constraints",
                    "Accessibility-first",
                ],
                use_cases=["Declarative UI construction", "Multi-platform UI", "Accessibility automation"],
            ),
            Project(
                name="BrowserBridge",
                slug="browserbridge",
                description="Event-driven browser automation for human-AI collaboration. Standards-based (CloudEvents, AsyncAPI, WebSocket), protocol-agnostic.",
                status=ProjectStatus.ALPHA,
                layer=Layer.LAYER_5,
                github_url="https://github.com/scottsen/browserbridge",
                maturity_note="Alpha - core features working",
                innovations=[
                    "Event-driven architecture",
                    "Standards-based protocols",
                    "Semantic DOM extraction",
                    "Human-AI collaboration primitives",
                ],
                use_cases=["Browser automation", "Web scraping", "UI testing", "Human-AI collaboration"],
            ),
            # ===== SPECIFICATION PHASE =====
            Project(
                name="Prism",
                slug="prism",
                description="Formally verified microkernel query engine. Minimal trusted core with provable correctness guarantees.",
                status=ProjectStatus.SPECIFICATION,
                layer=Layer.CROSS_CUTTING,
                github_url="https://github.com/scottsen/prism",
                is_private=True,
                maturity_note="Design phase - specification in progress",
                innovations=[
                    "Microkernel architecture (mechanism, not policy)",
                    "Formal verification",
                    "Minimal TCB (Trusted Computing Base)",
                    "Composable query primitives",
                ],
                use_cases=["Verified query execution", "Microkernel research", "Formal correctness"],
            ),
            Project(
                name="Agent Ether",
                slug="agent-ether",
                description="Deterministic protocols for multi-agent coordination. Message passing, state synchronization, and coordination primitives for intelligent agent systems.",
                status=ProjectStatus.SPECIFICATION,
                layer=Layer.LAYER_3,
                github_url="https://github.com/scottsen/agent-ether",
                is_private=True,
                maturity_note="Planning phase - protocol specification underway",
                innovations=[
                    "Deterministic coordination",
                    "Message-passing primitives",
                    "State synchronization",
                    "Provenance-complete interactions",
                ],
                use_cases=["Multi-agent systems", "Agent coordination", "Distributed AI"],
            ),
            # ===== PLANNED =====
            Project(
                name="Semantic Memory",
                slug="semantic-memory",
                description="Durable, queryable knowledge graphs with versioning. Persistent semantic continuity across tasks and time.",
                status=ProjectStatus.PLANNED,
                layer=Layer.LAYER_0,
                github_url="https://github.com/scottsen/semantic-memory",
                maturity_note="Concept stage - architecture design in progress",
                innovations=[
                    "Versioned semantic graphs",
                    "Provenance-complete transformations",
                    "Efficient incremental updates",
                    "Cross-session continuity",
                ],
                use_cases=["Persistent knowledge", "Semantic versioning", "Long-term memory"],
            ),
        ]

        self.log.info("all_projects_loaded", count=len(projects))
        return projects

    def get_production_projects(self) -> list[Project]:
        """Get all production-ready SIL projects.

        Returns:
            List of production Project instances
        """
        all_projects = self.get_all_projects()
        return [p for p in all_projects if p.status == ProjectStatus.PRODUCTION]

    def get_projects_by_layer(self) -> dict[Layer, list[Project]]:
        """Group all projects by their Semantic OS layer.

        Returns:
            Dict mapping Layer to list of Projects
        """
        all_projects = self.get_all_projects()
        by_layer = {}

        # Initialize all layers with empty lists
        for layer in Layer:
            by_layer[layer] = []

        # Group projects by layer
        for project in all_projects:
            by_layer[project.layer].append(project)

        self.log.info("projects_grouped_by_layer")
        return by_layer

    def get_project(self, slug: str) -> Optional[Project]:
        """Get a specific project by slug.

        Args:
            slug: Project slug (e.g., 'morphogen')

        Returns:
            Project instance or None if not found
        """
        all_projects = self.get_all_projects()
        for project in all_projects:
            if project.slug == slug:
                return project

        self.log.warning("project_not_found", slug=slug)
        return None
