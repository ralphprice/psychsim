# PsychSim — Master Design & Build Document, Part 6 (Supplements & Addenda, continued)

*Sealed, versioned supplement to `PsychSim_MASTER.md` and Parts 1–5. Not updatable once distributed;
further guidance becomes a new Part. Section numbering continues the global sequence (this Part =
S11–S13).*

This Part specifies an **instrument & infrastructure batch** — bucket (b), tooling that does **not**
touch the organism, the honesty wall, or the 8b.4 question. It contains: the **developed-agent bank**
(the primary capability, S11), the **Arena** micro-environment (its first consumer, folded under
Spawn, S12), and the **consolidated development roadmap** placing this batch against all outstanding
work (S13). The Claude Code session can be given this batch **once the core work is settled** (S13);
it will surface questions as it builds — expected.

---

## S11. The developed-agent bank (primary capability)

### S11.1 What it is

A **developed-agent store**: run a simulation, snapshot selected agents at chosen ages, persist their
**complete developed state with provenance**, and re-instantiate them later — into the Arena, into a
fresh simulation as its adult population, or into any experiment. This is the general capability;
the Arena (S12) is merely its first consumer. It exists because the project **needs a way to spawn
grown adults**, and there is only one honest way to get one (S11.5).

### S11.2 What is snapshotted

The agent's full developed state: the **substrate weights** (the sculpted connectome), **all four
matrices** (social, environmental, group, self-reflection), the **interoceptive state vector**,
**age**, and **provenance metadata** — the growth conditions and RNG seed that produced this agent, so
any banked individual can be traced to how it was grown. Snapshot = the complete state needed to
resume the agent exactly; nothing summarised, nothing lossy.

### S11.3 Auto-banking (a growing cache for variety)

Any normal simulation run **automatically banks** adults at selected ages into a growing cache, so the
project accumulates a sizeable, diverse library of grown individuals over time. This cache then feeds
**variety** into future simulations: instead of every spawn being fresh newborns, a run can be
seeded with banked adults who carry real developmental histories — which is closer to a real
population (adults with pasts) than an all-newborn cohort. The cache is a by-product of ordinary runs;
no special growth is needed to populate it.

### S11.4 Re-instantiation — banked adults keep living

A re-instantiated banked adult **continues to develop normally, resuming its natural cycle** — it is
**not frozen**. Its plasticity continues under the age/experience-decreasing schedule (Part 5 S10.1),
so at an adult age it changes slowly (small 1/n steps), exactly as it would have had it never been
banked. Banking is a pause-and-resume of a living developmental trajectory, not a freeze.

### S11.5 The honesty rule (the load-bearing constraint)

A developed adult state is the **product of a specific developmental history**. Therefore:
- **Grown and banked, never fabricated.** A banked adult's developed state is honest *because it was
  earned* by the meaning-blind plasticity from that agent's actual experience. A "system-generated
  adult" must mean **an agent grown through a fast standard/randomised developmental run** — **never**
  weights assigned directly at adulthood. Assigning adult weights hand-authors a developed state, which
  is the multi-seed stipulation problem one level up, and is forbidden.
- **Restored, never edited.** You snapshot and restore a banked agent; you do **not** reach into a
  banked state and adjust its developed weights before dropping it in. The moment a banked state is
  edited, it stops being "an adult the system grew" and becomes "an adult you authored." Snapshot /
  restore only.

### S11.6 Uses

