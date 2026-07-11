# PsychSim v12 — the serotonergic (dorsal raphe / 5-HT) node: DESIGN SPEC (for review)

**Status: design specification, for design-session review. NOTHING is built until this is reviewed AND
the sign-representation decision (§2) is ruled.** This closes the node-level gap recorded in v11's
`gaps_register` ("no serotonergic source; the principal aggression/impulsivity neuromodulator; revisit
before the CU study draws aggression-regulation conclusions"). Per the standing ruling, the CU-study
apparatus may be built in parallel; the study's **aggression-regulation** conclusions wait for this node.

Same discipline as v9/v10/v11: **existence + direction only, weights SCAFFOLD, emergent effects measured
not designed.** The one thing 5-HT must NOT be is coded as "5-HT → less aggression" — the dampening must
**emerge** from honestly-signed anatomy, or it means nothing.

---

## 1. Why a node, not an edge — and why it can't be skipped

Serotonin is the principal neuromodulator of impulsive/reactive aggression and impulse control — one of the
most robust findings in biological psychiatry (low central 5-HT function ↔ impulsive aggression; reduced
5-HT in PFC–amygdala circuits reduces top-down control over the amygdala–hypothalamus–PAG network). The
CU/psychopathy phenotype centrally involves this regulation. A substrate that has the *attack circuit*
(v9 VMHvl) and its *afferents* (v11 MeA/BNST→VMHvl) but **not its principal regulator** is anatomically
half-built for the study's purpose — and building the excitatory afferents while omitting the inhibitory
regulator would be cherry-picking-by-omission one level up. So the node goes in, with whatever it does.

A **node** (a circuit + its projection set + registration as a neuromodulator source) is a categorically
larger addition than an edge — hence its own spec, its own review, its own version (v12).

---

## 2. THE decision this spec exists to force: how to represent 5-HT's sign

**The problem, grounded.** 5-HT's excitatory/inhibitory effect is **receptor-determined and opposite across
targets**:
- On the **hypothalamic attack area** (VMHvl/anterior hypothalamus): **INHIBITORY** via **5-HT1A**
  (G-protein-gated K⁺ hyperpolarisation) — 5-HT *dampens* aggression there.
- On the **PFC controllers** (OFC/vmPFC/dACC): **EXCITATORY** via **5-HT2** — 5-HT *facilitates* the regions
  that inhibit aggression.

Both effects reduce aggression, **through opposite signs**. Our model derives each edge's sign from the
**source nucleus's principal transmitter** (`_sign()`), so every DR projection would be signed **`+1`
(excitatory)** — "serotonergic" is not GABA. That gets DR→PFC right and DR→attack-area **exactly wrong**
(exciting the very area 5-HT is known to inhibit, i.e. *increasing* aggression — the inverse of the reason
the node exists, and un-emergeable as dampening). **No single nucleus-level sign for DR can be honest.**

This is the VP→LHb sign-fidelity limitation (v11 `gaps_register`) brought to a head: there, one projection's
transmitter differed from its nucleus's; here, the *same* nucleus's projections have *opposite* functional
signs by receptor. The single-sign-per-nucleus convention is structurally inadequate for 5-HT.

**The options (a design-session ruling is required before build):**

- **(A) Sign all DR projections `+1` (keep the convention), measure.** *Rejected on its face for the
  aggression targets:* it encodes 5-HT as *exciting* the attack area, so the dampening cannot emerge — the
  substrate would say low-5-HT → *less* aggression, contradicting the robust literature. This is not
  "opposite to what we wanted" (which we'd keep); it is opposite to the measured biology, i.e. a fidelity
  failure, not a finding. Including it would make aggression-regulation conclusions *worse* than the
  pre-5-HT gap, not better.
- **(B) Register 5-HT only as a GATING neuromodulator (R5), no signed projections.** Add `"5HT": ["DR"]` to
  `NEUROMOD_SOURCE` and gate selected connections' *plasticity* with it. Sign-neutral (gating has no
  excit/inhib sign) — but the model's gating scales **plasticity/learning**, is **facilitatory**, and does
  not act on moment-to-moment drive. So it captures 5-HT's role in *learning* on gated pathways, **not** the
  acute aggression-dampening the node is for. A real but *different* aspect; insufficient alone.
- **(C) Convention-wide upgrade to projection/receptor-specific signs (RECOMMENDED).** Change `_sign()` from
  nucleus-level to **per-edge**, with each edge's sign taken from its projection-specific transmitter/receptor
  in the literature (uniform, cited — never hand-set to obtain a function). Then DR→VMHvl is 5-HT1A-inhibitory,
  DR→OFC is 5-HT2-excitatory, each because the biology says so. **This also fixes VP→LHb and any other
  mixed-nucleus edge at once** — the principled resolution flagged in v11. It is a *substantial, cited pass in
  its own right* (a schema `sign_basis`/receptor field per edge + re-deriving existing signs uniformly from
  the literature), so it likely **precedes or accompanies** the 5-HT node rather than being buried in it.
- **(D) Hybrid: (C) for the projections + (B)'s gating registration.** 5-HT both projects (receptor-signed
  edges) and gates plasticity — biologically both are true. Most complete; largest scope.

