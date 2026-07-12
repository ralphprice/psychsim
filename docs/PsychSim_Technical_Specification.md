# PsychSim — Technical Specification

**Status: v1 — describes the frozen v13 organism.** Grounded in the repository at
`/home/ralph/psychsim` (branch `main`, seed head `v13`); every claim is cited to a file.
Ordinal/structural claims only — no invented numbers. Parameters are **illustrative scaffold**
(structure cited; many connection strengths are placeholders, marked as such). In keeping with the
project's own discipline, known documentation/code drift and open verification items are kept
**visible** (inline `[VERIFY]` markers, consolidated in Appendix B) rather than hidden — none
affects the organism's behaviour.

> **Documentation-hygiene warning (read first).** Two of the documents named in the brief —
> `docs/ARCHITECTURE.md` and `docs/PsychSim_ARCHITECTURE.md` (they are byte-identical to each
> other) — describe the **pre-retirement** platform: a live "Panksepp 7-primary-system" drive
> engine (`drives.py`), a bolt-on `Executive` (`executive.py`), and "behavioural networks." **All
> of that was retired and deleted** (see `docs/PsychSim_CORE_RECORD.md`, "Substrate-social phase
> COMPLETE"). Those two docs remain accurate only for the **world/platform scaffolding** layer
> (`sim_world`, places, floorplans, timeline, environment matrix, activities, speech). The same
> caveat applies to `docs/PsychSim_Handover.md` §3.1–3.2. The authoritative record of the current
> organism is `docs/PsychSim_CORE_RECORD.md` + `docs/PsychSim_Outstanding_Register.md` + the seed
> file. This spec follows the authoritative record, not the stale architecture prose.

---

## 1. Overview and the research question

### 1.1 What PsychSim is
PsychSim is a **life-course and day-to-day social-simulation platform** built as the research
instrument for a PhD on the development of the **functioning, non-offending psychopath**
("sophropath") and its childhood form ("proto-psychopath"). The software — not the eventual
paper — is the active project (`docs/PsychSim_Handover.md` §0).

Its defining scientific commitment: the simulation contains **no hand-authored psychological
effects**. Feeling, behaviour, attitudes and personality are meant to **emerge** from an evolving,
neuroscience-grounded neural substrate, and are then **measured** — never scripted, never assigned
a verdict (`docs/PsychSim_Handover.md` §2; `docs/CORE_RECORD` throughout).

### 1.2 The research question
Whether, and by what developmental route, a **category-free neural substrate** — nothing about
outcomes encoded — can reproduce the emergence of the callous-unemotional (CU) phenotype, and its
differential-susceptibility interaction with childhood environment. The CU construct is scored on
the **callous-unemotional core** (being unmoved by, or exploiting, a vulnerable other), not on
reactive aggression or victimless reward-seeking. Crucially, whether a circuit deficit or a family
environment produces CU is a question the platform is built to **measure**, having refused to encode
the answer (`docs/PsychSim_CU_Study_Spec.md` §1, §6).

### 1.3 Honest scope
- **Functional, not biophysical.** Circuits are nucleus-level **rate units**, not spiking neurons;
  the warrant is behavioural, not biophysical (`core/substrate/engine.py`; `core.py` header).
- **Illustrative, not fitted.** Every invented dynamic constant is marked `SCAFFOLD`/placeholder
  and is a calibration target; nothing is tuned to a desired result (`core/substrate/params.py`
  header; seed `meta.scaffold_note`).
- **A simulation generates hypotheses, not evidence about people** (`docs/CORE_RECORD`; Handover §2).

---

## 2. Architecture layers

The system is a stack of layers with dependencies pointing **inward** (the core never depends on a
study extension; `docs/ARCHITECTURE.md` §1). From the inside out:

1. **Substrate** (`core/substrate/`) — the category-free neural engine: the seed loader (`model.py`),
   the dynamics engine (`engine.py`), the meaning-blind plasticity rule set (`plasticity.py`), the
   receptor-sign pharmacology table and scaffold constants (`params.py`), behaviour selection
   (`social.py`, `behaviour.py`), and the descriptive read-out (`readout.py`). The seed itself is
   `docs/neuralnetworks/psychsim_substrate_seed_v13.json` — the single source of truth for structure
   and parameters.

2. **Affective engine / development wrapper** (`core/affective_engine/`) — wraps one substrate
   instance per agent (`AffectiveAgent`, `agent.py`), the developmental life course (`development.py`),
   the physical endowment / body and interoceptive valence layer (`endowment.py`, `physical.py`,
   `interocept.py`), and the descriptive observer read-outs (`observer.py`, `readout.py`). The four
   interface matrices (relationships, environment, groups, self-reflection) attach here / in
   `sim_world`.

3. **World** (`core/sim_world`, `core/sim_viz`, plus `project.py`) — places with interiors and
   affordances, a two-rate clock/timeline, the Game-Master, relationship/environment/group matrices,
   the town spawn generator and the plan-view ("glass-roof") renderer. **This layer's mechanisms are
   real and current; the mind it drives is the substrate, not the retired Panksepp engine the older
   docs describe.** `[VERIFY]` some `sim_world` docstrings still describe the retired engine in prose
   (flagged for cleanup in `docs/Outstanding_Register` §3).

4. **Study extensions** (`extensions/`) — research bolt-ins that import the core and add one study's
   content (the core never depends on them). Reference extension: `extensions/sophropathy/` — the
   study's **plugin registration** (`module.py` — `MODULE`, hooks: `child_source`, `world_content`,
   `categorise`, `report`; `adult_source=None` keeps the core default), the **family model**
   (`society.py` — dispositions + the parent→caregiving-environment mechanism from a parent's CARE/
   CONTROL), the **study world** (`world.py` — venues, norms, and a neutral symmetric behaviour-reading
   `WARM…DISRUPTIVE`, deliberately non-forensic), and the **live town engine** (`engine.py` — the
   continuously-steppable `SimEngine`). Secondary: `extensions/justice/` (labelling-theory module). A
   study is a discoverable **module** (`core/modular/registry.py`; drop a package with a `MODULE`
   symbol — no core edit). "sophropathy" denotes the **functioning/adaptive end** of the psychopathy
   spectrum: one shared-root fearless (proto-psychopath) disposition, asked whether development drives
   it toward an adaptive ("sophropathic") or antisocial adult outcome.

5. **Instruments** (`core/`) — general research instrumentation independent of any study: the
   developed-agent **bank** (`agent_bank.py`), the **Arena** (`arena.py`, `arena_view.py`), the
   **scan controller** (`scan.py`, `scan_search.py`, `scan_match.py`), the parallel-instance harness
   (`parallel_world.py`).

