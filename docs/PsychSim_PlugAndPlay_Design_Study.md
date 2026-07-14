# PsychSim — Design Study: A Plug-and-Play Neural Substrate

**Design study. Status: STUDY ONLY — nothing built, nothing decided to build. For researcher review.**

**The question.** PsychSim is a code representation of a functioning brain. It will never be complete, so
what makes it a *better generic instrument* is not getting today's abstraction level perfect — it is being
**extensible**: a substrate where a new or better neural system (a better episodic, long-term, or
short-term memory; a new subsystem) can be **plugged in and integrated through explicit marked
connections** — wiring into the substrate the way a neural system wires into the brain (the stem-cell
analogy: a new pattern adapts and integrates into the existing network), rather than being bolted on
alongside as a parallel module.

**Governing value (not a subsystem — a rule):** *never introduce inaccuracy in the name of simplification.*
A small modelling error, run across a simulated lifetime, compounds destructively into nonsense. Accuracy is
load-bearing across developmental time. The model is an **accurate representation that lets us test
theories — it must not itself be a theory.** Mechanism is built from researched fact; what the mechanism
*does* emerges and is measured, never assumed.

**Governing discipline:** integrate through marked connections (integral), never bolt on (parallel). The
symbolic MemoryStream we just retired was a bolt-on *precisely because* it ran alongside the substrate
instead of wiring in through marked connections.

Episodic memory is the **immediate test case** — not because a current study needs it (we do not know what
future studies will ask; we must not build our guesses about their results into the substrate), but because
it is the clearest case of a system that represents *differently internally* (an ensemble/population
phenomenon, per the researched facts) and so it stress-tests whether the architecture is *truly*
plug-and-play or only pluggable-for-things-that-look-like-what-we-already-have.

---

## 1. Diagnostic — how plug-and-play is the substrate NOW? (verified against the codebase)

**Finding 1 — the engine is generic, not hardcoded.** Every operation iterates over `m.circuits.items()`
and `m.connections` (engine.py:29-32,65,71,136,164,170,198). The only hardcoded string in engine logic is
`"none"` (the null-neuromodulator sentinel) — *not a circuit identity*. **The engine runs whatever the seed
declares; it knows nothing about which circuits exist.** This is the plug-and-play core, already present: a
new neural system is added by *declaring its circuits and connections in the seed* — no engine change.

**Finding 2 — the seed already has explicit, marked, self-described interfaces.** The records ARE the marked
connections:
- **Circuit record:** id, name, nodes, function, domain, transmitters, activation_bounds,
  baseline_activation, homeostatic_setpoint, time_constant, developmental_online_age,
  plasticity_coeff_schedule_ref, calibration flag, sources, confidence, evidence_base.
- **Connection record:** source_circuit, target_circuit, default_weight + basis, weight_bounds,
  gating_neuromodulator, is_innate_reinforcer_link, eligibility_trace_tau, plasticity_schedule,
  developmental_online_age, source (provenance), confidence. **This is the marked connection: what wires to
  what, with what sign/strength/plasticity/onset, and why (provenance).**
- **Input channels:** how sensation enters (central_entry, feeds, modality, receptors).
- **`schemas` block:** the seed *formally self-describes* its record formats (circuit, connection,
  innate_wiring_entry, input_channel, physical_endowment, plasticity_rule). **The interface is declared, not
  merely implicit** — a new system's records must conform to the schema, which IS the plug interface.
- **`gaps_register`:** already tracks *what is not yet modelled* — the pluggable-slot concept in embryo.

**Diagnostic conclusion:** At the level of *adding circuits and connections that fit the current
representational vocabulary* (nucleus-level rate units wired by marked connections), the substrate is
**already substantially plug-and-play**: declare the circuits + connections + provenance conforming to the
schema, and the generic engine runs them, integrated through marked connections. This is the stem-cell
analogy already realised for same-vocabulary systems.

