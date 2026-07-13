# HSO M3.1 — Claude Code handover: the cross-homeostatic rule replacement

**Sealed design authority: `docs/PsychSim_HSO_M3_Rebuild_SPEC.md`** (and its parent
`docs/PsychSim_Homeostatic_SelfOrganization_SPEC.md`). Build against them. This handover covers **M3.1
ONLY** — replace the inert single-setpoint homeostatic rule with a working **cross-homeostatic** rule,
and prove it converges. This is the riskiest piece of the whole rebuild; prove it alone before anything
else (M3.2 timescales, M3.3 setpoints, M3.4 verification, M3.5 suite) is touched.

Context: M1/M2 (dual-verified, fe0a34a) found the homeostatic machinery **present-but-hollow** — the
current rule at rate 0.002 corrects ~0.14%/step (~10× too weak), activity never reaches setpoint,
weights are seed-default-dominated. **Verdict: full rebuild.** M3.1 is the first and hardest step.

---

## 0. What M3.1 IS and IS NOT

- **IS:** replace `homeo_factor` (the single-setpoint multiplicative rule) with the cross-homeostatic
  rule (spec §2.1); demonstrate it **converges** (activity reaches setpoint, perturbations self-correct)
  **without oscillating**, on the CURRENT uniform 0.1 setpoints (grounding the setpoints is M3.3 — M3.1
  isolates the *rule* from the setpoint values so we answer one question: does the rule converge at all?).
- **IS NOT:** grounding setpoints (M3.3), grounding timescales (M3.2), the full self-organization battery
  (M3.4), re-integrating v14 (M5), or observing emergent behaviour (M4). And **NOT** "make the old rule's
  rate bigger" — see §2.

**The one question M3.1 answers:** does the cross-homeostatic rule form converge — pull circuits to
setpoint, self-correct perturbations, without ringing? If yes, the rebuild is viable and M3.2/3.3/3.4
proceed. If it *can't* be made to converge, that's a finding to surface before going further.

---

## 1. The exact code to replace

