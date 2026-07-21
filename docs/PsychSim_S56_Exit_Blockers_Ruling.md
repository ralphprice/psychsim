# The two S56-exit blockers — RULING. **Both grounded from the literature. One authorises anatomy, one removes
# a refuted edge.**

**These are the two things standing between the selector build and the S56 exit measurement. I researched both
against the literature rather than the internal logic, because one authorises new anatomy and the other decides
an inferred edge — both need citation, not inference. The literature is decisive on both, and it sharpens the
vlPAG answer and settles the SOM+ route. Rulings.**

---

## 1. The vlPAG excitatory afferent — grounded, and the driver is the selector's OWN freeze-output population

**The diagnosis is decisive: freezing has no threat-driven excitatory driver — the disinhibitory gate is fully
open and delivers ~0.138 (essentially VMH alone). vlPAG needs an excitatory afferent. The literature gives a
grounded answer, and it is MORE SPECIFIC than "mPFC PL/IL generically":**

> **The canonical amygdala route to vlPAG freezing is the CeM → PAG projection** (the standard Tovote/CeA-PAG
> freezing pathway — the medial CeA output projects to the PAG to drive freezing). And the vlPAG "receives
> input from many brain areas… including the amygdala, hypothalamus, zona incerta and prefrontal cortex"
> (Chx10-freezing literature). **So the anatomically correct driver of the freezing column is the CEm
> freeze-output population — the very population the selector build created.**

**★ This is the key finding: the selector build's `CEm-freeze` output population IS the grounded driver of
vlPAG.** The CeM-to-PAG freezing pathway means the freeze-output population must actually PROJECT to and drive
the freezing column — not merely be labelled as the freeze-output. **The freezing column was dead because the
selector's freeze-output population was not wired to drive vlPAG; completing that projection is both the
grounded fix AND the completion of the selector's own architecture.** The freeze-output population selecting
"freeze" must produce freezing, which means driving vlPAG.

**RULING (primary):** **wire `CEm-freeze → vlPAG` as the grounded excitatory driver** — this is the CeM→PAG
freezing pathway, and it completes the selector (the freeze-output population drives the freezing column it
selects). **This is the within-model grounded fix; the driver already exists (the selector created it), it just
needs to reach vlPAG.**

**★ CRITICAL sign caveat — verify carefully:** CeM is **largely GABAergic**, so a naive `CEm-freeze → vlPAG`
excitatory edge may be wrong-signed. The CeM→PAG freezing mechanism in the literature works by **CeM output
neurons DISINHIBITING vlPAG** (inhibiting vlPAG-projecting GABAergic interneurons, i.e. the vlPAG-GABA the model
already has) **OR via a specific glutamatergic CeM subpopulation.** **Ground the sign before building:** if the
freeze-output drives vlPAG by disinhibition, the edge is `CEm-freeze → vlPAG-GABA` (inhibitory, releasing
vlPAG) — but the diagnosis says the disinhibitory gate is ALREADY fully open and delivers nothing, so
disinhibition alone is insufficient. **That means vlPAG needs actual EXCITATORY drive, not more disinhibition
— so the grounded driver is either a glutamatergic CeM-freeze subpopulation projecting directly to vlPAG, OR a
top-down excitatory afferent.**

**RULING (the excitatory driver, if CeM-freeze is disinhibitory-only):** **`mPFC PL → vlPAG` is the grounded
top-down excitatory afferent.** The prelimbic cortex regulates fear EXPRESSION (PL drives conditioned freezing;
IL suppresses it), and mPFC projects to vlPAG (the mPFC→PAG projection is well-documented, with dense
glutamatergic puncta in the ventrolateral column — Frontiers 2026). **So PL→vlPAG is a real, cited, glutamatergic
excitatory afferent that drives freezing.** Use PL (not IL — IL suppresses fear; PL expresses it), grounded.

**Sequencing the vlPAG fix:** (1) determine whether the CEm-freeze population reaches vlPAG by disinhibition
(→ `CEm-freeze → vlPAG-GABA`, but likely insufficient given the gate is already open) or by direct glutamatergic
drive (→ `CEm-freeze → vlPAG` excitatory, if a glutamatergic CeM-freeze subpopulation is grounded); (2) if the
column still lacks excitatory drive, add **`PL → vlPAG`** (the grounded top-down glutamatergic afferent). **The
freeze-output population driving its own column is the architecturally-correct primary; PL→vlPAG is the grounded
excitatory afferent the column needs if disinhibition is insufficient (which the diagnosis suggests it is).**
Authorise both as grounded; build the CeM-freeze→vlPAG completion first, measure, add PL→vlPAG if excitatory
drive is still missing.

