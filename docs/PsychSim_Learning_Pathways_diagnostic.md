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
