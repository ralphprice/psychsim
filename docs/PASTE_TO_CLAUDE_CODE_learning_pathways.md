# Paste this into the Claude Code session

---

`04f7dc9` is verified on the remote — the PFC↔memory loop close-out is confirmed and that phase is cleared:
`vlPFC→LA` correctly re-targeted to `vlPFC→ITC` (joining the vmPFC→ITC extinction route, cited), edge count
unchanged, vlPFC now regulates threat (lowers CeA) instead of exciting it, no other edge changed, plasticity/
engine byte-identical, full suite green. Good work — and the resequencing finding is accepted: the loop is
mechanism-complete but its closure is blocked on the learning-pathways phase, which comes next.

**Please now begin the learning-pathways phase per `docs/PsychSim_Learning_Pathways_Handover.md`.**

**Start with the diagnostic — surface it for review before building anything** (the discipline that's caught
wrong premises every time). Confirm against the actual code:

1. **Consequence/RPE learning exists** — the dopamine teaching signal (`neuromod_output("DA")`), the RPE-gated
   plasticity, `ValueLearner`/BCM consolidation. (Preliminary check says it's solid — confirm.)
2. **The Arena observational seed exists** — the perceiver already perceives the *other's emergent act* via
   `_perceive(other_act)` → `_add_physical_percept` → `felt_response`. (Confirm the perceiver perceives and
   reacts to others' acts.)
3. **The gap: vicarious learning and modeling/imitation are missing** — the perceiver reacts to others' acts
   but does NOT learn a disposition from the *consequence to the other* (vicarious), and there's no modeling/
   imitation. Confirm this is the gap.

Then surface the diagnostic for reviewer review **before** any build.

**Standing constraints (from the handover, restated so they're unmissable):** current architecture only —
episodic memory and the plug-and-play redesign are DEFERRED as a future parallel version (no ensemble work,
no restructuring); memory is the substrate (no symbolic store); integrate don't bolt on (use the existing
observational seed + DA/RPE plasticity machinery, not a parallel learning module); dispositions EMERGE, never
coded; full suite is the clearance gate; commit + push + STOP for reviewer verification on the remote.

The two phases connect precisely: vicarious learning — observing a consequence to another driving the
perceiver's own plasticity at reduced gain (vicarious < direct) — is what produces the control-disposition the
PFC loop needs. That's why learning comes first; the loop then closes as a consequence.

When you've completed and committed the diagnostic (or surfaced it for review), stop — I'll review it against
the remote before you begin building.

---
