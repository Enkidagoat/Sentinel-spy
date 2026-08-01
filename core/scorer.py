"""
Simple scoring utilities.

This module provides a conservative, explainable scoring mechanism
that ranks items based on keyword matches. It purposefully avoids
any functionality that would enable offensive actions.
"""

from typing import Dict, List
import yaml
from pathlib import Path


class Scorer:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = {}
        p = Path(config_path)
        if p.exists():
            import yaml as _yaml
            with open(p, "r") as fh:
                self.config = _yaml.safe_load(fh) or {}

        self.keywords = self.config.get("scoring", {}).get("keywords", {})
        self.thresholds = self.config.get("scoring", {}).get("thresholds", {"high": 10, "medium": 5})

    def score_text(self, text: str) -> Dict:
        score = 0
        matches = []
        text_l = text.lower()
        for word in self.keywords.get("high_risk", []) + self.keywords.get("medium_risk", []):
            if word.lower() in text_l:
                matches.append(word)
                # high_risk terms could weigh more
                weight = 5 if word in self.keywords.get("high_risk", []) else 2
                score += weight

        level = "low"
        if score >= self.thresholds.get("high", 10):
            level = "high"
        elif score >= self.thresholds.get("medium", 5):
            level = "medium"

        return {"score": score, "level": level, "matches": matches}
