# D6 CLOSEOUT — build instructions for the Claude Code session
### From the reviewer. One ordered pass. Nothing new opens. When this lands, D6 is closed.

**Machine framing dropped — nothing is gated. This is a normal build-and-suite pass. Three builds, two
finding-confirmations, one closure. In order. Do not open any new substrate work; the surfacing rule (§ end)
is part of the instruction.**

---

## BUILD 1 — `VMH → vlPAG` weight → strong (behaviourally live)

**What changes:** exactly one connection's weight. `VMH → vlPAG`: `low-moderate` → **`strong`**.
- `dominant_receptor` stays **AMPA** (already grounded). `source_circuit`/`target_circuit` unchanged. Sign
  unchanged (+, glutamatergic).
- `default_weight_basis`: `anatomy` → **`literature`** (Wang, Chen & Lin, *Neuron* 2015 — VMHdm/c→PAG is a
  behaviourally-decisive immobility drive, not a weak modulator).

**Record the column caveat in the connection's note** (do NOT re-point the edge): *this edge stands in for
`VMH → dlPAG`; it currently lands on `vlPAG` because the dorsolateral column is fused into `dPAG` (the dl/l
lump). Correction condition: the dl/l split (registered, not this pass).*

**Gate:** full suite. **This is NOT inert** — expect the golden to move and possibly the freezing floor to
change colour. **Deliberate, documented golden regen** — state the reason (driver strength grounded), confirm
the moved values are freezing-column-adjacent and expected.

---

## BUILD 2 — S57 step 2: apply the five maturation curves (behaviourally live)

**The mechanism (`a053a9d`) exists. This binds the five nodes to it.** For each, set `baseline` = the ADULT
target and `baseline_schedule_ref` = the named family:

| circuit | adult baseline | schedule family | shape |
|---|---|---|---|
| **DRN** | ~0.30 | `pfc_low_early_high_late` | monotonic low→high (frontal-inhibition-gated — grounded identification, not a pick) |
| **LC** | **0.15** (already its value → now the MATURE ENDPOINT of the curve, not a constant) | a low-early-high-late family | monotonic |
| **SNc** | ~0.18 | an early-plateau family | monotonic, early mature-age |
| **VTA** | **~0.136 (adult SETTLE, NOT the 0.18 peak)** | `adolescent` (Gaussian bump) | low→peak(0.18 @ ~16y)→settle |
| **BF-ACh** | ~0.25 | a steady-rise family | monotonic, childhood |

**Two hard notes:**
- **VTA's `baseline` is the adult settle (~0.136), and the `adolescent` schedule produces the 0.18 peak in
  adolescence.** Do NOT put 0.18 as the baseline — that was the peak, mislabelled in an earlier table. Your
  own preview (0.180 @ 16y → 0.136 @ 25y) is the correct curve; confirm it still holds.
- **Record `DRN`'s baseline-semantics note** (from `5756190`): the value is the *functional inhibitory
  efficacy* of the 5-HT system (matures UP via 5-HT1A-autoreceptor + frontal-innervation maturation), NOT
  tissue 5-HT (which peaks in infancy and falls). This is why the curve is low→high. Keep it in `DRN`'s
  function field so no one re-grounds it to tissue level and inverts it.

**Gate:** full suite. **Behaviourally live, large** (all development changes). **Deliberate, documented golden
regen.**

---

## CONFIRM — the two emergent findings (measure, don't build)

After Builds 1–2, run these as measurements and report the curves:
1. **Tremblay aggression trajectory:** provocation-aggression across age — expect **peak ~age 2, monotonic
   decline through childhood, cross to restraint ~adolescence, adult restraint** — with **no aggression leak
   at any age**. (Preview showed this; confirm it survives the full apply + `VMH→vlPAG` strong.)
2. **Adolescent reward-seeking:** reward-approach across age — expect **rise into adolescence, peak, settle**,
   tracking the VTA curve.

**These are the branch's payoff — two developmental phenomena EMERGING from grounded maturation curves, not
coded. If either does NOT emerge, STOP and report** — that is a finding either way and must not be smoothed.

---

## CONFIRM — the deletion (`0.1`, the outstanding item on `MeA→ATL-TP`)

Run the **full suite** against the current state (post-`a11c588` deletion) and confirm: **all four
classification labels byte-identical, no unexpected suite failures beyond the one authorized red** (which
Builds 1–2 may themselves resolve). **This closes S64's open gate** — the deletion becomes confirmed, not just
committed.

---

## THE FREEZING FLOOR VERDICT

After Builds 1–2, the floor's positive half is testable for the first time on grounded terms. **Report which:**
- **Green** → freezing fires when the driver is at grounded strength AND DRN is on its curve. The floor's
  authorized red is retired. **The freezing column WORKS.**
- **Still red** → report the residual. Per the earlier ruling, the floor's positive half was resting on
  scaffold balance; with two of those terms now grounded, a residual red is informative and points at the
  next real term (likely the selector's afferents or the gate-family baseline — both type-(b) backlog, NOT to
  be chased in this pass).

Either outcome closes D6's *claim* — the mechanism is now tested, which is the exit condition.

---

## CLOSE D6 — the important step

**After the above, D6 is closed by the testable-claims rule.** Do this explicitly:
1. **Update the return-path register: D6 CLOSED**, with the freezing-floor verdict recorded.
2. **Move ALL remaining substrate items to a `substrate_hardening_backlog` section** — do NOT open any:
   - the opioid system (multi-register, its own diagnosis)
   - the dl/l `dPAG` split (substrate-shape diagnosis; `VMH→vlPAG`'s correction condition)
   - S56 nine-node gate calibration (mechanism-design question)
   - the lump census (12 lumps, `MeA`'s SPLIT-BLOCKED edges, PBN subnuclei)
   - the input-surface gaps (PB-LOOMING, predator odor, IN-PROPRIO, etc.)
   - `noci→PBN` — **already closed-superseded** (S55; the PGi arc's `IN-SOMATO:nociception→PGi` serves it)
   - the 47 assumption-based connections + the §18 systemic conditions → **these feed the 209-connection
     audit, a later scoped STAGE, not backlog to chase now**
3. **The backlog is revisited ONLY if a later layer's testable claim requires a specific item.** That is the
   surfacing rule. Rabbit holes wait in the register.

---

## NEXT (not this pass — for the map): the climb begins at **D4 (imitation/modeling)**, then **D3
(representation — the purpose)**. The next deep dive is D3, and it is opened because it is the purpose, not
because a synapse is ungrounded.

---

### SURFACING RULE (part of this instruction)
**Nothing new opens in this pass.** If the build surfaces a new sub-problem, **triage it**: does it block one
of the confirmations above? If yes, report it and hold for a ruling. **If no, register it in
`substrate_hardening_backlog` and keep going.** We are closing D6, not enriching the substrate. The floor is
built. After this, we climb.
