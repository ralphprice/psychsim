# The `vlPAG` driver — **RULING. There is no missing driver.**
### Supersedes the un-sent DRN baseline ruling; that document's grounding is folded in below.

**Your diagnostic changed the question and it was right to. And you caught the sweep's impossible candidate
(`CeA → vlPAG-glut` — GABAergic, sign −1) by hand-verifying against the seed. An 8-agent sweep proposed an
edge that cannot exist; the verification caught it. That is the discipline holding at the point where a
volume of proposals is most likely to slip one through.**

---

## Q1 — `VMH → vlPAG` is **GLUTAMATERGIC.** The sign is right. **And it is right BY ACCIDENT.**

**Verified: `VMH → vlPAG` — `dominant_receptor: None`, `low-moderate`, `basis: anatomy`. Your ★★ stands.**

**The grounding, and it is already in the material from the MeA/VMH pass:**
> The VMH has **"a core region that contains the nucleus's glutamatergic PROJECTION CELLS, and a cell-poor
> shell region… mostly populated by GABAergic cells, which are thought to INHIBIT CORE NEURONS."**

**The VMH's GABAergic population is the SHELL, and it is LOCAL — it inhibits the core. It does not project.**
**So a long-range VMH projection cannot be GABAergic.** **`VMH → vlPAG` is glutamatergic; +1 is correct.**
**Re-ground the receptor. Do not flip it. Do not crank it.**

### ★ And this is the sharpest thing S44 has produced — record it above the census
> **`MeA → VMH`'s typing order gave the WRONG sign. `VMH → vlPAG`'s typing order gave the RIGHT sign. Same
> mechanism, opposite outcomes.**
> **So you cannot tell from the OUTCOME whether the MECHANISM is sound. "The sign looks right" is not
> evidence that it IS right.** **161 fallback edges — and the ones that happen to be correct are correct for
> no reason.** That is why the census is not optional: **it is not a hunt for wrong signs. It is a hunt for
> ungrounded ones, of which the wrong ones are a random subset.**

---

## Q2/Q3 — **the driver hunt is over. (a) is not the fix.**
Your rejections are all correct — `CeA` (GABAergic, impossible) · `PBN` (inert; the real gap is the missing
`noci → PBN` arm — **register it**) · `SC-Pv` (wrong modality, wrong column) · `PMd`/`AHN`/`DMH` (absent,
dorsal column). **The incumbent is correctly signed. There is no missing driver.**

---

## Q4 — **NO. And the framing needs correcting: it is not a level. The threat-delta should not exist.**

**Here is the grounding I was about to send you — and your diagnostic converged on it independently, from the
other end.**

**`DRN` is a pacemaker:** *"serotonergic neurons in DRN discharge with a **slow (1–2 Hz), regular
(clock-like) pattern, suggesting a homogeneous population of PACEMAKER neurons**"* (Aghajanian et al. 1968;
Mosko & Jacobs 1974/76; Aghajanian & Vandermaelen 1982) — *"the robustness of the steady firing under a
variety of conditions was taken to imply… **intrinsic tonic pacemaker mechanisms**."*

**And `DRN` is MEASURED not to respond to acute threat.** Wilkinson & Jacobs, freely-moving cats, three
stressors — **100 dB white noise, restraint, and CONFRONTATION WITH A DOG:**
> **"Despite behavioral and physiological evidence that all three manipulations induced a stress response,
> the maximal firing rate of 5-HT neurons was NOT SIGNIFICANTLY DIFFERENT from that observed under unstressed
> conditions."**

**What moves it: behavioural arousal state and tonic motor output. Not threat.**

```
DRN  baseline 0.05 / setpoint 0.1   ← the GENERIC SCAFFOLD
LC   baseline 0.15                  ← GROUNDED, pacemaker-class
```
> **`DRN` is a PACEMAKER-CLASS node at a DRIVEN-CLASS baseline. We fixed this exact error once — for `LC` —
> and never generalised it.** **Third form of partial completion: the node's own intrinsic rate is the missing
> determinant, and its synaptic inputs carry 100 % of its activity because the thing that should dominate
> them is not represented. `LHb → DRN` carries 100 % for exactly the reason `CeA → LC` did — and it is
> invisible to an afferent audit, because the missing input is not an input.**

