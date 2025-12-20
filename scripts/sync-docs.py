#!/usr/bin/env python3
"""
SIL Website - Manifest-Aware Documentation Sync Script
Syncs only public docs from SIL repo to website based on CONTENT_MANIFEST.yaml

PHILOSOPHY:
  Glass-box transparency: Only sync files explicitly marked category: public
  in CONTENT_MANIFEST.yaml. Default-deny approach - must opt-in to publication.

CHANGES FROM BASH VERSION:
  - Pure Python implementation (cleaner, more maintainable)
  - Native YAML parsing
  - Better error handling and reporting
  - Structured logging
  - Validates manifest integrity

USAGE:
  ./sync-docs.py              # Normal sync
  ./sync-docs.py --validate   # Validate only, don't sync
  ./sync-docs.py --dry-run    # Show what would be synced
  ./sync-docs.py --clean      # Remove internal files from website

SESSION: bronze-spark-1216
"""

import argparse
import shutil
import sys
from pathlib import Path
from typing import Dict, List

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Install with: pip install pyyaml")
    sys.exit(1)


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


class SyncStats:
    """Statistics tracking for sync operation"""
    def __init__(self):
        self.synced_files = 0
        self.synced_dirs = 0
        self.skipped_files = 0
        self.missing_files = 0
        self.internal_violations = 0
        self.violations_list: List[str] = []

    def summary(self) -> str:
        """Generate summary report"""
        lines = [
            f"Synced: {self.synced_files} files, {self.synced_dirs} directories",
            f"Skipped: {self.skipped_files} files",
        ]
        if self.missing_files > 0:
            lines.append(f"Missing: {self.missing_files} files (not found in source)")
        if self.internal_violations > 0:
            lines.append(f"Violations: {self.internal_violations} internal files in website")
        return "\n".join(lines)


