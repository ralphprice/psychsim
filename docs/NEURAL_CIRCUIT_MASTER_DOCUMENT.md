# Master Document — Neural Pathway / Network Model of the Human Mind

**Companion to `neural_circuit_model.json` (version `consolidated_pass1-4`)**

This document explains what the model is, how the single data file is structured, what each part means, how the parts fit together into a model of the mind, and how to use and extend it. It is the human-readable counterpart to the machine-readable JSON: the JSON is what you *load*; this is what tells you what you loaded and why it is shaped the way it is.

At a glance, the current model contains **97 circuits across 21 functional domains, 46 behavioural states, 320 state→circuit co-activation edges (187 established / 133 emerging), and 59 developmental-parameter rows** — all in one file.

---

## 1. What this model is (and is not)

**What it is.** A structured, machine-readable synthesis of documented human neural circuitry, organised so that a program can reason over it. It answers three questions in a connected way:

1. *What are the parts?* — a registry of neural circuits (nuclei/regions + the projections between them, their transmitters, and their function).
2. *How do the parts combine into behaviour?* — a co-activation table stating, for each behavioural state, which circuits drive it, modulate it, or are inhibited.
3. *How is the whole thing built and how does it change?* — a developmental/plasticity layer giving per-circuit onset, maturation, pruning, and plasticity rules.

Sitting above these is a fourth conceptual layer — the **large-scale networks** (default-mode, salience, frontoparietal, etc.) that the circuits compose into — which is described here and referenced throughout the data via each circuit's role.

**What it is not.** It is **not a complete map of the mind** — no such map exists, and the model says so explicitly and repeatedly. It is **not a set of measurements**: the co-activation weights are a qualitative expert-consensus scaffold, not empirical effect sizes or connectivity coefficients. And it is **not (yet) a dynamical system**: it is a *static* co-activation model — it tells you *which* circuits engage in a state, not the millisecond timing, sequence, or oscillatory coupling between them. Treat it as a well-organised substrate to reason over, prototype with, and progressively replace with measured values — not as ground truth.

---

## 2. Design philosophy and grounding frameworks

The model is deliberately layered from the innate and well-established outward to the derived and contested. It is scaffolded on five established frameworks so that it inherits their structure rather than inventing an idiosyncratic one:

- **RDoC (NIMH Research Domain Criteria)** — supplies the top-level organisation. Its six domains (Negative Valence, Positive Valence, Cognitive, Social, Arousal/Regulatory, Sensorimotor) and their constructs are the spine that maps behaviour to circuitry. Every circuit carries an RDoC mapping where one applies.
- **Panksepp's primary-process affective systems** (SEEKING, RAGE, FEAR, LUST, CARE, PANIC/GRIEF, PLAY) — the model of the *innate starting circuitry* the system develops from. The affective/motivational circuits are annotated with the Panksepp system they realise.
- **Cortico-striato-thalamo-cortical (CSTC) parallel loops** — the recurring motor/associative/limbic loop architecture that recurs across motor control, reward, and executive function.
- **Triple-network model + canonical resting-state networks** — the aggregation layer: how circuits compose into large-scale networks and how the system switches between them.
- **Hebbian plasticity + experience-expectant/experience-dependent development + critical-period biology** — the engine that builds the circuit set across the lifespan and makes it *evolve*.

The organising intuition: **innate subcortical/limbic circuitry comes online first and is largely hard-wired; cortical and especially prefrontal circuitry matures last and is shaped by experience; behaviour is the co-activation of these circuits; and individual minds diverge from shared starting circuitry through the interaction of genetic gains and experiential history within developmental windows.**

---

## 3. The epistemic framework

Because a truly complete, certain map does not exist, every claim is tagged, and the tags are load-bearing — you can and should filter the model by them.

