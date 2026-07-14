# PsychSim — Representational-Memory Layer, Phase 1: unify memory as one sub-symbolic substrate

**Design specification. Status: SPEC ONLY — nothing built. For researcher review.**

This is **Phase 1** of the representational layer (the mind's models-of-understanding — beliefs, attitudes,
morality, rules — that guide behaviour via the executive; dominance-hierarchy is the first application,
paused behind this layer). Phase 1 is the **foundation**: make memory **one sub-symbolic thing** by
dissolving the parallel symbolic memory-stream into the substrate's existing plasticity-memory
(**Reading A — integrate/unify, not extend**). The richer sub-symbolic episodic/retrieval capacity and the
PFC↔memory presentation loop are **later phases**, built on this unified foundation.

**Governing discipline: integrate, don't bolt on.** The symbolic `MemoryStream` is an existing *bolt-on* —
a parallel memory device running alongside the substrate. Phase 1 **un-bolts it**: same functional
behaviour, sourced from the substrate that already produces it, not from a scaffold on top.

---

## 0. The diagnostic this rests on (verified against the remote)

- **The substrate already has honest sub-symbolic memory: its plasticity.** `engine.py` holds
  `self.weight[]` (developed connection weights = the engram) and `self.eligibility[]` (short-term trace);
  `plasticity.py` does BCM correlation → eligibility trace → R5 consolidation → R4 homeostatic scaling →
  R7 pruning of long-silent weights. That IS the neuroscience of memory — engrams as distributed weights,
  LTP-analogue consolidation, graceful decay, forgetting-by-pruning. **Memory, sub-symbolically, exists.**
- **A separate symbolic `MemoryStream` (memory.py) runs at the town layer.** Episode records
  (`EpisodicMemory`: label, appraisal, dominant network, valence, importance), retrieved by
  **recency × importance × relevance** ("following the generative-agents memory-stream design"), feeding
  behaviour by **priming** an appraisal (a threatening past → threat-primed appraisal). It is called
  ONLY in `sim_world` (`gamemaster.py`, `daily.py`) — **never in the substrate life-course**
  (`affective_engine/development.py` does not call `prime()`/`retrieve()`).
- **The town layer already runs the substrate.** `person.social_act` → `mind.social_act` → the substrate's
  emergent act; `person.mind.engine` is the developing substrate. So the substrate the symbolic stream
  should dissolve into is **already present and developing in the same loop** — the symbolic stream just
  runs alongside it, `.add()`-ing records that don't feed back through the substrate.

**Conclusion:** this is not two memory systems competing inside the substrate; it is the substrate's honest
plasticity-memory **plus a parallel symbolic scaffold one layer up**. Phase 1 dissolves the scaffold into
the substrate. (This is the "we differ from Joon Park" the researcher flagged: memory becomes the
sub-symbolic substrate, not a symbolic episode-list.)

---

## 1. What Phase 1 IS and IS NOT

- **IS:** make the priming effect the symbolic stream produces **emerge from the substrate's developed
  weights** (which already produce it), and retire the symbolic `MemoryStream` as the scaffold it is — so
  memory is ONE sub-symbolic thing everywhere. Same functional behaviour (history shapes the agent),
  sourced from the substrate.
