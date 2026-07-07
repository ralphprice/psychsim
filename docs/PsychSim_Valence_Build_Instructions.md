# PsychSim — Claude Code build instructions (valence/motivation subsystem)

*Executable plan for building the design in `PsychSim_Valence_and_Motivation_Design.md` via the
`PsychSim_Valence_CodeChange_Map.md`. Written for Claude Code working in the repo. Work **one phase
at a time**, test after each, commit at each acceptance gate, and never break the invariants in §0.*

---

## 0. Orientation and invariants (read before touching anything)

**First actions:** place `PsychSim_Valence_and_Motivation_Design.md` and
`PsychSim_Valence_CodeChange_Map.md` in `docs/`; read both; read `README.md`,
`core/affective_engine/`, `core/sim_world/`, `core/modular/registry.py`, and
`extensions/sophropathy/`. Run the existing suite (`python run_tests.py`) and confirm it is green
before changing anything.

**Invariants — do not violate these in any phase:**
1. **Valence is computed, never stipulated.** No literal "warm = +0.6 / harsh = −0.7" anywhere. Value
   = drive reduction over the state vector.
2. **No coded arbiter.** Nothing may read a situation and directly output a behaviour, an emotion, or
   a category. Behaviour emerges from competition; categories are measured, not set.
3. **Named categories are observer read-outs, not primitives.** "fear", "callousness", "boldness",
   "psychopathy" are computed *over* the agent for reporting and *never fed back*. No seed carries an
   outcome category.
4. **The module contract is sacred.** Do **not** edit `core/modular/registry.py` or `project.py`.
   Studies stay discovered plugins under `extensions/`.
5. **All new numbers are scaffold.** Put every set-point, gain, rate, threshold, and capacity in a
   single discoverable place (a `params` module / clearly-named constants) so calibration can find
   them later. Add a comment `# SCAFFOLD` on each.
6. **Supersede legacy behind stable interfaces, with parity tests.** Keep `TraitSeed`, `develop`,
   `probe`, `classify`, the three matrices, and the plugin contract working at all times. Do **not**
   delete a legacy path until the new path reproduces it. Small, reversible commits.
7. **Keep the suite green.** Every phase adds tests and leaves `run_tests.py` passing.

If a design ambiguity blocks a phase, stop and surface it rather than guessing.

---

## Phase 0 — Safety net (characterisation baseline)
- Add **characterisation tests** (`tests/test_characterisation_*.py`) that snapshot current outputs of
  `develop`, `probe`, `classify`, and the three matrices for a fixed set of seeds
  (`typical_child_seed`, `shared_root_seed`, `sophropathic_seed`, `psychopathic_seed`) × environments
  (`warm_firm_home`, `harsh_inconsistent_home`) with fixed RNG seeds. These capture *current*
  behaviour so the migration can be parity-checked.
- **Acceptance:** suite green; characterisation snapshots committed. *Commit.*

## Phase 1 — Valence core (`interocept.py`) + rewire valence  *(honesty-critical #1)*
- Create `core/affective_engine/interocept.py`: `StateVector` (App. A variables + set-points, each
  tagged `fixed`/`allostatic`), `drive(state) -> (per_variable_vec, scalar_D)`, the **innate-
  perturbation table** (App. B: sensor→variable→direction→scaffold gain), `valence(D_prev, D_now) =
  BETA*(D_prev - D_now)`.
- Rewire `development.py`: replace the stipulated response-valence with (a) apply an event's
  perturbations to the state vector, (b) return the **computed** valence. Convert the scenario
  appraisals from *stipulated valences* to *perturbation specs*. `warm_firm_home` /
  `harsh_inconsistent_home` express perturbation patterns.
- `memory.py`: write `EpisodicMemory.valence` from the computed value; add optional per-variable
  `drive_reduction`.
- **Tests:** unit tests for drive/valence/perturbations; a parity test that the *sign and ordering* of
  valence for the canonical warm/harsh scenarios match the old qualitative behaviour (exact numbers
  will differ — that is expected and correct). Update characterisation snapshots with a note.
- **Acceptance:** `interocept` unit tests pass; `develop`/`probe` run; valence is computed. *Commit.*

## Phase 2 — Learning (`learning.py`) + plasticity in `drives.py`
- Create `core/affective_engine/learning.py`: value function `V` (anticipatory value); TD/RPE
  `delta = r + GAMMA*V_next - V`; three-factor plasticity apply (pre × post × dopamine=delta);
  `update(cue, r, drive_profile, ...)`.
- `drives.py`: route `imprint`/`window_plasticity` through the three-factor rule (keep the window/
  critical-period gating; add the `delta` factor). Make oxytocin/opioid **gates** that license
  social-cue plasticity; dopamine carries `delta`.
- **Tests:** RPE converges on a toy task; a cue paired with drive-reduction acquires positive
  anticipatory value; the prepared-fear multiplier (§B.3) makes a flagged cue acquire aversive value
  faster than an arbitrary cue.
- **Acceptance:** learning tests pass. *Commit.*

## Phase 3 — Matrices adopt the engine
- `sim_world/relations.py`: per-entity `value` + `drive_reduction_profile` updated via
  `learning.update`; **Dunbar layered capacity** (inner ~5, then ~15/~50/~150; SCAFFOLD sizes) with
  **decay without contact**; **allocate slots by |salience|**; each slot stores `value`, `salience`,
  `valence_sign`; support the **ambivalent** case (co-active attachment + threat toward one entity).
- `sim_world/environment_matrix.py`: value through the one engine; nature = arousal/stress drive-
  reduction (+ biophilia prior); animals via the social/oxytocin channels (a pet may take a
  `relations.py` slot); belongings = instrumental + extended-self.