Honest adult spawning (re-hydrate a grown one, don't fabricate one); a **library of known
individuals** grown under known conditions (grow agents under warm vs harsh, bank them, study *those
specific, provenance-known* adults); population variety for general sims; and the enabling substrate
for the Arena (S12) and the scan controller (Part 4 S8), both of which can draw banked agents.

---

## S12. The Arena (first consumer of the bank) — a micro spawn environment

### S12.1 What it is

An option **under Spawn** (folded in, not a new top-level surface): a small, closed, fully-observable
micro-world where a handful of agents live compressed lifetimes interacting, so emergent behaviour can
be watched directly. Its standing value is as a **development-and-regression harness**: run the same
Arena with the same seeds before and after an organism change (a new circuit, a new matrix) and **diff
the behaviour** — a reusable check that an upgrade did what it should.

### S12.2 The spec

Under Spawn, selectable:
- **Micro-environment** (dropdown, four to start): one room · one house · house + garden · an office.
  Each differs in **what is present to interact with** (space, objects, nature, privacy, escape),
  i.e. perturbation-pattern differences.
- **Roster size:** 2–5 agents.
- **Shared-hours-per-day dial:** how many hours the co-located agents actually spend together (e.g.
  2–4 h for children), the rest of each agent's day being its own separate experience stream.
- **Per-slot spawn source / age:** each slot is a fresh newborn, a system-grown agent (S11.5), or a
  **banked adult** (S11) — at a selectable age.

### S12.3 Honesty — environments are perturbation patterns

The Arena's only honesty exposure is through the matrices: the micro-environments must be specified as
**what is present to interact with**, never as valences or outcomes ("house + garden" affords space,
nature, privacy — it is **not** tagged "pleasant"). Agents' behaviour toward each other flows through
the four matrices. **The trap:** "locked in a room together" must not smuggle in a scripted stressor —
if confinement produces stress, it must be **because the substrate's own threat/social circuits
respond** to the perturbation pattern of a small space with a persistent other and no escape.
Emergent, never tagged.

### S12.4 The reduced-day dial keeps development undistorted

Sharing only 2–4 h/day is **not** a distortion — it maps to siblings in a household (shared space, but
each with a separate experience stream), and makes exposure duration a legitimate experimental dial
(*how much* shared time shapes *how much* co-development) rather than a claim of total lifelong
exposure.

### S12.5 The compression rule (sacred)

Compressed lifetimes come from **running wall-clock faster — never from altering the plasticity
constants.** The 1/n developmental schedule (Part 5 S10.1) is untouchable: speed the clock and the
same schedule yields a faithful fast life; crank the learning rates and you get a *different organism*
that develops artificially, turning the Arena into a lie generator. **Compress time, never the
developmental constants.**

### S12.6 The closed-system watch

A closed world of 2–5 interacting agents is a genuinely different regime (Part 5 S9.3, Regime B):
it can produce real emergent social dynamics (co-regulation, escalation between two agents,
folie-à-deux) *and* it can produce the closed-loop analogue of numerical instability. The Arena is a
**good place to probe** whether a small closed world preserves viable agents — but the trace must log
enough to **distinguish an interesting emergent social dynamic from numerical instability of a closed
loop.** Both are informative; conflating them is not.

---

## S13. Consolidated development roadmap (where this batch sits)

### S13.1 The full remaining order

**A — Open loop (active now):** route self-reflection into the developed outcome; re-run the 2×2;
design-session divergence review. *Gate: closes the divergence question for the complete organism; the
verdict is bounded-null until then.* (Part 5 + the review ruling.)

**B — Core completion (gated behind A):**
- **8b.4** — retire the legacy net engine + complete honesty #2 (`access`/category-primitive removal).
  Irreversible; only after A concludes. (MASTER Phase 8.)
- **8b.5** — reconcile `params ← seed`. (Part 2 S1.3.)
- **8b.6** — the full emergent-phenomena battery (ambivalent-bond conflict, negativity bias, rest of
  App. D / Part IV) **plus the two mechanism-gap organism changes**: continuous maturation → executive
  control capacity, and DA/satiety state-dependence as circuit modulation (the latter needs a seed
  edit → a future Part). (Part 3 S5.4.)

**C — Instrument & infrastructure batch (bucket b; the batch specced here + prior Parts; build once B
is settled):**
- **C1. Developed-agent bank** — foundational. (Part 6 S11.)
- **C2. Parallel-instance harness** — N independent substrate instances in one shared world; shared by
  the Arena and the scan controller. (Part 4 S8.5.)
- **C3. Arena** — first consumer of C1+C2; simplest; the regression harness. (Part 6 S12.)
- **C4. Scan controller / permutation search** — automated search over throttle configs; builds on
  C1+C2. (Part 4 S8.)
- **C5. Subcortical Allen-connectome audit** — independent one-off coverage pass. (Part 3 S6.)

**Parked:** the stale `core/neural/` 97-circuit engine artifact — not a track; revisited only as a
deliberate, separately-scoped decision if ever.

### S13.2 Sequencing note

The batch (C) is **bucket-(b) tooling** and does not touch the organism or 8b.4, so it sequences after
core completion (B). One caveat: the bank (C1) snapshots the developed-state representation, so it
should land **after 8b.5** (once the state/params representation is final) to avoid banking states in
a format that then changes. If the team wants the bank/Arena earlier as testing tools, that is
acceptable *after 8b.5* — but not before, and not ahead of the divergence review (A).

### S13.3 The honesty gates that apply across the whole batch

Meaning-blind mechanism throughout · environment = perturbation patterns, never valences/outcomes ·
**grown-and-banked, never fabricated; restored, never edited** · **compress wall-clock, never the
plasticity constants** · the scan's objective is a *measured* signature or held-out field-data
distance, never a drawn target ("broken" outcomes are the expected background) · and **no 8b.4 until
the divergence question (A) concludes.**
