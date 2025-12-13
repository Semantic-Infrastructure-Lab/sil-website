"""Elegant markdown rendering service with intelligent link rewriting.

This service transforms markdown content into HTML with:
- Automatic link rewriting (.md paths → web routes)
- Rich markdown extensions (tables, code blocks, TOC)
- Clean pipeline architecture (preprocess → render → postprocess)
"""

import re
from typing import TYPE_CHECKING, Any
from xml.etree.ElementTree import Element

import markdown
import structlog
from markdown.core import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

if TYPE_CHECKING:
    from sif_web.services.content import ContentService


class LinkRewriterTreeprocessor(Treeprocessor):
    """Rewrites markdown file links to web routes in the parsed tree.

    Examples:
        ./SIL_PRINCIPLES.md          → /docs/principles
        ../tools/README.md           → /projects
        canonical/SIL_MANIFESTO.md   → /docs/manifesto
        ../../projects/PROJECT_INDEX.md → /projects
    """

    def __init__(self, md: Markdown, link_map: dict[str, str]):
        """Initialize with link mapping.

        Args:
            md: Markdown instance
            link_map: Mapping of filename patterns to web routes
        """
        super().__init__(md)
        self.link_map = link_map
        self.log = structlog.get_logger()

    def run(self, root: Element) -> Element:
        """Walk the element tree and rewrite <a> hrefs."""
        for link in root.iter('a'):
            href = link.get('href', '')

            # Skip external links and anchors
            if href.startswith(('http://', 'https://', 'mailto:', '#')):
                continue

            # Rewrite .md links and relative directory links
            if '.md' in href.lower() or self._is_relative_dir_link(href):
                new_href = self._rewrite_link(href)
                if new_href != href:
                    self.log.debug(
                        "link_rewritten",
                        original=href,
                        rewritten=new_href
                    )
                    link.set('href', new_href)

        return root

    def _is_relative_dir_link(self, href: str) -> bool:
        """Check if href is a relative directory link (e.g., ../tools/, docs/innovations/).

        Detects:
        - Explicit relative: ./foo/, ../foo/
        - Implicit relative: docs/, docs/foo/ (no leading slash, no protocol)
        """
        # Skip absolute paths, anchors, and external links
        if href.startswith(('/', '#', 'http://', 'https://', 'mailto:')):
            return False

        # Skip file extensions
        if any(href.endswith(ext) for ext in ('.md', '.html', '.css', '.js', '.png', '.svg', '.jpg', '.gif')):
            return False

        # It's a directory link if it ends with / or looks like a directory path
        # (contains / but doesn't end with a file extension)
        return href.endswith('/') or (href.count('/') > 0 and '.' not in href.split('/')[-1])

    def _rewrite_link(self, href: str) -> str:
        """Convert markdown path to web route.

        Args:
            href: Original href (e.g., './SIL_PRINCIPLES.md' or '../tools/')

        Returns:
            Web route (e.g., '/docs/principles' or '/docs/tools-overview')
        """
        # Handle directory-style links (e.g., ../tools/, docs/innovations/)
        if self._is_relative_dir_link(href):
            # Extract directory name from path
            # ../tools/ -> tools, docs/innovations/ -> innovations, docs/ -> docs
            clean_path = href.rstrip('/')
            dir_name = clean_path.split('/')[-1]

            # Special case: 'docs' alone -> /docs (the index)
            if dir_name == 'docs' or clean_path == 'docs':
                return '/docs'

            # Look up directory in link map
            dir_key = f'{dir_name}/'
            if dir_key in self.link_map:
                return self.link_map[dir_key]

            # Fallback: log and return original
            self.log.warning("dir_link_not_mapped", href=href, dir_name=dir_name)
            return href

        # Handle .md file links
        path_parts = href.split('/')
        filename = path_parts[-1]

        # Remove .md extension and any anchors
        filename = filename.split('#')[0]  # Handle anchors like file.md#section

        # Look up in our link map
        if filename in self.link_map:
            route = self.link_map[filename]
            # Preserve anchor if present
            if '#' in href:
                anchor = href.split('#')[1]
                return f"{route}#{anchor}"
            return route

        # Fallback: log and return original (better than breaking)
        self.log.warning("link_not_mapped", href=href, filename=filename)
        return href


