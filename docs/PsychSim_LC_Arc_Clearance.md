# LC Arc `0d03054` — REVIEWER CLEARANCE (+ one serious follow-up) — Claude Code

**CLEARED on every ruled item — verified against the remote. The arc is sound and the discipline held
throughout. But the review found one thing the full suite CANNOT see, and it is serious: it must be fixed
before anything runs a life-course.**

---

## Verified on the remote — all clear

| ruled | verified at `0d03054` |
|---|---|
| `CeA->LC` via cited CRF-R1 | PRESENT, `recep=CRF-R1`, and `params.py:49` carries `"CRF-R1": +1  # Gs-coupled -> excitatory (standard CRF-R1 pharmacology)` — cited, not asserted |
| alpha2 `LC->LC` non-plastic, grounded, not load-bearing | PRESENT, `plasticity_schedule=None`, **bounds-pinned [0.5, 0.5]**, dropped from 0.85 to its grounded value per the ruling |
| LC pacemaker, grounded not window-fit | `baseline=0.15` — and **VTA remains 0.05**, so LC was individually raised on its own electrophysiology, not a blanket change |
| B dropped | `CeA->CeA-GABA` ABSENT; `CeA-GABA` afferents = `[PVN-OT]` only. Correct |
| PBN/NTS deferred not added | both ABSENT — correctly registered, not built |
| the dead hub is alive | LC afferents `[CeA, LC]` (was **ZERO**) |
| phasic drive | in `engine.py` with the CRF grounding in-comment ("CRF release fires on the event and adapts, it does not clamp LC at CeA's plateau level") |
| additive | edge count 212 -> 214 (+CeA->LC, +LC->LC) |

Read-out, seeds, registers, artifact retirement, acting-readiness handling: all as ruled.

---

## FINDING 1 (serious — fix before any life-course run)

**LC's pacemaker baseline (0.15) now sits ABOVE its homeostatic setpoint (0.1, the untouched generic
default). This creates an unsatisfiable homeostatic pressure that will erode `CeA->LC` toward zero over a
life-course — re-killing the NA teaching signal this entire arc exists to create.**

Mechanism, verified:
- `engine.py:185` — `da = (dt/tau) * (-(a[cid] - c.baseline) + inp)`. **`baseline` is the resting level**:
  with no input, activation relaxes *to* 0.15. The pacemaker is a floor, as intended.
- `mean_activity` is a running average of activation -> settles **>= 0.15**.
- `homeo_factor = 1.0 - HOMEO_RATE * (mean_activity - setpoint)` = `1 - 0.002*(0.15-0.1)` = **0.9999**,
  applied to **all** LC incoming weights every `HOMEO_EVERY=20` steps.
- **The target is unreachable**: homeostasis cannot pull LC below 0.15, because the relaxation always
  restores it. So the pressure never satisfies — it scales *forever*.
- `CeA->LC` bounds are **[0.0, 1.0]** — nothing stops the erosion. `0.9999^10000` ~ 0.37;
  `0.9999^50000` ~ 0.007.

**Why the suite missed it:** tests run short horizons. This compounds only over a life-course — precisely the
"small error, run over a lifetime, becomes nonsense" failure mode. It is silent and slow.

**The fix (grounded, same electrophysiology as the baseline):** **LC's `homeostatic_setpoint` should BE its
pacemaker rate.** A homeostatic setpoint is a neuron's *target firing rate*; for an autonomous pacemaker that
target IS the pacemaker rate. `baseline=0.15` with `setpoint=0.1` asserts two contradictory things about the
same neuron ("its intrinsic resting rate is 0.15" / "its homeostatic target is 0.1"). Raise the setpoint to
match the grounded pacemaker rate, on the same citation. Then `homeo_factor = 1.0` at rest — homeostasis and
the pacemaker **agree instead of fight**.

**This is a paired-value consistency rule, not a tune:** `baseline_activation` and `homeostatic_setpoint`
describe the same quantity (the circuit's intrinsic target rate) and must be set together. **Add to the
provisional-baselines register entry:** it is now *baselines AND their paired setpoints* — and LC is the
first demonstration that the generic 0.05/0.1 default pair breaks the moment one half is individually
grounded.

**Verify after the fix:** `homeo_factor` ~ 1.0 for LC at rest; `CeA->LC` stable over a long run (not eroding);
NA still fires phasically; full suite still green.

---

## FINDING 2 (register)

**The R4 homeostatic loop has NO plasticity guard.** `engine.py:226-231` scales **all** incoming weights —
guards are only `live_conn` / `not pruned`. So `plasticity_schedule=None` does **NOT** exempt an edge from
homeostatic scaling. The alpha2 survives *only* because it is bounds-pinned `[0.5, 0.5]`.

This is a partial category inconsistency: an edge marked non-plastic (a structural element, not a learned
association — the correct category call) **can still be modified by R4**. Register:
- Any future "non-plastic" designation must **also bounds-pin** to actually be non-plastic.
- Open question: should R4 skip `plasticity_schedule=None` edges outright, so "non-plastic" means what it
  says in one place rather than requiring two mechanisms to enforce it?

---

## Status
The arc is **cleared** — nothing to revert. **Finding 1 is a required follow-up before any life-course run**
(small, grounded, one value + its citation). Finding 2 is a register entry. Bring the setpoint fix for review;
then the next phase.
