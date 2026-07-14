# PsychSim — Representational-Memory Layer, Next Phase: the PFC↔Memory Presentation Loop

**Design specification. Status: SPEC ONLY — nothing built. For researcher review, then handover.**

## 0. Where this sits (context — read first)

The representational layer builds the mind's behaviour-guiding models (beliefs/attitudes/rules/morality →
emerge later; dominance-hierarchy = first application). **Memory Phase 1 is landed and verified**
(`origin/main`): memory is unified as ONE sub-symbolic substrate — the plasticity's developed weights (the
engram), emotionally weighted via neuromodulator-gated consolidation — with the symbolic overlay retired.

**A recent design arc considered episodic memory (an ensemble/population phenomenon) and a plug-and-play
architectural redesign to host it. Decision: HELD.** An isolated feasibility probe proved the ensemble
mechanism works and would be *provably inert* for unconnected rate circuits, but the faithful population→rate
readout is unsolved, so building it now isn't yet worth the cost. **The redesign is deferred as a future
*parallel version* for cross-system comparison — NOT part of this or any current build.** This phase, and
all near-term memory work, stays **within the current nucleus-level architecture, on the semantic/procedural
substrate we have.** No restructuring. No ensemble work. No risk to the working system.

**This phase = the PFC↔memory presentation loop:** the executive function contextually surfacing the
relevant learned *disposition/expectation* from the developed weights to modulate (often inhibit) the
behaviour the lower circuits propose — "the executive presents the relevant representation when the
situation calls for it, often inhibitory" (respecting authority = a contextual reminder that certain
behaviour is required or it could turn out badly). Grounded in the dlPFC↔hippocampus top-down-retrieval
research.

## 1. Diagnosis first (the governing discipline — do NOT spec a build on an unverified premise)

The last several specs were written from assumption and corrected by the build session reading the code (the
symbolic prime was already dead; the history-effect was bonding not threat). **This phase MUST begin with a
diagnostic against the actual code, surfaced for review, before any build.** A preliminary reviewer
diagnostic (verified against the remote) already shows the substrate is **largely present**, so the honest
framing is *diagnose → confirm what's live vs. present-but-inert → integrate/refine* — NOT "build a
retrieval loop from scratch."

**Preliminary diagnostic (reviewer, verified — the build session must confirm/extend):**
- **PFC circuits present:** vmPFC, dlPFC, dmPFC, OFC, dACC, vlPFC.
- **22 PFC→subcortical top-down control edges exist** (the "executive modulates behaviour" pathway):
  e.g. dmPFC→LA, vlPFC→LA, OFC→NAc-core, OFC→VTA, dACC→PAG-PANIC, vmPFC→DRN (AMPA, anatomy), OFC→DRN (AMPA,
  anatomy). **Many are `fallback` (unsigned) receptors / `assumption` basis** — the pathway EXISTS but is
  not fully signed/grounded.
- **Memory already reaches the PFC:** `HPCv→vmPFC` and `HPCv→dlPFC` both exist. HPCv also →LA, →BA,
  →NAc-shell. So the *memory→executive* and *memory→limbic* directions are **already wired**. The
  developed-weight disposition (Phase-1 memory) already projects toward the executive.

**So the loop's substrate is substantially present.** The open question is FUNCTIONAL, and the build MUST
answer it by reading/running the code before building: **is the executive actually modulating behaviour
based on the memory-derived disposition — or are these edges present-but-inert (like the dead prime)?**

## 2. What this phase IS and IS NOT

- **IS:** diagnose what's functionally live in the PFC↔memory loop; make the executive-contextual-modulation
  actually work through the *existing* wiring — the PFC surfacing/using the memory-derived disposition
  (via HPCv→PFC and the developed weights) to modulate (often inhibit) proposed behaviour contextually.
  Where the pathway exists but is unsigned/inert, sign/grounded it per the receptor facts so it functions.
- **IS NOT:** building episodic memory / any ensemble mechanism (deferred); the plug-and-play redesign
  (deferred); a new symbolic retrieval store (memory is the substrate — Phase 1); coding beliefs/rules
  (they emerge later, read out, never coded); dominance-hierarchy (the first *application*, comes after this
  layer). And NOT bolting on a parallel "retrieval module" — integrate into the existing PFC/HPCv wiring.

## 3. The mechanism (faithful to the research, integrated into what exists)

The research (dlPFC↔hippocampus top-down retrieval; PFC goal-modulated/selective retrieval and
retrieval-suppression; PFC inhibitory control) describes: the executive, in a context, does **goal-modulated
retrieval** of relevant memory and exerts **inhibitory/modulatory control** over the behaviour the lower
circuits propose. In our substrate, faithfully and within the current architecture:

