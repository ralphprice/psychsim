# `887af5d` — Vicarious Routing — CLEARED — Claude Code

**Verified on the remote. Cleared. This is a clean build and the restraint in it is the point.**

## Verified
- **`_add_consequence_percept` (arena.py:298)** — body is a bare read-out:
  `evoked = sum(max(0, activation - mean_activity) * _gain(c) for c in live) / len(live)`.
  **Bearer-pure** (reads only `bearer.engine`), **phasic** (`activation - mean_activity`, floored at 0 → an
  agent at rest displays nothing), **no coded coefficient** — `_gain(c)` is the circuit's own existing gain,
  and `min(1.0, evoked)` is a range clamp to the trigger vocabulary, not a chosen reduction.
- Wired at `arena.py:345` into `_social_episode`, through the **existing** `vulnerable_other` trigger →
  `IN-VIS:biological_motion` → SC-Pv → CeA. **No parallel module.**
- The docstring states the discipline correctly and will survive us: *"NO vicarious<direct gain term and NO
  chosen cue intensity… the vicarious/direct relationship is MEASURED, never assumed."*

## What you got right, on the record
- **You accepted the correction and it paid.** `vicarious < direct` **emerged uncoded** (NA 0.127 vs 0.208)
  from the transduction chain — noxious 0.9 → the bearer's own evoked display 0.472 → the perceiver's NA
  0.127. **Nothing chose 0.472**; it is the bearer's circuits responding. Had we built either option, that
  number would have been ours and the substrate could never have told us anything about vicarious learning.
- **The structural dissociation carries it alone** — direct engages CeA *and* VPL/S1/S2; observed engages the
  affective route only (VPL/S1/S2 stay at rest). Verified, faithful, already there.
- **You carried the saturation caveat correctly**: direct pins CeA at 1.000 for every drive ≥0.4, so the
  ratio is unquantifiable and **the difference is a lower bound**. And the retro-reading is right — the
  earlier "≈ equal" was **both arms pinned, not equality**. That is the punishment-read-out lesson applied
  unprompted.
- **You checked the cross-agent feedback without being asked** (A's distress → B → A; viable 0.904, settled).
  Correct instinct — that is a new loop and the CeA↔LC arc earned that reflex.

## NEW FLAG (register) — the contagion loop is damped by the very property that is an open question

The substrate now has a **cross-agent positive feedback loop**: A's distress → display → B's CeA → B's
distress → display → A's CeA → … That is **emotional contagion** — a real phenomenon, and good that it
exists.

**It does not run away because the display is phasic**: `activation - mean_activity` adapts, so sustained
distress stops being displayed and the loop gain falls to zero. **That is the same phasic property that
dissolved the CeA↔LC latch** — which is reassuring, but it means:

> **The contagion loop's stability currently DEPENDS on the display's phasic adaptation — and whether the
> display should be phasic is itself an open question (the registered "per-edge phasic character" entry).**
> If that character is ever revised, **the contagion loop must be re-checked in the same change.** Link the
> two register entries.

**And the open question has a study-relevant edge worth recording now:** because `mean_activity` is a running
average, **an agent in sustained distress adapts and stops displaying** — so others stop learning vicariously
from it. Display habituation is real, but people in sustained pain do not stop showing it entirely. Whether
our display should adapt *to zero* is the per-edge-phasic question applied to the display — and it bears
directly on the **chronic-adversity conditions the studies care about** (a chronically distressed child that
becomes invisible to observers is either a real phenomenon or an artifact of the adaptive baseline). Register
it; do not act on it now.

## Status
Cleared. Deferred/registered as ruled: life-course accumulation (CeA operating point), construct-validity
standing check, throttle-set audit — plus the contagion/phasic-display link above.

**Hold for the researcher's steer on phase sequencing before starting the next build.**
