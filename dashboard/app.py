"""
Small Flask dashboard for viewing simulated scan results.

This app runs only local/simulated scans by default and displays findings.
It exposes no destructive endpoints and includes a simulation-only "run scan" button.
"""

from flask import Flask, render_template, redirect, url_for, flash
from core.scanner import Scanner
from core.scorer import Scorer
from core.disruptor import simulate_remediation_flow
import logging

app = Flask(__name__)
app.secret_key = "dev-secret-key"  # for development only
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

scanner = Scanner()
scorer = Scorer()


@app.route("/")
def index():
    items = scanner.run_once()
    scored = []
    for it in items:
        s = scorer.score_text(it.get("text", ""))
        scored.append({"item": it, "score": s})
    return render_template("index.html", findings=scored)


@app.route("/simulate/<item_id>")
def simulate(item_id):
    # In this scaffold we find the item in the latest run (simulation)
    items = scanner.run_once()
    match = next((i for i in items if i.get("id") == item_id), None)
    if not match:
        flash("Item not found", "warning")
        return redirect(url_for("index"))
    sim = simulate_remediation_flow(item_id)
    flash(f"Simulated remediation for {item_id}", "info")
    return render_template("index.html", findings=[{"item": match, "score": scorer.score_text(match.get("text", "")), "simulation": sim}])
