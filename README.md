# sentinel-spy

Lightweight scaffold for a monitoring + analysis demo. This repo provides:
- core/ — modular stubs for scanning, scoring, and remediation suggestions (safe-only)
- dashboard/ — a small Flask UI to view simulated findings
- run.sh — launcher scaffold

Important safety notice
- This repository intentionally does NOT implement account takeover, unauthorized access, or data exfiltration.
- Files named `disruptor.py` and `exfil.py` are placeholders and must NOT be used to implement harmful actions. They contain simulation-only helpers and remediation suggestions.
- Only implement connectors that access data for which you have explicit authorization and that comply with the target service's Terms of Service and applicable laws.

Usage (development)
1. Create a virtual environment and install dependencies:
   bash run.sh

2. Edit `config.yaml` with allowed sources and settings. The default scanner is a simulator that returns safe sample data.

3. Start the dashboard:
   source .venv/bin/activate
   export FLASK_APP=dashboard.app
   export FLASK_ENV=development
   flask run --host=127.0.0.1 --port=5000

Environment variables
- `FLASK_APP=dashboard.app` — required to run the Flask app.
- `FLASK_ENV=development` — optional; enables development mode and more verbose output.
- `FLASK_RUN_HOST=127.0.0.1` — optional; defaults the dashboard host.
- `FLASK_RUN_PORT=5000` — optional; defaults the dashboard port.

Testing
- A test suite now exists under `tests/` and covers:
  - `core.scanner` (simulator connector, config loading, unknown connector handling)
  - `core.scorer` (high/medium/low scoring behavior)
  - `core.disruptor` (remediation suggestions and simulation output)
  - `dashboard.app` routes (`/` and `/simulate/<item_id>`)
- Run the suite with:
  source .venv/bin/activate
  python3 -m unittest discover -s tests -p 'test*.py'

Contributing
- Keep tests that validate behavior using simulated inputs.
- Never add code that performs unauthorized actions against third-party accounts.