### ★ And your diagnostic is the MECHANISM. Together: a five-step chain, every step a registered defect
1. **`dlPFC` saturates to 1.0** — §18.
2. `dlPFC → vmPFC → DRN` — your un-damped loop.
3. **`DRN`'s baseline is near-zero, so its afferents ARE its activity** — Form 3.
4. **→ `DRN` spikes under threat, which the literature says it does not do.**
5. **→ `DRN` crushes `vlPAG` → freezing cannot fire.**

> **Not one step in that chain is "`vlPAG` needs a driver." Your (b) is right, and the grounding says the
> defect is not the delta's SIZE — it is the delta's EXISTENCE.**

---

## ★ New finding, and it is mine: **`dlPFC` IS braked, and saturates anyway**

```
dlPFC      <- MDthal, S2-PPC, dACC, FPC, OFC, HPCv, VTA, LC, BF-ACh, dlPFC-GABA   ← NINE excitatory
dlPFC-GABA <- dlPFC     dlPFC-GABA -> dlPFC                                        ← a proper E-I loop
```
**`dlPFC` has a correct recurrent E-I brake and it saturates to 1.0 against nine afferents.** **A BRAKED node
saturating is worse news than an unbraked one doing it** — it means the brake layer is not merely incomplete,
it is **mis-calibrated where it exists.**

**And the cause is the concern I raised to Ralph in the status assessment:** the gate family's bands are
**inherited byte-for-byte** — a perfect defence against tuning that **takes no account of afferent load.**
**`dACC` has few afferents. `dlPFC` has nine. Same bands.** **The correlated-scaffold cost, biting on a
load-bearing node — and it is now manufacturing a neuromodulator's threat response.**
**Register in §18 and in the 209-edge audit's scope. Do not fix it in this pass** — it is a family-wide
calibration question and it needs its own grounding (the real E-I loop's gain scales with drive; ours is one
number).

---

## RULING — build, in order
1. **Re-ground `VMH → vlPAG`'s receptor: glutamatergic, cited (VMH's projection cells are the glutamatergic
   core; the GABAergic shell is local).** Sign unchanged. **Band untouched.**
2. **Ground `DRN`'s baseline** from the electrophysiology (1–2 Hz clock-like, rat; 3.42 ± 0.33 spikes/s quiet
   waking, cat) — **`LC`/`dPAG-GABA` precedent for the normalisation; setpoint paired.** **The arousal-state
   relation is groundable too** (the taxonomy's *ground the relation* case).
3. **`LHb → DRN` STAYS UNTOUCHED** — it becomes a modulation on a large tonic rate rather than the whole
   signal. **Exactly what happened to `CeA → LC` when `PGi` landed.**
4. **Re-measure. Does freezing fire on the existing `VMH` drive against a TONIC — rather than threat-spiked —
   `DRN`?** **If yes: there was never a driver gap, and the freezing floor goes green on a grounded rate. If
   no: the driver question is real and finally askable honestly.**
5. **Do NOT gate `DRN` down.** That would tune a symptom of a baseline class error.
6. **`DRN → vlPAG` and `VMH → vlPAG` bands untouched.**

**Register:** `noci → PBN` (the missing arm that makes PBN inert) · the `dlPFC` brake mis-calibration · **the
tonic sweep** — *"is it tonic?"* is a CLASS question we asked of `vlPAG`-glut (no) and never asked of `DRN`
(yes, since 1968). **Sweep `VTA`, `SNc`, `BF-ACh`, the `vlPAG`-DA population; confirm `LC` (0.15) and
`dPAG-GABA` (0.19) are the only two grounded. Report only.**

**`files.zip`:** keep the ~35 docs — **the diagnostics and rulings ARE the design history**, and that is the
master document's own principle. **Un-track the binary** (follow-up, no history rewrite). **And look inside it
first: the repo is public.**
