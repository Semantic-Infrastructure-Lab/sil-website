"""
GitHub service - fetches live repository data.

This service makes HTTP calls to GitHub API for live stats.
"""

from typing import Optional

import httpx
import structlog

log = structlog.get_logger()


class GitHubService:
    """Service for fetching GitHub repository data."""

    def __init__(self, token: Optional[str] = None) -> None:
        """Initialize GitHub service.

        Args:
            token: Optional GitHub API token for higher rate limits
        """
        self.base_url = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github+json"}
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        self.log = log.bind(service="github")

    async def get_repo_stats(self, owner: str, repo: str) -> Optional[dict]:
        """Fetch repository statistics from GitHub.

        Args:
            owner: Repository owner (e.g., 'scottsen')
            repo: Repository name (e.g., 'morphogen')

        Returns:
            Dictionary with repo stats or None if request fails
        """
        url = f"{self.base_url}/repos/{owner}/{repo}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=self.headers, timeout=5.0)
                response.raise_for_status()

                data = response.json()
                stats = {
                    "stars": data.get("stargazers_count", 0),
                    "forks": data.get("forks_count", 0),
                    "watchers": data.get("watchers_count", 0),
                    "open_issues": data.get("open_issues_count", 0),
                    "description": data.get("description", ""),
                    "homepage": data.get("homepage"),
                    "language": data.get("language"),
                    "last_updated": data.get("updated_at"),
                }

                self.log.info("repo_stats_fetched", owner=owner, repo=repo)
                return stats

            except httpx.HTTPError as e:
                self.log.error(
                    "repo_stats_failed", owner=owner, repo=repo, error=str(e)
                )
                return None