class LinkRewriterExtension(Extension):
    """Markdown extension that enables intelligent link rewriting."""

    def __init__(self, link_map: dict[str, str], **kwargs: Any):
        """Initialize with link mapping.

        Args:
            link_map: Mapping of filename patterns to web routes
            **kwargs: Additional extension config
        """
        self.link_map = link_map
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        """Register the link rewriter tree processor."""
        processor = LinkRewriterTreeprocessor(md, self.link_map)
        md.treeprocessors.register(
            processor,
            'link_rewriter',
            priority=0  # Run last, after all other processing
        )


class MarkdownRenderer:
    """Elegant markdown rendering service.

    Provides a clean pipeline for transforming markdown → HTML with:
    - Preprocessing (strip H1, normalize)
    - Rich markdown extensions (tables, fenced code, TOC)
    - Intelligent link rewriting (uses ContentService knowledge)
    - Postprocessing (future: syntax highlighting, sanitization)

    Usage:
        renderer = MarkdownRenderer(content_service)
        html = renderer.render(markdown_text)
    """

    def __init__(self, content_service: "ContentService"):
        """Initialize with content service for slug knowledge.

        Args:
            content_service: Service that knows all valid document slugs
        """
        self.content_service = content_service
        self.log = structlog.get_logger()

        # Build intelligent link map using content service knowledge
        self.link_map = self._build_link_map()

        # Configure markdown with extensions
        self.md = self._configure_markdown()

        self.log.info(
            "markdown_renderer_initialized",
            links_mapped=len(self.link_map)
        )

    def _build_link_map(self) -> dict[str, str]:
        """Build filename → web route mapping using ContentService.

        Returns:
            Dict mapping markdown filenames and directories to web routes
            Example: {'SIL_MANIFESTO.md': '/docs/manifesto', 'tools/': '/docs/tools-overview'}
        """
        link_map = {}

        # Get all categories we know about
        categories = ['canonical', 'architecture', 'research', 'meta', 'tools', 'innovations']

        for category in categories:
            # Use ContentService to discover slugs in this category
            slug_map = self.content_service._discover_slugs(category)

            for slug, filename in slug_map.items():
                # Map filename → web route
                link_map[filename] = f'/docs/{slug}'

            # Add directory mapping (category/ → appropriate overview page)
            # Priority: {category}-overview > {category} (from INNOVATIONS.md etc.) > overview
            overview_slug = f'{category}-overview'
            if overview_slug in slug_map:
                link_map[f'{category}/'] = f'/docs/{overview_slug}'
            elif category in slug_map:
                # Category has a main doc (e.g., innovations/ → INNOVATIONS.md → /docs/innovations)
                link_map[f'{category}/'] = f'/docs/{category}'
            elif 'overview' in slug_map:
                # Fallback for categories without prefixed overview
                link_map[f'{category}/'] = '/docs/overview'

        # Special cases for top-level directories
        link_map['PROJECT_INDEX.md'] = '/projects'
        link_map['projects/'] = '/projects'
        link_map['docs/'] = '/docs'

        self.log.debug("link_map_built", count=len(link_map))
        return link_map

    def _configure_markdown(self) -> markdown.Markdown:
        """Configure markdown processor with extensions.

        Returns:
            Configured Markdown instance
        """
        return markdown.Markdown(
            extensions=[
                'fenced_code',    # GitHub-style ```python code blocks
                'tables',         # GitHub-style tables
                'nl2br',          # Natural line breaks (2 spaces = <br>)
                'sane_lists',     # Better list behavior
                'toc',            # Table of contents generation
                LinkRewriterExtension(link_map=self.link_map),  # Our magic!
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
        3. Postprocess: (Future: syntax highlighting, etc.)

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

        # Stage 3: Postprocess (future enhancements go here)
        # html = self._postprocess(html)

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
