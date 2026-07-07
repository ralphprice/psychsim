# PsychSim — Character Generation Decision

*A reference decision for how sim characters are created. Read alongside
`PsychSim_Design_Document.md` (the neural substrate / mind model) and
`PsychSim_Handover.md` (the whole system).*

## Read first (authoritative references)
- **PsychSim_Design_Document.md** — the neural substrate and the mind model. Absorb the
  governing discipline (§0/§2: no hand-authored psychological effects; emergence only;
  "chaos is correct at this crude stage") and §2 (the internal model: 7 primary systems,
  reactivity vs strength, use-strengthening, developmental windows, the descriptive
  read-out, the always-on executive layer + the memory-driven learning route
  `install_monitors_from_memory`).
- **PsychSim_Handover.md** — the whole-system map: architecture, repo layout, how to run,
  the live engine/server/UI (§3.7), and the roadmap (§6).
- **PsychSim_Park_Review.md** — the Park generative-agents architecture we model the
  spatial day-to-day layer on (and why we replace its LLM cognition with our substrate).

## Principle (from the design doc's discipline — do NOT violate)
Every mind is a product of the neural substrate. Do NOT script personalities via
attributes. The ONLY directly-set ("given") attributes are scenario setup: **temperament
seed** (inherited reactivity biases), **role**, **home/workplace**, **age**. Personality,
behaviour, and the neural-network strength profiles MUST emerge from lived experience
through the substrate — never hand-set. (Given vs emergent: temperament/role/position are
"given", like placing a building; the strength profile of the systems is "grown".)

## We do NOT evolve every character live — two modes, one model

### A) Controlled-experiment mode (build first; keep permanently)
This is the correct design for controlled experiments, NOT merely a stepping stone.
- Grow a **library of adults** by running the substrate to adulthood, over varied
  temperament seeds and varied rearing environments.
- **Cache** each grown adult: serialise the Brain (per-system strength + reactivity) plus
  its temperament seed, role, and home/workplace.
- At experiment time, load cached adults as a **fixed background population** — identical
  across conditions, which IS the experimental control — and let only the **study
  subjects** (the children under study) evolve live around them.
- Rationale: a fixed, evolved environment is the correct experimental control;
  reproducible; cheap to reuse.

### B) Open-ended simulation mode (for the "watch-the-town" live sim; later)
Every character evolves live via the substrate, started at staggered times to produce a
natural spread of ages and roles.

## Rejected
Generating background characters with **scripted attribute-personalities** — inconsistent
with the emergence model; it would split the sim into two kinds of mind.

## Honest caveat
The quality of a grown-adult library depends on substrate maturity. The current crude
substrate pushes most minds toward SEEKING, so a library cached today is weakly
differentiated — fine for background scenery (temperaments still vary via the seed), and
it gets richer as the substrate matures.

## Implementation
- A `Brain` is just `{system: (strength, reactivity)}` — trivially serialisable to JSON.
  Add Brain save/load (e.g. `to_dict()`/`from_dict()`) in `core/affective_engine/drives.py`.
- Add a **character library**: grow-to-adulthood via the developmental life-stepper
  (`extensions/sophropathy/timeline_driver.py`) on the substrate, then cache
  brain + seed + role + home. Ship a small curated adult set to start.
- Loading path: `SimEngine` (`extensions/sophropathy/engine.py`) and the life-stepper
  should accept a pre-grown background population and only evolve the designated study
  subjects.
- Temperament seed is already supported: `brain_from_seed` / `AffectiveAgent.temperament_seed`.
