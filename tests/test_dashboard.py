import unittest

from dashboard.app import app


class DashboardTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_index_route_returns_dashboard_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Latest findings (simulated)", response.data)

    def test_simulate_route_returns_simulation_details(self):
        response = self.client.get("/simulate/sim-1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Simulated remediation for sim-1", response.data)
        self.assertIn(b"Simulation details", response.data)