## 2. `CEl-SOM → CEm-active` — the literature REFUTES it. Remove it, re-ground SOM+ as local inhibition.

**This is flagged as an inferred route, not a cited one. I checked Fadok 2017, and the literature is decisive:**

> **In Fadok et al. 2017, the SOM+ neurons of CeL suppress flight by LOCAL inhibition WITHIN CeL — SOM+ drives
> freezing by inhibiting the flight-promoting circuit locally, NOT via a projection to a CeM output
> population.** The SOM+/PKCδ+ mutual inhibition is a LOCAL CeL microcircuit. **The inferred `CEl-SOM →
> CEm-active` route is NOT how the biology works** — SOM+ does not project to a CeM output population to
> suppress it; it acts within CeL.

**Its sibling is grounded and stays:** `CEl-PKCδ → CEm-freeze` is directly grounded (Haubensak 2010 — PKCδ+ CeL
neurons gate the CeM output). **So one route is cited (PKCδ+ → CeM) and one is inferred-and-refuted (SOM+ →
CeM).**

**RULING: REMOVE the inferred `CEl-SOM → CEm-active` edge, and re-ground SOM+ as LOCAL CeL inhibition.** This is
the never-remove-anatomy-unilaterally EXCEPTION — **the edge is removed because it is REFUTED by the citation
(Fadok's local-suppression mechanism), not for convenience.** And it is replaced by the correct mechanism:
**SOM+ inhibits the flight/PKCδ+ population WITHIN CeL** — which is exactly the winner-take-all mutual inhibition
the selector build is already constructing. **So the removal doesn't lose the SOM+ function; it corrects it —
SOM+'s role is the local mutual inhibition (SOM+ ⊣ PKCδ+), not a projection to CeM.** The selector's SOM+/PKCδ+
mutual inhibition IS the grounded SOM+ mechanism; the inferred CEm projection was a redundant, uncited addition
that misplaced the same function.

> **This also tightens the selector's emergence measurement (the live failure-mode instance): the SOM+ →
> CEm-active edge, had it stayed, would have been a route by which the selection could rest on a specific edge
> weight rather than emerging from the local mutual inhibition. Removing it and grounding SOM+ as local CeL
> inhibition means the selection is produced by the SOM+ ⊣ PKCδ+ balance (the drives determine which wins),
> which is the emergent mechanism — not a projection weight. The removal makes the selection MORE emergent, not
> less.**

---

## 3. Handoff

1. **vlPAG excitatory afferent:** wire `CEm-freeze → vlPAG` as the primary (the CeM→PAG freezing pathway
   completing the selector's freeze-output) — **grounding the sign carefully** (CeM is GABAergic; determine
   whether it drives vlPAG by direct glutamatergic subpopulation or by disinhibition, and since the diagnosis
   shows disinhibition is already saturated-and-insufficient, the column likely needs actual excitatory drive).
   **If excitatory drive is still missing after the CeM-freeze completion, add `PL → vlPAG`** (prelimbic, the
   grounded top-down glutamatergic fear-expression afferent — PL not IL). Both grounded; build the freeze-output
   completion first, measure, add PL→vlPAG if needed.
2. **`CEl-SOM → CEm-active`:** REMOVE it (refuted by Fadok — SOM+ suppresses flight by LOCAL CeL inhibition, not
   a CeM projection), and confirm SOM+'s grounded role is the local SOM+ ⊣ PKCδ+ mutual inhibition the selector
   already builds. The removal corrects the mechanism and makes the selection more emergent.
3. **These unblock the S56 exit measurement** — with vlPAG actually driven (freezing column live) and the
   selector's SOM+/PKCδ+ mutual inhibition grounded, the exit test becomes measurable: freezing and aggression
   drivable as distinct selector states, the selection emerging from drive balance (perturb-and-follow), no
   scaffold weight the selection rests on.

> **Both blockers are grounded from the literature. The vlPAG driver is the selector's own freeze-output
> population completing the CeM→PAG freezing pathway (with the sign grounded carefully, and PL→vlPAG as the
> grounded excitatory afferent if disinhibition is insufficient — which the diagnosis says it is). The inferred
> SOM+→CEm-active edge is refuted by Fadok and removed — SOM+ acts by local CeL inhibition, which is the mutual-
> inhibition selector already being built, so the correction makes the selection more emergent, not less. Build
> the freeze-output→vlPAG completion, ground the sign, add PL→vlPAG if the column still lacks excitatory drive,
> remove the refuted SOM+ edge, and the S56 exit measurement is finally unblocked. Then measure whether the
> selection emerges — the last thing standing between the selector and the close.**
