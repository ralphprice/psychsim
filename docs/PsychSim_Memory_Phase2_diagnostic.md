# Memory Layer Phase 2 — diagnostic & trace (for design-session review; NOTHING built)

**Phase 2 goal (from the layer's phasing):** the richer sub-symbolic **episodic / retrieval** memory the
plasticity doesn't yet give — retrievable event-representations that *reactivate* (engram reactivation),
so the Phase-3 PFC↔memory loop has something to retrieve — with recency/importance/salience dynamics
realised in the substrate. This is the implementation session's diagnostic + trace, brought for review
**before any build**, same discipline as every prior phase.

## 1. What memory the substrate has NOW (verified against the code)
- **Plasticity = SEMANTIC / PROCEDURAL memory.** The developed weights are an always-on, *generalised*
  disposition: how the world works for this agent (threat-tuned, bonding-tuned), emotionally weighted via
  neuromodulator-gated consolidation (Phase 1). It shapes the ongoing response to any cue — but it is not
  event-addressable: there is no way to reactivate a *specific past episode*.
- **The hippocampus is a single lumped node, `HPCv`.** Afferents: `AdrenalCortex` (+, cortisol/stress),
  `DRN` (−, 5-HT). Efferents: `LA`, `BA`, `vmPFC`, `NAc-shell`, `dlPFC`. So `HPCv` currently acts as a
  **stress-sensitive context node** modulating threat/reward/PFC — NOT as an episodic store.
- **No episodic microcircuitry exists.** No DG, CA3, CA1, EC/subiculum; and no auto-associative recurrent
  structure anywhere (the only "recurrent" pairs are E/I interneuron loops and DMN/mentalizing cortical
  bidirectionals — none are an auto-associative attractor). So there is **no engram store and no
  pattern-completion** — nothing to reactivate, nothing for the PFC loop to retrieve.

**Conclusion:** the substrate's memory is genuinely semantic/procedural. Episodic/retrieval memory is
**absent**, and honestly so — see the crux.

## 2. The neuroscience of what's missing (cited)
Episodic memory is the hippocampal **DG → CA3 → CA1** system:
- **DG — pattern separation:** competitive learning converts overlapping cortical inputs into *sparse,
  decorrelated* event codes, keeping each memory distinct ([Rolls 2013, CA3 theory](https://pmc.ncbi.nlm.nih.gov/articles/PMC3691555/)).
- **CA3 — the auto-associative attractor:** recurrent collaterals store an event's pattern in *one trial*
  (Hebbian); a *partial cue* propagates through the strengthened recurrent connections and **reinstates the
  full stored pattern — pattern completion** ([Rolls 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3691555/);
  [pattern completion/separation review](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3812781/)).
- **CA1 — retrieval readout** back to cortex/EC.
- **Engram cells:** the sparse ensembles active at encoding *reactivate on recall* — reactivation IS the
  remembered experience ([engram/neurocomputational review](https://arxiv.org/html/2506.01659v1)).

The single load-bearing mechanism Phase 2 needs is the **CA3 auto-associative attractor**: one-trial
storage of an event-pattern + pattern completion from a partial cue. That is "a retrievable event-
representation that reactivates."

## 3. THE CRUX — a representational-level question (the real Phase-2 decision)
Episodic memory is fundamentally a **population / ensemble** phenomenon: a *sparse subset of neurons within
a region* (the engram) fires together and is later reactivated by pattern completion *across a recurrent
population*. But the PsychSim substrate is a **nucleus-level RATE model** — one scalar activation per region.
A single-rate `CA3` node cannot hold multiple distinct engrams (it is one number); pattern separation and
pattern completion have no substrate in a one-value-per-nucleus model.

So Phase 2 is **not** "add a few CA3/DG/CA1 nodes." Adding sub-symbolic episodic memory requires giving the
hippocampal system a **within-region ensemble / population representation** — a new representational layer,
a genuine extension of the substrate's abstraction level (which until now is one rate per nucleus). **This
is the fundamental Phase-2 design decision, and it's the design session's to shape.** It also explains
*why* Phase 1's memory was semantic/procedural: that is honestly all a nucleus-level rate model gives; the
episodic dimension needs the ensemble layer.

## 4. The design space (options for review — I have a lean, not a ruling)
- **(A) A faithful hippocampal ensemble layer.** Give the hippocampal system a within-region *population*
  (a vector of engram units) with DG-style sparse pattern separation + a CA3-style recurrent auto-
  associative attractor (one-trial Hebbian storage, pattern completion) + a CA1 readout back to cortex.
  Most grounded; the largest architectural step (introduces population-level representation into the model).
- **(B) An abstracted auto-associative store on the hippocampal node.** Attach a Hopfield-like attractor
  memory over the *existing* cortical/limbic activation vector (the event = the current activation pattern
  across the relevant circuits; store it; a partial cue reactivates it). Gets engram-reactivation /
  pattern-completion *behaviour* without building explicit DG/CA3/CA1 populations — a smaller step that
  stays closer to the current abstraction while adding the one missing mechanism (attractor recall).
- **(C) Something else the design session envisions** — e.g. a hybrid, or a scoping that defers the full
  ensemble layer.

**Recency / importance / salience dynamics** (the retrieval-scoring the retired symbolic stream did) map
cleanly onto the substrate in any option: **recency** = the eligibility/activation trace and weight decay;
**salience/importance** = the neuromodulator-gated consolidation confirmed in Phase 1 (high-arousal engrams
stored/reactivated more strongly). So those dynamics come "for free" from mechanisms we already have — they
don't need a symbolic scorer.

**My lean:** frame Phase 2 around the **minimal grounded attractor capacity** — option (B) as the first,
smaller step (one new mechanism: an auto-associative store + pattern completion on the hippocampal system,
salience-weighted, recency-decayed), proving engram reactivation works and gives the Phase-3 PFC loop
something to retrieve — with the full faithful ensemble layer (A) as a later refinement if the study needs
within-region engram structure. That keeps the "integrate, don't over-build" discipline: add the one
missing mechanism (attractor recall), not a whole new subsystem, until the minimal version is proven.

## 5. Questions for the design session (before any build)
1. **The representational-level decision** — do you want the faithful hippocampal ensemble layer (A), the
   abstracted auto-associative store (B, my lean as the first step), or another scoping? This is the crux;
   everything else follows from it.
2. **Scope of "event-representation"** — what constitutes a stored episode's pattern (the activation across
   which circuits — the whole cortical/limbic vector, or a defined subset)?
3. **The honesty posture** — engram reactivation must stay emergent/sub-symbolic (a stored *activation
   pattern* reactivated by an attractor), never a symbolic event-record with coded retrieval. Confirm the
   read-outs (what was retrieved) are descriptive, never fed back as coded behaviour.

**Nothing built.** This is the diagnostic + trace + design-space for the representational-level decision
that Phase 2 turns on. Once the design session rules the approach, I'll bring the grounded build proposal
(cited, minimal, keystone-clean) for review before any edge or code lands — same rhythm as Phases 1–2 of
the kinship arc and Memory Phase 1.