- **IS NOT:** building richer/episodic/retrieval memory (that's the next phase); building the PFC↔memory
  presentation loop (later phase); adding new circuits; changing what develops. It is a *consolidation /
  un-bolting*, not an extension.

---

## 2. Why the priming effect already lives in the substrate (the integration's basis)

The symbolic stream's `prime()` does one functional thing: **a threatening/negative past makes the agent
respond to a new situation as more threatening / less controllable / more socially wary** ("a learned
expectation"). But the substrate **already produces exactly this**, honestly:

- An agent whose history was threatening has, through plasticity (BCM + consolidation), **threat-tuned
  weights** — its threat circuits (CeA/LA, the DRN/vmPFC regulation) are developed to respond more strongly
  to threat-relevant cues. That IS "threat-primed," sourced from the developed substrate.
- A warm history tunes the bonding/reward weights (the OT/NAc circuits we completed) — "does not become
  threat-primed," honestly, because those weights developed differently.

So priming is **not a separate mechanism to preserve** — it is a *read-out of the substrate's developed
state*. The symbolic stream was computing, at the town layer, an effect the substrate produces at the
weight level. Integration = **let the effect come from the substrate**, retire the parallel computation.

Grounding (memory neuroscience): memory is distributed engrams strengthened by LTP with emotional tagging
and graceful decay (Josselyn/Frankland engram work; the consolidation literature; the "neural traces of
forgotten memories persist" finding). The amygdala's emotional tagging strengthens salient memories — which
in our substrate is the modulator-gated consolidation (R5-NMOD, the neuromodulator-driven gate) already
strengthening salient (high-activation) events more. **The substrate's plasticity already implements the
engram/consolidation/decay/salience picture; the symbolic stream is a redundant symbolic overlay of it.**

---

## 3. The build (un-bolt the scaffold, source the effect from the substrate)

### 3.1 Make the town-layer priming emerge from the substrate
Where the town layer currently calls `memory.prime(appraisal)` to nudge an appraisal from episode records,
the effect must instead come from **the agent's developed substrate state**. Concretely (exact mechanism to
be settled at build, but the shape):
- The agent's **developed weights already encode its history** (threat-tuned vs. warm-tuned). The "learned
  expectation" that priming injected is **already present** in how the substrate responds to the cue — so
  the honest change is to **stop overriding the appraisal with a symbolic prime and let the substrate's
  developed response carry the history-effect**. The substrate, run on the cue, already responds
  history-appropriately because its weights developed from that history.
- If any priming-like *fast* effect is genuinely needed beyond what the developed weights give (a
  short-term carryover between adjacent events), that is the **eligibility trace / recent-activation state
  the substrate already has** (the short-term memory), not a symbolic record. Use the substrate's own
  short-term state, not the episode-list.

### 3.2 Retire the symbolic MemoryStream as a behavioural device
- Remove the symbolic stream from the **behavioural path** (the `prime()`-based appraisal nudging in the
  town layer): behaviour is shaped by the substrate (developed weights + short-term substrate state), not by
  a parallel episode-list. Memory is ONE sub-symbolic thing.
- **The record-keeping question (flag for researcher):** the `MemoryStream` also serves as a *descriptive
  log* (`.summary()` — "N episodes, mean valence, modes run") for inspection/UI, and `EpisodicMemory`
  records are written for the trace. Retiring the stream as a *behavioural* device does NOT require deleting
  the *descriptive log* — a read-only event log for inspection is fine (it's a trace, not a memory
  mechanism). **Recommendation:** keep a purely-descriptive event log if useful for UI/trace, but it must be
  clearly NON-behavioural (nothing reads it back into behaviour) — so it can't drift back into being a
  parallel memory mechanism. The behavioural memory is the substrate; the log is just a record. Researcher
  to confirm: keep the descriptive log, or remove entirely.

### 3.3 What must NOT change
- **The substrate's plasticity is untouched** — BCM, eligibility, consolidation, homeostasis, pruning all
  stay exactly as they are. This phase does not modify how the substrate learns/remembers; it makes the
  substrate the *sole* memory, by removing the parallel symbolic overlay.
- **No new circuits, no weight changes, no sign changes.** This is a *code-architecture* integration (retire
  a parallel device, source its effect from the substrate), not a substrate change. The seed connectome is
  untouched.
- **Behaviour should be preserved or more honest** — the history-effect the symbolic prime produced comes
  from the developed substrate instead. If removing the symbolic prime *changes* behaviour, that change must
  be understood (is the substrate's history-effect weaker/stronger than the symbolic prime's? — a finding
  to surface, not to paper over by re-adding the prime).

---

## 4. Verification

- **Memory is one sub-symbolic thing:** grep-confirm the behavioural path no longer routes through the
  symbolic `MemoryStream.prime()`/`retrieve()`; behaviour is shaped by the substrate (developed weights +
  short-term substrate state). Any surviving `MemoryStream` use is purely descriptive (logging), reads back
  into nothing.
- **The history-effect is preserved via the substrate:** an agent developed under a threatening history
  responds to a new threat cue more strongly than one developed under a warm history — sourced from the
  *developed weights*, demonstrated by running the substrate (not by a symbolic prime). This is the priming
  effect, now emergent. Measure it (threatening-history vs warm-history response gradient).
- **Substrate plasticity unchanged:** the plasticity rules, consolidation, decay, pruning are byte-identical
  — confirm no change to `plasticity.py` / the engine's learning path.
- **Full suite green** — the gate. Town-layer behaviour may shift slightly (priming now from the substrate,
  not the symbolic overlay); if the golden regenerates, it regenerates *honestly* (the history-effect now
  sourced from the substrate). Any behavioural shift is understood and recorded, not tuned away.
- **v9 closure + all prior phenomena intact** — this touches memory architecture, not the circuits, so the
  substrate's emergent behaviour is preserved.

---

## 5. Honesty & process
- **Integrate, don't bolt on** — the whole phase is *un-bolting* an existing bolt-on (the symbolic stream).
  The test of success: memory is one sub-symbolic thing, and the priming effect comes from the substrate
  that already produced it, not a parallel device.
- **We differ from Joon Park (as ruled):** memory is the sub-symbolic substrate (engrams/weights,
  consolidation, decay), NOT a symbolic episode-stream. This phase makes that true by retiring the
  symbolic stream from the behavioural path.
- **No result is a target:** the history-effect emerging from the substrate is a *consequence* of the
  developed weights; if it differs from the symbolic prime's effect, that's a finding about what the
  substrate actually does, reported honestly — never re-add the symbolic prime to hit the old behaviour.
- **Full suite is the gate.** Golden regenerates honestly if behaviour shifts; library regrows.
- **Dual-reviewed:** the reviewer verifies against the remote that (a) the behavioural path no longer uses
  the symbolic memory, (b) the history-effect is sourced from the substrate (the gradient), (c) plasticity
  is unchanged, (d) suite green, (e) any behavioural shift is understood/recorded.
- **Commit + push + STOP for reviewer clearance before Phase 2** (the richer sub-symbolic episodic/retrieval
  memory).

---

## 6. What comes after (the layer's phasing — for context, NOT this phase)
- **Phase 2 — richer sub-symbolic memory:** the episodic/retrieval dimension the plasticity doesn't yet give
  (engram reactivation / retrievable event-representations, sub-symbolically — so the PFC loop has something
  to retrieve), with the recency/importance/salience *dynamics* realised in the substrate.
- **Phase 3 — the PFC↔memory presentation loop:** the executive contextually surfacing learned
  representations (often inhibitory) to modulate behaviour (grounded in dlPFC↔hippocampus top-down retrieval;
  Anderson retrieval-suppression; the mPFC goal-modulated-retrieval work).
- **Phase 4 — the missing learning pathways:** vicarious/observational (Bandura), modeling/imitation, built
  on the observational seed already in the Arena — so representations form through multiple routes, not just
  consequence-learning.
- **Then:** the higher-order read-outs (beliefs/attitudes/morality/rules) EMERGE from this layer and are read
  out (never coded — they are the *characters'* content, not ours); and **dominance-hierarchy re-enters as
  the first application** (rank = consequence-learned deference held in the unified memory, surfaced/overridden
  by the PFC as "respect").

---

*Phase 1 unifies memory as one sub-symbolic substrate by dissolving the parallel symbolic town-layer
memory-stream into the substrate's existing plasticity-memory — the priming effect sourced from the
developed weights that already produce it, the symbolic scaffold retired from the behavioural path. It is an
integration/un-bolting, not an extension: no new circuits, no weight changes, plasticity untouched. Nothing
is built until the researcher approves. Memory becomes the sub-symbolic substrate — the "we differ from Joon
Park" made concrete — and the foundation for the richer memory, the PFC-retrieval loop, and the learning
pathways that follow.*