- **Memory = the developed weights + their read-out via HPCv→PFC** (Phase-1 substrate memory). The
  "relevant disposition" is the memory-derived signal the PFC receives given the current context — no
  symbolic retrieval, no episode store.
- **Contextual presentation = the PFC's context-dependent response** to that memory-derived input, gated by
  the current situation (the PFC integrates current sensory/limbic state + the memory-derived disposition,
  and its output depends on context — which is what a rate-level PFC circuit receiving HPCv + current inputs
  already does *if the edges are live and signed*).
- **Modulation/inhibition = the existing PFC→subcortical control edges** (dmPFC→LA, OFC→DRN, dACC→PAG, etc.)
  carrying the executive's modulation onto the behaviour-proposing circuits. "Respecting authority" =
  contextually, the PFC's memory-informed output inhibits the defiant response via these edges.
- **The honest form:** the executive doesn't retrieve a symbolic rule; it receives a memory-derived
  disposition (learned anticipated-consequence, in the weights) and, *in context*, modulates the proposed
  behaviour through existing control edges. All emergent from the wiring — no coded rule, no coded retrieval.

**Grounding requirement:** any edge that must be signed/grounded to make the loop function (the `fallback`/
`assumption` PFC→limbic and HPCv→PFC edges) is signed from the receptor facts / cited anatomy — per-edge,
same methodology as all prior grounding. Making an inert-but-present edge functional by grounding its sign
is NOT a value change; it is completing the marked connection faithfully (the DRN/interneuron re-mark
precedent).

## 4. Verification

- **Diagnostic surfaced first** (before build): which PFC↔memory edges are live vs. present-but-inert; what
  the executive currently does with the memory-derived disposition; reviewed before any change.
- **The loop functions:** demonstrate that the executive *contextually modulates* proposed behaviour based on
  the memory-derived disposition — e.g., an agent whose developed weights encode "this situation went badly"
  shows PFC-mediated inhibition of the proposed response *in that context*, sourced from the memory→PFC→
  control-edge path (measured, emergent — NOT a coded rule). Report the contextual-modulation effect.
- **Inhibitory/modulatory control is real:** the PFC→subcortical edges actually change the downstream
  behaviour when the executive engages (not present-but-inert).
- **Any grounded/signed edge is per-edge cited** (receptor facts / anatomy), at its band — provenance
  recorded.
- **Full suite green** (the gate); golden regenerates honestly if behaviour shifts (the executive now
  modulating where it didn't); plasticity + existing circuits otherwise intact; v9 closure + Phase-1 memory
  intact.
- **No result is a target; no coded beliefs/rules** — the contextual modulation emerges from the wiring; if
  it differs from expectation that's a finding, not something to tune toward.

## 5. Process & honesty
- **Diagnose against the code first, surface for review, THEN build** — do not build on an unverified premise.
- **Integrate, don't bolt on** — use the existing PFC/HPCv wiring; sign/ground inert edges to make them
  function; do NOT add a parallel retrieval module.
- **Current architecture only** — no episodic/ensemble work, no plug-and-play redesign (both deferred as a
  future parallel version).
- **Memory is the substrate** (Phase 1) — no symbolic retrieval store.
- **Full suite is the gate; dual-reviewed** (reviewer verifies against the remote: the loop functions, edges
  cited/signed, suite green, any shift understood); commit + push + STOP for clearance before the next piece
  (the learning pathways, then dominance-hierarchy as the first application).

## 6. What comes after (context, NOT this phase)
- **Learning pathways** — vicarious/observational (Bandura), modeling/imitation, on the observational seed
  in the Arena, so dispositions form through multiple routes, not just consequence-learning.
- **Then** the higher-order read-outs (beliefs/attitudes/rules/morality) EMERGE from this layer, read out,
  never coded; and **dominance-hierarchy re-enters as the first application** (rank = consequence-learned
  disposition in the unified memory, surfaced/overridden by the PFC as respect vs. defiance — exactly the
  loop this phase builds).
- **The plug-and-play / episodic-ensemble redesign** — a deferred FUTURE PARALLEL VERSION for cross-system
  comparison; not current work.

---

*This phase builds the PFC↔memory presentation loop within the current architecture: the executive
contextually surfacing the memory-derived disposition (developed weights via HPCv→PFC) to modulate/inhibit
proposed behaviour through the existing PFC→subcortical control edges — integrating into wiring that is
already substantially present, grounding/signing the inert edges faithfully. It begins with a code
diagnostic surfaced for review (the substrate largely exists; the question is what's functionally live),
never builds on an unverified premise, stays entirely within the current architecture (episodic/ensemble and
the redesign deferred as a future parallel version), keeps memory as the substrate, and lets contextual
modulation emerge — never coding beliefs or rules. Nothing is built until the researcher approves the
diagnostic and this spec.*
