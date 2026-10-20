#!/usr/bin/env bash
# Runs the lqa checker tests.
set -euo pipefail
cd "$(dirname "$0")"
python3 -m unittest discover -s tests -v
