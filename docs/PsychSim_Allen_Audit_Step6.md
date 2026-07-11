# PsychSim Step 6 — Allen connectivity audit: a CANDIDATE-CONNECTION LIST

**Status:** deliverable for authorisation. **This is NOT a v11 seed.** Nothing here is written into
`psychsim_substrate_seed_v10.json`. Each candidate below is a *separate, reviewable* decision; if any
are authorised they would batch into a *deliberate* v11 pass, and even then as existence+direction
only (weights stay SCAFFOLD). A **short or empty list is a legitimate outcome** — "v9/v10 subcortical
coverage is already adequate" is a systematic confirmation worth having, and the effort spent auditing
must not imply edges must be added.

## Discipline (the ruling this obeys)

1. **Candidate list, per edge, not a seed.** Existence + direction only.
2. **Weights stay scaffold.** The Allen Mouse Brain Connectivity Atlas gives *projection density* in the
   mouse — never a functional weight, and never a claim about the human brain.
3. **The per-edge human homology cross-check is the load-bearing, non-automatable step.** Mouse↔human
   subcortical homology is good but not perfect; a plausible-looking Allen projection is not a candidate
   until the homology judgment is made and recorded.
4. **The density cutoff is a recorded judgment that travels with the list** (§4), like `_SCREEN_DELTA`.

## Method

The seed carries each circuit's anatomy (`id`, `name`, `nodes`, `transmitters`, `evidence_base`) but no
CCF acronym. Step 1 maps all 78 circuits to their Allen CCF ontology region and a homology class (§2);
this **sizes the diff** — only STRONG×STRONG subcortical pairs can yield a candidate on Allen grounds.
Step 2 flags the boundary cases (§3). Step 3 checks canonical, well-established subcortical projections
(Allen + tract-tracing) against the current 154 circuit→circuit edges, keeping only those that pass the
cutoff (§4) and recording the homology cross-check per edge (§5). Node-level gaps (a missing *circuit*,
not an edge) are noted separately (§6) — they are out of scope for an edge audit.

## 2. CCF ontology mapping (the foundation) — homology tally: **STRONG 50 / BOUNDARY 14 / NONE 14**

Only the **50 STRONG** circuits (amygdala nuclei, hypothalamus, habenula, VTA/SNc, PAG, brainstem
autonomic/defensive, basal ganglia, thalamic relays, primary sensory) are structures where the Allen
mouse atlas translates securely to human. The full 78-row map (per circuit: CCF region, homology class,
note) is committed at `docs/neuralnetworks/ccf_ontology_map.json` — documentary, **not** part of the
substrate seed; the classification drives everything below.

## 3. Homology-boundary cases (flagged — Allen data weak or inapplicable)

**BOUNDARY (14)** — a rodent homolog exists but is imperfect; an Allen projection here needs an explicit
caveat and is *not* admitted as a candidate on mouse data alone:
- **Insula gradient** `pIns / mIns / aIns` (AIp/AI/AId-AIv) — the anterior granular insula is
  primate-elaborated; the posterior→anterior interoceptive gradient is only partially rodent-homologous.
- **`OFC`** (ORBl/ORBm) — rodent lacks granular OFC. **`vmPFC`** (ILA / infralimbic) and **`dmPFC`**
  (PL/ACAd) and **`dACC`** (ACAd) — the standard rodent homologs, but partial.
- **`VMpo-thal`** (interoceptive thalamus) — VMpo is largely primate-specific (Craig); no clean mouse row.
- **`SC-Pv`** — SC strong, but the pulvinar (LP) homolog is weak. **`RMTg`** — functionally defined; Allen
  labelling varies. **`preSMA`** (MOs/M2), **`S2-PPC`**, **`V-ventral`/`V-dorsal`** — association-level, partial.

**NONE (14)** — outside the Allen mouse atlas entirely: granular lateral PFC (`dlPFC`, `vlPFC`, `FPC`,
`FEF`), the whole **social-cognition domain** (`rSMG-TPJ`, `pSTS`, `PCun-PCC`, `ATL-TP` — human association
cortex), and peripheral/endocrine (`RET`, `COCH`, `IML`, `SympOut`, `Pituitary`, `AdrenalCortex`).

