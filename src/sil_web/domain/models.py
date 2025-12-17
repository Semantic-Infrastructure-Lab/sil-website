"""
Domain models for SIL website.

Pure Python - no I/O, no database, no network calls.
These models represent the core concepts of the SIL ecosystem.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ProjectStatus(Enum):
    """Project maturity status."""

    PRODUCTION = "production"
    RESEARCH = "research"
    ALPHA = "alpha"
    SPECIFICATION = "specification"
    PLANNED = "planned"


class Layer(Enum):
    """The 6-layer Semantic OS architecture."""

    LAYER_0 = "Semantic Memory"
    LAYER_1 = "Universal Semantic IR"
    LAYER_2 = "Domain Modules"
    LAYER_3 = "Multi-Agent Orchestration"
    LAYER_4 = "Deterministic Engines"
    LAYER_5 = "Human Interfaces / SIM"
    CROSS_CUTTING = "Cross-Cutting Infrastructure"


@dataclass
class Project:
    """A SIL project - production system or research initiative."""

    name: str
    slug: str
    description: str
    status: ProjectStatus
    layer: Layer
    github_url: Optional[str] = None
    version: Optional[str] = None
    tests: Optional[int] = None
    coverage: Optional[int] = None
    pypi_url: Optional[str] = None
    innovations: list[str] = field(default_factory=list)
    use_cases: list[str] = field(default_factory=list)
    is_private: bool = False
    maturity_note: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate project data."""
        if not self.name:
            raise ValueError("Project name is required")
        if not self.slug:
            raise ValueError("Project slug is required")
        if self.github_url and not self.github_url.startswith("https://github.com/"):
            raise ValueError("GitHub URL must start with https://github.com/")

    @property
    def is_production(self) -> bool:
        """Check if project is production-ready."""
        return self.status == ProjectStatus.PRODUCTION

    @property
    def has_stats(self) -> bool:
        """Check if project has test/coverage stats."""
        return self.tests is not None and self.coverage is not None


@dataclass
class Document:
    """A canonical SIL document (manifesto, principles, etc.)."""

    title: str
    slug: str
    content: str
    category: str
    description: Optional[str] = None
    order: int = 0
    tier: int = 3  # 1=Founding, 2=Architecture, 3=Research

    def __post_init__(self) -> None:
        """Validate document data."""
        if not self.title:
            raise ValueError("Document title is required")
        if not self.slug:
            raise ValueError("Document slug is required")
        if not self.content:
            raise ValueError("Document content is required")

    @property
    def word_count(self) -> int:
        """Calculate word count of content."""
        return len(self.content.split())


@dataclass
class Author:
    """An author or contributor."""

    name: str
    github: Optional[str] = None
    website: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate author data."""
        if not self.name:
            raise ValueError("Author name is required")