6. **Live console** (`psychsim_server.py` + `ui/`) — a stdlib HTTP server driving a continuous
   step-loop, plus a Vite/React/TypeScript control panel: the Town open-world view, the Arena tab,
   and **read-only** Neural/matrix views over the live seed.

The core/module boundary is explicit (`docs/CORE_RECORD`, "The core / module boundary"): the core is
the universal organism + matrices + 1/n plasticity + behaviour selection + the general instruments
(bank, Arena, **scan controller / throttle**). Switch the study module off and you have a complete,
ordinary simulated human.

> `[VERIFY]` **Terminology correction (important — the brief conflates two things).** The "circuit-
> breaker / throttle" is **core** machinery, **not** `extensions/sophropathy/module.py`. The throttle
> is `core/substrate/engine.py::set_throttle` (attenuates a circuit's **output**, from birth, with a
> plasticity ceiling; it **never writes the seed**), exercised by the scan controller (`core/scan.py`).
> `sophropathy/module.py` is the study's **plugin registration** (`MODULE = Module(...)`); the study's
> actual behavioural footprint on a spawn is its **child-seed mix** (`child_source` — a `fearless_frac`
> minority seeded `fearless`, the rest `typical`), plus world content and its behaviour-reading. So
> the CORE_RECORD's "the circuit-breaker module is the entire footprint of the study-specific plugin"
> describes the throttle **used as a probe/stressor**; the throttle primitive itself lives in core as
> the scan controller's manipulation channel.

---

## 3. The substrate in detail

The substrate is the heart of the platform and the locus of every honesty guarantee. It is
**category-free**: a graph of nucleus-level rate circuits with receptor-signed edges, carrying **no
psychological meaning** — "a circuit is just an id" (`core/substrate/model.py` header).

### 3.1 The seed (single source of truth)
`docs/neuralnetworks/psychsim_substrate_seed_v13.json` (`meta.version = "v13"`) contains:

| element | count | seed key |
|---|---|---|
| circuits (nucleus-level rate units) | **82** | `circuits` |
| directed edges (connections) | **206** | `connections` |
| innate-wiring catalogue entries | **25** | `innate_wiring_catalogue` |
| input channels | **9** | `input_channels` |
| physical-endowment attributes | **7** | `physical_endowment` |
| plasticity rules | **8** | `plasticity_rules` |
| gaps-register entries | **20** | `gaps_register` |

Circuit **domains** (from the seed): sensory 18, defensive_threat 17, interoception_autonomic 14,
reward_approach 12, executive 11, affiliation 6, social_cognition 4 (= 82). Grain is nucleus level
(amygdala subnuclei kept separate: LA / BA / CeA / ITC).

`model.py` loads the seed **verbatim** into typed records (`Circuit`, `Connection`, `InputEdge`,
`SubstrateModel`) and supplies **no** dynamics and **no** meaning. Edges to/from circuits absent from
the index are **skipped with a warning** (connectome-gap handling), never hard-failed.

> `[VERIFY]` **Stale in-code counts.** `core/substrate/__init__.py` still says "73 circuits / 159
> connections" and `engine.py` / `model.NEUROMOD_SOURCE` comments still say "v7." These are stale
> docstrings; the loaded artefact is v13 (82/206). The authoritative counts are the seed file, not the
> prose (memory: "verify the artefact actually reloaded"). Recommend refreshing those headers.
> `[VERIFY]` `meta.supersedes` reads "v8" (the meta was last hand-edited then); the lineage note in
> `model.py` records v1–v12 archived, v13 live.

