# PsychSim — Valence/Motivation code-change map

*Companion to `PsychSim_Valence_and_Motivation_Design.md`. Translates that design (Appendices A–F
plus the endowment/epigenetics sections) into concrete changes against the **real** codebase. It is
the precursor to the Claude Code build instructions (plan step 6). Nothing here changes the module
contract in `core/modular/registry.py` or edits `project.py`.*

Verified layout this maps onto:
- `core/affective_engine/` — `core.py` (Appraisal, Network, **TraitSeed**, seeds `shared_root_seed` /
  `sophropathic_seed` / `psychopathic_seed` / …, `CIRCUITS`), `drives.py` (`System`, `Brain`, `Drive`,
  `imprint`, `window_plasticity`, `brain_from_seed`, `appraisal_to_stimulus`), `development.py`
  (`Environment`, `develop`, `probe`, `classify`, `Outcome`, the response-valence logic),
  `memory.py` (`EpisodicMemory` with a `valence` field), `executive.py`, `agent.py`.
- `core/sim_world/` — the three matrices already exist: **`relations.py`** (relationship),
  **`environment_matrix.py`** (environment), **`group_matrix.py`** (group), plus `person.py`,
  `population.py`, `gamemaster.py`, `world.py`.
- `core/neuraldesigner/` + the seed JSONs — the substrate.
- `extensions/sophropathy/` — the study plugin (`society.py` seeds, `world.py::study_category`,
  `report.py`, `module.py`).

---

## 1. Summary — files touched

| Design element (doc ref) | Primary file(s) | Kind |
|---|---|---|
| Interoceptive state vector + drive + **computed valence** (App. A/B) | **new** `affective_engine/interocept.py`; edit `development.py`, `memory.py` | ADD + REPLACE |
| Innate-perturbation table (App. B) | `affective_engine/interocept.py` (data); consumers in `development.py` | ADD |
| RPE learning + anticipatory value (App. C) | **new** `affective_engine/learning.py`; edit `drives.py` (plasticity) | ADD + MODIFY |
| Neuromodulators as gates (App. C) | `drives.py` / `learning.py` | MODIFY |
| Relationship matrix: Dunbar slots + salience/enemy/ambivalent (App. 4) | `sim_world/relations.py` | MODIFY (major) |
| Environment matrix onto one engine (nature/animals/belongings) (App. 3.2) | `sim_world/environment_matrix.py` | MODIFY |
| Group matrix: synchrony/endorphin + sociometer (App. 3.3) | `sim_world/group_matrix.py` | MODIFY |
| Distillation / default disposition (App. D.1) | `sim_world/relations.py` (pooled prior) + substrate weights | ADD |
| Observer read-out + **access→read-out honesty fix** (App. D.2 / E.4) | `core.py` (TraitSeed), plugin `world.py`/`report.py`; grep `access` consumers | MIGRATE (honesty-critical) |
| Behaviour selection + competition (App. F) | **new** `affective_engine/selection.py`; refactor `executive.py`; seed JSON nuclei | ADD + MODIFY |
| Endowment re-parameterisation + epigenetics (doc §5) | `core.py` (TraitSeed + seeds); **new** `affective_engine/epigenetics.py` | MODIFY + ADD |
| Differential-profile plugin re-expression (App. E) | `extensions/sophropathy/society.py`, `world.py`, `report.py` | MODIFY |
| Retire two-affect-pathway / legacy primitives | `drives.py`, `core.py`, `agent.py` behind stable interfaces | SUPERSEDE (staged) |

---

## 2. Per-area change specs

### 2.1 The valence core — `affective_engine/interocept.py` (NEW) + `development.py`, `memory.py`
- **Add `interocept.py`** defining: `StateVector` (the App. A variables + set-points, with a
  `fixed`/`allostatic` flag per variable), `drive(state) -> (per_variable_vector, scalar_D)`, the
  **innate-perturbation table** (App. B: sensor→variable→direction→gain), and
  `valence(D_prev, D_now) -> r = β·(D_prev − D_now)`.
- **`development.py`:** replace the current **stipulated** valence (the `response_valence` logic and
  the hard-set warm/harsh `social_valence` in the appraisal scenarios) with a call that (a) applies an
  event's perturbations to the state vector and (b) returns the *computed* `valence`. The
  scenario/appraisal definitions change from *"this outcome has valence −0.7"* to *"this event moves
  {threat-arousal ↑, social-contact ↓}"*; the number is then computed. `warm_firm_home` /
  `harsh_inconsistent_home` stay as `Environment`s but specify perturbation patterns, not valences.
