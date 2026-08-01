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
   export FLASK_APP=dashboard.app
   flask run --host=127.0.0.1 --port=5000

Contributing
- Keep tests that validate behavior using simulated inputs.
- Never add code that performs unauthorized actions against third-party accounts.
