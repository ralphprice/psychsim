# PsychSim — the Homeostatic Self-Organization Architecture (HSO)

**Foundational architectural specification. Status: SPEC ONLY — nothing built. For researcher review.**
This is the most consequential design change in the project. It replaces hand-set connection weights
with weights that **self-organize** from spawn-defaults toward **grounded setpoints**, so the substrate
finds its own balance rather than being tuned to behave. It re-grounds every weight and re-derives
every prior result. It comes BEFORE finishing v14 (v14's *anatomy* is kept; its *weights* migrate to
HSO with everything else).

**Framing (researcher ruling): full rebuild, not a patch.** The substrate already *has* fields named
`homeostatic_setpoint`, `time_constant_tau_ms`, `eligibility_trace_tau_ms`, and an `R4-HOMEO` rule —
but the system still behaved as if weights were static (the VTA pacemaker threaded into a narrow window;
saturations homeostasis should have prevented). So **the existing machinery is treated as UNVERIFIED
and UNTRUSTED until proven real.** Every existing setpoint value, timescale value, and the homeostatic
dynamics themselves are suspect until this rebuild grounds or replaces them. Fields existing on paper is
not evidence they function.

---

## 0. The principle (what may be fixed, and why)

> **A value may be fixed only if it is a property of the SUBSTRATE (the machine), not the STATE (where
> the machine currently is). Substrate properties are grounded and fixed; state is plastic and
> self-organizes. Freezing state as if it were a substrate property IS the fudge.**

- **Substrate property** — describes the machine itself: what each part targets, how fast it responds,
  what connects to what. The genome/hardware. The machine does not rewire its construction through
  experience → legitimately fixed → grounded by its proper method.
- **State** — describes where the machine currently sits: how strongly a connection is currently
  weighted, what a circuit is currently doing. The thing experience moves → must be plastic.

Every fudge in the substrate is the same category error: a **weight** (state) frozen as a fixed
constant (as if it were a substrate property). The fix is never "pick a better weight" (that moves the
fudge); it is "**make the weight plastic and let it self-organize toward a grounded setpoint.**"

This is the honesty wall, one level down — into the parameters. Just as *behaviour* must emerge rather
than be coded, the *weights* must emerge (via homeostasis) rather than be set. The setpoint is the
spawn-time fact (genetic, fixed, grounded); the weight is the emergent outcome (developed, not chosen).

---

## 1. The value taxonomy (the closed set — every value in the substrate classifies here)

| Value class | Fixed or plastic? | Grounded by | Notes |
|---|---|---|---|
| **Connection weights** | **PLASTIC** — spawn-default → self-organize | NOT chosen; homeostasis sets them | The bulk of the substrate. No hand-set weights. |
| **Setpoints** (target activity per population) | **FIXED** — genetic/ontogenetic | Measured target firing rates; honestly scaffold where unmeasured (but the *claim* — stable moderate rate — grounded) | The legitimately-fixed "what each part targets." |
| **Time constants** (response speed) | **FIXED** — physics/chemistry | Measured kinetics, differentiated by mechanism (§4) | ionotropic ≪ metabotropic ≪ neuromodulatory ≪ plasticity. |
| **Signs** (excitatory/inhibitory) | **FIXED** — receptor biology | Cited receptor (v12a `RECEPTOR_SIGN` — unchanged) | Not tuned; a sign is a biological fact. |
| **Structure** (circuits, connectivity, receptor identity) | **FIXED** — anatomy | Citation | The wiring diagram. |

**No free scaling constants.** What feels like "a constant needed so movements meet a scale" is always
one of: a **setpoint** in disguise (keep, grounded), a **time constant** in disguise (keep, measured),
or a **normalization that must be relative-to-setpoint** (emergent via homeostatic scaling, not a
hand-set absolute). The literature is explicit: homeostatic synaptic scaling keeps activity in range by
scaling weights *relative to the neuron's own target*, not by clamping to a fixed number — so "meeting a
scale" is achieved by the homeostatic process (scale weights until activity hits setpoint), and the
scale *emerges*. The taxonomy is closed: **setpoints, time constants, signs, structure** are the only
fixed classes; **everything else is plastic state.**