- **Confidence tags** — `E` (established), `Em` (emerging), `H` (hypothesised). Applied per circuit *and* per co-activation edge. Of the 320 edges, 187 are `E` and 133 are `Em`. This lets you run the model in "established-only" mode versus "established + emerging" mode and see how much of a result depends on softer evidence.
- **Human vs animal evidence** — each circuit's `evidence_base` records whether it rests on human data, human+animal, or is animal-dominant. This matters enormously in places: e.g. oxytocin/affiliation circuitry is `animal_dominant` (strong in voles; weak and inconsistent in human intranasal-oxytocin studies), so any conclusion leaning on it should be treated cautiously.
- **Contested points are flagged, not hidden.** The `meta.key_caveats` list records the places where the field genuinely disagrees or where a textbook claim has been overturned — for example: the "mirror" system exists but its role in *action understanding* is disputed; the classical Broca–Wernicke language model is superseded by the dual-stream model; the cortical "pain matrix" is a body-salience system rather than pain-specific; polyvagal theory's core premises are widely regarded as refuted; working-memory maintenance mechanism (persistent vs activity-silent vs oscillatory) is unresolved; and the rostro-caudal PFC hierarchy's apex is disputed.
- **Weights are a scaffold, not measurements.** The `+2/+1/0/−1/−2` values encode qualitative roles (drive/modulate/none/inhibit), not measured coupling. `meta.weights_are` says this in the file itself.

The discipline throughout has been: populate what is documented, mark the frontier honestly, and never fabricate a connection to appear complete.

---

## 4. The file: structure of `neural_circuit_model.json`

The file has five top-level keys.

### 4.1 `meta`
Self-describing header. Contains the version, a note that this file supersedes all earlier per-format files, the **`terminology_note`** (the state→circuit structure is the *co-activation table*, not a "matrix"), the **`weight_legend`** and **`confidence_legend`**, the statement that weights are a qualitative scaffold, and the **`key_caveats`** array. Read `meta` first — it makes the rest of the file interpretable without external documentation.

### 4.2 `circuits`
The registry index: an object keyed by circuit ID, each value giving `name`, `domain`, `confidence`, and `evidence_base`. This is the compact machine form of the full registry (the rich per-field registry — nodes, projections, transmitters, developmental notes — lives in the conversation/registry tables; the JSON keeps the index so the file is self-contained). 97 entries across 21 domains.

Example:
```json
"THREAT-01": {
  "name": "Amygdala acute-threat (fear)",
  "domain": "defensive_threat",
  "confidence": "E",
  "evidence_base": "human+animal"
}
```

### 4.3 `states`
A flat list of the 46 behavioural states/events the co-activation table is defined over — e.g. `acute_threat`, `reward_anticipation`, `focused_external_attention`, `rest_mind_wandering`, `speech_production`, `multistep_planning`, `acute_pain`, `hunger_energy_deficit`.

### 4.4 `coactivation`
The core of the model: a **tidy edge list**. Each element is one (state, circuit) engagement:
```json
{ "state": "acute_threat", "circuit_id": "AROU-01",
  "role": "drive", "weight": 2, "confidence": "E" }
```
- `weight` ∈ {`+2` drive, `+1` modulate, `−1` inhibit-mild, `−2` inhibit-strong}. A missing (state, circuit) pair means weight 0 (not consistently engaged, or unknown) — the list is intentionally sparse.
- `role` is the human-readable label for the weight.
- `confidence` is per-edge — the softest and most important field for interpretation.

This edge-list form was chosen over a dense grid because it (a) attaches a confidence tag to every individual engagement, (b) is trivial to filter and pivot, and (c) does not waste space on the many zero cells. It pivots to a states×circuits grid in one line (see §7).

### 4.5 `developmental_parameters`
A list of per-circuit rows, each with: `onset_approx`, `peak_or_milestone`, `functional_maturation`, `pruning_window`, `myelination_timing`, `sensitive_period_gates` (what window opens/closes and what it gates), `plasticity_type` (`EE` experience-expectant / `ED` experience-dependent / both), `plasticity_coeff_qualitative` (how plastic, and when), `confidence`, and `evidence_base`. 59 rows. This is the "engine" that lets the model be run forward across a lifespan.

---

## 5. The four conceptual layers, explained