**Recommendation: (C) (optionally (D)).** The 5-HT node cannot be honestly added under the current
nucleus-sign convention, and the honest fix is the uniform receptor/projection-sign upgrade — which is
itself a reviewed, cited pass. **So the real sequencing question for the design session is: do the
sign-convention upgrade first (fixing VP→LHb and enabling honest 5-HT), then the 5-HT node?** I have built
nothing; this is the decision to rule.

> Everything in §3–§6 below is written **assuming (C)** — each projection carries its receptor-determined
> sign. Under any other ruling the projection table's signs change, but the anatomy (existence + direction)
> does not.

---

## 3. The node

- **DRN — dorsal raphe nucleus** (primary; the serotonergic source most implicated in aggression/impulsivity).
  `domain: neuromodulatory`; `transmitters: serotonergic (5-HT)`; slow tonic dynamics (a modulatory tau,
  SCAFFOLD). Registered in `NEUROMOD_SOURCE` as `"5HT": ["DRN"]` so 5-HT is available as an R5 gate too.
- **MnR — median raphe** (SECONDARY, **deferred**): more implicated in anxiety/hippocampal tone than
  aggression. Flagged as a possible later addition; **not** in this pass, to keep it focused.

---

## 4. Projections (existence + direction; signs per §2-C, receptor-cited)

Efferents from DRN (the "node + its projections"). SCAFFOLD weights; signs are the receptor-determined
sign, **documented per edge as neurochemistry, never chosen for a function**:

| Edge | Receptor → sign | Grounded role (measured, not coded) |
|---|---|---|
| DRN → **VMHvl** | 5-HT1A → **inhibitory** | dampens the hypothalamic attack area (5-HT in AH/VMH inhibits aggression) |
| DRN → **CeA** | 5-HT1A (dominant) → **inhibitory** | dampens central-amygdala threat/aggression output |
| DRN → **BA/BLA** | mixed (5-HT1A/2A) → **inhibitory (scaffold, flagged)** | modulates amygdala reactivity; net sign a flagged scaffold |
| DRN → **OFC** | 5-HT2 → **excitatory** | facilitates orbitofrontal inhibitory control over aggression |
| DRN → **vmPFC** | 5-HT2 → **excitatory** | facilitates ventromedial-PFC regulation |
| DRN → **dACC** | 5-HT2 → **excitatory** | facilitates conflict/again-control |
| DRN → **HPCv** | 5-HT1B → **inhibitory** | the DRN→ventral-hippocampus reactive-aggression pathway |
| DRN → **NAc-shell** | 5-HT (mixed) → **scaffold, flagged** | reward/impulsivity modulation |
| DRN → **PAG** | 5-HT (mixed) → **scaffold, flagged** | defensive/pain modulation |
| DRN → **VTA** | 5-HT (mixed) → **scaffold, flagged** | 5-HT↔DA interaction |

Afferents TO DRN (the regulation LOOP — top-down control of the raphe; without them 5-HT is unregulated):

| Edge | Sign | Role |
|---|---|---|
| **vmPFC → DRN** | excitatory | prefrontal top-down control of raphe output (the impulse-control loop) |
| **OFC → DRN** | excitatory | orbitofrontal drive onto raphe |
| **LHb → DRN** | excitatory | the habenula→raphe aversion/disappointment input (LHb↔DR loop) |

