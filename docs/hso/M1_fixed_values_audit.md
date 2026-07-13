# HSO M1 — Fixed-Values Audit (diagnosis only)

**Design authority:** `docs/PsychSim_Homeostatic_SelfOrganization_SPEC.md` (sealed).
**Scope:** M1 of the audit-first gate. DIAGNOSIS ONLY — no values changed, nothing built.
**Substrate audited:** origin/main commit `b626c06` (v14 Phase 1.1: 83 circuits, 208 connection entries / 180 circuit→circuit).
**Method:** read-only extraction from the seed JSON. Reproducible by the reviewer independently (re-run the counts against the remote seed). No engine run is needed for M1 — it is a static audit of the seed's fixed fields.

**The question, per value (spec §0):** is this an honestly-grounded *substrate property*, or a frozen/fitted *state* value masquerading as one? Classes: **measured / class-grounded / scaffold-honest / FITTED.**

---

## Headline result

| Fixed value | Count | measured | class-grounded | scaffold-honest | **FITTED** |
|---|---|---|---|---|---|
| Setpoints (`homeostatic_setpoint`) | 83 | 0 | 0 | **83** (uniform 0.1) | **0** |
| Circuit timescales (`time_constant_tau_ms`) | 83 | 0 | 0 | **83** (near-uniform placeholder) | **0** |
| Eligibility timescales (`eligibility_trace_tau_ms`) | 208 | 0 | 0 | **208** (uniform 1000ms) | **0** |
| Weight *magnitudes* (`default_weight`) | 208 | 0 | 0 | **208** (symbolic bands) | **0** |

**No classic FITTED values were found** — there are no precision-threaded decimals (no `0.447` tuned to a window). This is the important and slightly counter-intuitive finding, and it is stated plainly: **the fudge in this substrate is structural, not per-value.** It is not "a fitted number here and there." It is that (a) the grounded substrate properties (setpoints, timescales) are collapsed to **uniform placeholders** that cannot represent real per-population differentiation, and (b) the weights are **set constants** (symbolic bands) rather than plastic state. Whether those set weights are *effectively static* — the actual crux — is M2's test, not M1's.

So M1's honest verdict is: **nothing is fitted; but nothing is grounded either.** The substrate rests on disclosed-scaffold uniform placeholders (setpoints, timescales) plus banded scaffold weights. That is exactly the condition HSO exists to replace — not by de-fitting individual numbers, but by grounding the substrate properties and making the weights self-organize.

---

## M1.1 — Setpoints (all 83 `homeostatic_setpoint`)

**Finding:** every one of the 83 setpoints is the identical value **0.1**. A single uniform placeholder; zero per-population differentiation.

**Classification: 83/83 scaffold-honest, 0 fitted.** A uniform value is the *opposite* of fitted — fitting would require per-population tuned numbers. The uniformity is a *disclosed* design choice: `tests/test_params_seed_reconciliation.py::TestTwoSetPointsStaySeparate` asserts the firing-rate setpoint is "uniform firing-rate homeostasis (uniform)," deliberately distinct from the varied interoceptive body-variable set-points. So the uniform 0.1 is an honest, documented starting assumption — **but it is NOT grounded per-population biology.**

**What grounding is *available* per class (for M3 — recorded, not applied):** real populations have *different* target rates, and the distinction is a **class property** even where the absolute is unmeasured:

| Population class | Circuits (examples) | Class target-rate character | Groundable as |
|---|---|---|---|
| Tonic-pacemaker neuromodulator | VTA, SNc, DRN, LC | autonomous tonic firing (Grace & Bunney; DA ~4–5 Hz) — a **standing non-zero tonic rate** | class-grounded (ratio grounded; absolute scaffold) |
| Tonically-active interneuron | (a VTA-GABA-class, deferred) | tonic inhibitory tone — standing rate above phasic neurons | class-grounded |
| Phasic / near-silent-at-rest | LA, BA, VMHvl, PAG, most projection nuclei | low resting rate, driven up phasically | class-grounded (low tonic) |
| Endocrine | Pituitary, AdrenalCortex | slow hormonal, distinct regime | class-grounded |

**F1 root-cause CONFIRMED.** F1 (the VTA pacemaker failure this session) was exactly this: VTA is a tonic-pacemaker population whose target rate is a *different class* from the phasic majority, and the uniform-0.1 scheme could not represent it — giving VTA-GABA a matched (non-0.1) setpoint broke the S2.5 uniform-setpoint invariant. F1 is direct evidence that **real populations have different target rates and the uniform 0.1 is the simplification.** (This does not make 0.1 "fitted"; it makes it *insufficiently differentiated*.)

