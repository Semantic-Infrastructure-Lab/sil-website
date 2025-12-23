"""
Metrics service for loading canonical SIL/SIF metrics.

Loads metrics from canonical YAML file in TIA repository.
Single source of truth for all production metrics.
"""

from pathlib import Path
from typing import Any, Dict

import yaml


class MetricsService:
    """Service for loading and providing canonical metrics."""

    def __init__(self, metrics_path: Path | None = None):
        """Initialize metrics service.

        Args:
            metrics_path: Path to metrics YAML file. If None, uses canonical TIA path.
        """
        if metrics_path is None:
            # Default to canonical TIA metrics file
            # This assumes sil-website is at /home/scottsen/src/projects/sil-website
            # and TIA is at /home/scottsen/src/tia
            metrics_path = Path.home() / "src" / "tia" / "metrics" / "sil-metrics.yaml"

        self.metrics_path = metrics_path
        self._metrics: Dict[str, Any] | None = None

    def _load_metrics(self) -> Dict[str, Any]:
        """Load metrics from YAML file.

        Returns:
            Metrics dictionary

        Raises:
            FileNotFoundError: If metrics file doesn't exist
            yaml.YAMLError: If YAML parsing fails
        """
        if not self.metrics_path.exists():
            raise FileNotFoundError(
                f"Metrics file not found: {self.metrics_path}\n"
                "Expected canonical metrics at: ~/src/tia/metrics/sil-metrics.yaml"
            )

        with open(self.metrics_path) as f:
            return yaml.safe_load(f)

    @property
    def metrics(self) -> Dict[str, Any]:
        """Get metrics (cached).

        Returns:
            Complete metrics dictionary
        """
        if self._metrics is None:
            self._metrics = self._load_metrics()
        return self._metrics

    def reload(self) -> None:
        """Reload metrics from file (useful for development)."""
        self._metrics = None

    # Convenience accessors for common metrics

    @property
    def reveal(self) -> Dict[str, Any]:
        """Get Reveal system metrics."""
        return self.metrics["systems"]["reveal"]

    @property
    def morphogen(self) -> Dict[str, Any]:
        """Get Morphogen system metrics."""
        return self.metrics["systems"]["morphogen"]

    @property
    def tiacad(self) -> Dict[str, Any]:
        """Get TiaCAD system metrics."""
        return self.metrics["systems"]["tiacad"]

    @property
    def genesisgraph(self) -> Dict[str, Any]:
        """Get GenesisGraph system metrics."""
        return self.metrics["systems"]["genesisgraph"]

    @property
    def sil_website(self) -> Dict[str, Any]:
        """Get SIL website info."""
        return self.metrics["websites"]["sil"]

    @property
    def sif_website(self) -> Dict[str, Any]:
        """Get SIF website info."""
        return self.metrics["websites"]["sif"]

    @property
    def lab(self) -> Dict[str, Any]:
        """Get lab metrics (team, sessions, etc)."""
        return self.metrics["lab"]

    def get_display_metric(self, system: str, metric: str) -> str:
        """Get display-formatted metric.

        Args:
            system: System name (e.g., "reveal", "morphogen")
            metric: Metric name (e.g., "version", "downloads.monthly_display")

        Returns:
            Formatted metric value

        Example:
            >>> metrics.get_display_metric("reveal", "version")
            "0.25.0"
            >>> metrics.get_display_metric("reveal", "downloads.monthly_display")
            "3K+"
        """
        parts = metric.split(".")
        value = self.metrics["systems"][system]
        for part in parts:
            value = value[part]
        return str(value)