### 3.2 Circuits (nodes)
Each `Circuit` (`model.py` L104–116) carries: `id`, `domain`, `baseline` (default 0.05), activation
`bounds` (default 0–1), `tau_ms` (time constant), `homeostatic_setpoint` (uniformly 0.1 across
circuits — a firing-rate homeostasis quantity, R4-HOMEO, distinct from interoceptive body set-points),
`online_age` (developmental gate), `schedule_ref` (plasticity schedule name), `calibration_active`,
`sign` (from the nucleus's principal transmitter), and a descriptive `name`/`function` **never read by
the dynamics**. Example circuits: LA/BA/CeA/ITC (amygdala), BNST, PAG, HYPdm, VMHvl (attack area), VTA/
SNc (dopamine), NAc-core/shell, LC (noradrenaline), DRN (serotonin), vmPFC/dmPFC/dlPFC/vlPFC/OFC/dACC/
FPC (prefrontal), rSMG-TPJ/pSTS/PCun-PCC/ATL-TP (social-cognition/mentalizing), plus the sensory relays
and autonomic/endocrine chain (NTS/PBN/insula/PVN/RVLM/adrenal/pituitary).

### 3.3 Edges and receptor-derived signs (the pharmacology table)
Each `Connection` (`model.py` L119–133) carries `source`, `target`, `weight0`, `bounds`,
`gating_neuromodulator`, `eligibility_tau_ms`, `online_age`, `calibration_active`,
`is_innate_reinforcer_link`, a `sign`, and a cited `dominant_receptor`.

**Sign is receptor-derived, never chosen for behaviour** (v12a upgrade). Per edge:
`sign = f(source transmitter, cited dominant target receptor)`:
- Where a `dominant_receptor` is cited, `_receptor_sign` (`model.py` L86–95) parses the leading
  receptor token and looks up its **fixed pharmacology class** in `params.RECEPTOR_SIGN`
  (`params.py` L39–55) — e.g. AMPA/NMDA/D1/5-HT2A/α1 → `+1` (excitatory); GABA-A/D2/5-HT1A/α2/
  µ-opioid → `−1` (inhibitory). **40 of 206** edges cite a receptor.
- Otherwise `_sign` (`model.py` L78–83) falls back to the source nucleus's **principal
  transmitter** (leading "GABA…" → inhibitory, else excitatory).

The honesty property is structural: to flip a sign dishonestly a builder would have to **cite a false
receptor** — a checkable lie against Guide-to-Pharmacology, not a silent tune (`params.py` L34–38).
This is what made the serotonin node possible: 5-HT's sign is **opposite across its targets**
(5-HT1A inhibitory on the attack area, 5-HT2A excitatory on the PFC controllers) and is
un-representable under a nucleus-level rule.

### 3.4 Input channels and physical endowment (the body loop)
**9 input channels** (`input_channels`): IN-VIS, IN-AUD, IN-OLF, IN-GUST, IN-SOMATO, IN-PROPRIO,
IN-VESTIB, IN-INTERO, and IN-CONSPEC (the v10 social-visual conspecific-valuation stream — face/body
of a conspecific → OFC/NAcc valuation, deliberately **not** an IN-VIS sub-channel so generic visual
novelty cannot prefix-match it). Sensory edges whose source is a channel become `InputEdge`s driven
when the channel is injected (`engine.inject_channel`, prefix-matched).

**Innate value** enters only through the cited **primary-reinforcer / prepared-bias links**. The
catalogue's 25 entries are grouped: `PR-*` primary reinforcers (sweet/bitter/sour/umami/salt/
nociception/thermal/contact/homeostatic), `PB-*` prepared biases (looming/startle/face/biomotion/
voice), `LB-ANCESTRAL-THREAT`, `SR-*` social primaries (separation/proximity/rejection), and `IW-*`
the v10–v13 innate-wiring additions (attractiveness-reward, formidability-submit, the four Allen
afferents, the 5-HT regulator). **21 edges** are flagged `is_innate_reinforcer_link` in the seed —
e.g. `IN-SOMATO:nociception→LA/CeA`, `SC-Pv→CeA/PAG`, `StN→CeA`, `IN-GUST:sweet→NAc-shell/VTA`,
`IN-INTERO:contact_loss→PAG-PANIC`.
> `[VERIFY]` The seed's `assembly_status.how_value_enters` still names only the original **3** cited
> innate links (a v-early statement); the current seed flags 21 `is_innate_reinforcer_link` edges.
> The prose is stale relative to the data — worth reconciling. `is_innate_reinforcer_link` is
> **provenance only** (not read by `engine.py`'s dynamics).

**Physical endowment** — 7 attributes (`physical_endowment`): PH-ATTRACT, PH-SIZE, PH-MUSCLE,
PH-AGILITY, PH-HEALTH, PH-SENSORY, PH-TEMPERAMENT. The **wired subset** (`core/affective_engine/
physical.py`): attractiveness and formidability become a **bearer-pure stimulus** on IN-CONSPEC
(`physical_stimulus`); **biological sex** is a per-agent birth parameter conditioning only PH-SIZE
mean and a **VMHvl input-reactivity gain** (`vmhvl_reactivity` — E5 own-strength × E6 sex factor,
scaling VMHvl's *input*, never adding a standing drive, so it cannot manufacture unprovoked
aggression). Physical perception fires **Arena-only** (design ruling). PH-AGILITY/PH-SENSORY are
deferred as bearer capacities (`docs/Outstanding_Register` §4). Outcomes (beauty premium, CU sex
ratio) are `scan_match` targets, **never** weights (`physical.py` header; seed `meta.v10_additions`).

### 3.5 Dynamics (the engine)
`SubstrateEngine` (`core/substrate/engine.py`) advances the network with an explicit forward-Euler
leaky-integrator step (`step`, default `DT_MS = 50`). Per step, six phases:

1. **Activation update** — for each live circuit, net input = external drive + Σ over live incoming
   edges of `edge.sign × weight × a[source] × output_gain(source)` + channel-edge drive; the driven
   input is scaled by any per-circuit `reactivity`; then `da = (dt/tau)·(−(a−baseline) + input)`;
   clamp to bounds. **The only nonlinearity in the activation path is the bound clamp** — no sigmoid
   squashing. Updates are synchronous (all circuits read the same pre-step state).
2. **BCM sliding threshold** `theta` update + an EMA of mean activity.
3. **Per-connection plasticity** (see §3.6).
4. **R4-HOMEO** synaptic scaling (every `HOMEO_EVERY` steps).
5. **R8** competitive normalisation of incoming weights.
6. **R7-STRUCT** pruning of long-silent connections.

`settle(ticks)` runs one **episode** (co-active connections get `exp_count += 1`, so
experience-decreasing plasticity counts per-episode). **Live set** is gated by two switches
(`_refresh_live`): a circuit/edge is live iff `calibration_active AND online_age ≤ age_years` (and,
for an edge, both endpoints live).

### 3.6 Plasticity — the meaning-blind rule set (8 rules)
`core/substrate/plasticity.py`. Every function takes **only** numeric activity/weight/age arguments;
nothing references a circuit's identity or any reward/behaviour/outcome term (the honesty wall at
code level). The 8 seed rules:

- **R1-HEBB** (coincidence) — subsumed into R3-BCM (never stands alone; unstable).
- **R2-RATE** — a rate-level (not spike-timing) modelling choice; flagged `scaffold`.
- **R3-BCM** (workhorse) — `bcm_term = a_pre·a_post·(a_post − theta)`, `theta` tracks the circuit's
  **own** recent activity (nothing external).
- **R4-HOMEO** — slow multiplicative synaptic scaling toward a firing-rate set-point.
- **R5-NMOD** — three-factor neuromodulatory gating: `consolidation = eligibility_trace × modulator`,
  where the **modulator MUST be a circuit's live output** passed in by the engine — the function
  cannot fetch or set it, so it cannot smuggle an outcome (the "DANGER POINT" rule).
- **R6-DEVGATE** — all updates scaled by `eta(age, schedule)`; **age enters only here, as a rate,
  never as a target** (high early, adolescent resurgence, low adult).
- **R7-STRUCT** — activity-dependent pruning/addition within connectome limits.
- **R8-BOUNDS** — finite bounds + competitive normalisation (`normalise_incoming`).

> `[VERIFY]` **On "Oja":** the brief lists Oja among the rules. There is **no Oja-named function**; the
> Oja role (weight-vector normalisation / competition) is filled by **R8 `normalise_incoming`**. State
> it as "R8 competitive normalisation plays the Oja role," not a separate Oja update.
>
> `[VERIFY]` `plasticity.maturation()` (a functional-**capacity** curve, distinct from the plasticity
> **rate** `eta`) is defined and feeds downstream **behaviour selection** (adolescent-risk inverted-U),
> but is **not called** inside the substrate integration loop.

### 3.7 Neuromodulation — circuit OUTPUTS, not set scalars
`neuromod_output(nmod)` (`engine.py`) returns the **mean live activation of the source circuit(s)**
(× throttle gain), never a value set from an outcome. The source map `NEUROMOD_SOURCE` (`model.py`):
NA→[LC], DA→[VTA, SNc], ACh→[BF-ACh], OT→[PVN-OT], CRF→[PVN, BNST], **5HT→[DRN]**. Across the 206
edges, `gating_neuromodulator` usage is: ACh 26, NA 17, DA 17, OT 8, CRF 2, none 136.
> `[VERIFY]` 5-HT is **registered** as an R5 gate source (so it is available), but **no connection is
> 5HT-gated yet** — the DRN acts through its direct receptor-signed projections. Confirmed by the
> `NEUROMOD_SOURCE["5HT"]` comment in `model.py`.

