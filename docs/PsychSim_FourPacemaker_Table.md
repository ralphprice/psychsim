# The four-pacemaker grounding table — **DRN, VTA, SNc, BF-ACh**
### The reviewer's literature pass. Needs no machine. Assembled 2026-07-18.

**The purpose (from the tonic sweep): four neuromodulator pacemakers sit at the generic 0.05 baseline. `LC`
(0.15) and `dPAG-GABA` (0.19) are the only two grounded. This table grounds the other four — adult tonic rate
AND developmental trajectory — as one piece, so we can decide whether S57 serves one node or five.**

**The headline is in the developmental column, so I am putting it first.**

---

## ★ THE FINDING: all four MATURE postnatally. S57 is a MECHANISM, not an over-engineering.

**We grounded `LC` and asked whether its rate matures (S58, open). We grounded `DRN`-as-pending and inferred
its rate must mature (the keystone break). This table answers the question for all four at once, and the
answer is uniform:**

| region | matures postnatally? | evidence |
|---|---|---|
| **DRN** (5-HT) | **YES — sharply** | *"immature HYPEREXCITABILITY transitions to adult state during the first three postnatal weeks"* — depolarised RMP, higher firing rate, **absent 5-HT1A autoreceptor response, absent GABA synaptic activity** in the immature state (J Neurosci 2014, 34:4809). **A named sensitive period.** |
| **BF-ACh** | **YES — linearly** | cholinergic spontaneous activity *"increases linearly from P10 into adulthood,"* driven by a maturing I_NaP current, mirroring tissue ACh and ChAT expression (J Neurosci 2021, 41:3597). |
| **SNc** (DA) | **YES** | somatodendritic fields mature early (P4–P10) but *"spontaneous glutamatergic EPSCs show a developmental sequence"* — immature SNc DA neurons are **larger, more frequent, bursty**; the adult pacemaker pattern consolidates by P30–P50 (PMC4448554). |
| **VTA** (DA) | **YES** | the DA-system-development literature treats VTA DA firing as postnatally maturing; the intrinsic-current basis (I_H, SK) develops across the juvenile period (parallel to SNc; MDPI IJMS 2024). |

> **This is not four coincidences. The neuromodulator pacemakers as a CLASS mature their tonic rate across the
> juvenile period — which is exactly the developmental window the CU/sophropathy study lives in.** **S57 (a
> developmental trajectory for neuromodulator baselines) is therefore a real mechanism serving at least FIVE
> nodes (`LC` included — S58 now answered: yes, `LC` matures too, its immature state is part of the same
> literature).** **It is not an over-engineering. Build it.**

**And it retro-justifies the keystone ruling completely.** `DRN`'s scaffold-low was standing in for the
serotonergic system's immaturity — and the immaturity is not a hand-wave, it is a *named, dated, mechanistic
transition with a sensitive period.* **The toddler's low 5-HT brake is the immature DRN before its three-week
transition. We were right not to freeze an adult constant over it.**

---

## THE ADULT RATES (for when S57 exists — NOT to be built as static constants; see the ruling)

**Normalisation, held identical to `LC`/`dPAG-GABA`:** baseline = adult tonic rate ÷ a functional reference
for that cell type; setpoint paired at ~2× baseline (the `LC` 0.15/0.30-style pairing). **Rates are
in-vivo/slice electrophysiology, adult, rodent unless noted.**

| region | adult tonic rate (grounded) | proposed baseline | note |
|---|---|---|---|
| **DRN** (5-HT) | **0.5–2 Hz**, slow/regular/clock-like; 1.72 ± 0.50 Hz under anaesthesia (single-neuron reconstruction, PMC3913638); Aghajanian 1968 / Aghajanian & Vandermaelen 1982 | **~0.25–0.35** | 5-HT's low ceiling (functional max ~5–6 Hz) makes its tonic/max ratio higher than LC's. **This is the range that broke the keystone as a constant — which is the point: it is the ADULT value.** |
| **VTA** (DA) | **0.5–5 Hz** pacemaker in vitro (1–5 Hz, peak ~3 Hz, PMC7040182; 0.5–4 Hz, Nat Commun 2024); ≤10 Hz in vivo with bursts | **~0.15–0.20** | tonic only; bursting is phasic and not a baseline. |
| **SNc** (DA) | **1–10 Hz** pacemaker-like in vivo, slow/regular; *the* textbook autonomous pacemaker (PMC12585177) | **~0.15–0.20** | matched to VTA; both midbrain DA. |
| **BF-ACh** | **~7 Hz active waking**, 14 Hz REM (behaving; PMC4548510) — **arousal-state-locked, like DRN** | **~0.20–0.30** | the rate is *state-dependent*, so its "baseline" is a waking-state value; flag the state-dependence for S56/relation-grounding. |