- **The rule:** `core/substrate/plasticity.py:105` —
  `homeo_factor(mean_activity, setpoint, rate) = 1.0 - rate*(mean_activity - setpoint)`. This is the
  single-setpoint multiplicative rule. **Replace it** (don't just re-rate it — §2).
- **The call site:** `core/substrate/engine.py:196` — applied every `params.HOMEO_EVERY` (20) steps, over
  each circuit's **incoming** weights, clamped to bounds. The new rule plugs in here.
- **`params.HOMEO_RATE = 0.002`** (plasticity comment: "must beat BCM growth") — M2 showed it's ~10× too
  weak; but the fix is the RULE FORM, and the rate is then set by the convergence criterion (§3), not
  hand-picked.

---

## 2. Why NOT "just make it stronger" (the trap — spec §1)

The naive inference from "the rule is ~10× too weak" is "multiply HOMEO_RATE by 10." **Do not build
this.** A single-setpoint multiplicative rule strong enough to actually reach setpoint **oscillates** — a
large-gain single-target negative feedback overshoots and rings. The literature is explicit: the stable
solution is a **different rule form** (cross-homeostatic), not a bigger rate on the same form. So M3.1 is
a rule *replacement*. (This is the project's core lesson at the mechanism level: the fix for a weak rule
is the right *form*, not a tuned *constant*. A rate that merely converges is found by the convergence
criterion and *any* rate in the converging range works — the rule form guarantees such a range exists;
that's what distinguishes it from threading a fudge value.)

---

## 3. The cross-homeostatic rule (grounded — spec §2.1)

Grounding: the cross-homeostatic family "autonomously tune[s] the network to produce robust, self-
sustained dynamics in an inhibition-stabilized regime" by "tuning all synaptic weight classes in
parallel" (Cartiglia et al. 2025, *Nat Commun* 16); nonlinear inhibitory plasticity stabilizes excitatory
synapses without upper bounds (Agnes & Vogels 2022, *PLoS Comput Biol*); local scaling lets heterogeneous
networks self-organize "without precise initialization" (2025).

### 3.1 The core idea — tune E and I incoming weights SEPARATELY against the postsynaptic setpoint
The "cross" property: for a circuit *c* over-active relative to its setpoint, the rule **both** down-
scales its incoming **excitatory** weights **and** up-scales its incoming **inhibitory** weights; when
under-active, the reverse. Because E and I are adjusted in opposite directions against the *same*
postsynaptic setpoint, the system converges to an **inhibition-stabilized balance** instead of ringing
(the single-sided rule only scaled all incoming weights one way, which can't balance E against I).

### 3.2 The critical implementation detail — the E/I split uses the EXISTING sign
The rule needs to know, per incoming edge, whether it's excitatory or inhibitory. **This information
already exists — do NOT add a new field.** Each edge's sign is derived from its `dominant_receptor` via
the v12a `RECEPTOR_SIGN` table (the same `_sign()` the engine already uses to apply the weight). So:
- For circuit *c*, partition its incoming edges into **excitatory** (sign +1) and **inhibitory** (sign −1)
  using the existing sign derivation.
- Apply the cross-homeostatic update: excitatory-incoming scaled by a factor **decreasing** in
  (*ā_c − s_c*); inhibitory-incoming scaled by a factor **increasing** in (*ā_c − s_c*).
- Edges on the transmitter fallback (no `dominant_receptor`) use their fallback sign, same as the engine
  does now — consistent with existing behaviour.

### 3.3 Concrete form (finalize against the rate model — sealed ruling #1)
Resolve the exact update at build against the rate model — the simplest cross-homeostatic form that
converges. A reasonable starting form (to validate, not assume):
- excitatory incoming: `w_E *= 1 - rate_E * (ā_c - s_c)`
- inhibitory incoming: `w_I *= 1 + rate_I * (ā_c - s_c)`
with `rate_E`, `rate_I` set so the system converges (§4) — and if a single symmetric rate converges,
prefer it (fewer knobs). **The acceptance test (§4) decides the form and the rate; do not hand-pick to a
behaviour.** If the simplest form oscillates, the literature's nonlinear-inhibitory variant (Agnes &
Vogels) is the next form to try — surface the choice with the convergence evidence.

---

## 4. Acceptance tests (M3.1 is done when these pass — spec §0, §2.3)

Run on the CURRENT uniform 0.1 setpoints (setpoint grounding is M3.3):
1. **Convergence:** pin a circuit far from setpoint (the CeA-at-0.8, setpoint-0.1 case M2 exposed) →
   develop → it **reaches** the setpoint (or a bounded neighbourhood). Run for all 83 circuits; report how
   many converge.
2. **Self-correction:** perturb a developed weight → the circuit returns to setpoint-consistent state
   (the VTA-threadable-weight case must now self-correct — the weight can no longer be threaded into a
   narrow window).
3. **No oscillation (the stability gate):** from multiple starts and after perturbations, circuits settle
   **monotonically or with bounded, decaying transient** — NO ringing, NO runaway, NO silencing. A rule
   that reaches setpoint *by oscillating* is **rejected**. This is the gate that distinguishes the
   cross-homeostatic form from a merely-stronger single-setpoint rule.
4. **Learning preserved:** the homeostatic timescale must stay slow relative to BCM/DA-gated learning, so
   associative learning still works (the `test_paired_learns_more_than_unpaired` that F2 broke must pass —
   note M3.1 is on uniform setpoints, so this checks the *rule* doesn't erase learning; the full F2
   resolution is M3.2's timescale separation).
5. **Full suite green** — the gate. The behaviour WILL shift (the rule changes); regenerate the golden.
   The suite passing means the *machinery* is sound; it does NOT mean any prior emergent pattern survived
   (that's M4's observation, and no pattern is a target).

**If the rule cannot be made to converge without oscillating on the uniform setpoints — STOP and surface
it.** That would be a finding about the rule form, and it's better known now than after M3.2/3.3 build on
it.

---

## 5. Honesty + process
- **This is DIAGNOSIS-ADJACENT but it DOES change the mechanism** — so unlike M1/M2, the behaviour shifts
  and the golden regenerates. The full suite is the gate (not inline checks — twice this session inline
  checks missed what the suite caught).
- **The rate is set by the convergence criterion, not hand-picked.** Report the converging range; if only
  a razor-thin rate converges, that's a red flag the *form* is wrong (a good rule form has a broad
  converging range). Any rate in the range works — that's what makes it principled, not fitted.
- **Byte-additive to STRUCTURE** — M3.1 changes the *rule* (plasticity.py) and may add rule parameters,
  but adds/removes NO circuits, edges, or signs. The connectome is unchanged.
- **Dual-reviewed** — the reviewer independently re-derives the convergence/self-correction/no-oscillation
  tests against the remote. A "the substrate now self-organizes" claim cannot be certified by the builder
  alone; the reviewer must reproduce the acceptance tests.
- **Commit + push + STOP for reviewer clearance before M3.2.** Do not proceed to timescale grounding until
  the rule is proven to converge and cleared.

---

## 6. Hand-off note (for the implementation session)

> **HSO M3.1 — replace the inert homeostatic rule with the cross-homeostatic rule, prove it converges.**
> Design authority: `docs/PsychSim_HSO_M3_Rebuild_SPEC.md`. M1/M2 (dual-verified) found the homeostatic
> machinery present-but-hollow (rate 0.002 corrects ~0.14%/step, activity never reaches setpoint, weights
> seed-default-dominated) → full rebuild. M3.1 is the first, riskiest step: the rule form.
>
> **Replace** `homeo_factor` (plasticity.py:105, the single-setpoint `1 - rate*(act-setpoint)`, called at
> engine.py:196) with the **cross-homeostatic** rule: for each circuit, tune its incoming **excitatory**
> weights and incoming **inhibitory** weights in OPPOSITE directions against its setpoint (over-active →
> down-scale E, up-scale I; under-active → reverse) → converges to inhibition-stabilized balance instead
> of ringing. **The E/I split uses the EXISTING edge sign** (derived from `dominant_receptor` via the
> v12a RECEPTOR_SIGN table — do NOT add a field). Grounded: Cartiglia et al. 2025 (*Nat Commun*); Agnes &
> Vogels 2022. Resolve the exact update form at build against the rate model (ruling #1) — simplest form
> that converges.
>
> **Do NOT just increase HOMEO_RATE** — a stronger single-setpoint rule OSCILLATES; the fix is the rule
> FORM, not the rate. The rate is then set by the convergence criterion (any rate in the converging range
> works — a broad range is the sign the form is right; a razor-thin range means the form is wrong).
>
> **Prove it on the CURRENT uniform 0.1 setpoints** (grounding setpoints is M3.3 — isolate the rule). Done
> when: (1) circuits pinned far from setpoint REACH it (the CeA-0.8→0.1 case); (2) perturbed weights
> self-correct (the VTA weight can no longer be threaded); (3) NO oscillation/ringing/runaway/silencing
> (the stability gate — a rule that converges by ringing is REJECTED); (4) associative learning preserved;
> (5) full suite green, golden regenerated. **If it can't converge without oscillating — STOP and
> surface** (a finding about the form, better known now).
>
> **Process:** full suite is the gate (behaviour shifts, golden regenerates); byte-additive to structure
> (rule change only — no circuits/edges/signs added or removed); dual-reviewed (reviewer re-derives the
> acceptance tests independently against the remote — a self-organization claim can't be builder-certified);
> commit + push + STOP for clearance before M3.2 (timescales). Ledger the convergence evidence (converging
> rate range, per-circuit convergence, the no-oscillation demonstration) to `docs/hso/M3.1_...`.