Each edge = one `innate_wiring_catalogue` entry with its citation; each `default_weight_basis: assumption`
(SCAFFOLD); each sign carries its receptor basis in the `source` note.

---

## 5. What must EMERGE (not be coded)

Under (C), the anatomy is: DRN **inhibits** the attack area (5-HT1A) **and excites** the PFC controllers
(5-HT2) **which inhibit** the attack area. So **high 5-HT → dampened aggression** (both routes) and **low
5-HT → disinhibited impulsive aggression** should **emerge** — never a coded `5HT → -aggression` weight.
The measurement (a v12 guard): a low-DRN-tone agent shows *more* provoked aggression / *less* restraint than
a high-DRN-tone agent, **as an emergent consequence** of the signed loop — and if it does not emerge, that is
a finding about the wiring/weights to surface, not to tune. The CU-relevant claim (5-HT hypofunction ↔ the
impulsive-aggression component of the phenotype) is then a `scan_match` target, never a built-in.

---

## 6. Versioning, guards, gaps

- **v12 = v11 + DRN node + its projections + `NEUROMOD_SOURCE["5HT"]`.** Additive; v11 connectome
  byte-identical. Archive v11.
- **Guards (measured, nothing tuned):** the v9 aggression closure must still hold; the v11 measurements
  (LHb revival, DA stability, the E5 neutral floor — now weight-dependent, re-checked) must still hold; and
  the emergent 5-HT/aggression dampening (§5) is the new measurement. The characterisation golden will move
  (a real connectome change) → inspect + regenerate. **Regrow the background library under v12** (a v11-grown
  bank is stale — the `_restore_engine` version-guard added in v11 will catch it).
- **`gaps_register` (v12):** MnR deferred; per-target receptor heterogeneity collapsed to one dominant sign
  per edge (SCAFFOLD, flagged — e.g. amygdala/NAc/PAG/VTA "mixed"); all magnitudes SCAFFOLD; the citations'
  DOIs verified at build (below).

---

## 7. Sources (verified from search; DOIs finalised at build, per v10/v11 practice)

- 5-HT in anterior hypothalamus/VMH **inhibits** aggression via **5-HT1A**; DRN serotonergic innervation:
  hamster aggression / 5-HT1A work — [PMC2692818](https://pmc.ncbi.nlm.nih.gov/articles/PMC2692818/);
  5-HT1A autoreceptor GIRK inhibition of DRN firing — [PubMed 26634643](https://pubmed.ncbi.nlm.nih.gov/26634643/).
- DRN→ventral-hippocampus modulates **reactive aggression** via **5-HT1B** (2024) —
  [PubMed 39159717](https://pubmed.ncbi.nlm.nih.gov/39159717/).
- 5-HT **facilitates PFC (OFC/ACC)** suppression of aggression via **5-HT2**; low 5-HT reduces PFC control
  over amygdala–hypothalamus–PAG — Neurobiology of Aggression & Violence review
  [PMC4176893](https://pmc.ncbi.nlm.nih.gov/articles/PMC4176893/); testosterone/cortisol/serotonin review
  [PMC3294220](https://pmc.ncbi.nlm.nih.gov/articles/PMC3294220/).
- Serotonin & human impulsive aggression (Coccaro et al.) — Biol Psychiatry 2021
  [S0006322321013329](https://www.sciencedirect.com/science/article/pii/S0006322321013329);
  receptors/transporters in escalated aggression (Miczek) — [PMC3684010](https://pmc.ncbi.nlm.nih.gov/articles/PMC3684010/).

---

## 8. What I am asking the design session to rule

1. **The sign representation (§2):** (C) the projection/receptor-specific sign upgrade (recommended, and it
   also resolves VP→LHb) — done as its own cited pass *before/with* the node — or another option. **This is
   the blocking decision; the node cannot be honestly built without it.**
2. **Scope:** DRN only (MnR deferred) ✔ as proposed? The efferent/afferent set in §4 — add, trim, or extend?
3. **Sequencing:** sign-convention upgrade first (fixing VP→LHb, enabling honest 5-HT) → then DRN node → then
   re-validate any pre-5-HT CU seeds (their provenance already marks them provisional).

I have built nothing. On your ruling I draft the sign-convention-upgrade spec (if (C)) and/or the DRN build.