### 3.8 Seed lineage (additive, byte-identical topology)
Each version is additive or sign-only; **prior topology byte-identical**; v1–v12 archived
(`model.py` header; `docs/CORE_RECORD`; `docs/Outstanding_Register` §1):

- **v9** — new circuit **VMHvl** (hypothalamic attack area) + a provocation→attack pathway
  (`IN-INTERO:provocation→VMHvl`, `VMHvl→PAG`, `VMHvl→HYPdm`), closing the OBS-3 gap (provocation
  previously reached the attack effectors only via the **GABAergic CeA**, which inhibits them, so
  more provocation deepened attack suppression). `CeA→PAG/HYPdm` inhibition **untouched** (fear stays
  the baseline threat response). Emergent, un-tuned developmental result: overt aggression at age ~2,
  progressive restraint by age 8+ via the maturing STN brake.
- **v10** — physical endowment + biological sex; **IN-CONSPEC** channel + 3 percept edges.
- **v11** — 4 Allen-audit subcortical afferents (existence+direction only, weights scaffold):
  MeA→VMHvl, LH→LHb, VP→LHb, BNST→VMHvl. Lesson recorded: **completeness includes inhibition** —
  edges are kept because the anatomy exists, never cherry-picked by whether the emergent sign suits
  the hypothesis.
- **v12 / v12a** — the **sign-convention upgrade**: per-edge receptor-derived signs; 20 edges cited a
  receptor → **exactly 3 flips** (MeA→VMHvl −→+, VP→LHb −→+, BNST→VMHvl +→−). v11's MeA→VMHvl "brake"
  **retired as an artifact** (a result is only as trustworthy as its sign convention); one authorised
  magnitude-only recalibration (MeA→VMHvl 0.5→0.1) so the conspecific cue *primes* rather than
  *drives* the attack area.
- **v13 / 2.1b** — the **DRN (dorsal raphe / 5-HT) node** + 10 receptor-signed edges (opposite signs
  across targets) + `NEUROMOD_SOURCE["5HT"]=["DRN"]`; **plus 3 cortical inhibitory interneurons**
  (DRN-GABA, vmPFC-GABA, dlPFC-GABA). 78→82 circuits, 186→206 edges. Headline emergent (a `scan_match`
  target, **not coded**): lowering 5-HT tone (throttling DRN) **increases provoked aggression** — the
  clinical direction — emerging from the *net* of competing signed pathways, with no coded
  `5HT → −aggression` rule.

