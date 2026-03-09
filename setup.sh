#!/bin/bash
# Setup script for greeting-card-pdf plugin
# Creates an isolated Python venv with Playwright + Chromium

set -e

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PLUGIN_DIR/.venv"

if [ -d "$VENV_DIR" ]; then
  echo "greeting-card-pdf: venv already exists at $VENV_DIR"
  exit 0
fi

echo "greeting-card-pdf: creating venv..."
python3 -m venv "$VENV_DIR"

echo "greeting-card-pdf: installing Playwright..."
"$VENV_DIR/bin/pip" install --quiet playwright

echo "greeting-card-pdf: installing Chromium (this may take a minute)..."
"$VENV_DIR/bin/python3" -m playwright install chromium

echo "greeting-card-pdf: setup complete."
