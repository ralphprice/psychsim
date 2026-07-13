# PsychSim — HSO M3: the homeostatic rebuild spec

**Design specification. Status: SPEC ONLY — nothing built. For researcher review.**
Scoped from the M1/M2 audit (dual-verified on origin/main, fe0a34a): the homeostatic machinery is
**present-but-hollow** — R4-HOMEO at rate 0.002 corrects ~0.14%/step, ~10× too weak; activity never
reaches setpoint; weights are seed-default-dominated (effectively static); all 83 setpoints are uniform
0.1 placeholders; timescales are placeholder-uniform (~200ms); 0/208 weight magnitudes grounded (74
`assumption`). **Verdict: full rebuild, not targeted repair.** M3 replaces the inert rule with a working
self-organizer, grounds the setpoints and timescales, and verifies weights self-organize.

M4 (verify the substrate still functions correctly, then observe what it now produces) and M5
(re-integrate v14 anatomy) follow M3. Prior clearances are NOT grandfathered: the M1/M2 finding is that
the substrate has **not been self-organizing at all** — weights sat at hand-set bands, essentially
unmoved by homeostasis — so once weights genuinely self-organize, the substrate's behaviour is observed
afresh (no prior emergent pattern is assumed to carry over, and none is a target to preserve).

---

## 0. What M3 must achieve (the acceptance criteria, from the M2 evidence)

The M2 crux test is the acceptance test, inverted. M3 succeeds when:
1. **Activity converges to setpoint** — a circuit pinned far from its setpoint is pulled to it by the
   homeostatic rule over development (the current rule fails this: CeA pinned ~0.8, setpoint 0.1,
   uncorrected).
2. **Perturbations self-correct** — perturb a developed weight → homeostasis returns the circuit to its
   setpoint-consistent state (the current rule fails: barely-moving weights stay perturbed, which is
   why the VTA weight could be threaded into a narrow window).
3. **Seed defaults do not dominate** — two agents with different spawn weights on an edge converge to
   the same developed weight (the current rule fails: developed weight ≈ spawn weight).
4. **The hand-tuned interneuron-stabilizer weights self-resolve** — the DRN-GABA / CeA-GABA / cortical-
   interneuron weights we hand-set across v13/v14 are no longer needed; an inhibition-stabilized network
   finds its own E/I balance. **This is the payoff: the whole reactive "add-an-interneuron-and-tune-its-
   weight" pattern ends.**
5. **No oscillation / no instability** — the rule converges smoothly, not by ringing (see §2.3 — the
   naive "just make it 10× stronger" fails this).

---

## 1. Why "make R4-HOMEO stronger" is the WRONG fix (the trap to avoid)

The M2 finding is "the rule is ~10× too weak," and the naive inference is "multiply the rate by 10."
**This is wrong and must not be built.** A single-setpoint multiplicative rule (`w *= 1 - rate·(act -
setpoint)`) that is strong enough to actually reach setpoint will **oscillate** — it overshoots,
over-corrects, and rings, because a single-target negative feedback with a large gain is unstable. The
literature is explicit that simply strengthening a single-setpoint rule doesn't give stable convergence;
the stable solution is a **different rule form**, not a bigger rate on the same form. So M3 is a rule
*replacement*, not a rate *increase*. (This is itself an instance of the project's core lesson: the
fix for the weak rule is the right *mechanism*, not a tuned *constant*.)

---

## 2. The mechanism — the cross-homeostatic rule (grounded)

The literature's converging answer for **stable, self-organizing E/I balance** is the **cross-homeostatic
family**: plasticity at excitatory and inhibitory synapses each depends on **both** the excitatory and
inhibitory setpoints, and the rule "autonomously tune[s] the network to produce robust, self-sustained
dynamics in an inhibition-stabilized regime" by "automatically tuning all synaptic weight classes in
parallel" (Cartiglia et al. 2025, *Nat Commun* 16; the neuromorphic cross-homeostatic result). Companion
grounding: nonlinear inhibitory plasticity stabilizes excitatory synapses *without* needing upper bounds
or extra homeostatic mechanisms (Agnes & Vogels 2022, *PLoS Comput Biol*); local synaptic scaling lets
"noisy, heterogeneous networks spontaneously discover optimal synaptic configurations... without precise
initialization" (2025) — i.e. weights self-organize from *any* start, which is the property M2 found
missing.

### 2.1 The rule form (concrete)
Replace the single-setpoint `homeo_factor` with a **cross-homeostatic update** that adjusts weights by
weight-class (E vs. I) against the deviation of the *target* population from its setpoint:
- **Excitatory→X weights** adjust so that X approaches its setpoint (down-scale when X over-active).
- **Inhibitory→X weights** adjust so that X approaches its setpoint (relax inhibition when X *under*-
  active) — the inhibitory weights are plastic too, and their target is the *postsynaptic* setpoint.