- **`memory.py`:** `EpisodicMemory.valence` stays but is now written from the computed value; add an
  optional per-variable `drive_reduction` field so memory records *which* drives moved (feeds C.5).
- **Honesty note:** this is the #1 fix — it is what makes "a punishment for one is a reward for
  another" emergent rather than decreed.

### 2.2 Learning — `affective_engine/learning.py` (NEW) + `drives.py`
- **Add `learning.py`:** the value function `V` (anticipatory value), the TD/RPE update
  `δ = r + γV' − V`, and the **three-factor plasticity** application (pre × post × dopamine=δ). Provide
  `update(cue, r, ...)` used by the matrices.
- **`drives.py`:** the existing plasticity (`imprint`, `window_plasticity`) becomes the substrate
  application of the three-factor rule; keep the window/critical-period gating, add the δ factor.
  Make the neuromodulators **gates**: oxytocin/opioid license social-cue plasticity (App. C.4),
  dopamine carries δ — not stored "values".
- Anticipatory value from here is the input to selection (2.6).

### 2.3 The three matrices — `relations.py`, `environment_matrix.py`, `group_matrix.py`
Common change: each per-entity record gains a **learned `value` + `drive_reduction_profile`**, updated
by `learning.update(...)` after each interaction (the App. C.9 pattern). Then:
- **`relations.py` (major):** add the **Dunbar layered capacity** — inner slots (~5), then ~15/~50/~150
  bands — with **decay without contact**; **allocate slots by |salience|**, not positive valence; each
  slot stores `value`, `salience`, and a `valence_sign`, enabling the **enemy** and **ambivalent**
  cases (co-active attachment + threat toward one entity → App. 4.3). Expose the ambivalence to the
  selection/BIS path (2.6, 2.7).
- **`environment_matrix.py`:** route value through the one engine; ground **nature** as arousal/stress
  drive-reduction (+ biophilia prior), **animals** through the social/oxytocin channels (a pet may
  take a `relations.py` slot), **belongings** as instrumental + extended-self.
- **`group_matrix.py`:** keep dominance/prestige status (already present); **add** the
  **synchrony/endorphin belonging** factor (coordinated activity → belonging ↑) and the **sociometer**
  (esteem tracks inclusion). Same value engine.

### 2.4 Distillation / default disposition — `relations.py` (+ substrate)
- The default is **partly automatic** (the substrate weights are the running sediment — no code
  needed). **Add** a **pooled prior**: a slow global estimate of social-outcome expectation; each new
  entity record is **initialised from it** and blended with entity-specific evidence by a
  precision/count weight (App. D.1); entity estimates slowly update the prior. This gives
  transference, early-caregiver primacy, and ambivalent defaults for free.

### 2.5 Observer read-out + the honesty migration — `core.py` + plugin
- **Honesty-critical (App. E.4):** `TraitSeed.access` currently carries **outcome-category** weights
  (`callous_exploitation`, `strategic_prosociality`, `cool_instrumental_boldness`, …) as seed
  **inputs**. **Remove these from the seed.** The seed carries only **temperament parameters** (2.8).
  The categories become **observer read-outs** computed in the plugin's `world.py::study_category` /
  `report.py` from *emergent* behaviour and substrate activity. **Grep every consumer of `access`**
  (`core.py`, `drives.py`, `agent.py`, the plugin) and re-point them at the read-out.
- The `categorise`/`report` hooks are the observer layer (App. D.2): computed over behaviour, **never
  fed back**; add the study metrics (triarchic / CU / punishment-learning / aggression-type) here.

### 2.6 Behaviour selection — `affective_engine/selection.py` (NEW) + `executive.py` + seed JSON
- **Add `selection.py`:** basal-ganglia action selection (App. F). Candidates = affordances with input
  strength = anticipatory value ⋅ current drive (2.1/2.2). Implement **accumulation-to-threshold with
  disinhibition** (direct/Go release + indirect/NoGo + STN global hold) → a winner; **dopamine sets the
  gain** (Go/NoGo balance, threshold, vigour, softmax temperature).
- **`executive.py` (refactor):** recast the executive as a **parameter-setter on selection**, not a
  decider — proactive threshold/NoGo bias, reactive **STN "hold"** (the Aron IFG→STN stop), dACC
  conflict monitoring. Keep the existing "learn inhibitory monitors from memory" (reversal learning),
  but route it as *which candidates to bias*, through `selection.py`.
