# Uniform-Start Stability Diagnostic — Claude Code handover

**This supersedes the HSO M3.1/M3.2 direction. Read this framing first — the approach has pivoted.**
Nothing about HSO (the cross-homeostatic rule, setpoints, timescale hierarchy) is built or committed. It
is **shelved as a fallback**, invoked ONLY if this diagnostic shows a specific failure (§4, outcome 2).
This handover is a **DIAGNOSTIC, not a build** — like M1/M2. It ADDS NOTHING. It removes the hand-set
weight bands and asks whether the substrate already self-organizes from a blank uniform start.

---

## 0. Why the pivot (the core, in three sentences)

The goal was always: **remove arbitrary constants from neural-pathway development so weights aren't
guessed.** HSO pursued that by adding a self-organizing optimizer — but that *relocated and multiplied*
the arbitrariness (208 guessed weights → 83 guessed setpoints + guessed rate/tau/cadence constants), and
the machinery ballooned (learning-vs-homeo conflict → timescale separation → 8× development → 2–3 hr
suite). **The honest cure is simpler: specify only what we can ground (a connection's existence and
sign — anatomy), set EVERY weight to ONE identical starting value (choosing nothing about relative
strengths), and let the EXISTING plasticity differentiate them through experience.** Magnitude emerges
from use, not from us. The only human numbers left in pathway development are anatomy, sign, and one
universal starting constant — which asserts *nothing* per-connection, so it is the opposite of a fudge.

**Governing test for every decision from here:** does this REMOVE arbitrary constants, or ADD them? This
diagnostic removes them (208 bands → 1 value) and adds nothing. That is why it is the next step.

---

## 1. What the diagnostic IS and IS NOT

- **IS:** set all connection weights to ONE identical starting value; keep the existing plasticity
  (R3-BCM, R5-NMOD, R6-DEVGATE), the existing weight-bounds (R8 clamp), and the existing competitive
  normalization (R8 normalise_incoming) EXACTLY as they are; run a NORMAL-length development; observe
  which of three outcomes (§4) occurs. Report. **Change nothing else. Add nothing.**
- **IS NOT:** building HSO, adding setpoints, adding a homeostatic rule, adding timescales, lengthening
  development, or tuning anything. If you find yourself wanting to add a stabilizer — STOP; that's
  outcome-2 territory and it's a ruling, not a build (§4).

---

## 2. The one change to make

- **`core/substrate/model.py:218`** — currently `w0 = _num_weight(k.get("default_weight", "moderate"))`,
  which maps each edge's per-connection band (`low`/`moderate`/`moderate-strong`/`strong`) to a number.
  **Replace the per-connection band lookup with ONE uniform starting value** applied to every connection
  (e.g. `w0 = params.UNIFORM_START_WEIGHT` for all edges — a single constant, same for all 208). The sign
  is applied separately (from the receptor, unchanged) — so an inhibitory edge starts at −(uniform),
  excitatory at +(uniform); the *magnitude* is identical across all connections. **The point: zero
  per-connection information in the starting weights.**
- **That is the ONLY change.** Do not touch plasticity.py, the bounds, the normalization, the development
  length, or anything else.

### 2.1 The starting value — uniform by default, research-grounded where the literature supports a bias
Pick one value as the **balancing point** (e.g. 1, or 0, or a neutral mid-range value) and apply it
universally by default. It is NOT a per-connection guess (identical everywhere), so it carries no
relative-strength claim — it is the null: "we assert nothing about which connections are innately
stronger."

**The one exception — a research-grounded innate bias.** Some pathways are genuinely stronger from birth
(a denser/more potent projection, a higher baseline firing rate) — and where the **academic literature
supports this**, the starting value for that connection should be set to a more appropriate biased value.
The critical distinction: **this is an educated guess grounded in the research, NOT a convenience fit and
NOT a random choice.** A starting bias is legitimate ONLY if its source is the literature (cite it — the
projection is documented as dense/strong, or its baseline firing rate is measured); it is a fudge if it
is chosen because it makes a result come out right. So:
- **Default: the uniform balancing-point value** (no innate claim — experience differentiates).
- **Where the literature grounds a real innate strength difference: that grounded value** (cited, an
  educated guess from research — e.g. grounded in documented projection density or baseline firing rate).
- **Never a convenience fit.** The line is grounded-in-literature vs. chosen-for-outcome, not
  approximate vs. precise — a research-informed approximate value is honest; a hand-picked one is not.