### 5.1 Circuit registry — the parts list
A "circuit" here is a functional unit defined by its **anatomical nodes and the directed projections between them**, its **principal transmitters/neuromodulators**, and the **function/behaviour** it supports. IDs follow a readable domain-prefixed scheme: `THREAT-`, `REW-`, `STR-`, `AFF-`, `EXEC-`, `AROU-`, `INT-`, `MEM-`, `CSTC-`, `ATT-`, `SOC-`, `WM-`, `VIS-/AUD-/SOM-`, `LANG-`, `MOT-`, `AUT-/SYM-/PAR-`, `ENDO-`, `PAIN-`, `ENS-`, `PFC-/TRACT-`. The 21 domains span the affective/motivational core, the regulatory and arousal systems, the cognitive systems, the sensory and motor hierarchies, and the autonomic/neuroendocrine/pain/enteric periphery, plus the frontal executive architecture and its white-matter tracts.

Two structural notes: some circuits are **cross-referenced aliases** (e.g. the dorsolateral-PFC node `PFC-DL` is the same substrate as the working-memory/control circuit `EXEC-01`; the frontal eye fields `FEF-01` = the dorsal-attention node `DAN-01`) — the registry records the anatomical node and the functional circuit both, noting the identity, rather than pretending they are separate systems. And the **white-matter tracts** (`TRACT-SLF`, `TRACT-CING`, `TRACT-UNC`, `TRACT-FAT`, `TRACT-FS`) are listed as structural substrate but carry **no co-activation weight** — they are the wiring, not a state-engaged node.

### 5.2 Co-activation table — the wiring of behaviour
This is where circuits become mind. For each state, the table names the **driving** circuits (what produces the state), the **modulating** circuits (what supports/shapes it), and the **inhibited** circuits (what is suppressed). Read a state by filtering the edge list to that state and sorting by weight.

The single most important interpretive caution: **these are co-activation roles, not causal or temporal claims.** `acute_threat` driving both the amygdala (`THREAT-01`) and the periaqueductal grey (`THREAT-03`) says they are jointly engaged in that state with those roles — not that one causes the other, and not in what order. Use the weights as priors over engagement, to be refined by data.

### 5.3 Network aggregation — the large-scale organisation
Circuits compose into the brain's canonical large-scale networks. The model's placements:

| Network | Constituent circuits (representative) | Role |
|---|---|---|
| Default-mode (DMN) | `DMN-01`, `MEM-01/03`, `SOC-01` (mentalizing), `PFC-VM` | Internally-directed thought, autobiographical memory, prospection, mentalizing |
| Salience (SN) | `INT-02`, `INT-01`, `THREAT-01`, ventral striatum | Detects salient events; proposed switch between internal and external modes |
| Frontoparietal / central-executive | `EXEC-01/02/04`, `CSTC-ASSOC`, `PFC-DL` | Externally-directed control, working memory, decisions |
| Dorsal attention | `DAN-01`/`ATT-01`, `FEF-01`, `VIS-02` | Top-down spatial/feature attention |
| Ventral attention | `VAN-01`/`ATT-02` | Bottom-up reorienting (overlaps salience) |
| Sensorimotor | `MOT-01/02/03`, `SOM-01` | Movement execution + somatosensation |
| Visual / Auditory | `VIS-01/02`, `AUD-01` | Sensory processing (two-stream organisation) |
| Language | `LANG-01/02` | Dorsal production + ventral comprehension |
| Limbic | `THREAT-*`, `REW-04`, `AFF-01`, `MEM-01` | Emotion, valuation, memory, affiliation |

The key dynamic is the **triple-network model**: the salience network (anterior insula + dorsal anterior cingulate) is proposed to toggle the system between the default-mode network (internal focus) and the central-executive network (external focus), which are broadly anticorrelated. The **cerebellum** (`MOT-04/05`) is treated not as a resting-state cortical network but as a domain-general modulator/forward-model layer attached to all of them via closed cortico-cerebellar loops. Where network boundaries are contested (salience vs ventral-attention; the low-signal limbic network; 7-vs-17 parcellation granularity), this is noted.

