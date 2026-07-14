# Learning Pathways — Revised Build Steer (post-diagnostic) — Claude Code

**The diagnostic (`f42a696`) was reviewed and verified on the remote. It stands — but the reviewer's
verification found the handover's build premise is TOO SIMPLE, in a way that is load-bearing for whether this
phase unblocks the PFC loop. This note corrects the build shape. Do the load-bearing verification FIRST,
surface it, before building the full mechanism.**

## The finding that corrects the premise

The handover said: "route observed consequences into the DA-gated BCM → the control-disposition forms → the
loop unblocks." **The reviewer verified the PFC→control edges against the remote, and most are NOT DA-gated:**

| control edge | plastic | gated by |
|---|---|---|
| `vmPFC→ITC` | yes | **DA** |
| `dmPFC→LA` | yes | **NA** |
| `vlPFC→ITC` | yes | **NA** |
| `vlPFC→STN` | yes | none |
| `vmPFC→DRN` | yes | none |
| `OFC→DRN` | yes | none |
| `vmPFC→DRN-GABA` | yes | none |
| `OFC→DRN-GABA` | yes | none |

**So a DA-routed vicarious signal reaches only `vmPFC→ITC` — NOT the NA-gated control edges (`dmPFC→LA`,
`vlPFC→ITC`) that carry most of the executive-inhibition pathway.** Routing observed consequences uniformly
into DA would build a vicarious mechanism that *works* (tunes DA-gated reward/bonding edges) but does NOT
unblock the loop (never reaches the control dimension). That is the manufacture-the-answer trap waiting to
happen — avoid it.

## The corrected mechanism (more faithful to the research, and it's what reaches the control edges)

Vicarious learning is NOT purely dopaminergic. Observing another's **punishment** — the case that produces
the control-disposition ("defiance punished → inhibit") — is an **aversive** observation, which engages the
**noradrenergic/stress** system, not the dopaminergic/reward one. Observing another **rewarded** is
appetitive → dopaminergic. So:

**Vicarious learning routes the observed consequence into the teaching signal of the neuromodulator that
MATCHES THE OUTCOME'S VALENCE — DA for an observed appetitive outcome, NA for an observed aversive outcome —
at reduced gain (vicarious < direct), which then gates plasticity on the edges that neuromodulator gates.**
This is faithful to direct learning (which already matches neuromodulator to valence) AND it is the only route
that reaches the NA-gated control edges to form the control-disposition and unblock the loop. Observed
punishment → NA teaching signal → tunes `dmPFC→LA` / `vlPFC→ITC` toward inhibition → control-disposition
forms → loop unblocks.

## THE LOAD-BEARING FIRST TASK (do this and surface it BEFORE building the full mechanism)

The corrected mechanism depends on the substrate having an **NA teaching signal** analogous to the DA one.
`reward_signal() = neuromod_output("DA")` is the DA teaching/RPE signal. **Verify against the code:**

1. **Does an NA teaching/RPE-analogue signal exist** (an aversive/threat teaching signal, e.g.
   `neuromod_output("NA")` used to gate consolidation the way DA is)? Or is DA currently the ONLY neuromodulator
   wired as a teaching signal into `consolidate()`?
2. **Can an observed aversive consequence, routed through NA, actually tune the NA-gated control edges
   (`dmPFC→LA`, `vlPFC→ITC`) toward inhibition?** Demonstrate the path reaches them.

**Two outcomes — surface whichever it is, do NOT force:**
- **(i) NA teaching signal exists / is groundable** → aversive vicarious learning routes through it, reaches
  the NA-gated control edges, loop unblocks. Clean — proceed to build the full valence-matched vicarious
  mechanism.
- **(ii) NA teaching signal does NOT exist** → vicarious aversive learning has nowhere to route. This is a
  genuine finding, NOT something to fix by re-gating the control edges to DA (that would be a false-mechanism
  dodge — the control edges are NA-gated because threat-regulation learning is noradrenergic, which is likely
  correct anatomy). Surface it: the substrate may need a grounded NA teaching-signal mechanism (a real,
  cited addition), OR the control-disposition forms through another route to identify. **This would mean the
  phase surfaces a further upstream dependency — report it for a reviewer decision before building.**

## Then (only if outcome (i)) the full build
Extend the observational seed so the perceiver perceives the **consequence to the other WITH ITS VALENCE**
(aversive = other hurt/punished; appetitive = other rewarded), presented at reduced gain, routed to the
**valence-matched teaching neuromodulator** (NA aversive / DA appetitive), gating the same plastic weights
direct learning tunes — integrated into `felt_response`/plasticity, no parallel module. The disposition
EMERGES, never coded.

**Verify:** observed punishment (not direct) shifts the perceiver's NA-gated control edges toward inhibition,
measured + emergent + reduced-gain (the resequencing payoff — this unblocks the PFC loop); observed reward
shifts appetitive/DA-gated disposition; new mechanism cited; full suite green (golden regen honestly);
consequence-learning + Phase-1 + v9 intact. No result is a target.

## Scope
- **Modeling/imitation is DEFERRED to a following sub-step** — not this phase. Vicarious learning is now
  load-bearing enough (the valence-matched routing + the NA-teaching-signal question) to take the full focus.
  Flag modeling as deferred, not dropped.
- **Current architecture only** (episodic/ensemble + plug-and-play redesign remain deferred); memory is the
  substrate; integrate don't bolt on; dispositions emerge never coded.

## Process
- **Do the load-bearing NA-teaching-signal verification FIRST and surface it** (outcome (i) or (ii)) **before
  building the full mechanism.** If (ii), stop and report — do not build or force.
- Full suite is the gate; dual-reviewed on the remote; commit + push + STOP for reviewer clearance.