---

## 2. The mechanism — homeostatic self-organization (grounded in the literature)

The field's answer to "how do you avoid hand-tuned weights": weights self-organize toward a target via
homeostatic plasticity. Networks from *homogeneous/uniform* weight starts self-organize to stable,
realistic weight distributions — structure "appears in a self-organized way rather than being imprinted
statically" (Effenberger et al. 2015, *PLoS Comput Biol*; the balanced-state STDP+homeostasis result).

### 2.1 The homeostatic rule
Each circuit maintains a running average of its own activity and adjusts its **incoming** weights up or
down based on the deviation from its **setpoint** — a target activity level. Grounding:
- The two-term **cross-homeostatic** rule is the most biologically plausible form that yields stable
  self-sustained, **inhibition-stabilized** networks with all units converging to setpoints (Sanzeni
  et al. 2022, *PNAS*; Mackwood et al.; the neuromorphic cross-homeostatic result, *Nat Commun* 2025).
- **Inhibitory homeostatic/STDP** specifically "eliminates runaway excitation and pathological network
  states" (Effenberger 2015). **This is the general solution to the saturation problem** — the DRN,
  vmPFC, CeA, VTA saturations we fixed one-at-a-time by adding interneurons and tuning weights are, in
  this framework, prevented automatically by homeostatic balance. The interneurons still must *exist*
  (anatomy); their *weights* self-organize.
- Setpoints are "ontogenetically determined" and neurons regulate receptor density based on deviation
  of a Ca²⁺-sensor running-average from that setpoint (Sanzeni 2022; Turrigiano & Nelson 2004).

### 2.2 Weight normalization is relative, not absolute
Hebbian growth is contained by **homeostatic synaptic scaling** (scale incoming weights relative to the
neuron's target), NOT by fixed weight-normalization constants (Turrigiano; the SOM-with-synaptic-scaling
result). This is why there are no free scaling constants — the scale is set by the setpoint + scaling.

### 2.3 The critical property: weights must ACTUALLY self-organize
The rebuild's central acceptance test (and the thing the current machinery is suspected of failing):
**perturb a weight → homeostasis pulls it back toward its setpoint-consistent value.** If a perturbed
weight self-corrects, weights are genuinely plastic. If it stays perturbed (because the homeostatic
rule is too weak relative to the seed weight, or the seed weight dominates the dynamics), weights are
*effectively static* — nominally plastic, actually frozen. **The VTA narrow-window thread is the
signature of effectively-static weights** (a genuinely homeostatic weight cannot be threaded into a
narrow window — the system would move it away). This test runs on every weight class (§6).

---

## 3. Setpoints — the grounding problem (crux #1)

Setpoints are the legitimately-fixed quantity, so they carry the honesty burden the weights used to.
**The suspicion to resolve: the 83 existing `homeostatic_setpoint` values may be fitted targets** — in
which case the system self-organizes toward *fitted setpoints* and the fudge merely moved from weights
to setpoints. This rebuild treats all 83 as unverified.

### 3.1 How setpoints are honestly grounded (the hierarchy)
1. **Measured target rate** — where the literature gives a population's baseline/target firing rate,
   use it (grounded). Many subcortical/cortical populations have measured tonic rates.
2. **Relative/class-based** — where an absolute rate isn't measured, ground the setpoint by *population
   class* (e.g. tonic pacemaker populations vs. phasic populations vs. interneurons) with the *ratio/
   relationship* grounded even if the absolute isn't. A DA neuron's tonic pacemaker rate is a *class
   property* (Grace & Bunney) even where the exact value is scaffold.
3. **Honestly scaffold** — where neither is available, the setpoint is marked `# SCAFFOLD`, and — the
   key honesty move — **the CLAIM is grounded even when the number is placeholder**: "this population
   homeostibates toward a stable moderate rate" is a grounded claim; the specific 0.NN is scaffold. The
   sign/direction is grounded; the magnitude is disclosed as placeholder.