### 3.9 Instability as a diagnostic of missing anatomy (v13 finding)
The DRN↔PFC top-down loop first saturated (mutual excitation drove DRN and vmPFC to 1.0). The fix was
**not** to rebalance or remove a real edge but to add the missing local **GABAergic interneuron** the
real raphe/cortex has (silence-tested: silence the interneuron and the target runs hot — the proof it
is anatomy, not a tuned weight). The unresolved `PFC→DRN` afferents are **deferred** in the gaps
register, not faked (`docs/CORE_RECORD` v13 section; memory: "instability = a missing inhibitory
element").

### 3.10 Gaps register (declared incompleteness)
The seed carries a **20-entry `gaps_register`** — declared, not hidden. Notable open items: qualitative
newborn weights; incomplete connectome projection list; receptor-subtype distributions/glia not
represented; approximate developmental-onset ages; social-cognition weights rest on human imaging only
(no rodent homolog to audit against Allen); the deferred `DRN→VTA` sign, median raphe (MRN), and the
`PFC→DRN` loop; and the note that the **sign convention is improved where cited, not claimed complete**.

---

## 4. Development and the descriptive read-out

### 4.1 The agent wrapper
`AffectiveAgent` (`core/affective_engine/agent.py`) wraps **one private `SubstrateEngine`** (the
shared seed **structure** is immutable and read-only; each agent's developing **state** is its own —
the proven no-bleed / independence guarantee). It also holds the temperament `seed`/`gain`, episodic
`memory`, and v10 `physical`/`sex`. `__post_init__` seeds temperament into the substrate
(`seed_substrate` — temperament → circuit **reactivity biases**, never outcome categories) and applies
the physical (VMHvl) calibration. The tick verb is **`social_act(appraisal, age_years)`** →
`respond_to_substrate` → the basal-ganglia race in `substrate/social.py` (multi-affordance selection
with surround inhibition and an STN/executive hold; "restrain" if nothing crosses threshold).
Restore-into-mind paths: `adopt_engine` / `adopt_developed` (restored-never-edited).

### 4.2 Developmental time is REAL
`develop(agent, env, n_episodes=48, …)` (`development.py`) maps episodes onto a **real 0→18-year age
axis** (`span = 18.0`); each episode passes the resulting `age_years` into `set_age`, and the
substrate's `eta(schedule_ref, age_years)` / `maturation(schedule_ref, age_years)` are functions of
**developmental age only** — never of wall-clock or episode count. `develop()` **exposes no
plasticity-rate parameter**, so no fast loop can touch the developmental schedule. This is the
"compression is wall-clock only" discipline (`docs/MASTER_Part6` §S12.5 "sacred"; asserted by
`tests/test_arena.py`). Two senses of "compression" to keep distinct:
- **Forbidden** — altering plasticity constants to make growth "look" faster/successful. Never done.
- **Sanctioned** — running wall-clock faster and **sampling** experience (48 episodes standing in for
  18 years) on a **faithful age axis**; the higher-resolution growth path is the batch life-stepper /
  Arena. Real developmental *age* is preserved either way; only experience *density* is reduced.

> `[VERIFY]` **Doc/code drift in `development.py`.** The module docstring and ~half its identifiers
> (`CTRL_LR`, `ACCESS_LR`, `THREAT_CREEP`, `_plasticity`, `_importance`, `_env_gates`,
> `_affordance_strength`, `_gate`, the `graded` parameter) describe/implement a **retired**
> developmental-plasticity mechanism and are **not called** by the live `develop`/`live_moment` path
> (all real plasticity is now the substrate's BCM). Do not describe that docstring's rule set as the
> operative mechanism. Also: `live_stimulus` (L246) has unreachable dead code (a second `return resp`
> referencing an undefined name) — latent bug, currently unreachable.

### 4.3 Environment as perturbation, value as computed
`Environment` (warmth/structure/recognition; `warm_firm_home` vs `harsh_inconsistent_home`) describes
**what a caregiving response does to a child's interoceptive state** (a perturbation pattern), never a
decreed valence. Its `response_valence` is **computed** by reading a reference child-state through
`interocept.valence_of_event`, so the same response yields **different value** in agents with
different endowments (`development.py`; `interocept.py`). The interoceptive layer (`interocept.py`) is
the one valence engine: `D = Σ_k w_k·deviation(H_k, H*_k)`; `r = β·(D_prev − D_now)` — value computed
from the agent's own regulated state, with the only innate event→value links the cited primary-
reinforcer set. `state_from_substrate` reads state-variable **levels from live substrate activity**,
so valence computes over each agent's own substrate.

### 4.4 The descriptive read-out (no verdict)
Read-outs are **descriptive measurement and attach NO verdict** (`readout.py`, `observer.py`):
- `substrate_profile` / `read_mind` (`readout.py`) run a neutral probe, average activation per
  circuit **domain** ("anatomy, not outcome categories"), normalise to a profile, and pick a
  `dominant` domain — an emergent read-out, explicitly "not a verdict." **Read-only by construction**:
  the full developed+transient state is frozen and restored, so measuring never develops the agent.
- `observer.py` computes named psychological constructs — triarchic boldness/meanness/disinhibition
  (Patrick 2009), callous-unemotional (Frick), empathy, reactive-vs-instrumental aggression,
  passive-avoidance deficit — **over emergent behaviour, and NEVER fed back into the mechanism**. It
  **deliberately returns no single "psychopathy" verdict** — that is the thesis's interpretive
  question. `profile_from_substrate` is likewise read-only (freeze/restore in a `finally` block).
- **Panksepp / affect labels appear ONLY as read-out labelling** here, never as the live engine.
  `[VERIFY]` `observer.instrumental_aggression` is hard-set to 0.0 with the honest caveat
  "cold/calculated exploitation: not grounded in the substrate" — a known read-out gap.

### 4.5 The four interface matrices
Relationships (`sim_world/relations.py` — ties, standing, reciprocity, strain), environment
(`environment_matrix.py` — emergent attractions/aversions to Things, with revisable inherited leans),
groups (`group_matrix.py` — belonging, dominance-vs-prestige status), and **self-reflection** (routed
as a **non-feedback read-out**: it observes the developed state without altering it — executive
trajectory byte-identical with/without it; `docs/CORE_RECORD` OBS-1 Note B). All are driven by
emergent behaviour, not scripted.

---

## 5. Instruments

### 5.1 The Town (coarse open-world spawn)
The open-ended "watch-the-town" simulation: a spawned settlement (real ONS demography ratios, homes/
school/workplaces, floor plans, gardens), populated by a society with standing relational ties, run on
a two-rate clock; each `Person` owns an `AffectiveAgent` mind (the substrate). Developmental time runs
on the **real clock** via the life-stepper — the live engine runs **no** separate/compressed
developmental clock. Idle towns skew **appetitive** by design (aggression is provocation-gated); this
is correct, not a missing repertoire (`docs/CORE_RECORD`, "Watching the sim — read this first").

### 5.2 The Arena (fine-detail lens — an instrument, not a study)
`core/arena.py` + `core/arena_view.py`. A confined micro-environment where **2–5 agents** (hard-
enforced, `ROSTER_MIN/MAX = 2,5`) are developed and watched at high detail — explicitly a
**development-and-regression harness**, not a study ("a study is any manipulation, run here at high
detail; the Arena is general instrumentation"). Key properties:
- **4 micro-environments** (`one_room`, `one_house`, `house_garden`, `office`); `MicroEnv.escape` is a
  **structural count** of present affordances (never a valence). Fewer affordances → higher co-located
  fraction (`confine`); it shifts the social/solo **mix**, never scales a perturbation's intensity.
- Agents perceive each other via `_ARENA_PERCEPTION` — the other's act presented in the neutral
  trigger vocabulary (a stimulus, never a valuation). Whether confinement "reads as strain" must
  **emerge** from each agent's own circuits.
- Each slot is an **independent** `AffectiveAgent`; sources are `newborn`/`grown`/`banked` (banked =
  restored, never edited).
- **Compression is wall-clock only (sacred).** Episodes run fast over a **real childhood span**; age
  advances on the real 1/n schedule (`age = childhood_years · i/E`); **plasticity constants
  untouched**. The Arena defines only scaffold constants (`_TIE_STEP`, `_CONFINE_*`), none a rate or a
  valence.
- **`ArenaTrace`** logs per-episode emergent acts, weight drift, and per-pair tie strain; analysis
  methods `signature()` (deterministic regression diff), `peak_activation()`, `viable()` (no
  persistent saturation) and `settled()` (Regime-B oscillation check) distinguish emergent escalation
  from closed-loop numerical instability. (OBS-4: the Arena's first act was to catch a silent
  plumbing null that would have invalidated its own dynamics — probing, not assuming.)

> `[VERIFY]` **Inspector tension.** `docs/PsychSim_Arena_UI.md` §4.3 promises live per-agent
> mind/memory/standing inspection "all the way through the run," but `arena_view.py` states
> `run_arena` returns only the `ArenaTrace` and **discards the agents** — deep per-agent inspection is
> flagged as a not-yet-done reviewed core change. The UI spec describes an intended, not-yet-wired
> capability.

### 5.3 The scan controller (found-not-fitted search)
`core/scan.py` (+ `scan_search.py` search-for-effect, `scan_match.py` search-for-match). Structural
honesty guards, inherited for free by any study that uses it:
- **Manipulates node throttles only** (`MANIPULATION_SCOPE = "nodes only"`; connection-level deferred);
  the **only** channel to the substrate is `engine.set_throttle`. The throttleable set is
  **seed-derived** (a query over domain tags), not curated. The `Throttle` type is *named* on purpose
  so a slider-vs-fraction inversion can't silently run every experiment backwards.
- **Never writes the model** — a test asserts the shared model is byte-unchanged across a run
  (found-not-fitted, architectural).
- **Objective is scalar-by-construction, per-signature** — `punishment_learning`, `dissociation_index`
  (cognitive-mentalizing MINUS affective-empathy) — each grounded on its own; **no composite blend**
  and **no distance-to-a-drawn-target**. `scan_search` optimises **one named read-out at a time** as a
  contrast from the intact control.
- **Provenance-validated** — every result stamps `provenance["substrate"] = model.meta["version"]`
  read from the **live model** (can't drift from the artefact actually run), plus scope + episode count.
- **Never self-certifies** — a hit is `candidate_hypothesis`, **never `finding`**; promotion needs a
  robustness probe. For search-for-match, `load_field_pattern` **rejects** any pattern missing
  `source`/`population`/`instrument`/`not_used_in_calibration:true`; a placeholder source is marked
  `placeholder_not_corroboration`; and every result carries `corroboration: false` — "the scan NEVER
  reports a match as corroboration."
- **Coarse-to-fine, viable-first** — binary screen single circuits, then grade only the top-k plus
  low-order pairs; non-viable (all-pinned) agents recorded but not scored.

### 5.4 The developed-agent bank
`core/agent_bank.py`. Snapshots an agent's **complete developed state** (sculpted connectome weights,
per-connection `exp_count`, BCM `theta`, mean activity, pruned flags, throttle, age, the four matrices,
interoceptive state vector, physical/sex, provenance) and re-instantiates it to **resume** developing
(pause-and-resume, not freeze — plasticity continues under the 1/n schedule). Two load-bearing
invariants: **grown-and-banked, never fabricated** (the only way state enters is `bank()` on an agent a
run actually grew) and **restored, never edited**. `_restore_engine` raises a clear **"stale bank,
regrow"** error on a connection-count mismatch rather than padding (a stale bank = the connectome
version that grew it differs from the one restoring it).
> `[VERIFY]` The length-guard does **not** catch a **sign-only** version change (a v11-grown bank
> restored into v12 loads without a stale flag). Mitigated for now by regrowing the cache under each
> new seed version; a snapshot version-stamp is a deferred hardening item (`Outstanding_Register` §4).

### 5.5 What a "study" is
A study is **any manipulation-and-observation**. The Arena is the fine-detail lens (few agents, high
detail); the Town is the coarse open-world; the scan controller is the search instrument; the bank is
the grow-once/re-hydrate capability. None of these is psychopathy-specific.

### 5.6 The sophropathy study extension (the reference bolt-in)
`extensions/sophropathy/`. Its footprint on the neutral core:
- **`module.py`** — `MODULE = Module(...)` discovered by `project.py`; `child_source` seeds a
  `fearless_frac` (default 0.15) minority as the shared-root fearless child, the rest typical;
  `adult_source=None` (no change to core default); `categorise=study_category`; `report`.
- **`society.py`** — child dispositions (`typical` / `fearless` = `shared_root_seed` / `fearless_
  calculating`) and parent dispositions (`normal` / `sophropathic` / `psychopathic`);
  `parent_to_environment(parent)` derives the caregiving `Environment(warmth, structure, recognition)`
  from the parent's CARE and CONTROL gains — the intergenerational mechanism. Explicitly not fitted.
- **`world.py`** — study world content: venues (home/school/workplace/community), per-place `NORMS`, a
  **symmetric** behaviour spectrum `WARM/COOPERATIVE/CONSIDERATE/SELF_DIRECTED/BOISTEROUS/DISRUPTIVE`
  (positive pole first-class), and `study_category(behaviour, affordance)`. Deliberately non-forensic
  ("no theft, no lock, no offence vocabulary").
- **`engine.py` — `SimEngine`** — the live continuously-steppable town (Park-style is→decide→move
  loop): `step()` moves everyone on role schedules (A* pathing) then runs co-location
  `group_encounter`s; `snapshot()`/`person_detail()` are **read-only** `read_mind` measurements
  (snapshotting never develops an agent); controlled-experiment mode swaps non-subject adults for fixed
  banked-library brains and freezes them so only study subjects evolve; save/load pickles the whole
  running world. Development runs on the **real clock** via the life-stepper — no compressed
  developmental clock.
- **Seven-stage programme** (`stages.py`, per `README.md`): Stage 1 balanced society → Stage 7
  dispositional-parents × fearless-children, demonstrating differential susceptibility. `[VERIFY]`
  `stages.py`, `lived.py`, `report.py`, `townlife.py`, `timeline_driver.py`, `library.py`,
  `viz_bridge.py` were not individually read for this draft — enumerate/verify if the spec needs them.

### 5.7 The live console (server + UI)
**`psychsim_server.py`** — a dependency-free stdlib `ThreadingHTTPServer` running one global
`SimEngine` (the sophropathy Town spawn), stepped on a background daemon thread while playing (default
port 8765, population 80, seed 7, tick 15 min). It also serves the built React SPA from `ui/dist` at
`/`. Endpoints (GET unless noted): `/town` (geometry), `/plan` (glass-roof SVG + grid→pixel mapping),
`/state` (live poll — positions/drives/clock), `/person`, `/saves`, `/library`, `/modules`, `/profiles`,
`/roles`, `/matrix` + `/matrix/items`, `/neural`, `/arena/{environments,sources,relationships}`,
`/report/{cohort,subject}`, `/health`; and `POST /cmd` accepting
`play|pause|speed|add_person|respawn|save|load|delete_save|matrix_upsert|matrix_delete|arena_run`
(unknown → HTTP 400).

**`ui/` — Vite + React + TypeScript SPA.** Shell = `TelemetryStrip` + `TabBar` + `ControlRail` + active
tab. **Seven tabs:** Town, Arena, Development Cohort, three Matrix tabs (social/environment/group), and
**Neural**. Read-only vs editable:
- **Neural view is READ-ONLY over the live seed — enforced structurally.** `NeuralView.tsx` imports
  only `getNeural` (no `sendCommand`); it renders circuits/connections + verbatim seed provenance
  (confidence/evidence/sources, a `SCAFFOLD` chip), with a `READ-ONLY` banner ("Circuit changes go
  through a reviewed seed pass, not this browser"). The old `neuraldesigner` sandbox is gone;
  `neural_upsert`/`neural_delete` are **deleted** and fall through to the HTTP-400 unknown-command
  rejection — **there is no browser write path into the organism**. `types.ts` `NeuralView` carries
  `read_only` + `source_of_truth`.
- **Matrix tabs are editable of *definition vocabulary* only** (role-pair / thing / group **types** via
  `matrix_upsert`/`matrix_delete`) — the runtime traces (ties/bonds/memberships) are emergent and
  read-only; no organism/seed write.
- **Town Inspector** is a **descriptive read-out only** — role, normalised domain-profile bars, group
  standing, memories; "never a psychopath/sophropath label (that classifier is gone)." No edit
  controls.
- **Arena tab** wires `core/arena.py` (never reimplements the run): 2–5 roster enforced; environments
  shown as their present Things + structural `escape` count (never a "stressful" tag); temperament as
  gain-dim **parameters**, never outcome-named presets; relationships **emerge**.
- **Control rail** drives the sim only (transport/spawn/population/library/session) — "nothing here
  inspects or edits the organism." The deprecated temperament-preset dropdown was **removed** (a
  disposition is measured, never selected).

> `[VERIFY]` **The throttle panel / scan controller is NOT yet exposed in the live server or UI.** There
> is no `/scan` or `/throttle` endpoint, no throttle `cmd`, and no Scan/Throttle tab — consistent with
> the "deferred UI-sync pass" (the study throttle panel, with the scan controller, is unwired). State
> this explicitly; do not imply the throttle panel is live. The scan controller is fully built and
> tested at the Python level; only its **UI surface** is deferred (and is part of the CU-study control
> surface, §8.3).
>
> `[VERIFY]` **Stale Panksepp remnants in the UI/world (comment/label level only, no behavioural
> coupling):** `ui/src/types.ts` still documents a `DRIVES` list as "the 7 Pankseppian primary
> systems" (but `PersonLive.drive` is a free string and `PersonDetail.systems` an open record — the
> runtime does not depend on the 7-name list); `world.py` comments call emergent actions "Panksepp
> behaviours." Candidates for the deferred label-cleanup pass; flag so they are not read as the live
> engine.

---

## 6. The honesty wall (structural guarantees + how each is tested)

The honesty wall is **load-bearing and structural** — enforced by architecture and tests, not by
discipline alone. Enumerated:

| # | Guarantee | Where enforced | How tested |
|---|---|---|---|
| G1 | **Plasticity rules are meaning-blind** (see only local activity/weight/age; never that a circuit is "fear" or a state "threat") | `plasticity.py` — every function's args are numeric | `test_substrate_learning.py`, `test_engine.py`; code review that no branch keys on identity |
| G2 | **Neuromodulators are circuit OUTPUTS, not set scalars** (R5 modulator = a source circuit's live activity) | `engine.neuromod_output`; `plasticity.consolidate` cannot fetch/set the modulator | `test_serotonin_regulation.py`, `test_substrate.py`; DA/satiety state-dependence emerges (OBS-2) |
| G3 | **Edge signs are receptor-derived** (pharmacology table); a dishonest flip requires citing a false receptor | `params.RECEPTOR_SIGN`, `model._receptor_sign` | `test_substrate.py`; v12a re-sign produced exactly 3 flips, golden 0-classification-flips |
| G4 | **Read-outs are descriptive, attach NO verdict**, and are never fed back (freeze/restore) | `readout.py`, `observer.py` | `test_neural_readonly.py`, `test_observer*.py`; executive trajectory byte-identical with/without self-reflection |
| G5 | **Provenance is validated** — a scan result stamps the *live* substrate version; field data requires `not_used_in_calibration` | `scan.develop_and_measure`, `scan_match.load_field_pattern` | `test_scan*.py`, `test_scan_match.py` |
| G6 | **Found-not-fitted** — the search never writes the model (byte-unchanged); no drawn-target objective slot | `scan.py` (only channel = `set_throttle`) | `test_scan.py` asserts model byte-unchanged across a run |
| G7 | **Two-switch gated activation** — structure exists in full; activation is a gated subset (`developmental_online` = biology, `calibration_active` = tuning) | `engine._refresh_live` | `test_substrate.py`, phenomena battery age curves |
| G8 | **Additive, byte-identical lineage** — each seed version additive/sign-only; prior topology byte-identical; guarded edges (e.g. `CeA→PAG/HYPdm` inhibition) unchanged | seed archival + `model.py` | `test_aggression_pathway.py` guards `CeA→PAG/HYPdm`; golden characterisation tests catch any topology drift |
| G9 | **No outcome categories as causal primitives** — the Panksepp drive engine and coded outcome-category network were removed; categories live only as observer read-outs | `drives.py` / `executive.py` deleted | `test_characterisation.py` golden reframed; grep-clean of category names as primitives |
| G10 | **Bank: grown-and-banked / restored-never-edited** — no path assigns adult weights directly | `agent_bank.py` | `test_agent_bank.py` |

**Meta-principles the wall enforces** (from `MEMORY` / `CORE_RECORD`): outcomes **emerge and are
measured, never coded**; never cherry-pick anatomy by sign (inhibition is kept because it *exists*);
a measured result is only as trustworthy as its sign convention (re-derive on re-sign, retire old
findings); instability is a diagnostic of missing inhibitory anatomy (add the cited element, never
rebalance a real edge); never remove real anatomy unilaterally (explicit permission + design session,
asked before acting; commit a checkpoint at every step).

---

## 7. Determinism / reproducibility + testing

- **Zero third-party deps for the simulation core** — Python standard library only (`pyproject.toml`);
  the UI build needs Node, but the Python sim does not.
- **Deterministic by seed** — situation streams, temperament sampling, physical draws and Arena runs
  flow from explicit RNG seeds (`situation_seed`, `world_seed`, Arena `seed`); the controlled-
  experiment mode grows an identical **fixed background** cohort so any shift is attributable to the
  manipulation alone.
- **Golden characterisation tests** — a normalised read-out "golden" catches any topology/sign drift;
  each seed bump regenerates it and records the shape of the change (leaves, max |Δ|, classification
  flips), so a silent change fails the suite ("the golden moving is the system telling the truth").
- **Test suite** — **529 tests collected** across **63 test files** (`tests/`); the record cites the
  v13 full suite at 518 green. `[VERIFY]` exact pass/skip split not re-run here — recommend
  `python -m pytest -q` for the current count (skips are honestly-marked obsolete verdict-asserting
  tests). Coverage spans substrate (engine/plasticity/divergence/behaviour/social/phenomena battery/
  serotonin regulation/params-seed reconciliation), affective engine (endowment/interocept/observer/
  learning), instruments (arena/arena_view/scan/scan_match/scan_search/agent_bank/parallel_world), and
  world/UI (townlife/timeline/matrices/neural read-only).
- **Params ← seed reconciliation is guarded** (`test_params_seed_reconciliation.py`): the substrate
  reads every per-circuit parameter from the seed; `params.py` holds only code-side dynamics scaffold;
  the representation cannot silently drift.
- **Save/load** of a whole running world is a Python pickle + JSON sidecar — complete and faithful but
  code-version-bound (a research tool, not a long-term archive format).

---

## 8. Status and roadmap

### 8.1 The organism is FROZEN at v13
Per `docs/Outstanding_Register` §5: **organism changes are frozen after 2.1b (v13)**. No further seed
versions before the study without an explicit re-opening. Done and on `origin/main`: the complete core
organism (substrate + four matrices + 1/n plasticity + behaviour selection); the legacy Panksepp
engine fully retired; coded outcome-categories removed as primitives; the 5/5 emergent-phenomena
battery; the full instrument suite (bank, parallel harness, Arena, scan controller); the v9→v13 seed
lineage; and the UI console (Phases 0–8 + accessibility).

### 8.2 The three deliberate future substrate passes (recorded, post-study)
Created by the v13 pass, deliberately scheduled **after** the study (not gaps, not drift —
`Outstanding_Register` §2.1b):
1. **Systematic cortical-E/I pass** — the other cortical pyramidal circuits (dmPFC, OFC, dACC, …) also
   lack their local PV/SST interneurons (their current afferent balance masks it); add the real
   interneurons as a grounded, reviewed batch. Any afferent change to a masked cortical circuit must
   re-check for saturation.
2. **Adolescent-risk maturation** — whether to wire a **delayed** PFC-interneuron developmental
   trajectory (immature prefrontal control in an adolescent window). The adult substrate already
   produces the adolescent-risk inverted-U, so this is a refinement to test, not a gap.
3. **Proactive inhibitory-interneuron audit** — two passes each surfaced a saturating circuit missing
   its inhibitory partner (long-range excitation is well-represented, local inhibition under-
   represented); a deliberate systematic audit is warranted **after the study**.

Also parked (`Outstanding_Register` §4, promote only by explicit decision): median raphe (MRN) node;
the deferred `DRN→VTA` sign and `PFC→DRN` loop; connection-level throttling; the bank version-stamp;
development peer-perception pathway; PH-AGILITY/PH-SENSORY as bearer capacities; real held-out
field-data patterns.

### 8.3 The CU study — a separate downstream instrument, gated on §9
The callous-unemotional study is **not** part of the core organism; it is a downstream control surface
(`docs/PsychSim_CU_Study_Spec.md`) that turns the finished instrument suite into a conducted
experiment. Design highlights:
- The **backtester IS the scan controller** applied to a CU objective — **no new tool** (it inherits
  every structural guard: measured-signature-or-held-out objective, no drawn target, `set_throttle`-
  only, coarse-to-fine, viable-first, `candidate_hypothesis` never `finding`).
- A **validated CU seed** is a *discovered* throttle configuration + a family/environment context,
  applied to a **standard newborn** developed to target age (~18) — never a pre-grown or hand-authored
  agent; the name (`CU-Profile-A`) records **what it was proven to do**, and provenance travels with
  it (`corroboration: false`; a seed never self-certifies). It **replaces** the deprecated `fearless`
  temperament preset (a temperament is an input; CU is an outcome — naming a preset after an outcome
  presupposes the answer).
- **Family/SES variables enter as perturbation-pattern distributions, never coded effects** — whether
  the environment interacts with the throttle to shape CU must **emerge and be measured**.
- **5-HT / sign-upgrade dependency:** any CU seed validated before the sign upgrade (2.1a) and the DRN
  node (2.1b) must carry `aggression_regulation: provisional`. Since both landed in v13, the apparatus
  can now be built and aggression-regulation findings can be non-provisional once re-validated.

**Gate:** the CU surface is **pending the four open research-design questions in §9 of the CU spec**
(the CU signature set; the held-out clinical CU profiles; the full family/environment variable set and
each one's perturbation definition; the target-age default and assessment battery). These are
researcher decisions to be made **before** build, not unilaterally.

### 8.4 The finish line
`Outstanding_Register` §5: complete the CU-study apparatus on complete regulatory anatomy, **then run
the study** — and the build is complete. Resist "one more system" unless it is genuinely identified as
missing and promoted deliberately.

---

## Appendix A — key file map

| Concern | Files |
|---|---|
| Seed (source of truth) | `docs/neuralnetworks/psychsim_substrate_seed_v13.json` |
| Substrate loader / dynamics / plasticity / params | `core/substrate/{model,engine,plasticity,params}.py` |
| Behaviour selection / read-out | `core/substrate/{social,behaviour,readout}.py` |
| Agent / development / body / observer | `core/affective_engine/{agent,development,endowment,physical,interocept,observer}.py` |
| Instruments | `core/{arena,arena_view,scan,scan_match,scan_search,agent_bank,parallel_world}.py` |
| Study extension | `extensions/sophropathy/{module,engine,society,world}.py` |
| Live console | `psychsim_server.py`, `ui/src/**` |
| Authoritative records | `docs/PsychSim_CORE_RECORD.md`, `docs/PsychSim_Outstanding_Register.md`, `docs/PsychSim_CU_Study_Spec.md` |
| Stale-for-the-mind (world layer only) | `docs/ARCHITECTURE.md`, `docs/PsychSim_ARCHITECTURE.md`, `docs/PsychSim_Handover.md` §3.1–3.2 |

## Appendix B — known documentation/code drift + open verification items

Kept visible, not hidden (the same honesty the spec describes). **None affects the organism's
behaviour** — they are prose/label drift (stale in-code counts, retired-engine comments), deferred
UI, and draft-coverage notes. Several are already tracked: the stale `ARCHITECTURE.md` pair (item
alongside #1) and the Arena trace-extension (#7) are recorded in `Outstanding_Register.md`.

1. Stale in-code counts (`substrate/__init__.py` "73/159", `engine.py`/`NEUROMOD_SOURCE` "v7";
   `meta.supersedes` "v8") vs the loaded v13 artefact (82/206).
2. "Oja" is R8 `normalise_incoming`, not a separate rule; `maturation()` feeds behaviour selection, not
   the substrate loop.
3. Seed `assembly_status.how_value_enters` names 3 innate links; the seed flags 21
   `is_innate_reinforcer_link` edges (prose stale vs data).
4. 5-HT registered as a gate source but no edge is 5HT-gated yet (direct projections only).
5. `development.py` doc/code drift (retired plasticity prose + dead constants/helpers; `graded` dead;
   `live_stimulus` unreachable dead code).
6. `observer.instrumental_aggression` hard-set 0.0 (known read-out gap).
7. Arena UI spec promises live per-agent inspection that `arena_view` does not yet expose (trace-only).
8. Bank length-guard misses a sign-only version change (regrow-per-version mitigation; version-stamp
   deferred).
9. The throttle panel / scan controller UI is **not yet wired** (deferred UI-sync pass).
10. Stale Panksepp labels in `ui/src/types.ts` and `world.py` comments (label-level only).
11. Exact test pass/skip split not re-run (529 collected; record cites 518 green at v13).
12. Terminology: "circuit-breaker/throttle" = core `set_throttle`/scan controller, not
    `sophropathy/module.py`.
13. `sophropathy/{stages,lived,report,townlife,timeline_driver,library,viz_bridge}.py` not individually
    read for this draft.
