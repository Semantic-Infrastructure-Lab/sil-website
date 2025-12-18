"""
Tests for frontmatter parsing and privacy filtering.

These tests verify that:
- Frontmatter is correctly parsed (private, beth_topics, tags)
- Privacy filtering works at service layer
- Missing frontmatter uses safe defaults
"""

import pytest
from pathlib import Path
from sil_web.services.content import ContentService, ProjectService
from sil_web.domain.models import ProjectStatus


class TestContentServicePrivacy:
    """Tests for ContentService privacy filtering."""

    @pytest.fixture
    def content_service(self, tmp_path):
        """Create ContentService with temporary docs directory."""
        # Create temporary docs structure
        docs_path = tmp_path / "docs"
        docs_path.mkdir()

        # Create essays directory for testing
        essays_dir = docs_path / "essays"
        essays_dir.mkdir()

        return ContentService(docs_path)

    def test_load_document_filters_private_by_default(self, content_service, tmp_path):
        """Should filter private documents when include_private=False."""
        # Create a private document
        essays_dir = tmp_path / "docs" / "essays"
        private_doc = essays_dir / "private-essay.md"
        private_doc.write_text("""---
title: Private Essay
private: true
tier: 1
order: 1
---

This is private content.
""")

        # Should return None when include_private=False (default)
        doc = content_service.load_document("essays", "private-essay", include_private=False)
        assert doc is None

    def test_load_document_includes_private_when_requested(self, content_service, tmp_path):
        """Should include private documents when include_private=True."""
        # Create a private document
        essays_dir = tmp_path / "docs" / "essays"
        private_doc = essays_dir / "private-essay.md"
        private_doc.write_text("""---
title: Private Essay
private: true
tier: 1
order: 1
---

This is private content.
""")

        # Should return document when include_private=True
        doc = content_service.load_document("essays", "private-essay", include_private=True)
        assert doc is not None
        assert doc.title == "Private Essay"
        assert doc.private is True

    def test_load_document_public_by_default(self, content_service, tmp_path):
        """Should treat documents without private field as public."""
        # Create a document without private field
        essays_dir = tmp_path / "docs" / "essays"
        public_doc = essays_dir / "public-essay.md"
        public_doc.write_text("""---
title: Public Essay
tier: 1
order: 1
---

This is public content.
""")

        # Should load successfully (default private=False)
        doc = content_service.load_document("essays", "public-essay", include_private=False)
        assert doc is not None
        assert doc.title == "Public Essay"
        assert doc.private is False

    def test_list_documents_filters_private(self, content_service, tmp_path):
        """Should filter private documents from list."""
        # Create public and private documents
        essays_dir = tmp_path / "docs" / "essays"

        public_doc = essays_dir / "public-essay.md"
        public_doc.write_text("""---
title: Public Essay
tier: 1
order: 1
---

Public content.
""")

        private_doc = essays_dir / "private-essay.md"
        private_doc.write_text("""---
title: Private Essay
private: true
tier: 1
order: 2
---

Private content.
""")

        # List without private (default)
        docs = content_service.list_documents(category="essays", include_private=False)
        assert len(docs) == 1
        assert docs[0].slug == "public-essay"

    def test_list_documents_includes_private_when_requested(self, content_service, tmp_path):
        """Should include private documents when include_private=True."""
        # Create public and private documents
        essays_dir = tmp_path / "docs" / "essays"

        public_doc = essays_dir / "public-essay.md"
        public_doc.write_text("""---
title: Public Essay
tier: 1
order: 1
---

Public content.
""")

        private_doc = essays_dir / "private-essay.md"
        private_doc.write_text("""---
title: Private Essay
private: true
tier: 1
order: 2
---

Private content.
""")

        # List with private
        docs = content_service.list_documents(category="essays", include_private=True)
        assert len(docs) == 2
        slugs = {d.slug for d in docs}
        assert "public-essay" in slugs
        assert "private-essay" in slugs

    def test_frontmatter_parses_beth_topics(self, content_service, tmp_path):
        """Should parse beth_topics from frontmatter."""
        essays_dir = tmp_path / "docs" / "essays"
        doc_file = essays_dir / "test-essay.md"
        doc_file.write_text("""---
title: Test Essay
tier: 1
order: 1
beth_topics:
  - topic-1
  - topic-2
---

Content.
""")

        doc = content_service.load_document("essays", "test-essay")
        assert doc.beth_topics == ["topic-1", "topic-2"]

    def test_frontmatter_parses_tags(self, content_service, tmp_path):
        """Should parse tags from frontmatter."""
        essays_dir = tmp_path / "docs" / "essays"
        doc_file = essays_dir / "test-essay.md"
        doc_file.write_text("""---
title: Test Essay
tier: 1
order: 1
tags:
  - tag1
  - tag2
---

Content.
""")

        doc = content_service.load_document("essays", "test-essay")
        assert doc.tags == ["tag1", "tag2"]


class TestProjectServicePrivacy:
    """Tests for ProjectService privacy filtering."""

    @pytest.fixture
    def project_service(self):
        """Create ProjectService instance."""
        return ProjectService()

    def test_get_all_projects_filters_private_by_default(self, project_service):
        """Should filter private projects when include_private=False."""
        # Get all projects (should exclude private ones)
        projects = project_service.get_all_projects(include_private=False)

        # Check that no private projects are included
        for project in projects:
            assert project.is_private is False

    def test_get_all_projects_includes_private_when_requested(self, project_service):
        """Should include private projects when include_private=True."""
        # Get all projects including private
        all_projects = project_service.get_all_projects(include_private=True)
        public_projects = project_service.get_all_projects(include_private=False)

        # Should have more projects when including private
        assert len(all_projects) >= len(public_projects)

        # Verify private projects are included
        private_count = sum(1 for p in all_projects if p.is_private)
        assert private_count > 0

    def test_get_production_projects_filters_private(self, project_service):
        """Should filter private projects from production list."""
        # Get production projects (should exclude private ones)
        prod_projects = project_service.get_production_projects(include_private=False)

        # Check that no private projects are included
        for project in prod_projects:
            assert project.is_private is False
            assert project.status == ProjectStatus.PRODUCTION

    def test_get_projects_by_layer_filters_private(self, project_service):
        """Should filter private projects from layer grouping."""
        # Get projects by layer (should exclude private ones)
        by_layer = project_service.get_projects_by_layer(include_private=False)

        # Check that no private projects are included in any layer
        for layer, projects in by_layer.items():
            for project in projects:
                assert project.is_private is False

    def test_get_project_filters_private_by_default(self, project_service):
        """Should return None for private projects when include_private=False."""
        # First, find a private project slug
        all_projects = project_service.get_all_projects(include_private=True)
        private_projects = [p for p in all_projects if p.is_private]

        if private_projects:
            private_slug = private_projects[0].slug

            # Should return None when include_private=False
            project = project_service.get_project(private_slug, include_private=False)
            assert project is None

    def test_get_project_includes_private_when_requested(self, project_service):
        """Should return private projects when include_private=True."""
        # First, find a private project slug
        all_projects = project_service.get_all_projects(include_private=True)
        private_projects = [p for p in all_projects if p.is_private]

        if private_projects:
            private_slug = private_projects[0].slug

            # Should return project when include_private=True
            project = project_service.get_project(private_slug, include_private=True)
            assert project is not None
            assert project.is_private is True
