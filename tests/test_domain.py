"""
Domain model tests.

These tests verify pure domain logic - fast, no I/O.
"""

import pytest

from sil_web.domain.models import (
    Document,
    Layer,
    Project,
    ProjectStatus,
)


class TestProject:
    """Tests for Project domain model."""

    def test_create_valid_project(self):
        """Should create a valid project."""
        project = Project(
            name="Test Project",
            slug="test-project",
            description="A test project for validation",
            status=ProjectStatus.PRODUCTION,
            layer=Layer.LAYER_2,
            github_url="https://github.com/test/project",
        )

        assert project.name == "Test Project"
        assert project.slug == "test-project"
        assert project.is_production is True

    def test_project_requires_name(self):
        """Should raise error if name is empty."""
        with pytest.raises(ValueError, match="name is required"):
            Project(
                name="",
                slug="test",
                description="Test",
                status=ProjectStatus.PRODUCTION,
                layer=Layer.LAYER_2,
                github_url="https://github.com/test/project",
            )

    def test_project_requires_valid_github_url(self):
        """Should raise error if GitHub URL is invalid."""
        with pytest.raises(ValueError, match="GitHub URL must start"):
            Project(
                name="Test",
                slug="test",
                description="Test",
                status=ProjectStatus.PRODUCTION,
                layer=Layer.LAYER_2,
                github_url="https://gitlab.com/test/project",
            )

    def test_project_is_production(self):
        """Should correctly identify production projects."""
        prod = Project(
            name="Prod",
            slug="prod",
            description="Production",
            status=ProjectStatus.PRODUCTION,
            layer=Layer.LAYER_2,
            github_url="https://github.com/test/prod",
        )

        research = Project(
            name="Research",
            slug="research",
            description="Research",
            status=ProjectStatus.RESEARCH,
            layer=Layer.LAYER_1,
            github_url="https://github.com/test/research",
        )

        assert prod.is_production is True
        assert research.is_production is False

    def test_project_has_stats(self):
        """Should correctly identify projects with stats."""
        with_stats = Project(
            name="WithStats",
            slug="with-stats",
            description="Has stats",
            status=ProjectStatus.PRODUCTION,
            layer=Layer.LAYER_2,
            github_url="https://github.com/test/stats",
            tests=100,
            coverage=85,
        )

        without_stats = Project(
            name="NoStats",
            slug="no-stats",
            description="No stats",
            status=ProjectStatus.RESEARCH,
            layer=Layer.LAYER_1,
            github_url="https://github.com/test/nostats",
        )

        assert with_stats.has_stats is True
        assert without_stats.has_stats is False


class TestDocument:
    """Tests for Document domain model."""

    def test_create_valid_document(self):
        """Should create a valid document."""
        doc = Document(
            title="Test Document",
            slug="test-doc",
            content="This is test content.",
            category="test",
        )

        assert doc.title == "Test Document"
        assert doc.slug == "test-doc"
        assert doc.word_count == 4

    def test_document_requires_title(self):
        """Should raise error if title is empty."""
        with pytest.raises(ValueError, match="title is required"):
            Document(
                title="",
                slug="test",
                content="Content",
                category="test",
            )

    def test_document_word_count(self):
        """Should correctly calculate word count."""
        doc = Document(
            title="Test",
            slug="test",
            content="One two three four five",
            category="test",
        )

        assert doc.word_count == 5
