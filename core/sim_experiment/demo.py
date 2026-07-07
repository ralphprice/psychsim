"""demo.py -- run the factorial experiment and report it."""
from __future__ import annotations
from .batch import run_factorial
from .lifecourse import run_life
from .conditions import seeds, conditions


def report(n_runs: int = 30) -> str:
    L = ["", "#" * 92,
         "  LIFE-COURSE EXPERIMENT: trait configuration x moral environment",
         f"  {n_runs} independent life courses per cell; outcome read from behaviour",
         "#" * 92, ""]

    fr = run_factorial(n_runs=n_runs)
    L.append(fr.table())

    # a worked single life with its stage-by-stage trace
    L.append("")
    L.append("  ONE LIFE, TRACED STAGE BY STAGE (shared_root, harsh home then warm turn):")
    sp = conditions()["harsh_home_then_warm_turn"]
    r = run_life(seeds()["shared_root"], sp, trace=True)
    for step in r.stage_trace:
        L.append(f"     {step}")
    L.append(f"     => final: {r.classification}"
             + (f" / {r.psychopathy_subtype}" if r.psychopathy_subtype else ""))
    L.append("")
    L.append("  READING: with the fearless root disposition held fixed, the moral")
    L.append("  environment moves the outcome; and because plasticity declines with")
    L.append("  age, WHEN in the life course the environment is warm or harsh matters,")
    L.append("  not just whether it is. This is the counterfactual a real cohort")
    L.append("  cannot run: same disposition, different life, measured impact.")
    L.append("#" * 92)
    return "\n".join(L)
