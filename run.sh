#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [[ ! -f "venv/pyvenv.cfg" ]]; then
  echo "Creating venv at ./venv ..."
  python -m venv venv
fi

# Activate venv (Linux/macOS) or Git-Bash on Windows
if [[ -f "venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "venv/bin/activate"
elif [[ -f "venv/Scripts/activate" ]]; then
  # shellcheck disable=SC1091
  source "venv/Scripts/activate"
else
  echo "Could not find venv activation script under ./venv" >&2
  exit 1
fi

cd "$ROOT_DIR/env"
python llm_env.py "$@"

