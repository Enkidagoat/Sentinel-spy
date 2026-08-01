#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# Activate & install
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Virtualenv created and dependencies installed. To run the dashboard:"
echo "  source .venv/bin/activate"
echo "  export FLASK_APP=dashboard.app"
echo "  flask run --host=127.0.0.1 --port=5000"
