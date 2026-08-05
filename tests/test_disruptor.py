import unittest

from core.disruptor import suggest_remediation, simulate_remediation_flow


class DisruptorTests(unittest.TestCase):
    def test_suggest_remediation_returns_steps(self):
        steps = suggest_remediation("account-123")

        self.assertIsInstance(steps, list)
        self.assertGreaterEqual(len(steps), 1)
        self.assertTrue(all("action" in step and "description" in step for step in steps))

    def test_simulate_remediation_flow_returns_simulated_status(self):
        result = simulate_remediation_flow("account-123")

        self.assertEqual(result["account"], "account-123")
        self.assertEqual(result["status"], "simulated")
        self.assertIsInstance(result["simulated_steps"], list)
        self.assertEqual(result["simulated_steps"], suggest_remediation("account-123"))