For THIS diagnostic, start with the pure uniform case (all connections at the balancing point, no innate
biases yet) — it is the null hypothesis that tells us how far experience-alone gets us. Where the
diagnostic later shows a pathway *needs* an innate strength that experience doesn't produce, THAT is the
signal to ground its starting value from research (a follow-on, not this pass). Record the uniform value
used; if the outcome depends sharply on it, that itself is a finding.

---

## 3. The existing machinery it runs against (unchanged — for reference)

These already exist and STAY exactly as they are — they are what differentiates the weights and what may
(or may not) stabilize them:
- **Plasticity (differentiates weights through experience):** R3-BCM (correlation), R5-NMOD
  (consolidation = eligibility × live-modulator), R6-DEVGATE (age-scaled learning rate). These move the
  uniform weights apart based on what the organism lives. (plasticity.py; composed in engine.py.)
- **Brake #1 — weight bounds (R8 clamp):** `clamp_weight` (plasticity.py:113), applied at engine.py:189 —
  holds each weight within its bounds.
- **Brake #2 — competitive normalization (R8):** `normalise_incoming` (plasticity.py:117), applied at
  engine.py:207 — holds total incoming drive to a circuit roughly constant, so incoming weights *compete*
  (one grows only as others shrink). **This is the key existing anti-runaway mechanism** — it may already
  prevent Hebbian blow-up without anything new.
- **R7-STRUCT prune** (long-silent weights) also exists. Leave it.

Note: R4-HOMEO exists in the composition but is the inert rule M2 showed does ~nothing at rate 0.002 —
leave it as-is (inert); the diagnostic is about whether we need it, so don't touch it either way.

---

## 4. The three outcomes to observe (the whole point)

Run a normal-length development from uniform starting weights and classify the result:

1. **STABLE + DIFFERENTIATED** — weights move apart sensibly through experience, settle, don't blow up,
   don't collapse. → **This is the answer. We are DONE.** The substrate self-organizes through living,
   from anatomy alone; HSO was never needed; the hand-set bands were replaceable by one value + plasticity.
   Report the developed weight distribution and the functional checks (§5).
2. **RUNS AWAY** — used pathways grow unbounded / weights pin at ceiling / activity saturates. → Do NOT
   add HSO reflexively. First test whether the EXISTING brakes hold it: is R8 competitive normalization
   actually active (`params.NORMALISE`)? Do the weight bounds bind? **Report whether bounds + competition
   contain the runaway.** Only if the existing brakes genuinely CANNOT hold it does HSO come off the shelf
   as the fallback stabilizer (researcher ruling) — and even then, the simplest form, not the full
   setpoint/tau apparatus. **This is a STOP-and-surface, not a build-HSO.**
3. **STAYS FLAT** — nothing differentiates; weights sit at the uniform value, development produces no
   structure. → A genuine missing element (plasticity too weak, or something absent). STOP and surface —
   do not add machinery to force differentiation; think about what's genuinely missing, grounded.

**In all three cases: observe and report. Do not fix on discovery.** (Outcome 1 needs no fix; outcomes 2
and 3 are rulings, not builds.)

---

## 5. What to measure (the diagnostic report)

- **Weight distribution after development** — did the uniform weights differentiate? Into what? (A
  long-tailed / structured distribution = differentiation; a flat spike at the uniform value = flat;
  everything pinned at bounds = runaway.)
- **Stability** — do weights settle, or drift/oscillate/blow up over the development?
- **Functional checks (does the substrate still WORK — these are functional invariants, NOT targets):**
  does v9 aggression closure still hold (aggression emerges under provocation, floor at neutral)? Does
  associative learning still work (paired > unpaired)? These verify the substrate is a working substrate
  from uniform starts — they are correctness checks, not results to preserve.
- **NOT** "did the inverted-U survive" or any emergent-pattern preservation — that is M4-style observation
  for later, and no pattern is a target. This diagnostic is only: *does uniform-start + existing
  plasticity produce a stable, differentiated, working substrate?*

---

## 6. Recorded for later — NOT built now (register)

- **Innate strength differences (Point 1 follow-on):** where the diagnostic shows a pathway needs an
  innate strength experience alone doesn't produce, ground that starting value in the research (projection
  density / baseline firing rate — cited, an educated guess from literature, never a convenience fit). A
  follow-on to this diagnostic, not part of it.
