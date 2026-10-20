#!/usr/bin/env bash
# Installs the lqa skill into Claude Code's personal skills folder.
set -euo pipefail
cd "$(dirname "$0")"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/lqa"
bash test.sh >/dev/null
mkdir -p "$DEST"
rsync -a --delete --exclude '__pycache__' lqa/ "$DEST/"
echo "Installed lqa to $DEST"
