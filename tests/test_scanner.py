import unittest
import tempfile
from pathlib import Path
import yaml

from core.scanner import Scanner, SimulatorConnector


class ScannerTests(unittest.TestCase):
    def test_simulator_connector_fetch_returns_items(self):
        conn = SimulatorConnector()
        items = conn.fetch()

        self.assertIsInstance(items, list)
        self.assertGreaterEqual(len(items), 1)
        self.assertEqual(items[0]["source"], "simulator")

    def test_scanner_loads_config_and_runs(self):
        config = {"scanner": {"sources": [{"name": "example_source", "type": "simulator", "params": {}}]}}
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config_path.write_text(yaml.safe_dump(config))

            scanner = Scanner(config_path=str(config_path))
            items = scanner.run_once()

            self.assertGreaterEqual(len(items), 1)
            self.assertEqual(items[0]["source"], "simulator")

    def test_scanner_skips_unknown_connector_types(self):
        config = {"scanner": {"sources": [{"name": "bad_source", "type": "unknown", "params": {}}]}}
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "config.yaml"
            config_path.write_text(yaml.safe_dump(config))

            scanner = Scanner(config_path=str(config_path))
            self.assertEqual(scanner.connectors, [])
            self.assertEqual(scanner.run_once(), [])