### 5.4 Developmental / plasticity engine — how it is built and evolves
This layer is what makes the model a model of a *developing* mind rather than a static adult snapshot. It encodes, as per-circuit parameters, eight rules:

1. **Maturational sequence** — brainstem/arousal and limbic first; sensory/motor next; association and prefrontal last; within the frontal lobe, back-to-front, with frontopolar cortex (`PFC-FP`) and the uncinate tract (`TRACT-UNC`) among the very last to mature (into the 20s–30s).
2. **The "mid-20s" figure is a soft asymptote, not a switch** — prolonged prefrontal maturation is real, but the popular "brain matures at 25" claim is an oversimplification; model it as a growth curve asymptoting across the early-to-mid-20s with wide variance, not a step.
3. **Synaptic overproduction then activity-dependent pruning, region by region** — each area overshoots synapses then prunes on its own schedule (visual cortex peaks in infancy; prefrontal pruning continues into the third decade).
4. **Pruning mechanism** — microglial/complement-tagged elimination, strong in early childhood but (contrary to a popular story) not the dominant driver of *normal* adolescent prefrontal pruning.
5. **Hebbian wiring** — co-active inputs strengthen, uncorrelated inputs prune; split into experience-expectant (waits for species-typical input in a window) and experience-dependent (encodes idiosyncratic experience lifelong).
6. **Critical/sensitive periods are opened and closed by inhibition** — parvalbumin-interneuron maturation opens a window; perineuronal nets close it as a molecular brake; windows are in principle re-openable. The clearest windows: vision/amblyopia (to ~7–8y), native phonology (first year), first-language grammar (to ~puberty, graded), face processing, HPG organisation, thyroid-dependent early brain maturation.
7. **Adolescent limbic–prefrontal reorganisation** — the reward/socioemotional system matures earlier than the cognitive-control system, producing a transient window of heightened reward-seeking with immature control (the dual-systems account — a strong heuristic, but its link to real-world risk is contested).
8. **Genetics × experience → divergence** — genetic variants set gains on transmitter systems; experience writes history into synaptic weights within each circuit's windows; identical starting circuitry thereby diverges into distinct individuals.

---

## 6. How the layers connect — worked examples

**Trace `acute_threat`.** Filter the co-activation table to this state: it *drives* the amygdala (`THREAT-01`), periaqueductal grey (`THREAT-03`), locus-coeruleus noradrenaline (`AROU-01`), and sympathetic output (`SYM-01`); *modulates* the HPA axis, salience node, and threat-context memory; and *inhibits* the default-mode network and (under high arousal) deliberative prefrontal control. Now cross to the network layer: this is the salience/limbic system seizing control and suppressing the default-mode network. Now cross to the developmental layer: the driving circuits (`THREAT-01/03`, `AROU-01`, `SYM-01`) are early-maturing and largely hard-wired (`EE`, low plasticity), whereas the regulating circuit (`THREAT-04`, vmPFC extinction) matures late — which is exactly why threat regulation is weak in childhood and adolescence. One query touches all three layers.

**Trace `reading`.** It *drives* the visual ventral stream (`VIS-01`, including the visual word-form area) and the ventral language stream (`LANG-02`, meaning), with the dorsal language stream (`LANG-01`, grapheme–phoneme) and attention/eye-movement circuits modulating. Developmentally, reading is a *cultural* skill with no innate circuit — it recycles the experience-expectant visual system and the language system through experience-dependent learning, which is why it has no critical-period entry of its own but depends on the sensory/language windows that do.

**See development change a state.** The same `reward_anticipation` state engages the same circuits at any age, but the developmental layer tells you the *gains* differ: `REW-01` (mesolimbic dopamine) carries a high adolescent plasticity coefficient and peak striatal dopamine, while `EXEC-01` (control) is still maturing — so the identical co-activation profile produces more reward-driven behaviour in an adolescent than in an adult. The model captures individual and developmental variation not by changing the wiring but by changing the parameters on it.

---

## 7. Using and extending the model

