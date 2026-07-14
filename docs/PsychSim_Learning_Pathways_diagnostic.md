# Learning Pathways — code diagnostic (for review; NOTHING built)

Per the governing rule (diagnose against the actual code, surface for review, before any build). Confirms
the preliminary reviewer diagnostic. **Headline: all three points confirmed — consequence-learning exists,
the observational seed exists, vicarious learning + modeling are the gap — with two clarifications from
reading the code.**

## Point 1 — consequence/RPE learning EXISTS (confirmed) — with a clarification
- The substrate's consequence-learning is **DA-gated BCM**: `reward_signal() = engine.neuromod_output("DA")`
  (agent.py) — the live mean activation of the DA source circuits (VTA/SNc); this **IS the RPE** (the
  design's `delta = neuromod_output("DA")`, not a separately-computed TD error). It gates consolidation:
  `consolidate() = lr · eta · modulator · eligibility`, modulator = the DA circuit's live output (R5-NMOD,
  plasticity.py / engine.py:178). Solid and live.
- **CLARIFICATION:** the handover's "ValueLearner/BCM consolidation" conflates two things. `ValueLearner`
  lives in `affective_engine/learning.py` — the **retired valence-engine** learner; it is **NOT in the
  substrate learning path** (test_substrate_learning::test_no_shadow_td_learner asserts the substrate agent
  has no `ValueLearner`/`gamma`). **The learning to integrate vicarious into is the DA-gated BCM**, not
  ValueLearner. (`Appendix C`'s `delta = r + gamma·V′ − V` is the functional-level description; the
  implementation is the DA signal = the RPE.)

## Point 2 — the observational SEED exists (confirmed)
`arena.py::_social_episode`: the perceiver perceives the other's emergent **act** —
`_perceive(other_last_act)` → `_add_physical_percept` / `_add_signature_percept` → `felt_response`. And
`felt_response` **develops the perceiver** (develop=True → "the substrate DEVELOPS through the moment; the
BCM plasticity in settle() IS the use-dependent strengthening"). So the perceiver perceives, reacts to, and
**learns from its OWN reaction** to the other's act. The seed is present and live.

## Point 3 — the GAP: vicarious learning + modeling are missing (confirmed) — with a clarification
- **No vicarious learning.** The observational seed feeds the other's **ACT**, never the **consequence to
  the other**. Nothing computes/presents "the other being hurt / rewarded / punished" to the perceiver, and
  the perceiver's plasticity is driven by its OWN reaction (its own `reward_signal`), not by an observed
  outcome to another. So the perceiver does not learn a disposition from *what happens to others* — the
  Bandura vicarious-reinforcement gap.
- **No modeling/imitation.** No mechanism biases the perceiver's behaviour toward the observed act.
- **CLARIFICATION (an important distinction):** `observer.py` has a `vicarious_response` — but that is the
  empathy **read-out** (the agent's momentary *response to others' distress*, probed with a distress cue),
  NOT vicarious **learning**. The perceiver already *responds* to another's distress (the `vulnerable_other`
  cue → felt_response); what's missing is *learning a lasting disposition from the observed consequence to
  the other*. Response-to-distress ≠ learning-from-others'-outcomes. The gap stands.

## The build shape (for review — NOT built; brought so the reviewer can steer before I build)
Faithful to Bandura + the current architecture:
- **Vicarious learning (primary):** extend the observational seed so the perceiver also perceives the
  **consequence to the other** (the other's valenced outcome — an outcome the Arena can present, as it
  presents the act), and route that observed consequence into the perceiver's **own DA-gated BCM at REDUCED
  gain** (vicarious < direct, per the research) — sourced from the *observed* outcome, tuning the same
  plastic weights direct experience tunes. Integrate into `felt_response` / the DA-gated plasticity — **no
  parallel learning module.** The disposition **emerges**; no coded rule, no coded "copy this."
- **Modeling/imitation (secondary):** a grounded mechanism biasing the perceiver's behaviour toward the
  observed act. Flag if it risks scope-creep; primary deliverable is vicarious learning.

