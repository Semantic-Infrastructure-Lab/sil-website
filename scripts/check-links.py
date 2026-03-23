#!/usr/bin/env python3
"""SIL Website Link Checker

Crawls all internal pages, extracts every href, and verifies each link.
Exits 1 if any broken links are found.

Usage:
    python scripts/check-links.py [base_url]
    python scripts/check-links.py https://semanticinfrastructurelab.org
    python scripts/check-links.py https://sil-staging.mytia.net
"""

import sys
from collections import defaultdict
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import httpx

# Statuses treated as broken for internal links
INTERNAL_BROKEN = {404, 410, 500, 502, 503, 504}

# Statuses treated as broken for external links (429 = rate limited, not broken)
EXTERNAL_BROKEN = {404, 410, 500, 502, 503, 504}

# Static asset extensions — skip checking these
SKIP_EXTENSIONS = {
    ".css", ".js", ".png", ".jpg", ".jpeg", ".gif", ".ico",
    ".svg", ".woff", ".woff2", ".ttf", ".eot", ".map",
}


class LinkExtractor(HTMLParser):
    def __init__(self, page_url: str):
        super().__init__()
        self.page_url = page_url
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value and not value.startswith(("#", "mailto:", "tel:")):
                    self.links.append(urljoin(self.page_url, value))


def normalize(url: str) -> str:
    """Strip fragment and trailing slash for deduplication."""
    url = url.split("#")[0]
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    return parsed._replace(path=path, fragment="").geturl()


def is_internal(url: str, base_host: str) -> bool:
    return urlparse(url).netloc == base_host


def should_skip(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return True
    if not parsed.netloc:
        return True
    ext = "." + parsed.path.rsplit(".", 1)[-1].lower() if "." in parsed.path.rsplit("/", 1)[-1] else ""
    return ext in SKIP_EXTENSIONS


def check_links(base_url: str) -> int:
    base_url = base_url.rstrip("/")
    base_host = urlparse(base_url).netloc

    # Phase 1: crawl all internal pages and collect every link
    pages_to_crawl: set[str] = {normalize(base_url + "/")}
    crawled: set[str] = set()
    # link -> list of pages that reference it
    found_on: dict[str, list[str]] = defaultdict(list)

    client = httpx.Client(
        follow_redirects=True,
        timeout=15.0,
        headers={"User-Agent": "SIL-LinkChecker/1.0 (semanticinfrastructurelab.org)"},
    )

    print(f"Crawling {base_url} ...")
    print()

    with client:
        # Crawl internal pages
        while True:
            remaining = pages_to_crawl - crawled
            if not remaining:
                break
            url = next(iter(remaining))
            crawled.add(url)

            try:
                resp = client.get(url)
            except httpx.TimeoutException:
                found_on[url]  # ensure key exists
                print(f"  TIMEOUT  {url}")
                continue
            except Exception as e:
                print(f"  ERROR    {url}  ({e})")
                continue

            if "html" not in resp.headers.get("content-type", ""):
                continue

            extractor = LinkExtractor(url)
            extractor.feed(resp.text)

            for raw_link in extractor.links:
                link = normalize(raw_link)
                if not link or should_skip(link):
                    continue
                found_on[link].append(url)
                if is_internal(link, base_host) and link not in crawled:
                    pages_to_crawl.add(link)

        # Phase 2: check every discovered link (internal already crawled, check external)
        broken: list[tuple[str, str, int | str]] = []

        print(f"Crawled {len(crawled)} internal pages. Checking {len(found_on)} unique links ...\n")

        for url, sources in sorted(found_on.items()):
            if should_skip(url):
                continue

            internal = is_internal(url, base_host)

            # Internal pages were already fetched — check their status now
            if internal and url in crawled:
                try:
                    resp = client.get(url)
                    status = resp.status_code
                except httpx.TimeoutException:
                    broken.append((sources[0], url, "TIMEOUT"))
                    print(f"  ✗ TIMEOUT  {url}")
                    print(f"    linked from: {sources[0]}")
                    continue
                except Exception as e:
                    print(f"  ⚠  ERROR  {url}  ({e})")
                    continue

                if status in INTERNAL_BROKEN:
                    broken.append((sources[0], url, status))
                    print(f"  ✗ {status}  {url}")
                    print(f"    linked from: {sources[0]}")

            elif not internal:
                # Check external link
                try:
                    resp = client.head(url, follow_redirects=True)
                    status = resp.status_code
                    # Some servers reject HEAD — retry with GET
                    if status in (405, 403):
                        resp = client.get(url)
                        status = resp.status_code
                except httpx.TimeoutException:
                    # Don't fail deploy over external timeouts
                    print(f"  ⚠  TIMEOUT (external, skipped)  {url}")
                    continue
                except Exception as e:
                    print(f"  ⚠  ERROR (external, skipped)  {url}  ({e})")
                    continue

                if status in EXTERNAL_BROKEN:
                    broken.append((sources[0], url, status))
                    print(f"  ✗ {status}  {url}")
                    print(f"    linked from: {sources[0]}")

    # Report
    print()
    print("=" * 60)
    if not broken:
        print(f"✅ All links valid ({len(found_on)} checked across {len(crawled)} pages)")
        return 0
    else:
        print(f"❌ {len(broken)} broken link(s) found:\n")
        for source, url, status in broken:
            print(f"  {status}  {url}")
            print(f"       from: {source}")
        print()
        return 1


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "https://semanticinfrastructurelab.org"
    sys.exit(check_links(base))