### 3.2 The setpoint audit (every one of the 83)
Classify each existing setpoint: **measured / class-grounded / scaffold-but-honest / FITTED.** The
FITTED ones (set to make a behaviour work) are the fudges — re-derive from 3.1 or mark honest-scaffold.
Run independently (reviewer + build session) against the remote — an audit for fitting cannot be
certified by the entity that may have fitted.

---

## 4. Time constants — the measured hierarchy (crux #2, and it fixes the VTA learning failure)

Time constants are fixed substrate properties grounded in **measured kinetics**, differentiated by
mechanism. The measured hierarchy (from the neural-mass / timescale literature):

| Mechanism | Timescale (measured) | Source |
|---|---|---|
| Membrane | 5–50 ms | Neural-timescales review (2024); std. |
| **Ionotropic** synaptic (glutamate/GABA-A) | ~1.7–50 ms (fast) | Häusser & Roth 1997; enteric/CNS fast-EPSP data |
| **Metabotropic** synaptic (GABA-B, mGluR) | 150 ms – 2.5 s (slow) | slow-EPSP data |
| **Neuromodulatory** (dopamine, serotonin) | 10 s – minutes (very slow) | slow synaptic depolarization data |
| **Plasticity** (weight change) | seconds–minutes (induction), hours–days (consolidation); **nonlinear/threshold** | Inglebert; BTSP; slow-plasticity review |

**This directly resolves the VTA F2 failure.** F2 was tonic DA (neuromodulatory, *very slow*)
flattening phasic RPE (fast) because the plasticity gate read *absolute* DA, conflating timescales that
are physically different by orders of magnitude. HSO separates them: the phasic reward signal and the
tonic DA level operate on their measured (different) time constants, so tonic level and phasic contrast
are distinguishable. **The VTA impasse was a symptom of not respecting the measured timescale
hierarchy** — HSO fixes it by construction, not by tuning. The existing `time_constant_tau_ms` /
`eligibility_trace_tau_ms` fields are audited against this measured hierarchy (measured vs. placeholder
vs. fitted), same as setpoints.

---

## 5. Spawn-defaults — the child's starting endowment

The ONLY values set at spawn are the child's defaults; after that the system establishes its own order.
- **Weights spawn UNIFORM / undifferentiated** (the literature shows self-organization works from
  uniform/homogeneous/Gaussian starts). The child is born with an *undifferentiated* connectome; **
  development differentiates it** via HSO toward the setpoints. This is the researcher's principle made
  literal: "we set defaults at spawn; after that the system establishes its own working order."