class ContentManifest:
    """Parser and handler for CONTENT_MANIFEST.yaml"""

    def __init__(self, manifest_path: Path):
        self.manifest_path = manifest_path
        self.manifest = self._load_manifest()
        self.public_files: List[Dict] = []
        self.internal_files: List[str] = []
        self._parse_manifest()

    def _load_manifest(self) -> Dict:
        """Load and parse YAML manifest"""
        if not self.manifest_path.exists():
            raise FileNotFoundError(
                f"CONTENT_MANIFEST.yaml not found at {self.manifest_path}\n"
                "Please create the manifest first."
            )

        try:
            with open(self.manifest_path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Failed to parse manifest: {e}")

    def _parse_manifest(self):
        """Extract public and internal file lists from manifest"""
        # Parse flat files list with visibility field (bronze-spark-1216 design)
        if 'files' in self.manifest:
            for item in self.manifest['files']:
                path = item.get('path', '')
                visibility = item.get('visibility', '')

                if not path:
                    continue

                # Skip flagged files
                if item.get('flagged_for_removal'):
                    continue

                if visibility == 'public':
                    # Handle directory patterns (path ends with /)
                    if path.endswith('/'):
                        self.public_files.append({
                            'type': 'dir',
                            'path': path.rstrip('/'),
                            'pattern': item.get('pattern', '*.md'),
                            'purpose': item.get('purpose', '')
                        })
                    else:
                        self.public_files.append({
                            'type': 'file',
                            'path': path,
                            'purpose': item.get('purpose', ''),
                            'under_review': item.get('under_review', False)
                        })

                elif visibility == 'internal':
                    self.internal_files.append(path)

    def get_stats(self) -> Dict:
        """Get statistics from manifest"""
        return self.manifest.get('stats', {})


class DocSync:
    """Main documentation sync orchestrator"""

    def __init__(self, args):
        self.args = args
        self.stats = SyncStats()

        # Setup paths
        script_dir = Path(__file__).parent.resolve()
        self.website_root = script_dir.parent
        self.sil_repo = self.website_root.parent / "SIL"
        self.website_docs = self.website_root / "docs"
        self.manifest_path = self.sil_repo / "docs" / "CONTENT_MANIFEST.yaml"

        # Load manifest
        self.manifest = ContentManifest(self.manifest_path)

    def print_header(self):
        """Print script header"""
        print("=" * 50)
        print("SIL Documentation Sync (Manifest-Aware)")
        print("=" * 50)
        print()

        if self.args.dry_run:
            print(f"{Colors.YELLOW}DRY RUN MODE - No files will be modified{Colors.NC}")
            print()

        if self.args.validate:
            print(f"{Colors.BLUE}VALIDATE ONLY MODE - No sync, just validation{Colors.NC}")
            print()

    def validate_environment(self):
        """Validate required directories exist"""
        if not self.sil_repo.exists():
            print(f"{Colors.RED}ERROR: SIL repository not found at {self.sil_repo}{Colors.NC}")
            print("Please ensure SIL repo is cloned at the expected location.")
            sys.exit(1)
        print(f"{Colors.GREEN}✓{Colors.NC} Found SIL repo: {self.sil_repo}")

        if not (self.sil_repo / "docs").exists():
            print(f"{Colors.RED}ERROR: SIL docs directory not found{Colors.NC}")
            sys.exit(1)
        print(f"{Colors.GREEN}✓{Colors.NC} Found SIL docs directory")

        print(f"{Colors.GREEN}✓{Colors.NC} Found CONTENT_MANIFEST.yaml")
        print()

    def sync_directory(self, source_dir: Path, dest_dir: Path, pattern: str = "*.md"):
        """Sync a directory using rsync-like behavior"""
        if not source_dir.exists():
            print(f"{Colors.YELLOW}⚠{Colors.NC} Source directory not found: {source_dir}")
            self.stats.missing_files += 1
            return

        # Create destination directory
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Copy all matching files
        files_synced = 0
        for source_file in source_dir.rglob(pattern):
            if source_file.is_file():
                # Calculate relative path and destination
                rel_path = source_file.relative_to(source_dir)
                dest_file = dest_dir / rel_path

                # Create parent directories
                dest_file.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                if not self.args.dry_run:
                    shutil.copy2(source_file, dest_file)
                files_synced += 1

        self.stats.synced_files += files_synced
        self.stats.synced_dirs += 1

        return files_synced

    def sync_file(self, source_path: Path, dest_path: Path):
        """Sync individual file"""
        if not source_path.exists():
            print(f"{Colors.YELLOW}  ⚠{Colors.NC} Missing: {source_path.relative_to(self.sil_repo / 'docs')}")
            self.stats.missing_files += 1
            return False

        # Create parent directory
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        if not self.args.dry_run:
            shutil.copy2(source_path, dest_path)

        print(f"  {Colors.GREEN}✓{Colors.NC} {source_path.relative_to(self.sil_repo / 'docs')}")
        self.stats.synced_files += 1
        return True

    def sync_public_content(self):
        """Sync all public content from manifest"""
        print("=" * 50)
        print("Syncing Public Documentation")
        print("=" * 50)
        print()

        # Group files by type
        dirs_to_sync = []
        files_to_sync = []

        for item in self.manifest.public_files:
            if item['type'] == 'dir':
                dirs_to_sync.append(item)
            else:
                files_to_sync.append(item)

        # Sync directories
        for item in dirs_to_sync:
            clean_path = item['path'].replace('docs/', '')
            source_dir = self.sil_repo / "docs" / clean_path
            dest_dir = self.website_docs / clean_path

            print(f"Syncing {clean_path}/...")
            if self.args.dry_run:
                print(f"  {Colors.YELLOW}[DRY RUN]{Colors.NC} Would sync {source_dir} -> {dest_dir}")
            else:
                files_count = self.sync_directory(source_dir, dest_dir, item.get('pattern', '*.md'))
                print(f"{Colors.GREEN}✓{Colors.NC} {clean_path} synced ({files_count} files)")
            print()

        # Sync individual files
        if files_to_sync:
            print("Syncing individual files...")
            for item in files_to_sync:
                file_path = item['path'].replace('docs/', '')
                source_path = self.sil_repo / "docs" / file_path
                dest_path = self.website_docs / file_path

                if self.args.dry_run:
                    print(f"  {Colors.YELLOW}[DRY RUN]{Colors.NC} Would sync {file_path}")
                else:
                    self.sync_file(source_path, dest_path)
            print()

        print(f"{Colors.GREEN}✓{Colors.NC} Public files synced")
        print()

    def validate_no_internal_files(self):
        """Check for internal files in website repo"""
        print("=" * 50)
        print("Validation")
        print("=" * 50)
        print()

        print("Checking for internal files in website repo...")

        for internal_path in self.manifest.internal_files:
            clean_path = internal_path.replace('docs/', '')
            website_file = self.website_docs / clean_path

            if website_file.exists():
                print(f"{Colors.RED}✗{Colors.NC} Found internal file: {clean_path}")
                self.stats.internal_violations += 1
                self.stats.violations_list.append(clean_path)

        if self.stats.internal_violations == 0:
            print(f"{Colors.GREEN}✓{Colors.NC} No internal files found in website repo")
        else:
            print(f"{Colors.YELLOW}⚠ Found {self.stats.internal_violations} internal files in website repo{Colors.NC}")
            print()
            print("To remove these files:")
            for violation in self.stats.violations_list:
                print(f"  rm {self.website_docs / violation}")
            print()
            print("Or run: ./scripts/sync-docs.py --clean")

        print()

    def clean_internal_files(self):
        """Remove internal files from website repo"""
        print("=" * 50)
        print("Cleaning Internal Files from Website")
        print("=" * 50)
        print()

        removed = 0
        for internal_path in self.manifest.internal_files:
            clean_path = internal_path.replace('docs/', '')
            website_file = self.website_docs / clean_path

            if website_file.exists():
                print(f"Removing: {clean_path}")
                if not self.args.dry_run:
                    website_file.unlink()
                removed += 1

        if removed == 0:
            print(f"{Colors.GREEN}✓{Colors.NC} No internal files found to remove")
        else:
            print()
            print(f"{Colors.GREEN}✓{Colors.NC} Removed {removed} internal files")
        print()

    def show_file_counts(self):
        """Show file counts by directory"""
        if self.args.validate or self.args.dry_run:
            return

        print("Synced files by category:")

        dirs = ['manifesto', 'foundations', 'research', 'systems',
                'architecture', 'meta', 'essays']

        for dir_name in dirs:
            dir_path = self.website_docs / dir_name
            if dir_path.exists():
                count = len(list(dir_path.rglob('*.md')))
                print(f"  {dir_name:<13} {count:>2} documents")

        print()
        total = len(list(self.website_docs.rglob('*.md')))
        print(f"Total: {total} markdown files")
        print()

    def validate_manifest_stats(self):
        """Validate manifest statistics match reality"""
        print("Checking manifest statistics...")

        stats = self.manifest.get_stats()
        expected_public = stats.get('public_files', 0)
        expected_internal = stats.get('internal_files', 0)

        actual_count = len(list(self.website_docs.rglob('*.md')))

        print(f"Expected public files: {expected_public}")
        print(f"Actual files in website: {actual_count}")
        print(f"Expected internal files: {expected_internal} (should NOT be in website)")

        # Allow some tolerance for generated files
        if actual_count > expected_public + 5:
            print(f"{Colors.YELLOW}WARNING: More files in website than expected{Colors.NC}")
            print("Check for files not in manifest")

        print()

    def print_summary(self):
        """Print final summary"""
        print("=" * 50)

        if self.stats.internal_violations > 0:
            print(f"{Colors.YELLOW}⚠ Sync completed with {self.stats.internal_violations} internal file violations{Colors.NC}")
            print("=" * 50)
            print()
            print("Action required: Remove internal files from website repo")
            print("Run: ./scripts/sync-docs.py --clean")
            return 1
        elif self.args.dry_run:
            print(f"{Colors.BLUE}✓ Dry run completed - no files modified{Colors.NC}")
            print("=" * 50)
            return 0
        elif self.args.validate:
            print(f"{Colors.GREEN}✓ Validation passed - no issues found{Colors.NC}")
            print("=" * 50)
            return 0
        elif self.args.clean:
            print(f"{Colors.GREEN}✓ Clean completed successfully{Colors.NC}")
            print("=" * 50)
            return 0
        else:
            print(f"{Colors.GREEN}✓ Documentation sync completed successfully{Colors.NC}")
            print("=" * 50)
            print()
            print(self.stats.summary())
            return 0

    def run(self):
        """Main execution flow"""
        self.print_header()
        self.validate_environment()

        if self.args.clean:
            self.clean_internal_files()
            return self.print_summary()

        if not self.args.validate:
            self.sync_public_content()

        self.validate_no_internal_files()

        if not self.args.validate:
            self.show_file_counts()
            self.validate_manifest_stats()

        return self.print_summary()


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        description='Manifest-aware documentation sync from SIL repo to website',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                # Normal sync
  %(prog)s --dry-run      # Show what would be synced
  %(prog)s --validate     # Check for issues without syncing
  %(prog)s --clean        # Remove internal files from website
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be synced without actually syncing'
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate manifest and check for internal files in website'
    )

    parser.add_argument(
        '--clean',
        action='store_true',
        help='Remove internal files from website repo'
    )

    args = parser.parse_args()

    try:
        sync = DocSync(args)
        return sync.run()
    except Exception as e:
        print(f"{Colors.RED}ERROR: {e}{Colors.NC}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