- The "cross" property: because both E and I weights onto a circuit are tuned against that circuit's
  setpoint (and the network's E/I setpoints jointly), the system converges to an **inhibition-stabilized
  balance** rather than oscillating — the E and I adjustments counter-balance.
- **Concrete update (to be finalized at build against the rate model):** for each circuit *c* with
  running mean activity *ā_c* and setpoint *s_c*, the incoming excitatory weights scale by a factor
  decreasing in (*ā_c − s_c*) and the incoming inhibitory weights scale by a factor *increasing* in
  (*ā_c − s_c*) — so over-activity both damps excitation and recruits inhibition, and under-activity
  does the reverse. This is the two-sided balance the single-sided rule lacked.

### 2.2 Rate and timescale (grounded, not tuned)
- The homeostatic timescale is **slow** — homeostatic scaling operates over hours in biology; in the
  model it must be slow relative to the fast plasticity (BCM/DA-gated learning) so learning isn't
  erased, but fast enough to actually reach setpoint over a development. The M2 finding sets the floor:
  0.002 is ~10× too weak. The *rule form* (§2.1) is what gives stable convergence; the rate is set so
  convergence completes within a development **and is verified by the acceptance test (§0.1–0.3), not
  hand-picked to a number.** (A rate that converges is found by the convergence criterion, not by
  threading a value — the difference from a fudge is that *any* rate in the converging range works, and
  the rule form guarantees a converging range exists.)
- **Separate the timescales by mechanism (this resolves F2).** The measured hierarchy (HSO spec §4):
  ionotropic (~ms) ≪ metabotropic (~100s ms) ≪ neuromodulatory (~10s s) ≪ plasticity/homeostasis
  (slowest). Ground each circuit's `time_constant_tau_ms` by its mechanism class (not the uniform 200ms).
  **This fixes the tonic/phasic-DA conflation (F2):** phasic reward operates on the fast timescale, tonic
  DA on the slow neuromodulatory timescale, so they become distinguishable and the VTA learning failure
  resolves *by construction* — the reward-completion pass then lands cleanly on this.

### 2.3 The stability requirement (the acceptance gate for the rule itself)
The rule must be shown to **converge, not oscillate**: from multiple starts and after perturbations, all
circuits settle to their setpoints monotonically (or with bounded, decaying transient), with no ringing,
no runaway, no silencing. This is verified empirically (§4) — a rule that reaches setpoint by oscillating
is rejected. The cross-homeostatic form is chosen precisely because it converges where the single-setpoint
form rings; the build must *demonstrate* this, not assume it.

---

## 3. Grounding the setpoints (M1 found all 83 are uniform-placeholder)

With a *working* homeostatic rule, the setpoint becomes load-bearing — the rule drives activity *to* it,
so a wrong setpoint now produces wrong activity (it didn't matter before, when the rule was inert). So the
setpoints must become real. Per sealed ruling #2 (no quota):
- **Measured** where the literature gives a population target rate.
- **Class-grounded** where it gives a class property (tonic-pacemaker vs. phasic vs. interneuron rates
  differ — the DA pacemaker tonic rate is a class property even where the absolute is scaffold; this is
  what F1 needed and the uniform scheme couldn't provide).
- **Honest-scaffold** otherwise — with the grounded *claim* ("homeostibates toward a stable moderate
  rate"), the value marked scaffold.
- The M1 ledger (`docs/hso/M1_fixed_values_audit.md`) lists what grounding is available per population;
  M3 applies it. **The uniform 0.1 is replaced by per-population setpoints of the appropriate class.**
- **Setpoints are a substrate property (fixed), not state** — they don't develop; the weights develop
  *toward* them. Individual/genetic variation enters as a **setpoint-shift** (sealed ruling #5), not a
  per-circuit weight.

---

## 4. Verification (the M2 crux test, inverted into acceptance tests)

Every acceptance criterion (§0) is an empirical test, run against the rebuilt rule:
- **Convergence:** pin a circuit far from setpoint → it reaches setpoint over development (the CeA-0.8-
  →0.1 case must now succeed). Run for all 83.
- **Self-correction:** perturb a developed weight → the circuit returns to setpoint-consistent state (the
  VTA-threadable-weight case must now self-correct — the weight can no longer be threaded).
- **Start-independence:** two agents, different spawn weights on an edge → converge to the same developed
  weight (seed default no longer dominates). **This also finally decides sealed ruling #3** (spawn-default
  scheme): if convergence is start-independent, fully-uniform spawn works; if the start still biases the
  outcome, class-uniform. *Now* it's decidable, because now there's a working self-organizer to test it
  against (M2 correctly noted this couldn't be decided while nothing self-organized).
- **Interneuron self-resolution:** remove the hand-set interneuron-stabilizer weights (DRN-GABA/CeA-GABA/
  cortical) → the network still reaches E/I balance via the cross-homeostatic rule (the payoff: the
  hand-tuned weights were compensating for the absent self-organizer; with it present, they self-resolve).
- **Stability:** no oscillation/ringing/runaway/silencing from any start (§2.3).
- **Full suite green** — the gate. But note: M3 changes the homeostatic rule and the setpoints, so the
  behaviour *will* shift; the golden regenerates, and **M4 is where the substrate's behaviour is
  observed afresh** (the suite
  passing means the machinery is sound; M4 *observes and describes* what the substrate now produces —
  no pattern is a target).

---

## 5. What M3 does NOT do (scope boundary)
- **M3 does not observe/describe the substrate's emergent behaviour** — that's M4. M3 builds the working
  self-organizer and verifies it self-organizes (the acceptance tests). What the substrate then produces
  (whether the inverted-U appears or not) is M4's observation — not a target either way.
- **M3 does not re-integrate v14 anatomy** — that's M5.
- **M3 does not build the reward-completion pass** — but it *enables* it (the timescale separation §2.2
  resolves F2; the reward-completion work lands on M3's foundation).
- **M3 does not add or remove anatomy** — it changes the *rule* and the *setpoints/timescales* (substrate
  properties), not the circuits/edges/signs (structure). The connectome is unchanged; the weights become
  genuinely plastic.

---

## 6. Sequenced build (phased, each reviewed, full-suite-gated)
1. **M3.1 — the cross-homeostatic rule.** Replace `homeo_factor` with the cross-homeostatic form (§2.1);
   verify convergence + stability on the *current* uniform setpoints first (isolates the rule from the
   setpoint grounding — does the rule converge at all?). This is the riskiest piece; prove it alone.
2. **M3.2 — ground the timescales** (§2.2) by mechanism class; verify F2 resolves (tonic/phasic DA
   separable).
3. **M3.3 — ground the setpoints** (§3) per-population; verify activity converges to the *grounded*
   setpoints, and F1 resolves (VTA pacemaker rate representable).
4. **M3.4 — verify weight self-organization** (§4 full battery): self-correction, start-independence
   (decides ruling #3), interneuron self-resolution, stability. 
5. **M3.5 — full suite green + golden regenerate**; hand to M4 for result re-derivation.

Each phase: byte-additive to structure (no anatomy change), full-suite-gated, dual-reviewed (reviewer
re-derives the acceptance tests independently against the remote — a self-organization claim can't be
certified by the builder alone), commit + push + STOP for clearance before the next.

---

## 7. Sealed rulings (researcher-finalized)

1. **Rule variant — resolve at M3.1 against the rate model.** Prove convergence with the simplest
   cross-homeostatic form that works; the acceptance test (§0, §4) decides. Do not pre-specify the
   variant.
2. **Setpoint grounding — VERY DEEP.** This is foundational and done once — the setpoint grounding (§3)
   gets a thorough literature pass, not a light one. Every setpoint that *can* be grounded in a measured
   or class target rate IS, with only the genuinely-unavailable ones left honest-scaffold (still no
   quota, ruling #2 — but the effort is maximal because a wrong setpoint now drives wrong activity under
   the working rule). Get it right; we are not revisiting it.
3. **Interneuron self-resolution — KEEP THE NODES, weights go plastic.** The interneuron *nodes*
   (DRN-GABA, CeA-GABA, cortical — real, cited anatomy: Knobloch, Challis, etc.) STAY; only their
   hand-set *weights* become plastic and self-organize. Removing the nodes would cut real anatomy;
   making their weights plastic is the point. The self-organizer owns the weights; the anatomy is
   preserved.
4. **M4 is FUNCTIONAL VERIFICATION + HONEST OBSERVATION — not result-chasing.** No result is a target.
   M4 verifies the substrate still *functions correctly* (the functional invariants — v9 aggression
   closure, the neutral floor, the substrate operating as a working substrate) and then **observes and
   honestly describes whatever the self-organized substrate now produces.** The adolescent inverted-U
   (and every other emergent pattern) is an *observation to report*, NOT a result to preserve or
   re-derive — if it emerges, we describe it; if it does not, we describe that. Re-deriving it as if it
   must survive would make it a target, which is the tuning-toward-a-wanted-outcome trap one level up.
   The model produces what it produces; we observe. (This corrects an earlier framing that treated
   results as things to re-derive — they are not.)

---

*M3 replaces the inert homeostatic rule with a working cross-homeostatic self-organizer, grounds the
setpoints and timescales it drives toward, and verifies that weights genuinely self-organize — perturbations
self-correct, seed defaults stop dominating, and the hand-tuned interneuron weights self-resolve. It is a
rule REPLACEMENT (not a rate increase — that would oscillate), grounded in the cross-homeostatic
literature. Nothing is built until the researcher reviews. M4 (verify the substrate still functions
correctly, then observe what it produces — no result a target) and M5 (re-integrate v14) follow.*