*(Proposed baselines are the reviewer's normalisation for the build session to check against the `LC`
precedent — not authored values. The build session pins them the way it pinned `dPAG-GABA`'s 0.19.)*

---

## DISCLOSURES (the honest column)
1. **Species.** All rodent. `LC` and `dPAG-GABA` were also rodent — **consistent, not a new extrapolation.**
2. **State-dependence for BF-ACh (and partly DRN).** These rates track arousal state, not a fixed tonic. **Their
   honest form is the taxonomy's RELATION grounding** (like `LC`'s arousal coupling), not a bare constant.
   Flag for S56.
3. **VTA developmental curve** is the least directly measured of the four (inferred from the shared DA-system
   maturation literature + SNc's direct sequence). **Grounded as "matures, curve parallel to SNc" — mark it
   the weakest of the four developmental claims.** The DIRECTION (matures) is solid for all four; the SHAPE is
   directly measured for DRN, BF-ACh, SNc and inferred for VTA.
4. **DRN heterogeneity.** A fast-firing (>8 Hz) subset and non-clock-like cells exist (PMC4971071). Our single
   `DRN` node is a lump over these — **register with the existing `DRN`-embedded-in-`vlPAG` grain note.**

---

## THE RULING — what to build, and the trap to avoid

**DO NOT build the adult rates as static `baseline_activation` constants. That is the exact `DRN` category
error, at four-node scale.** A static 0.30 on `DRN` gives a two-year-old an adult 5-HT brake; a static 0.18 on
`VTA`/`SNc` and 0.25 on `BF-ACh` give a two-year-old an adult DA and ACh tone. **The table proves all four
mature — so freezing any of them as a constant is the error the keystone caught, four times over.**

**Order:**
1. **Build S57 FIRST — the developmental-baseline mechanism.** The substrate has `developmental_online_age`
   (onset) and `plasticity_coeff_schedule_ref` (plasticity curves) but nothing for a maturing baseline. **S57
   is that missing field: a baseline that follows an age curve, exactly parallel to how `pfc_low_early_high_late`
   gives edges a maturing weight.** **The table is its specification — five nodes (`LC`, `DRN`, `VTA`, `SNc`,
   `BF-ACh`), each an adult target + a maturation curve.**
2. **Then apply it to all five**, with the adult rates above as the mature-state targets and the developmental
   evidence as the curve. **`LC`'s existing 0.15 becomes the mature endpoint of `LC`'s curve, not a lifelong
   constant** — which resolves S58.
3. **Then re-run the aggression keystone and the freezing floor** against age-appropriate rates. **Prediction:
   the keystone's young→aggress half now holds because the age-2 DRN rate is the immature (low) value BY
   MECHANISM, not by scaffold — and it will correctly decline as the curve matures, which is the Tremblay
   trajectory the model should reproduce.** **If that emerges, a real developmental phenomenon has come out of
   grounded maturation curves, and it is a finding.**

**This is why the table had to precede S57: we now know S57 serves five nodes, we have all five adult targets
and four of five curves in hand, and building the mechanism without the table would have been building an
empty field for an unknown number of users.**

---

## What this unblocks
**Tier 2 opens behind this.** But note the reorder the table forces: **S57 moves to the FRONT of Tier 2**, because
`DRN`'s baseline (2.1) can no longer be "grounded" as a constant — it is grounded as *the mature endpoint of an
S57 curve.* So: **S57 (build the mechanism, five-node spec) → `DRN`/`VTA`/`SNc`/`BF-ACh`/`LC` baselines as curve
endpoints → the keystone/floor re-run → then `VMH→vlPAG`'s band (2.2), S56 (2.4), the selector (2.5), the
opioid system (2.6).**

**Everything holds: keystone green; freezing floor the one authorized red; `DRN` 0.05 `UNGROUNDED — pending`,
now with its pending mechanism fully specified.**
