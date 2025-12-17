"""Elegant markdown rendering service for clean HTML output.

This service transforms markdown content into HTML with:
- Rich markdown extensions (tables, code blocks, TOC)
- Clean pipeline architecture (preprocess → render)
- No link rewriting (source docs use clean URLs)
"""

import re
from typing import TYPE_CHECKING

import markdown
import structlog

if TYPE_CHECKING:
    from sil_web.services.content import ContentService


class MarkdownRenderer:
    """Elegant markdown rendering service.

    Provides a clean pipeline for transforming markdown → HTML with:
    - Preprocessing (strip H1, normalize)
    - Rich markdown extensions (tables, fenced code, TOC)
    - Clean URL handling (source docs use web-ready paths)

    Usage:
        renderer = MarkdownRenderer(content_service)
        html = renderer.render(markdown_text)
    """

    def __init__(self, content_service: "ContentService"):
        """Initialize markdown renderer.

        Args:
            content_service: Service for content discovery (unused but kept for compatibility)
        """
        self.content_service = content_service
        self.log = structlog.get_logger()

        # Configure markdown with extensions
        self.md = self._configure_markdown()

        self.log.info("markdown_renderer_initialized")

    def _configure_markdown(self) -> markdown.Markdown:
        """Configure markdown processor with extensions.

        Returns:
            Configured Markdown instance
        """
        return markdown.Markdown(
            extensions=[
                'fenced_code',    # GitHub-style ```python code blocks
                'tables',         # GitHub-style tables
                'md_in_html',     # Parse markdown inside HTML tags like <details>
                'nl2br',          # Natural line breaks (2 spaces = <br>)
                'sane_lists',     # Better list behavior
                'toc',            # Table of contents generation
            ],
            extension_configs={
                'toc': {
                    'permalink': False,  # Don't add ¶ symbols
                    'toc_depth': '2-4',  # Only h2-h4 in TOC
                }
            }
        )

    def render(self, content: str) -> str:
        """Render markdown to HTML with full pipeline.

        Pipeline stages:
        1. Preprocess: Clean and prepare markdown
        2. Render: Apply markdown extensions

        Args:
            content: Raw markdown content

        Returns:
            Rendered HTML
        """
        # Stage 1: Preprocess
        content = self._preprocess(content)

        # Stage 2: Render with extensions
        html = self.md.convert(content)

        # IMPORTANT: Reset state for next render
        # markdown.Markdown is stateful and reuses internal structures
        self.md.reset()

        return html

    def _preprocess(self, content: str) -> str:
        """Preprocess markdown before rendering.

        Current operations:
        - Strip YAML frontmatter (metadata handled separately)
        - Strip first H1 (template provides page header)
        - Normalize line endings

        Args:
            content: Raw markdown

        Returns:
            Preprocessed markdown
        """
        # Strip YAML frontmatter (between --- delimiters)
        content = self._strip_frontmatter(content)

        # Strip first H1 to avoid duplicate h1 tags
        # (HTML semantic structure: one h1 per page)
        content = self._strip_first_h1(content)

        return content

    def _strip_frontmatter(self, text: str) -> str:
        """Remove YAML frontmatter from markdown.

        Frontmatter is metadata between --- delimiters at the start of file.
        Example:
            ---
            title: "Page Title"
            description: "Page description"
            ---

        Args:
            text: Markdown content

        Returns:
            Content with frontmatter removed
        """
        # Match YAML frontmatter: starts with ---, ends with ---
        # Must be at very beginning of file
        pattern = r"^---\s*\n.*?\n---\s*\n"
        return re.sub(pattern, "", text, count=1, flags=re.DOTALL)

    def _strip_first_h1(self, text: str) -> str:
        """Remove first h1 heading to avoid duplicate h1 tags.

        Templates provide the page header, so we remove the markdown h1
        to maintain proper semantic HTML structure.

        Args:
            text: Markdown content

        Returns:
            Content with first h1 removed
        """
        pattern = r'^#\s+.+$'
        return re.sub(pattern, '', text, count=1, flags=re.MULTILINE)