- **Genetic predisposition enters as a spawn-default DEVIATION**, honestly: where a genetic/individual
  difference is modelled (e.g. a temperament predisposition, the CU study's spawn parameters), it sets
  a *starting-point offset* or a *setpoint shift* — a spawn-time fact (like sex, like the kinship
  signature) — NOT a fixed adult weight. Predisposition biases where self-organization *starts* or what
  it *targets*; the developed weights still emerge. (This is how the sophropathy module's `fearless_frac`
  and the CU spawn parameters remain honest under HSO — they're spawn-defaults/setpoint-shifts, inputs,
  not coded outcomes.)
- **Setpoints and time constants are NOT spawn-state** — they're substrate properties, the same for the
  species (with grounded genetic/individual variation where modelled). They don't develop; the weights
  develop toward them.

---

## 6. The migration plan (how the existing substrate moves to HSO without losing grounded anatomy)

The grounded *anatomy* (circuits, connectivity, signs, receptors — everything v9–v14 correctly built)
is KEPT. What changes is that *weights stop being hand-set* and *setpoints/timescales get grounded*.
Migration is itself phased and reviewed (the same discipline), full-suite-gated per phase.

- **M1 — Establish the taxonomy in the seed + audit the fixed values.** Tag every value by class (§1).
  Independently audit all 83 setpoints (§3.2) and all timescales (§4) → classify measured/class-grounded/
  scaffold-honest/**fitted** → re-ground or honest-scaffold the fitted ones. Deliverable: a committed
  per-value ledger (this *is* the constants-audit the researcher demanded, now structured by taxonomy).
- **M2 — Verify weight plasticity is REAL (the crux test, §2.3).** For every weight, perturb → does
  homeostasis pull it back? Produce the list of **effectively-static weights** (perturbation doesn't
  self-correct). These are where HSO is currently hollow. If most weights are effectively static, that
  confirms the rebuild is needed (not a patch); if most already self-organize, the scope narrows —
  either way, M2 tells us the true size, honestly, from evidence.
- **M3 — Strengthen/replace the homeostatic rule** so weights genuinely self-organize toward setpoints
  (the cross-homeostatic + inhibitory-homeostatic form, §2.1), with relative scaling (§2.2). Spawn
  weights uniform (§5). Verify: a perturbed weight now self-corrects; the network is inhibition-
  stabilized (no saturation without hand-set interneuron weights — the saturations self-resolve).
- **M4 — Re-derive every prior result under HSO.** The phenomena battery, v9 closure, and CRITICALLY
  **the adolescent inverted-U** are re-run on the self-organized substrate. Each result either SURVIVES
  (now far stronger — emerged from a substrate that found its own balance, zero tuned weights) or does
  NOT (was partly an artifact of hand-set weights — which we needed to know). Both outcomes are the
  honesty working. This is the cost and the point: HSO puts every result back on the table, and the
  ones that survive are trustworthy in a way they were not before.
- **M5 — Re-integrate v14 anatomy under HSO** (the OT/VP pathway, the signature, the interneurons — all
  KEPT as structure; their weights self-organize). Then resume v14 Phases 2–5 on the HSO foundation, and
  the VTA/pacemaker reward-completion (which HSO's timescale separation resolves).

---

## 7. What this costs, and what it buys (honest assessment)

**Costs:** it's the largest change in the project; it re-derives every result (including the inverted-U,
which may not survive); it precedes and reworks v14; the migration is itself a multi-phase reviewed
effort. Prior clearances are not grandfathered — the inverted-U's status is provisional until M4.

**Buys:** it *dissolves* the fitted-weight fudge entirely (weights aren't set, so they can't be fitted);
it *subsumes* much of the target-cell/interneuron audit (saturations self-resolve under homeostatic
balance, so the reactive interneuron-and-tune pattern ends); it *resolves the VTA impasse by
construction* (timescale separation); and it makes the model's central claim TRUE in a way it currently
is not — "we specified the machine's grounded properties (setpoints, timescales, anatomy) and it
organized its own weights" is a stronger, more novel, more defensible thesis than "we built a model and
tuned it to behave." The honesty wall now reaches all the way down: nothing is fitted, because the only
fixed things are grounded substrate properties and everything else emerges.

---

## 8. Open items for researcher review
1. **Migration sequencing** — M1→M5 as specified, or adjust. (M1+M2 are audit/diagnosis and could run
   first to size the rebuild before committing to M3's mechanism work.)
2. **Setpoint grounding depth** — how much target-rate literature to pull now vs. mark honest-scaffold
   (a scaffold setpoint with a grounded *claim* is honest; the question is how many to fully ground up
   front).
3. **Uniform-spawn scope** — fully uniform weights at spawn, or class-uniform (interneurons start at one
   default, projection neurons at another)? The literature supports uniform *and* Gaussian starts; the
   choice affects how much development must do.
4. **Result re-derivation bar** — what counts as a result "surviving" M4 (exact reproduction, or the
   same qualitative phenomenon with real margins — the shape-not-argmax standard we already adopted).
5. **Genetic-predisposition representation** — spawn-default offset vs. setpoint-shift for modelled
   individual differences (both honest; which fits the CU study's spawn parameters best).

---

*This spec makes the weights emerge instead of being set — the honesty wall applied to the parameters
themselves. Only grounded substrate properties (setpoints, timescales, signs, structure) are fixed;
every weight self-organizes from a uniform spawn toward its grounded setpoint. Nothing is built until
the researcher reviews and rules on sequencing and the open items. The existing machinery is trusted
only where this rebuild proves it real.*