> Consequence: **no candidate below touches a BOUNDARY or NONE circuit.** Every candidate is STRONG×STRONG.

## 4. Density cutoff (recorded judgment — travels with the list)

An edge is admitted as a candidate only if **all** hold:
- (a) it is a **major / dense** projection in the Allen atlas or canonical tract-tracing — not a sparse or
  minor one;
- (b) **both endpoints are STRONG-homology circuits already in the model**;
- (c) it is **functionally relevant to a domain the model actively simulates** (threat/aggression,
  reward/aversion, affiliation, autonomic);
- (d) it is **genuinely absent** from the current connectome.

Edges failing any of (a)–(d) are listed sub-threshold (§5.1) with the reason. This is deliberately strict:
the failure mode to avoid is a plausible Allen row becoming a candidate on density alone.

## 5. Candidate edges

Existence + direction only; weights would be SCAFFOLD if ever authorised. "Density" is the mouse Allen
tier (qualitative). "Homology" is the per-edge human cross-check — the load-bearing judgment.

| # | Candidate edge | Domain | Allen density | Homology cross-check (mouse→human) | Why it may be missing / what it grounds |
|---|---|---|---|---|---|
| C1 | **MeA → VMHvl** | defensive / aggression | **High** (MeApd axons dense in VMHvl) | **STRONG** — MeA and VMHvl are among the most conserved social-behaviour nuclei; the conspecific-aggression circuit is documented across rodents and implicated in primates | VMHvl currently has `in=0` — it receives *only* the abstract `IN-INTERO:provocation` channel. **MeA→VMHvl is the anatomical afferent that channel abstracts**: the route by which conspecific/social cues reach the attack area. Present: MeA→VMH (general) and MeA→BNST; the *ventrolateral-specific* attack edge is absent. |
| C2 | **LH → LHb** | reward / aversion | **High** ("innervates almost-entirely the LHb") | **STRONG** — LHA and LHb are deeply conserved; the aversion/escape signal is a core diencephalic circuit | LHb currently has `in=0` — its aversion afferents are absent. LH→LHb is the major glutamatergic drive that reports aversive/escape value to the habenula (which then reaches VTA via the present LHb→RMTg→VTA disappointment path). |
| C3 | **VP → LHb** | reward / aversion | **Moderate–High** (separate GABA + Glu) | **STRONG** — ventral pallidum and habenula are conserved basal-forebrain/epithalamic structures | Complements C2: the pallidal-habenular route carrying reward-disappointment/aversion. VP currently projects only to VTA; the VP→LHb aversion arm is absent. |
| C4 *(secondary)* | **BNST → VMHvl** | defensive / aggression | **Moderate** | **STRONG** — extended-amygdala↔hypothalamus, conserved | Extended-amygdala modulation of the attack area; secondary to C1. Included as secondary because its density/dominance is lower than MeA→VMHvl. |

**Provenance for the cross-checks (sources consulted, mouse unless noted):**
- C1: Lin et al. 2011 *Nature* 470:221 (VMHvl aggression locus); Hashikawa et al. 2017 *Nat Neurosci*
  20:1580 (Esr1+ VMHvl, sex-differentiated); Nordman et al. 2020 *J Neurosci* 40(25):4858 (MeA→VMHvl
  potentiation drives aggression); Yang/Anderson review, *PMC5770748* (MeApd axons dense in VMHvl).
- C2: Lecca et al. 2017 *eLife* 30697 (LH→LHb drives escape); LH→LHb "innervates almost-entirely the
  LHb" / ethanol study *PMC5500222*.
- C3: Knowland et al. 2020 *PubMed 32009492* (VP→LHb glutamatergic, aversion/depression);
  Stephenson-Jones et al. 2016 *Nature* 539:289 (pallidal reward/aversion to habenula).
- C4: Lebow & Chen 2016 (BNST extended-amygdala); Nordman et al. 2020 (MeA/BNST→VMHvl aggression control).

