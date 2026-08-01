"""
Report export placeholder — NO EXFILTRATION.

This module intentionally does NOT implement any functionality to
exfiltrate data outside of authorized, auditable channels.

Provided helpers:
- make_local_report(report_data, path): writes a local JSON report for audit.

If you need to securely archive reports, implement encryption and storage
only in ways that are auditable, legal, and compliant with policy.
"""

import json
from pathlib import Path
from typing import Any, Dict


def make_local_report(report: Dict, out_path: str = "logs/report.json") -> Path:
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    return p