- `sim_world/group_matrix.py`: keep dominance/prestige; add synchrony/endorphin belonging and the
  sociometer.
- **Tests:** slot capacity + eviction by salience; an **enemy** (negative value, high salience) holds
  an inner slot; an **ambivalent** entity is flagged; environment/group entries update by RPE.
- **Acceptance:** matrix tests pass. *Commit.*

## Phase 4 — Behaviour selection (`selection.py`) + `executive.py` refactor + seed nuclei
- Create `core/affective_engine/selection.py`: candidates = affordances with input =
  anticipatory-value ⋅ current-drive; **accumulation-to-threshold with disinhibition** (Go release +
  NoGo + STN global hold); dopamine sets the gain (Go/NoGo balance, threshold, vigour, softmax
  temperature). All thresholds/rates SCAFFOLD.
- `executive.py`: refactor into a **parameter-setter on selection** — proactive threshold/NoGo bias,
  reactive **STN "hold"**, dACC conflict monitoring. Keep the existing monitor-learning (reversal
  learning) but route it as *which candidates to bias*, through `selection.py`. It must not pick
  actions directly.
- Seed JSON / `neuraldesigner`: ensure the **motor-selection loop nuclei** (dorsal striatum, GPe,
  GPi/SNr, motor thalamus) exist; add if absent (NAc/VTA/preSMA→STN already present).
- Wire the **BIS hook**: an unresolved approach/avoid near-tie holds the arousal variable elevated
  (feed back into `interocept.py`).
- **Tests:** a dominant-value candidate wins; a near-tie produces slow/oscillating selection **and**
  arousal stays elevated (the ambivalent-bond signature); a weakened/immature brake lets a prepotent
  high-value candidate win (impulsivity); running the maturation schedule reproduces an adolescent
  risk-taking bump that resolves with executive maturation.
- **Acceptance:** selection tests pass; the live loop closes. *Commit.*

## Phase 5 — Endowment re-parameterisation + epigenetics (`epigenetics.py`)
- `core.py::TraitSeed`: carry the **new endowment parameters** (state-vector set-points, drive weights
  `w_k`, neuromodulator reactivities, innate-perturbation gains, physical-trait baselines). Provide a
  mapping from the legacy `gains` to reactivities so existing seeds still construct.
- Create `core/affective_engine/epigenetics.py`: an early-window modifier that reads accumulated early
  experience during `develop(...)` and **shifts allostatic set-points/reactivities** semi-
  permanently (the Study-3 / OXTR-type hook).
- **Tests:** differential susceptibility — the fearless seed diverges by environment while the typical
  seed internalises under adversity; early adversity shifts the arousal set-point and persists.
- **Acceptance:** endowment tests pass. *Commit.*

## Phase 6 — The honesty migration: `access` → observer read-out  *(honesty-critical #2)*
- **Grep every consumer** of `TraitSeed.access` (`core.py`, `drives.py`, `agent.py`, the plugin).
- Remove the outcome-category weights (`callous_exploitation`, `strategic_prosociality`,
  `cool_instrumental_boldness`, …) from all seeds. Re-point consumers.
- Implement those categories as **observer read-outs** in `extensions/sophropathy/world.py`
  (`study_category`) and `report.py`, computed from *emergent* behaviour and substrate activity.
- **Tests:** no seed carries an outcome category; the plugin's reports still produce the categories
  (now computed, not seeded); behaviour is unchanged by the removal (they were supposed to be
  outputs).
- **Acceptance:** honesty-critical #2 done; plugin reports parity. *Commit.*

## Phase 7 — Differential-profile plugin re-expression
- `extensions/sophropathy/society.py`: re-express `typical_child_seed` and `fearless_child_seed`
  (=`shared_root_seed`) in the **new temperament parameters** (App. E.2); `sophropathic_seed` /
  `psychopathic_seed` stay as adult attractors.
- `world.py` / `report.py`: the observer metrics (triarchic / CU / punishment-learning / reactive-vs-
  instrumental aggression), operationalised from the thesis's instruments.
- **Tests:** the sophropath/psychopath split **emerges** from temperament × environment (assert it is
  *not* coded — e.g. the same fearless seed reaches different outcomes under warm-firm vs harsh-
  inconsistent homes); a validation-target run shows the divergence.
- **Acceptance:** plugin runs; divergence emergent. *Commit.*

## Phase 8 — Distillation + legacy retirement
- `sim_world/relations.py`: add the **pooled prior** (default disposition); initialise each entity
  from it; blend by evidence count (partial pooling); let entity estimates slowly update the prior.
- **Tests:** transference (a new entity resembling a known one inherits value); early-caregiver primacy
  (early interactions dominate the default); an ambivalent early environment yields an ambivalent
  default.
- Retire the legacy **two-affect-pathway** internals now that the substrate + valence engine reproduce
  them — behind the stable interfaces; remove or clearly deprecate dead paths.
- **Acceptance:** distillation tests pass; legacy removed/deprecated; **full suite green**. *Commit.*

---

## Cross-cutting requirements
- **Testing:** unit + parity/characterisation per phase; keep `run_tests.py` green throughout.
- **Scaffold registry:** collect all SCAFFOLD numbers in one params module; this is the surface the
  calibration plan will target.
- **Validation hooks:** expose the observer read-outs and the named validation-target scenarios
  (ambivalent-bond conflict, adolescent risk-taking, negativity bias, differential susceptibility,
  "punishment for one = reward for another") as runnable probes for the validation phase.
- **Documentation:** update `docs/` and the affected `README.md` files as each subsystem changes.

## The "never do" list (quick reference)
Edit `registry.py`/`project.py` · add a coded arbiter · seed an outcome category · stipulate a
valence · delete a legacy path before parity holds · leave a scaffold number un-marked · land a phase
with the suite red.