## The connection to the PFC loop (and a caveat to verify)
This is the resequencing payoff: vicarious learning is what should produce the **history-dependent
control-disposition** the PFC↔memory loop needs — observing another's defiance punished should tune the
perceiver's **plastic control edges** (vmPFC→ITC, dmPFC→LA, vlPFC→STN…) toward "in this context, inhibit."
**Caveat to demonstrate at build:** the PFC-loop diagnostic + Memory-Phase-1 found the current developed
history-effect lives in the plastic **bonding** edges, while the control dimension has been history-invariant.
So the build must *show* that the observed-consequence → DA-gated BCM path can actually tune the plastic
**control** edges (not just bonding) — i.e. that vicarious learning reaches the control dimension. That is
the load-bearing verification (handover §3: "it produces a control-disposition"), and it's exactly what
unblocks the loop. If it turns out the DA-gated BCM can't reach the control edges from an observed
consequence, that's a finding to surface — not to force.

**Nothing built.** Surfacing the diagnostic before any change, as ruled. Confirmed the three points (with the
two clarifications); the build shape is above for your steer. How do you want to proceed?

---

## LOAD-BEARING CHECK (revised steer): does an NA teaching signal exist? — OUTCOME (ii)

The revised steer (`PsychSim_Learning_Pathways_RevisedSteer.md`) corrected the build premise: the PFC→control
edges are mostly **NA-gated** (`dmPFC→LA`, `vlPFC→ITC` = NA; `vmPFC→ITC` = DA; `vlPFC→STN` = none), so vicarious
learning must route by **valence-matched neuromodulator** — DA for observed reward, **NA for observed
punishment** — and NA is the only route that reaches the control edges. First task: verify an NA teaching
signal exists. **Result: OUTCOME (ii) — the NA teaching-signal mechanism exists but its signal is INERT,
because the NA source (LC) is unafferented. This is the same structural gap as the Part-1 PVN-OT hub.**

**What exists (the mechanism is sound):**
- `neuromod_source["NA"] = ["LC"]`; the R5-NMOD gate uses `neuromod_output("NA")` for NA-gated edges. Injecting
  LC confirms the gate rises and **would reach the control edges**: LC 0→0.5→1.0 ⇒ `neuromod_output("NA")`
  0.05→0.55→1.0 (which gates `dmPFC→LA` / `vlPFC→ITC` consolidation). So *if* LC rose with an aversive event,
  the aversive teaching signal would tune the control edges — the mechanism is correct.
- LC even has efferents (LC→LA/BA/CeA/dlPFC/IML — it distributes noradrenaline).

**What's missing (the isolated gap):**
- **`LC` has ZERO afferents** (no circuit, no channel). So it never rises: `neuromod_output("NA")` is flat at
  0.050 under **every** aversive condition tested (nociception, CeA, provocation, CO2-acidosis). There is no
  functional NA teaching signal.
- Contrast — DA works: reward (sweet) drives VTA→0.71 and `neuromod_output("DA")` 0.049→0.382. DA is a valenced
  reward teaching signal; NA is inert. **So aversive vicarious learning has nowhere to route** — the NA-gated
  control edges are gated by a signal that never fires.
- This is exactly the **PVN-OT unafferented-hub gap (Part 1)**: a neuromodulator hub wired to *distribute*
  (efferents present) but not *driven* (afferents absent).

**The upstream dependency (surfaced for a reviewer decision — NOT built, NOT forced):**
Before aversive vicarious learning can be built (and the PFC loop unblocked), the substrate needs a functional
NA teaching signal — i.e. **LC needs its grounded afferents: the aversive drivers of noradrenaline.** These are
textbook and all present as circuits already: **`CeA→LC`** (central-amygdala threat-arousal drive of LC),
**nociception / `PBN→LC`** (spino-parabrachial pain), **`NTS→LC`** (A2 visceral/autonomic). Completing them
(cited, at band — the PVN-OT afferent-completion precedent) makes LC rise with aversive outcomes →
`neuromod_output("NA")` becomes the aversive teaching signal → the NA-gated control edges tune toward inhibition
→ the control-disposition forms → the loop unblocks.

**Do NOT force:** re-gating the control edges to DA would be a false-mechanism dodge — they are NA-gated because
threat-regulation learning is noradrenergic (correct anatomy). Per the steer, stop and report on outcome (ii):
this phase surfaces a **further upstream dependency (the LC afferent completion)** that must be decided before
the vicarious mechanism is built. The dependency chain: vicarious aversive learning → needs a functional NA
teaching signal → needs LC to rise with aversive events → needs LC's (currently absent) afferents.
