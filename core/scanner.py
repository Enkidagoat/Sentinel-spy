"""
Scanner module (simulation-first).

This module provides a simple, safe interface for scanning sources.
By default it runs in simulation mode (returns canned sample posts).
If you add real connectors, implement Connector.fetch() and ensure
you have authorization to access those sources.
"""

from typing import List, Dict
import time
import yaml
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Connector:
    """Abstract connector interface for real integrations.

    Implementations MUST NOT perform unauthorized actions.
    """

    def fetch(self) -> List[Dict]:
        raise NotImplementedError


class SimulatorConnector(Connector):
    """Returns simulated public posts for development and testing."""

    def __init__(self, params: Dict = None):
        self.params = params or {}

    def fetch(self) -> List[Dict]:
        logger.debug("SimulatorConnector.fetch called")
        return [
            {
                "id": "sim-1",
                "source": "simulator",
                "text": "Example: credentials leaked for service X",
                "timestamp": time.time(),
                "metadata": {},
            },
            {
                "id": "sim-2",
                "source": "simulator",
                "text": "Routine post about deployment success",
                "timestamp": time.time(),
                "metadata": {},
            },
        ]


class Scanner:
    """High-level scanner that manages connectors."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.connectors = self._init_connectors()

    def _load_config(self) -> Dict:
        if not self.config_path.exists():
            return {}
        with open(self.config_path, "r") as fh:
            return yaml.safe_load(fh) or {}

    def _init_connectors(self) -> List[Connector]:
        connectors = []
        for src in self.config.get("scanner", {}).get("sources", []):
            if src.get("type") == "simulator":
                connectors.append(SimulatorConnector(src.get("params")))
            else:
                # For real connectors, add classes that implement Connector.fetch().
                logger.warning("Unknown connector type %s; skipping", src.get("type"))
        return connectors

    def run_once(self) -> List[Dict]:
        """Fetch from all connectors and return accumulated items."""
        results = []
        for c in self.connectors:
            try:
                results.extend(c.fetch())
            except Exception:
                logger.exception("Connector failed")
        return results