- **Seed JSON / `neuraldesigner`:** ensure the **full motor-selection loop nuclei** exist — dorsal
  striatum, GPe, GPi/SNr, motor thalamus (the seed already has NAc, VTA, and preSMA→STN). Add if
  absent.
- **BIS hook:** an unresolved approach/avoid near-tie holds arousal elevated (App. F.6) — wire the
  selection conflict state back to the arousal variable in `interocept.py`.

### 2.7 Endowment + epigenetics — `core.py` (TraitSeed) + `epigenetics.py` (NEW)
- **`core.py::TraitSeed`:** extend to carry the **new endowment parameters** — state-vector set-points,
  drive weights `w_k`, neuromodulator reactivities (fear/opioid/oxytocin/dopamine gains), innate-
  perturbation gains (App. B.5), and physical-trait baselines. (This is the re-parameterisation that
  replaces the legacy `gains`/`access` scheme; `gains` map onto the reactivities, `access` is removed
  per 2.5.)
- **Add `epigenetics.py`:** an early-window modifier — reads accumulated early experience during
  `development.develop(...)` and **shifts the allostatic set-points/reactivities** semi-permanently
  (App. A.1(3), doc §5.2). This is the Study-3 hook (OXTR-type effects).

### 2.8 The differential-profile plugin — `extensions/sophropathy/`
- **`society.py`:** re-express `typical_child_seed` and `fearless_child_seed` (=`shared_root_seed`) in
  the **new temperament parameters** (App. E.2); drop the `access` category weights. `sophropathic_seed`
  / `psychopathic_seed` stay as the **adult attractors** (parent seeds).
- **`world.py::study_category` + `report.py`:** implement the observer read-outs (App. E.5). No
  outcome is coded — the split must emerge from temperament × environment.
- **`module.py`:** unchanged in shape (`child_source`, `categorise`, `report` already wired).

---

## 3. What is superseded (staged, not big-bang)

The legacy **two-affect-pathway** engine — `drives.py`'s `System`/`Brain`/`Drive` as *primitive
affect systems* and `core.py`/`agent.py`'s appraisal-as-primitive — is superseded by the **substrate
(neuraldesigner) as the source of activation** + the **valence engine (2.1/2.2) as the source of
value**. Migrate behind stable interfaces: keep `TraitSeed`, `develop`, `probe`, `classify`, the three
matrices, and the plugin contract; swap the *internals* so activation comes from the substrate and
value from the state vector. Validate behaviour parity at each step; do not delete legacy paths until
the substrate path reproduces them.

---

## 4. Build order (dependencies)

1. **`interocept.py`** (state vector + innate perturbations + computed valence) → rewire
   `development.py`, `memory.py`. *Everything depends on this.*
2. **`learning.py`** (RPE + anticipatory value) → extend `drives.py` plasticity.
3. **Matrices** (`relations.py`, `environment_matrix.py`, `group_matrix.py`) adopt value + profile;
   add slots/enemy/ambivalent to `relations.py`; add group factors.
4. **`selection.py`** + **`executive.py`** refactor + seed nuclei → close the live loop; wire BIS→arousal.
5. **`TraitSeed` re-parameterisation** + **`epigenetics.py`**.
6. **Honesty migration** (2.5): `access` → observer read-out; grep and re-point consumers.
7. **Plugin re-expression** (2.8), depends on 5 + 6.
8. **Distillation** pooled prior (2.4), depends on 3.

---

## 5. Risks and checks

- **Biggest risk — the legacy migration (§3).** Stage it; keep interfaces; parity-test at each step.
- **The honesty migration (2.5) touches many consumers of `access`** — grep first, migrate atomically,
  re-run the plugin's reports to confirm categories still compute (now as read-outs).
- **No new coded arbiter.** Selection (2.6) and the matrices (2.3) must not contain a rule that reads
  the situation and outputs a behaviour/category — the outcome must emerge (App. F.8 / D.2).
- **All numbers are scaffold** (set-points, gains, β/γ/α/λ, thresholds, slot sizes/decay) — calibrated
  later against the human studies; none asserted.
- **Module contract intact** — no edits to `registry.py` or `project.py`; the plugin stays discovered.

---

## 6. The three honesty-critical changes (do not lose these)

1. **Computed valence replaces stipulated valence** (`development.py` → `interocept.py`, 2.1).
2. **Outcome-category weights migrate from seed *inputs* to observer *outputs*** (`core.py` + plugin,
   2.5) — the seed carries temperament only.
3. **Selection and biases stay emergent** — the executive is a parameter-setter, biases and the
   sophropath/psychopath split emerge, nothing is decreed (2.6, 2.8).
