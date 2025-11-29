"""
Content service - loads SIL documents and project data.

This service handles I/O: reading files, parsing markdown, loading YAML.
"""

from pathlib import Path
from typing import Optional

import frontmatter
import structlog

from sil_web.domain.models import Document, Layer, Project, ProjectStatus

log = structlog.get_logger()


class ContentService:
    """Service for loading SIL content (docs, projects)."""

    def __init__(self, docs_path: Path) -> None:
        """Initialize content service.

        Args:
            docs_path: Path to SIL repository docs directory
        """
        self.docs_path = docs_path
        self.log = log.bind(service="content")

    def load_document(self, slug: str) -> Optional[Document]:
        """Load a canonical document by slug.

        Args:
            slug: Document slug (e.g., 'manifesto', 'principles')

        Returns:
            Document instance or None if not found
        """
        # Map slugs to actual file paths
        doc_files = {
            "manifesto": "SIL_MANIFESTO.md",
            "principles": "SIL_PRINCIPLES.md",
            "charter": "SIL_TECHNICAL_CHARTER.md",
            "glossary": "SIL_GLOSSARY.md",
            "research": "SIL_RESEARCH_AGENDA_YEAR1.md",
            "founders-letter": "FOUNDERS_LETTER.md",
        }

        if slug not in doc_files:
            self.log.warning("document_not_found", slug=slug)
            return None

        doc_path = self.docs_path / "canonical" / doc_files[slug]
        if not doc_path.exists():
            self.log.error("document_file_missing", slug=slug, path=str(doc_path))
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
            category="canonical",
            description=description,
        )

        self.log.info("document_loaded", slug=slug, word_count=doc.word_count)
        return doc

    def list_documents(self) -> list[Document]:
        """List all available canonical documents.

        Returns:
            List of Document instances
        """
        slugs = [
            "founders-letter",
            "manifesto",
            "principles",
            "charter",
            "glossary",
            "research",
        ]

        docs = []
        for slug in slugs:
            doc = self.load_document(slug)
            if doc:
                docs.append(doc)

        self.log.info("documents_listed", count=len(docs))
        return docs


class ProjectService:
    """Service for loading SIL project data."""

    def __init__(self) -> None:
        """Initialize project service."""
        self.log = log.bind(service="projects")

    def get_production_projects(self) -> list[Project]:
        """Get all production-ready SIL projects.

        Returns:
            List of production Project instances
        """
        projects = [
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
        ]

        self.log.info("production_projects_loaded", count=len(projects))
        return projects

    def get_project(self, slug: str) -> Optional[Project]:
        """Get a specific project by slug.

        Args:
            slug: Project slug (e.g., 'morphogen')

        Returns:
            Project instance or None if not found
        """
        projects = self.get_production_projects()
        for project in projects:
            if project.slug == slug:
                return project

        self.log.warning("project_not_found", slug=slug)
        return None