- **Epigenetic spawn-state modification (deferred layer):** epigenetics shifts starting values — making
  some pathways more (or less) important from birth — via marks that can be inherited or set by early
  environment. **Structurally identical to genetic predisposition:** a spawn-time INPUT that shifts the
  starting state, from which the phenotype still EMERGES through development (the honesty rule is the same
  — an input, not a coded outcome). It belongs with the **CU study's individual-differences design** (the
  CU literature has real epigenetic findings — methylation patterns, environmental modification of
  expression), NOT in the current weight-grounding work. **Deferred — do not build now** (pulling it in
  would balloon scope exactly as HSO did). Recorded here so it is not lost; placed precisely when the CU
  study's spawn-parameters are designed.

---

## 7. Honesty + process
- **DIAGNOSTIC — but it changes behaviour** (uniform starts shift everything), so unlike M1/M2 the
  golden will move. The full suite is the gate; regenerate the golden; the library regrows (the
  connectome is UNCHANGED — same circuits/edges/signs — only the starting weights change, so the regrow
  is about the new developed state, not a structural change).
- **Byte-additive to structure** — no circuits, edges, or signs added/removed. The ONLY change is the
  starting-weight assignment (model.py:218) → one uniform value.
- **Change nothing else, add nothing, fix nothing on discovery.** The whole value of this diagnostic is
  that it adds nothing — it tests whether the substrate already does what we wanted. Adding a stabilizer
  the moment it wobbles is the exact trap (that's outcome-2, a ruling).
- **Dual-reviewed** — the reviewer independently re-derives the three-outcome classification against the
  remote (does uniform-start actually differentiate / run away / stay flat, and do the existing brakes
  hold?). Push the diagnostic + the developed-weight report; the reviewer reproduces it.
- **Commit + push + STOP for reviewer verification and the outcome ruling.** Do not proceed past the
  diagnostic — the next step depends entirely on which outcome (§4) occurred, which is the researcher's
  call.

---

## 8. Hand-off note (for the implementation session)

> **Uniform-Start Stability Diagnostic — supersedes the HSO M3 direction (HSO is shelved as fallback).**
> This is a DIAGNOSTIC, not a build — it ADDS NOTHING. The goal: remove guessed weights by setting EVERY
> connection to ONE identical starting value (zero per-connection choice) and letting the EXISTING
> plasticity differentiate them through experience — then observe whether that's stable. (HSO relocated
> the arbitrariness to guessed setpoints+taus and ballooned into an 8× development; this removes it
> instead of relocating it.)
>
> **The one change:** `core/substrate/model.py:218` — replace the per-connection band lookup
> (`_num_weight(k.get("default_weight", ...))`) with ONE uniform starting value for ALL 208 edges (sign
> still applied from the receptor, unchanged; only the magnitude is made identical everywhere). **That is
> the only change** — do NOT touch plasticity, bounds, normalization, or development length. Add NOTHING.
>
> **Keep exactly as-is:** the plasticity (R3-BCM, R5-NMOD, R6-DEVGATE) that differentiates weights; the
> weight-bounds clamp (plasticity.py:113, engine.py:189); the R8 competitive normalization
> (plasticity.py:117, engine.py:207) — the key existing anti-runaway brake. Leave inert R4-HOMEO as-is.
>
> **Run a NORMAL-length development from uniform weights and classify the outcome:** (1) STABLE +
> DIFFERENTIATED (weights move apart sensibly, settle, work) → **DONE, HSO never needed**; (2) RUNS AWAY →
> test if the EXISTING bounds + competition hold it; only if they genuinely can't does HSO come off the
> shelf (STOP and surface — a ruling, NOT a reflexive HSO build); (3) STAYS FLAT → genuine missing
> element, STOP and surface. **Do not fix on discovery in any case.**
>
> **Report:** developed weight distribution (did uniform differentiate?), stability, and functional
> checks (v9 closure holds? paired>unpaired learns? — these are correctness invariants, NOT results to
> preserve; NO inverted-U-survival framing). Process: full suite is the gate (golden moves, library
> regrows — but connectome UNCHANGED, structure byte-additive); dual-reviewed (reviewer re-derives the
> outcome classification against the remote); commit + push + STOP for the outcome ruling (the next step
> depends entirely on which outcome occurred — researcher's call).
