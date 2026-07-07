#!/usr/bin/env bash
# sync.sh — commit any pending changes and push to origin/main.
#
#   ./sync.sh                 # commit with an auto timestamp message, then push
#   ./sync.sh "message"       # commit with your message, then push
#
# Safe to run anytime: if the working tree is clean it just reports and exits.
set -euo pipefail
cd "$(dirname "$0")"

if [ -z "$(git status --porcelain)" ]; then
  echo "Nothing to sync — working tree clean."
  exit 0
fi

msg="${1:-sync: $(date '+%Y-%m-%d %H:%M')}"
git add -A
git commit -q -m "$msg"
git push -q origin main
echo "Synced to origin/main: $msg"
