#!/usr/bin/env bash
# PsychSim clearance gate -- launches the suite DETACHED (survives the monitoring shell's SIGTERM)
# and BLOCKS until it finishes, so that when this script is invoked via Bash with
# run_in_background: true the harness fires a real completion notification.
#
#   tools/gate.sh                                   # full clearance gate
#   tools/gate.sh test_substrate test_scan          # fast subset, same tracking
#
# Both halves matter: setsid alone is invisible to the harness (no alert ever fires);
# run_in_background alone can be SIGTERM'd mid-run. See CLAUDE.md.
set -uo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)

LOG=${GATE_LOG:-"${TMPDIR:-/tmp}/psychsim-gate-$(date +%Y%m%d-%H%M%S).log"}
export PYTHONPATH="core:extensions:."

if [ $# -gt 0 ]; then
  MODULES=(); for m in "$@"; do MODULES+=("tests.${m#tests.}"); done
  CMD=(python3 -u -m unittest "${MODULES[@]}" -v)
  WHAT="subset: $*"
else
  CMD=(python3 -u -m unittest discover -s tests -v)
  WHAT="FULL clearance gate"
fi

echo "=== PsychSim gate: $WHAT"
echo "=== started $(date '+%F %T')   log: $LOG"
echo "=== NOTE: the full gate is ~78 min and grows with the connectome. Silence is not a hang."

# guard: one suite at a time (concurrent runs contend on library/ and corrupt each other)
if pgrep -f "[u]nittest (discover|tests\.)" >/dev/null 2>&1; then
  echo "!!! ABORT: a suite is already running -- run ONE at a time:"
  ps -eo pid,etime,args | grep "[u]nittest" | cut -c1-110
  exit 2
fi

setsid "${CMD[@]}" > "$LOG" 2>&1 < /dev/null &
sleep 2
PID=$(pgrep -n -f "[u]nittest (discover|tests\.)" || true)
if [ -z "$PID" ]; then
  echo "!!! gate failed to start -- log follows:"; cat "$LOG"; exit 1
fi
echo "=== running as pid $PID; waiting for it to finish ..."

tail --pid="$PID" -f /dev/null          # blocks until the detached suite exits

echo
echo "=============== GATE FINISHED $(date '+%F %T') ==============="
tail -30 "$LOG"
echo
echo "--- FAIL / ERROR ---"
grep -E "^(FAIL|ERROR):" "$LOG" || echo "  (none)"
echo "--- full log: $LOG ---"

# exit non-zero if the suite did not report OK, so the outcome is unambiguous
grep -qE "^OK" "$LOG" && exit 0 || exit 1
