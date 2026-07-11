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

## 8. v11 outcome — all four added with honest signs (the sign-correction)

**Ruling: Option A — add all four edges with their honest `_sign()`-derived neurochemical signs, weights
SCAFFOLD, and measure whatever emerges. Cherry-pick nothing; override no sign.** All four were authorised
(existence + direction); the sign is *not* something anyone authorises — it emerges from the source's
principal transmitter, and the behaviour is whatever results.

**A correction to §5's framing, recorded so it is not repeated.** During the v11 pre-build I read the
*rationale* for why each edge exists ("MeA→VMHvl is the route by which a conspecific cue reaches the attack
area") as an *authorised excitatory function*, found that our convention signs MeA→VMHvl and VP→LHb
**inhibitory** (both are GABA-leading), and proposed deferring those two ("add only the sign-compatible
pair"). **That was cherry-picking** — selecting the neurochemistry whose emergent sign matched the story we
expected, which is the same move as hand-setting a sign, done by omission. There is no authorised sign; a
model that keeps only the excitatory edges that drive the studied outcome has *encoded* the outcome.
Inhibition is half the machine and is kept because it *exists*. Distinguish two things the earlier framing
collapsed: "the convention signs it opposite to what we wanted" = the model working (keep it); "the
convention signs it opposite to the literature's *projection-specific* transmitter" = a real fidelity
limitation to document (below).

**What went in (v11 = v10 + 4 edges; v10 connectome byte-identical):**

| Edge | Emergent sign (source transmitter) | Measured effect | 
|---|---|---|
| C1 MeA→VMHvl | **−1 inhibitory** (MeA GABA/glutamate → GABA-leading) | a conspecific cue **brakes** the attack area (drive MeA, no provocation → VMHvl 0.000). Biologically sensible — you don't attack every conspecific you see — and it can only *help* the neutral floor hold. A finding, kept. |
| C2 LH→LHb | +1 excitatory | **revives the previously afferent-less (dead) LHb**: aversion drive reaches the habenula, and LHb→RMTg⊣VTA now suppresses DA (isolated: LHb→VTA 0.000). |
| C3 VP→LHb | **−1 inhibitory** (VP GABAergic) | the reward/hedonic arm (VP→LHb 0.000). **Sign-fidelity limited — see below.** |
| C4 BNST→VMHvl | +1 excitatory | an extended-amygdala afferent now reaches the attack area (drive BNST → VMHvl 0.43), beyond the abstract provocation channel. |

**Integration guards (measured, nothing tuned):** the v9 aggression closure holds **unchanged**
(provocation→aggress, plain threat→avoid, neutral→restrain); DA is **stable** (resting VTA v11 0.077 ≈ v10
0.084 — bounded, no collapse/blowup); the characterisation golden moved by a **connectome-change shape**
(42 small leaves, max |Δ|=0.0047, **no classification flips**) and was regenerated.

**Documented sign-fidelity limitation (VP→LHb).** The nucleus-level `_sign()` (Dale-by-nucleus) signs
VP→LHb **inhibitory** because VP is GABA-leading; the literature's LHb-projecting VP population is
**glutamatergic/aversive**. Our single-sign-per-nucleus convention cannot represent a projection whose
specific transmitter differs from its source's dominant one. This is recorded in the seed's
`gaps_register` and is to be resolved **only** by a convention-wide upgrade to projection-specific signs
(uniform, cited) if ever undertaken — **never** by a per-edge override to obtain a function.

**The 5-HT node stays on the required list.** Recorded in `gaps_register`: no serotonergic (dorsal/median
raphe) source exists, and 5-HT is the principal aggression/impulsivity-regulating neuromodulator — so a
model missing it cannot honestly measure aggression regulation. A required future *node*-pass (grounded,
cited, reviewed), and **to be revisited before the CU study draws aggression-regulation conclusions.**

**Meta-lesson (the governing principle):** completeness includes the effects that work *against* the
phenomenon under study. We include every neurochemical effect we know of — inhibitory and excitatory
equally, whether or not it suits the hypothesis — and add missing systems (5-HT) as we learn of them. The
job is to build the machine as it is and report what it does.

### 8.1 Integration findings from the v11 full-suite gate (surfaced, not tuned away)

The first full suite after v11 surfaced six red tests. None were the connectome being wrong; each was the
system telling the truth about a v11 consequence. Recorded here because two are load-bearing:

- **Stale-cache under a connectome change (3 errors).** The committed background library
  (`library/adults.json`) held adults *grown under v10* — 154-length per-connection arrays — which
  IndexError'd deep in `step()` when restored into the 158-edge v11 model. This is the same class as the
  pre-v10 physical-neutral case: **a bank is stale when the connectome version that grew it differs from
  the one restoring it.** Fixed per the standing rule — **regrow the cache** (`build_default_library()`
  under v11) — and added a **defensive guard** in `_restore_engine`: a connection-count mismatch now raises
  a clear "stale bank, regrow" error instead of a cryptic IndexError. It never pads the missing edges
  (that would fabricate weights the adult never developed — restored-never-edited).

- **The E5/E6 neutral-floor changed basis: structural → behavioural (the load-bearing one).** E5/E6's
  neutral-floor guard held at v10 **by construction** — VMHvl's *only* input was `provocation`, so the
  reactivity gain had nothing to amplify at neutral. **v11 gives VMHvl afferents** (MeA→VMHvl inhibitory,
  BNST→VMHvl excitatory), so that structural guarantee is gone. Measured consequence: the floor **still
  holds behaviourally** — at neutral both a strong and a weak agent restrain (residual aggress drive ~0.003,
  far below threshold), and the provoked strong>weak differential is intact — but it now holds *because the
  neutral net afferent drive is negligible*, not *because there is nothing to amplify*. The false "by
  construction" claim was corrected in `physical.py`, `engine.py`, and the test (reframed to the behavioural
  invariant). **This is a genuine cross-version interaction: adding VMHvl afferents weakened an E5/E6
  honesty argument from structural to behavioural. Flagged for the design session.**

- **Formidability-perceiver (1 fail, intent intact).** Seeing a formidable other still drives the
  perceiver's defensive submission (CeA 0.67) and NOT attack — but VMHvl is now *suppressed below* baseline
  (0.00) by the inhibitory MeA→VMHvl brake, rather than sitting exactly at baseline. The v10 exact-baseline
  assertion was a numeric artifact; the invariant (defensive dominates, attack not driven up) is reasserted.

- **Seed-version string + the params↔seed reconciliation path** updated v10→v11 (mechanical).

---
*Sources consulted:*
[Nordman 2020 J Neurosci 40(25):4858](https://www.jneurosci.org/content/40/25/4858) ·
[VMHvl & aggression review PMC5770748](https://pmc.ncbi.nlm.nih.gov/articles/PMC5770748/) ·
[Hypothalamic–amygdala dimorphic aggression, Neuron 2024](https://www.cell.com/neuron/fulltext/S0896-6273(24)00457-4) ·
[LH→LHb escape, eLife 30697](https://elifesciences.org/articles/30697) ·
[LH→LHb vs VP→LHb, PMC5500222](https://pmc.ncbi.nlm.nih.gov/articles/PMC5500222/) ·
[VP→LHb depression, PubMed 32009492](https://pubmed.ncbi.nlm.nih.gov/32009492/) ·
[LHb value-guided behaviour review](https://www.sciencedirect.com/science/article/pii/S2211124724002961)
