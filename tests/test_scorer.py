import unittest
import tempfile
from pathlib import Path
import yaml

from core.scorer import Scorer


class ScorerTests(unittest.TestCase):
    def test_score_text_with_high_risk_keyword(self):
        config = {
            "scoring": {
                "keywords": {"high_risk": ["leak"], "medium_risk": ["breach"]},
                "thresholds": {"high": 5, "medium": 2},
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config_path.write_text(yaml.safe_dump(config))

            scorer = Scorer(config_path=str(config_path))
            result = scorer.score_text("Example leak detected")

            self.assertEqual(result["level"], "high")
            self.assertEqual(result["score"], 5)
            self.assertIn("leak", result["matches"])

    def test_score_text_with_medium_risk_keyword(self):
        config = {
            "scoring": {
                "keywords": {"high_risk": ["leak"], "medium_risk": ["breach"]},
                "thresholds": {"high": 10, "medium": 2},
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config_path.write_text(yaml.safe_dump(config))

            scorer = Scorer(config_path=str(config_path))
            result = scorer.score_text("A breach occurred")

            self.assertEqual(result["level"], "medium")
            self.assertEqual(result["score"], 2)
            self.assertIn("breach", result["matches"])

    def test_score_text_without_keywords(self):
        config = {
            "scoring": {
                "keywords": {"high_risk": ["leak"], "medium_risk": ["breach"]},
                "thresholds": {"high": 10, "medium": 5},
            }
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config_path.write_text(yaml.safe_dump(config))

            scorer = Scorer(config_path=str(config_path))
            result = scorer.score_text("A normal status update")

            self.assertEqual(result["level"], "low")
            self.assertEqual(result["score"], 0)
            self.assertEqual(result["matches"], [])