**The real open question (what episodic memory stress-tests):** can a system that represents *differently
internally* — episodic memory is factually an ensemble/population phenomenon (sparse engrams, CA3 recurrent
attractor, pattern separation/completion) — plug in through these marked connections, when the current
vocabulary is one-scalar-per-region rate units? A truly plug-and-play brain-model should allow a subsystem's
*internal representation* to be whatever the facts require, integrated through a well-defined *interface* —
**exactly as the brain does**: regions with very different internal representations (cortical columns,
hippocampal ensembles, brainstem nuclei) wired through defined projections.

---

## 2. The design principle the diagnostic points to

The brain is *already* the existence proof of what we want: heterogeneous internal representations,
integrated through defined connections. Hippocampal CA3 (ensemble/attractor) and a brainstem nucleus (near
rate-like) coexist and communicate through projections that don't require them to share an internal code.

**So the plug-and-play architecture is: each neural system represents faithfully *internally* (at whatever
granularity the researched facts require), and integrates through its *marked connection interface*.** The
substrate does NOT have to be uniformly ensemble or uniformly nucleus-level. This **dissolves the
abstraction-level tension** that stalled the memory work:
- Not "make everything ensemble" (an enormous rebuild), nor "keep everything nucleus and approximate
  episodic memory" (an inaccuracy-for-simplification — forbidden by the governing value).
- Instead: **an episodic-memory system represents internally as an ensemble (faithful to fact) and plugs
  into the rate-level substrate through marked connections** — which is both accurate AND how the brain
  actually is.

This is faithful (the real ensemble mechanism, not an abstraction that mimics recall), integral (wired
through marked connections, not bolted alongside), and does not force a whole-substrate rebuild.

**The make-or-break design question this raises (the crux):** what is the **interface** between an
internally-ensemble subsystem and a rate-level circuit? A rate circuit outputs/receives one scalar; an
ensemble subsystem has a population state. The interface must define — faithfully, per the neuroscience —
how a population projects to a rate target (e.g., the population's aggregate drives the target, as real
projections summate) and how a rate source projects into a population (e.g., as afferent drive distributed
across the population, as EC input drives DG/CA3). **If that interface can be specified faithfully and
generically, the substrate is truly plug-and-play across representational levels.** This is what the build
phase (if approved) would have to get right, and it is the crux the study surfaces.

---

## 3. What the study finds the architecture needs to be *fully* plug-and-play

Not a rebuild — targeted extensions to the *interface vocabulary*, so systems of different internal
representation can plug in:

1. **A subsystem-type declaration.** Today a "circuit" is implicitly a rate unit. To let an ensemble
   subsystem plug in, the schema needs to allow a system to declare its *internal representation type*
   (rate unit; population/ensemble; and whatever future types the facts require — the point is
   extensibility, not enumerating today's list). The engine, already generic over declared circuits, would
   dispatch on the declared type. Rate units remain exactly as they are (no change to existing circuits);
   an ensemble subsystem is a new declarable type.

2. **A cross-representation connection interface.** The marked-connection record needs to express a
   connection between representations of *different* type — faithfully: population→rate (aggregate/summation,
   per real projection biology), rate→population (distributed afferent drive), population→population (the
   projection patterns the facts specify, e.g. EC→DG sparse, DG→CA3 mossy-fiber). The *marking* (source,
   target, sign, plasticity, provenance) is unchanged in spirit — it just spans representational levels.

3. **Provenance/accuracy preserved across the interface.** Every cross-representation connection carries its
   citation/basis exactly as every current connection does — the interface is not an excuse to gloss. The
   governing value holds at the interface: the population→rate summation, the rate→population distribution,
   must be *how the facts say the projection works*, not a convenient approximation.

4. **The generic engine dispatches on representation type.** Because the engine already iterates over
   whatever is declared, the extension is: for each system, run its declared dynamics (rate relaxation as
   now; ensemble/attractor dynamics for a population system); for each connection, apply the
   type-appropriate transfer. Existing rate circuits are untouched — they are one declared type among the
   (initially two) types.

**This is an extension of the interface vocabulary, not a rebuild of the substrate.** The 83 rate circuits
stay exactly as they are. What changes is that the *schema and engine gain the ability to host a subsystem
of a different internal representation, wired in through marked cross-representation connections* — making
the substrate genuinely plug-and-play across representational levels, which is what a faithful, extensible
brain-model needs and what episodic memory (the first such system) requires to plug in accurately.

---

## 4. What this makes possible (the payoff — and why it serves a *generic* tool)

- **Episodic memory plugs in as a faithful ensemble subsystem** (DG/CA3/CA1 as a population system with the
  real separation/attractor/completion mechanism), wired to the rate-level substrate (EC-analogue afferents,
  amygdala emotional-modulation of consolidation, cortical readout targets) through marked
  cross-representation connections. Faithful, integral, no rebuild.
- **Any future better memory model** (short-term, long-term, working) plugs in the same way — its internal
  representation whatever the facts require, integrated through marked connections.
- **The model stays a representation, not a theory.** Because episodic and semantic/procedural memory would
  both be present as *real mechanisms*, the *relative contribution of each to any behaviour becomes emergent
  and measurable* — the tool can *investigate* memory's role (including testing the academic assumptions we
  must NOT build in) rather than presupposing it. This is the generic-instrument payoff: it can answer
  questions we have not yet posed, because it represents the machinery faithfully rather than encoding our
  current guesses about what the machinery does.