### 5.1 Sub-threshold / excluded (audited, deliberately NOT candidates)

- **PBN → BNST** — established, STRONG homology, but functional relevance to the model's active domains is
  moderate (interoceptive→extended-amygdala); fails (c) at the current cutoff. Reconsider if an
  interoceptive-threat pathway is later built out.
- **CeA → PBN** (descending) — established, STRONG homology, but CeA's effector coverage in the model is
  already substantial (CeA→PAG/HYPdm/PVN/RVLM); marginal on (c).
- **LS (SEPT) → LHA / VTA** — the lateral septum is a rodent hub, but the specific functional relevance is
  diffuse; fails (a)/(c) as a *specific* dense functionally-scoped edge.
- **PAG → premotor / magnocellular reticular** — the freezing/motor output; the effector (e.g. Mc) is not
  a circuit in the model, so it fails (b) (no endpoint). Effector-boundary, not a gap.
- **DStr → SNr/GPi** — basal-ganglia output; SNr/GPi are not circuits in the model — effector boundary,
  fails (b).

## 6. Structural (node-level) observations — flagged, NOT proposed as edges

These are **missing circuits**, not missing edges, so they are out of scope for this audit and are recorded
only so the gap is visible. Each would be a much larger, separate v11 decision (a node + its whole
projection set), never folded in here:

- **No serotonergic source (dorsal/median raphe, 5-HT).** The model has NA (LC), DA (VTA/SNc), ACh
  (BF-ACh), OT (PVN-OT), CRF (PVN/BNST) — but **no 5-HT node**. Serotonin is a major modulator of
  aggression, mood, and impulse control, i.e. directly relevant to the sophropathy/CU question. This is the
  single most consequential *node-level* absence. **Flagged for consideration; not proposed.**
- Absent endpoints that would license further canonical projections: **entopeduncular / GPi** (a major LHb
  afferent), **ventral premammillary PMv** (a VMHvl afferent), **tuberomammillary / histamine**. Node-level.

## 7. Conclusion & recommendation

The subcortical connectome is **largely adequate**: across 50 STRONG-homology circuits and 154 edges, the
audit surfaces **three well-grounded candidate afferents (C1–C3) plus one secondary (C4)** — a short list,
concentrated in exactly two places where the current model uses an *abstraction* in lieu of the anatomical
afferent:
- the **attack area** (`VMHvl`), currently driven only by the `provocation` input-channel — C1 (and C4)
  would give it its conspecific-cue afferent;
- the **habenula** (`LHb`), currently with no afferents — C2/C3 would give it its aversion inputs.

**Recommendation:** treat C1 (MeA→VMHvl) and C2 (LH→LHb) as the two strongest candidates for a possible
v11 pass; C3 (VP→LHb) and C4 (BNST→VMHvl) as secondary. **But this is a list for authorisation, not a
seed** — I am not adding any edge. The largest real gap is node-level (no 5-HT, §6), which is deliberately
*not* on the candidate list because it is not an edge decision. If none are authorised, "coverage adequate,
one node-level flag recorded" is an honest and acceptable close to Step 6.

---
*Sources consulted:*
[Nordman 2020 J Neurosci 40(25):4858](https://www.jneurosci.org/content/40/25/4858) ·
[VMHvl & aggression review PMC5770748](https://pmc.ncbi.nlm.nih.gov/articles/PMC5770748/) ·
[Hypothalamic–amygdala dimorphic aggression, Neuron 2024](https://www.cell.com/neuron/fulltext/S0896-6273(24)00457-4) ·
[LH→LHb escape, eLife 30697](https://elifesciences.org/articles/30697) ·
[LH→LHb vs VP→LHb, PMC5500222](https://pmc.ncbi.nlm.nih.gov/articles/PMC5500222/) ·
[VP→LHb depression, PubMed 32009492](https://pubmed.ncbi.nlm.nih.gov/32009492/) ·
[LHb value-guided behaviour review](https://www.sciencedirect.com/science/article/pii/S2211124724002961)