**Load and inspect (Python):**
```python
import json, collections
m = json.load(open("neural_circuit_model.json"))
edges = m["coactivation"]                 # 320 edges
circuits = m["circuits"]                  # 97 circuits
```

**Read one state (drivers first):**
```python
s = [e for e in edges if e["state"] == "acute_threat"]
for e in sorted(s, key=lambda x: -x["weight"]):
    print(e["weight"], e["role"], e["circuit_id"], e["confidence"])
```

**Run "established-only" vs "with emerging":**
```python
strong = [e for e in edges if e["confidence"] == "E"]      # 187 edges
allev  = edges                                              # 320 edges
```
Comparing results across these two sets shows how much a conclusion leans on softer evidence — the intended use of the per-edge confidence tags.

**Pivot the edge list to a states×circuits grid** (if you want the dense form):
```python
import pandas as pd
df = pd.DataFrame(edges)
grid = df.pivot_table(index="state", columns="circuit_id",
                      values="weight", fill_value=0)
```

**Weight a state by evidence quality** (e.g. down-weight emerging edges):
```python
w = {"E": 1.0, "Em": 0.5, "H": 0.25}
score = {c: 0 for c in circuits}
for e in s:
    score[e["circuit_id"]] += e["weight"] * w[e["confidence"]]
```

**Extend it.** New content slots into the same schema without restructuring: add a circuit to `circuits`, add its edges to `coactivation` (with per-edge confidence), and add a row to `developmental_parameters`. Keep everything in this one file. Do not reintroduce parallel copies in multiple formats — the edge list pivots to any shape you need.

---

## 8. Coverage, frontier, and honest limitations

**Covered.** All six RDoC domains at circuit level — Negative Valence, Positive Valence, Cognitive (attention, working memory, executive control, language, perception, declarative memory), Social, Arousal/Regulatory, Sensorimotor — plus the autonomic, neuroendocrine, pain, and enteric systems, and the frontal executive architecture with its white-matter tracts. The model is structurally complete against RDoC.

**The frontier (honestly).**
- **Temporal dynamics** — the single biggest gap. This is a static co-activation table; it has no timing, sequence, oscillatory coupling, or state-transition rules. Adding a dynamical layer (per-circuit time constants + a state-transition structure) is what would let the model be *simulated* over time rather than queried state-by-state.
- **Quantitative grounding** — the weights and plasticity coefficients are qualitative priors; replacing them with measured values (from developmental cohorts, connectomics, causal perturbation) is the path from scaffold to instrument.
- **Remaining content gaps** — gustation and the vestibular system; the neuroimmune axis; a deeper pain taxonomy (RDoC has no pain construct); receptor-subtype and glial spatial detail.
- **Structural humility** — circuit boundaries, network definitions, and developmental timings are all disputed in places; the model records the competing views rather than resolving them. Several affiliation/Panksepp anatomies rest on animal work; treat human node-level detail there as uncertain.

The model is best understood as a **living scaffold**: comprehensive in coverage, explicit about confidence, honest about the frontier — a substrate for reasoning about the architecture of mind, not a finished theory of it.

---

## Appendix — quick reference

**Domains (21):** defensive_threat, reward_motivation, stress, affiliation, executive_control, executive_frontal, frontal_tract, arousal_regulatory, interoception, episodic_memory, cstc_scaffold, attention, social_cognition, working_memory, sensory, language, motor, autonomic, neuroendocrine, pain, enteric.

**Weight legend:** `+2` drive · `+1` modulate · `0`/absent none-or-unknown · `−1` inhibit (mild) · `−2` inhibit (strong).

**Confidence legend:** `E` established · `Em` emerging · `H` hypothesised.

**Grounding frameworks:** RDoC (organisation) · Panksepp primary-process systems (innate starting circuitry) · CSTC parallel loops (recurring loop architecture) · triple-network + canonical resting-state networks (aggregation) · Hebbian/experience-expectant-vs-dependent/critical-period biology (developmental engine).

**Current totals:** 97 circuits · 21 domains · 46 states · 320 co-activation edges (187 `E` / 133 `Em`) · 59 developmental-parameter rows · 1 file.