- **Extensibility is the deliverable**, not episodic memory specifically. Episodic memory is the first
  system to exercise the cross-representation plug interface; once that interface exists, the substrate is
  extensible across representational levels for whatever comes next.

---

## 5. The disciplined path (guarding against the HSO-ballooning failure)

This is a real architectural extension, so it follows the discipline that the whole project has learned:

1. **This study first** — reviewed, before any build. (Here.)
2. **If the direction is approved:** a focused *interface specification* — precisely how a cross-
   representation connection works (population↔rate transfer), faithful to the projection biology, generic
   enough to host future types. Reviewed before any code.
3. **Then the first pluggable system** — episodic memory as an ensemble subsystem — built against that
   interface, its internal mechanism faithful to the researched facts (the master reference), integrated
   through marked connections, dual-reviewed, full suite, verified on the remote.
4. **Never introduce inaccuracy to simplify** — at every step. The interface transfers must be how the facts
   say projections work. If a faithful transfer is unknown, that is a *gap to register*, not a place to
   approximate.
5. **Integrate, don't bolt on** — the ensemble subsystem wires in through marked connections (integral). If
   it ends up running *alongside* the substrate rather than *wired into* it, that is the bolt-on failure and
   the design is wrong.

---

## 6. What the study is NOT proposing
- **NOT** a rebuild of the 83 rate circuits — they stay exactly as they are (one declared representation type).
- **NOT** making everything ensemble — systems represent at the granularity the facts require; rate where
  rate is faithful, ensemble where ensemble is faithful.
- **NOT** the bolted-on attractor (the option that mimics recall's behaviour over the rate vector) — that is
  an abstraction that seems to do what we observe, which the governing value forbids; the pluggable episodic
  system is the *real* ensemble mechanism, internally.
- **NOT** building episodic memory now — this study is about the *plug-and-play architecture*; episodic
  memory is the test case that shows what the architecture must support, and the first candidate to plug in
  *if and when* the interface is built.
- **NOT** scoping to any current study — the substrate is built faithful to the brain's machinery so it can
  answer questions not yet posed.

---

*The design study's conclusion: PsychSim is already substantially plug-and-play for same-vocabulary systems
(generic engine + marked, schema-described connections + a gaps register). To be a fully extensible,
faithful brain-model, it needs a modest, targeted extension — a cross-representation interface so a subsystem
of a different internal representation (episodic memory as an ensemble, per the facts) can plug in through
marked connections, exactly as heterogeneous brain regions integrate through defined projections. This is an
interface-vocabulary extension, not a substrate rebuild; it keeps the model a faithful representation (not a
theory), makes memory's role in behaviour emergent-and-measurable, and is the honest resolution of the
abstraction-level question. Nothing is built. The recommended next step, if the direction is approved, is a
focused, faithful, reviewed interface specification before any code — with episodic memory as the first
system to plug in.*
