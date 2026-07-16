# Expression Phase C — the display is the EFFECTOR output; vicarious<direct re-derived and it holds

Phase C re-points the distress display from the internal affective circuits to the **efferent expression
effectors**, and routes each onto the sense that actually perceives it. The vicarious/direct dissociation was
re-derived off the new display **and it holds** — reported with the disclosures the ruling required, nothing
preserved by default, nothing tuned.

## What was built (`arena.py`, `substrate/social.py` — no connectome change)
- **`_DISTRESS_DISPLAY` now reads the EFFECTORS** — `NuFac` (face) and `NuAmb-vocal` (voice) — never the
  affective circuits. The old `(CeA, vlPAG, BA)` display was reading the *drive*, not the *expression*; a
  co-located perceiver cannot see a CeA.
- **Each effector is presented on the sense that picks it up**, as two SEPARATE limbs:
  - face → `displayed_distress_face` → `IN-VIS:face_like` → `SC-Pv` → `CeA` (the seen face; short subcortical road)
  - cry → `displayed_distress_cry` → `IN-AUD:voice` → `A1-belt` → `LA` → `CeA` (the heard cry; longer cortical road)
- **Read above the bearer's FIXED rest activation** (`rest_activation`, a new memoised per-circuit rest
  reference), never the running `mean_activity`. **This closes chronic-distress invisibility at source:** the
  running mean adapts to sustained distress and hides it; a fixed rest reference keeps a chronically distressed
  face visible. Demonstrated — under chronic pain the effector display holds ~0.116 on the fixed reference
  while the running-mean reading fades toward 0. A face at rest still displays nothing (activation ≈ rest).

**Correction to the ruling, flagged in-code:** the ruling named `IN-CONSPEC:face_like`; that channel has **no
edges**. The real distress-face channel is `IN-VIS:face_like → SC-Pv` (the same one the appraisal path and the
observer probe already use). Built on the real channel.

## vicarious < direct — RE-DERIVED off the effector display, HOLDS
| | CeA | LC | VPL | S1 |
|---|---|---|---|---|
| **vicarious** (bearer's displayed face+cry) | 0.520 | 0.223 | 0.085 | 0.149 |
| **direct** pain (own nociception 0.9) | 1.000 | 0.354 | 0.490 | 0.423 |

- **vicarious CeA < direct CeA** (0.520 < 1.000), uncoded.
- **The sensory-discriminative route stays at rest for vicarious** (VPL 0.085, S1 0.149) but engages for direct
  (VPL 0.490, S1 0.423). Neither the seen face nor the heard cry carries the `IN-SOMATO:nociception → VPL →
  S1/S2` component direct pain has — the structural whole of the difference, intact on the new display.
- **Measurement limit unchanged:** the direct arm **saturates** (CeA=1.000), so the difference is a **lower
  bound**, not a ratio. Same limit that traveled with the original result.

**The dissociation is visible in the display itself:** bearer in pain displays face 0.067 / cry 0.003; bearer
in separation displays face 0.000 / cry 0.113. Pain drives the face, separation the voice — but see the
architectural caveat (S22): this is currently **guaranteed by an absence** (no PAG column reaches the face), a
weaker claim than one that survives Phase D's crosstalk. **Not stated as "the model shows a modality
dissociation."**

## ★ The disclosures the ruling required — carried, and one is a finding
- **The effector display is WEAK.** The perceiver's vicarious response moves CeA only 0.491 → 0.520 (Δ+0.029),
  because the effector displacement (face 0.067) is a far smaller signal than the old affective-hub display
  (0.472). This is **§18 from the other side**: the old affective-circuit display *overstated* the vicarious
  signal; the effector display is the honest, smaller magnitude. **Reported, not tuned** — the display is the
  bearer's actual efferent output, whatever it gives.
- **The vocal half runs on `PAG-PANIC` + `dPAG` only** — `vlPAG → NRA` is grounded and DORMANT (the freezing
  column has no drive, S20), so the display currently under-reads any distress routed through freezing.
- **The facial half runs on `BA → dACC → NuFac` alone**, in a cortex where 8 of 11 nodes are still unbraked (S18).
- **Effect sizes are biased upward** (S18): the *existence* of vicarious<direct is the safe claim; its
  *magnitude* is provisional.

## Contagion — damped by real dynamics, not the phasic trick
Removing the display's phasic adaptation (the old, fragile single-mechanism damper) does **not** make the
contagion loop run away: an 18-year 2-agent Arena stays **viable** (peak 0.952) and **settled**. The damping
now comes from the loop gain being <1 (the weak effector display + channel attenuation) and the perceiver's own
homeostasis — "at source", as ruled.

## Verification
- **Full suite green** (no regrow — no connectome change; 90 circuits / 226 edges unchanged; the change is
  Python: the effector read + two perception-channel triggers + the fixed-rest helper).
- `test_arena`, `test_observer`, `test_observer_substrate` all pass (25/25); the characterisation golden is
  unchanged (the display path is not exercised by the snapshot).
- Throttle set untouched. `DEFENSIVE_OUTPUT` untouched (a separate read-out).

## Registered
S22 (the modality dissociation is architectural — guaranteed by an absence — and is a Phase D measurement, not
a Phase C claim) · the reachability-vs-shortest-path method note · the byte-identical-twin anti-tuning pattern.