---

## M1.2 — Time constants

**Finding:**
- `time_constant_tau_ms`: **78 × 200ms**, **4 × 100ms** (the local interneurons: DRN-GABA, vmPFC-GABA, dlPFC-GABA, CeA-GABA), **1 × 300ms** (DRN).
- `eligibility_trace_tau_ms`: **208 × 1000ms** (perfectly uniform across every edge).

**Classification: 0 mechanism-grounded, 83 placeholder.** The 100 / 200 / 300 split is a *coarse 3-level gesture* (interneuron-faster / standard / serotonergic-slower), but the values are round placeholders, not measured kinetics. The eligibility trace is a single uniform 1000ms.

**The measured hierarchy the audit tests against (spec §4):** ionotropic ~1.7–50 ms ≪ metabotropic 150 ms–2.5 s ≪ neuromodulatory 10 s–minutes ≪ plasticity (induction s–min, consolidation hrs–days). These mechanisms differ by **3–4 orders of magnitude**. The current values compress that entire range to essentially one value.

**Mismatch (mechanism vs. current tau):**

| Mechanism (inferred from transmitters) | n | Measured tau | Current tau | Direction of error |
|---|---|---|---|---|
| Ionotropic glutamate / GABA-A (fast synapses) | ~55 | ~1.7–50 ms | 200 ms (100 ms for the 4 interneurons) | **~4–100× too SLOW** |
| GABAergic projection MSNs (mixed iono/metabo) | ~8 | tens of ms – ~1 s | 200 ms | roughly in-band (coincidentally) |
| **Neuromodulator sources** (DA/5-HT/NA/ACh/OT) | 6 (VTA, SNc, DRN, LC, BF-ACh, PVN-OT) | **10 s – minutes (10 000–60 000 ms)** | **200 ms (DRN 300 ms)** | **~50–300× too FAST** |

**F2 root-cause CONFIRMED.** F2 (the associative-learning collapse) was tonic DA flattening the phasic RPE because the plasticity gate reads *absolute* `neuromod_output("DA")`. The audit shows why the model *cannot* separate them: **every neuromodulator source runs at ~200ms, the same timescale as fast synaptic transmission.** There is no slow tonic-DA timescale distinct from the phasic burst — they are one 200ms signal. The uniform eligibility trace (1000ms) compounds it. **The timescale hierarchy is placeholder-uniform, not mechanism-differentiated — this is the structural root of F2**, and it is a substrate-property grounding gap (M3), not a weight problem.

---

## M1.3 — Weight-bases (all 208 `default_weight_basis` + `default_weight`)

**Finding — basis distribution:** `anatomy` 114 · `assumption` **74** · `innate_reinforcer` 19 · `literature` 1.
**Finding — weight bands:** `low` 48 · `low-moderate` 23 · `moderate` 101 · `moderate-strong` 31 · `strong` 4 · **1 numeric outlier** (`MeA→VMHvl` = `0.1`).

**Key distinction:** `default_weight_basis` grounds the edge's **existence / strength-band assignment**, not a *measured magnitude*. Even `anatomy`-basis edges (114) have their *existence and sign* grounded by anatomy, but their *weight magnitude* is still a qualitative band, not a measured synaptic weight. So **the count of weights with a grounded magnitude is 0/208** — consistent with the spec's whole premise (weight magnitudes should be plastic, not set).

**The honest positives:**
- Weights are **symbolic bands**, not precision decimals — *more* honest than false precision. Nobody threaded a `0.447` to hit a window. (The one numeric, `MeA→VMHvl` = 0.1, is a minor convention inconsistency — flagged, not a fudge.)
- The `innate_reinforcer` (19) and `literature` (1) bases are the most grounded; `anatomy` (114) grounds existence/sign.

**The ungrounded-weight set — 74 `assumption`-basis edges (36%):** the self-admitted guesses. Full list in Appendix A. Two patterns worth flagging for M3/M4:
1. The **DRN serotonergic projection set** (DRN→VMHvl/CeA/OFC/vmPFC/dACC/HPCv/BA/NAc-shell/PAG/VTA and the LHb/PFC→DRN loop) — added v12b/v13 with assumption weights.
2. The **interneuron feedback edges** — `DRN-GABA→DRN` (moderate), `vmPFC-GABA→vmPFC` (moderate-strong), `dlPFC-GABA→dlPFC` (moderate-strong). These are precisely the *"add an interneuron and tune its weight to stabilize the loop"* pattern the spec (§2.1) says HSO **dissolves** — inhibitory homeostasis eliminates runaway excitation by construction, so these tuned stabilizer weights should self-organize rather than be set. They are prime M2 crux-test targets.

