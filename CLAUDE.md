# PsychSim — operating instructions

## Long-running work: ALWAYS make it harness-tracked

The clearance gate takes **~78 minutes and grows with the connectome**. Two things are required, and
they solve *different* problems:

| Need | Mechanism | Fails if omitted |
|---|---|---|
| Survive the monitoring shell's SIGTERM | `setsid ... &` | job dies mid-run |
| Get notified on completion | Bash call with **`run_in_background: true`** | **no alert ever fires — you sit idle** |

**Use `tools/gate.sh`**, invoked via Bash with `run_in_background: true`. It launches the suite
detached *and* blocks until it exits, so completion actually re-invokes you.

```
tools/gate.sh              # full clearance gate
tools/gate.sh test_substrate test_aggression_pathway   # fast subset, same tracking
```

Never launch a long job with `setsid` alone and then promise to report back — a `setsid` process is
invisible to the harness, so no notification is generated. That mistake left a user polling
repeatedly while nothing was watching the run.

**Verify the artefact, not the launch.** A detached job can die silently: a `setsid` regrow once
produced a 0-byte log and left `library/adults.json` untouched while the shell reported "Done".
Check mtime / `git status` before believing a background step succeeded.

**Hung vs working:** `ps -p <pid> -o etime,time,pcpu`. CPU time ≈ elapsed at ~100% means it is
computing, not deadlocked. Long silences in the cohort-evolver modules (`test_engine`,
`test_environment_matrix`, `test_group_matrix`, `test_timeline`, `test_townlife`) are expected.

**Never `pkill -f run_tests.py`** — the launcher's own command line matches, so it self-kills. Kill by
PID.

## Reporting a gate

**A partial log is not evidence.** Report the *finished* gate with real counts — never "no failures so
far". If a gate was started, it must be returned to and reported; not reporting it is the same failure
as not running it.

## Connectome changes

Any node/edge added or removed invalidates `library/adults.json` (bank version-guard, keyed on
`len(model.connections)`). **Regrow is a mandatory step of the change, not a follow-up**, and the full
suite — not inline checks — is the clearance gate. Batch changes: regrow once at the end.

```
python3 -c "from sophropathy.library import build_default_library; print(build_default_library().save())"
```

Input-channel edges (`IN-*`) do **not** count toward the guard; adding a sensory band needs no regrow.

## Research discipline (these override default helpfulness)

- **Never tune a value to make a test pass.** A diagnosed red is honest; a green on an incomplete
  substrate is misleading. If a scalar seems load-bearing, the error is almost always a missing
  *mechanism* the number is standing in for — trace the pathway before touching the value.
- **Never add, remove, or defer real anatomy unilaterally.** Explicit permission is required, asked
  *before* acting — not remove-then-flag.
- **Never compress developmental time.** Wall-clock compression only.
- **Behaviour emerges.** Wire what an agent *perceives*; never script what it *does*. If you find
  yourself hardcoding which mode a selector picks, stop.
- **Measure before characterising.** A clean mechanistic story is a flag to measure, not a conclusion
  to act on. Several confident causal stories in this project were refuted by their own measurement.
- **Effect sizes on an incomplete substrate are upper bounds** (the S18 law: incompleteness inflates,
  grounding deflates — confirmed repeatedly). A result that *grows* under grounding is the anomaly.
- **Commit a checkpoint at every step** for rollback.
