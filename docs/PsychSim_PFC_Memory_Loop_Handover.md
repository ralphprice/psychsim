# Memory Layer — PFC↔Memory Presentation Loop — Claude Code handover

**Build the PFC↔memory presentation loop: the executive contextually surfacing the memory-derived
disposition to modulate (often inhibit) proposed behaviour — within the current architecture, integrated
into wiring that is already substantially present.** Design authority:
`PsychSim_PFC_Memory_Loop_SPEC.md` (reviewed).

## 0. Critical framing (read before anything)

- **Memory Phase 1 is DONE + verified** (`origin/main`): memory is ONE sub-symbolic substrate (the
  plasticity's developed weights = engram, emotionally weighted via neuromodulator-gated consolidation),
  symbolic overlay retired. Memory IS the substrate — **do not add a symbolic retrieval store.**
- **Episodic memory + the plug-and-play redesign are DEFERRED** — a feasibility probe proved the ensemble
  mechanism works and would be inert for unconnected circuits, but the faithful population→rate readout is
  unsolved, so it's held as a **future PARALLEL VERSION for cross-system comparison.** **This build stays
  entirely within the current nucleus-level architecture. No ensemble work. No restructuring. Zero risk to
  the working system.**
- **This build = the PFC↔memory presentation loop.** The executive, in a context, surfaces the relevant
  learned *disposition/expectation* from the developed weights and modulates (often inhibits) the behaviour
  the lower circuits propose. (Your example: "respecting authority" = the executive contextually reminding
  that certain behaviour is required "or it could turn out badly" — an inhibitory, memory-informed,
  context-triggered modulation.)

## 1. DIAGNOSE FIRST — do not build on an unverified premise (the hard-learned rule)

The last specs were written from assumption and you correctly caught the errors by reading the code (the
symbolic prime was already dead; the history-effect was bonding not threat). **Begin by diagnosing the
actual code and surface it for reviewer review BEFORE building.** A preliminary reviewer diagnostic
(verified against the remote) shows the substrate is **largely present** — so the honest job is
*diagnose → confirm live vs. present-but-inert → integrate/refine*, NOT build-from-scratch:

- **PFC circuits present:** vmPFC, dlPFC, dmPFC, OFC, dACC, vlPFC.
- **22 PFC→subcortical top-down control edges exist** (the executive-modulation pathway): dmPFC→LA,
  vlPFC→LA, OFC→NAc-core, OFC→VTA, dACC→PAG-PANIC, vmPFC→DRN (AMPA/anatomy), OFC→DRN (AMPA/anatomy), etc.
  **Many are `fallback` (unsigned) / `assumption` basis** — pathway EXISTS but not fully signed/grounded.
- **Memory already reaches the PFC:** `HPCv→vmPFC`, `HPCv→dlPFC` both exist (HPCv also →LA, →BA, →NAc-shell).
  The developed-weight disposition already projects toward the executive.

**The open question is FUNCTIONAL — answer it by reading/running the code before building:** is the executive
actually modulating behaviour based on the memory-derived disposition, or are these edges present-but-inert
(like the dead prime was)? Confirm/extend this diagnostic and surface it for review.

## 2. The build (integrate into what exists; faithful to the research)

Research basis: dlPFC↔hippocampus top-down/goal-modulated retrieval; PFC inhibitory control &
retrieval-suppression. In our substrate, within the current architecture:

- **Memory = developed weights + their HPCv→PFC read-out** (Phase-1 substrate memory). No symbolic retrieval.
- **Contextual presentation = the PFC's context-dependent response** to the memory-derived input (PFC
  integrates current sensory/limbic state + the memory-derived disposition; its output depends on context —
  which a rate-level PFC circuit receiving HPCv + current inputs already does *if the edges are live and
  signed*).
- **Modulation/inhibition = the existing PFC→subcortical control edges** carrying the executive's modulation
  onto behaviour-proposing circuits (dmPFC→LA, OFC→DRN, dACC→PAG…).