Under HSO all 208 weights become plastic (self-organize toward setpoints), so "ungrounded weight" is *less* alarming than it sounds — the weight won't be *set* at all after M3. M1's job is only to surface which weights were never grounded, so M3/M4 know.

---

## What M1 establishes (and hands to M2)

1. **Setpoints:** uniform-scaffold (not fitted). Groundable per class in M3. F1 is the evidence they must differentiate.
2. **Timescales:** placeholder-uniform (not fitted). The neuromodulator-source compression is the F2 root; M3's measured hierarchy resolves it by construction.
3. **Weight magnitudes:** 0/208 grounded; 74/208 self-declared assumption; the rest ground existence, not magnitude. No magnitude is measured.
4. **The fudge is structural, not per-value.** There is nothing to "de-fit." The remediation (M3) is *grounding* substrate properties and *making weights plastic*, not correcting fitted numbers.

**The open question M1 cannot answer — and hands to M2:** the weights are *set constants*, but are they *effectively static* (frozen) or do they already *self-organize* despite being set? That is the crux test. M1 shows the weights are ungrounded-and-set; M2 shows whether the existing homeostatic machinery makes them plastic in practice.

---

## Appendix A — the 74 `assumption`-basis edges (ungrounded-weight set)

```
sensory_thalamus->LA[low]  sensory_cortex->LA[low]  LA->BNST[low-moderate]  CeA->BNST[low-moderate]
vmPFC->ITC[low]  HPCv->LA[low]  HPCv->BA[low]  HPCv->vmPFC[low]  dmPFC->LA[low-moderate]
dmPFC->BA[low-moderate]  VTA->OFC[low-moderate]  VTA->vmPFC[low]  OFC->NAc-core[low]  OFC->VTA[low]
sensory_cortex->OFC[low]  BA->NAc-core[low]  HPCv->NAc-shell[low]  V-ventral->LA[low]  V-ventral->OFC[low]
A1-belt->LA[low]  GUST-cortex->NAc-shell[low]  vlPFC->LA[low-moderate]  dlPFC->NAc-core[low-moderate]
HPCv->dlPFC[low]  dACC->PAG-PANIC[low-moderate]  V-ventral->MeA[low]  aIns->CeA[low-moderate]
aIns->PBN[low]  aIns->PVN[low]  vmPFC->PVN[low-moderate]  pSTS->rSMG-TPJ[low]  pSTS->dmPFC[low]
V-dorsal->pSTS[low]  V-ventral->pSTS[low]  rSMG-TPJ->dmPFC[low]  dmPFC->rSMG-TPJ[low]
rSMG-TPJ->PCun-PCC[low]  PCun-PCC->rSMG-TPJ[low]  PCun-PCC->dmPFC[low]  dmPFC->PCun-PCC[low]
ATL-TP->dmPFC[low]  ATL-TP->rSMG-TPJ[low]  aIns->rSMG-TPJ[low]  rSMG-TPJ->aIns[low]  MeA->ATL-TP[low]
BA->pSTS[low]  BA->ATL-TP[low]  IN-CONSPEC:attractive_face->NAc-shell[low]  IN-CONSPEC:attractive_face->OFC[low]
IN-CONSPEC:formidability_cue->CeA[low]  MeA->VMHvl[0.1]  LH->LHb[moderate]  VP->LHb[moderate]
BNST->VMHvl[moderate]  DRN->VMHvl[moderate]  DRN->CeA[moderate]  DRN->OFC[moderate]  DRN->vmPFC[moderate]
DRN->dACC[moderate]  DRN->HPCv[moderate]  DRN->BA[moderate]  DRN->NAc-shell[moderate]  DRN->PAG[moderate]
LHb->DRN[moderate]  vmPFC->DRN[moderate]  OFC->DRN[moderate]  vmPFC->DRN-GABA[moderate]  OFC->DRN-GABA[moderate]
DRN-GABA->DRN[moderate]  DRN->VTA[low]  vmPFC->vmPFC-GABA[moderate]  vmPFC-GABA->vmPFC[moderate-strong]
dlPFC->dlPFC-GABA[moderate]  dlPFC-GABA->dlPFC[moderate-strong]
```