- **The honest form:** the executive receives a memory-derived disposition (learned anticipated-consequence,
  in the weights) and, in context, modulates the proposed behaviour through existing control edges. Emergent
  from the wiring — **no coded rule, no coded retrieval.**

**Where the loop is present-but-inert:** if edges exist but are `fallback`/unsigned so the modulation can't
function, **sign/ground them from the receptor facts / cited anatomy** — per-edge, at band. Making an
inert-but-present edge functional by grounding its sign is a marked-connection completion (the DRN/interneuron
re-mark precedent), NOT a value change. Cite each.

## 3. Verify
- **Diagnostic surfaced first** (live vs. inert edges; what the executive currently does with memory) —
  reviewed before any change.
- **The loop functions:** an agent whose developed weights encode "this went badly" shows PFC-mediated
  contextual inhibition of the proposed response *in that context*, sourced from memory→PFC→control-edge
  (measured, emergent — NOT a coded rule). Report the contextual-modulation effect (with-context vs.
  without-context, or bad-history vs. neutral-history modulation).
- **Inhibitory/modulatory control is real** (the PFC→subcortical edges actually change downstream behaviour
  when the executive engages).
- **Any signed/grounded edge is per-edge cited** (receptor facts / anatomy), at band, provenance recorded.
- **Full suite green** (gate); golden regenerates honestly if behaviour shifts; plasticity + existing
  circuits otherwise intact; v9 + Phase-1 memory intact.
- **No result is a target; no coded beliefs/rules.**

## 4. Process
- **Diagnose → surface for review → build.** Never build on an unverified premise.
- **Integrate, don't bolt on** — use existing PFC/HPCv wiring; sign inert edges to make them function; NO
  parallel retrieval module.
- **Current architecture only** — no episodic/ensemble, no redesign (deferred as future parallel version).
- **Memory is the substrate** — no symbolic store.
- **Full suite is the gate; dual-reviewed** (reviewer verifies on the remote: loop functions, edges
  cited/signed, suite green, shift understood); **commit + push + STOP for clearance** before the next piece.

## 5. Hand-off note (for the implementation session)

> **Build the PFC↔memory presentation loop** — the executive contextually surfacing the memory-derived
> disposition to modulate/inhibit proposed behaviour. Authority: `PsychSim_PFC_Memory_Loop_SPEC.md`.
> **CURRENT ARCHITECTURE ONLY** — episodic memory + the plug-and-play redesign are DEFERRED as a future
> parallel version; no ensemble work, no restructuring. Memory is the Phase-1 substrate (developed weights +
> HPCv→PFC read-out) — **no symbolic retrieval store.**
>
> **DIAGNOSE FIRST** (don't build on an unverified premise — the prior specs' premises were wrong and you
> caught them by reading the code): the substrate is largely present — PFC circuits (vmPFC/dlPFC/dmPFC/OFC/
> dACC/vlPFC), 22 PFC→subcortical control edges (many `fallback`/unsigned), and HPCv→vmPFC/dlPFC already
> wire memory to the executive. **Confirm what's functionally LIVE vs. present-but-inert, surface it for
> review, THEN build.**
>
> **Build:** make the executive contextually modulate proposed behaviour from the memory-derived disposition
> (memory→PFC→existing control edges), emergent — no coded rule/retrieval. Where edges exist but are inert/
> unsigned, sign/ground them per receptor facts / anatomy, per-edge cited, at band (a marked-connection
> completion, not a value change).
>
> **Verify:** the contextual-modulation effect is real and emergent (bad-history/context → PFC-mediated
> inhibition of the proposed response, measured); PFC→subcortical control actually changes behaviour; signed
> edges cited; full suite green (golden regen honestly if behaviour shifts); v9 + Phase-1 intact. **No result
> is a target; no coded beliefs.**
>
> **Process:** diagnose → surface → build; integrate don't bolt on; current architecture only; full suite is
> the gate; dual-reviewed on the remote; commit + push + STOP for clearance before the learning pathways
> (then dominance-hierarchy as the first application of this loop).
