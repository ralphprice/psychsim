# The `VTA` curve — **RULING: keep the bump. It is real, measured, and the 0.18 was mislabelled.**

**Your dilemma was: a bump-then-decline can't also be a matures-to-adult baseline. Correct — so one of the two
assumptions is wrong, and the literature says which. The bump is real; the "0.18 = adult target" is the error.
`VTA` is the one node whose curve is genuinely non-monotonic, and that is a GROUNDED feature, not a problem to
smooth away.**

---

## 1. The empirical fact — the adolescent DA peak is a directly-measured transient overshoot

**This is not inference from receptor densities; it is direct electrophysiology, replicated, in the region
itself:**
> **"VTA dopamine neurons fire faster in adolescence than in adults"** — *"Elevated dopamine neuron firing in
> adolescent rats was also observed in cell-attached recordings in ex vivo brain slices… VTA dopamine neurons
> fire faster in adolescence, potentially because GABA tone increases as rats reach adulthood"* (J Neurophysiol
> 2012, Jn.00077.2012).
> And in vivo: **"Tonic firing rates in the VTA are observed to be higher in adolescents than in adult
> animals"** (developmental review, PMC4560964), tied to *"adolescent-specific developmental increases in
> incentive motivation."*
> Mechanism named: *"as the dopamine network matures, inhibitory feedback loops form… may contribute to…
> more tightly regulated behaviors in adults"* (J Neurosci 2022) — **the decline is real and it is
> GABA/inhibitory maturation catching up.**

> **So the shape is: low in childhood → PEAK in adolescence → SETTLE to a lower adult value. The bump is the
> single best-established fact about VTA development, and it is the neural basis of adolescent
> reward-seeking/risk-taking — which the sophropathy/CU study cares about directly.** **Removing the bump to
> make the curve monotonic would delete a grounded developmental phenomenon to satisfy a labelling
> assumption.**

## 2. The resolution — your option (b), and it dissolves the dilemma

**You framed two options. (b) is correct: keep the adolescent bump; the adult value is the post-peak settle.**
**The 0.18 I gave you in the four-pacemaker table was labelled "adult target" — that was MY error. 0.18 is the
ADOLESCENT PEAK. The adult VTA value is LOWER — the settle.**

- **Adolescent peak: ~0.18** (the higher adolescent firing).
- **Adult settle: ~0.13–0.14** (your preview's 0.136 @ 25y is not a bug — it is the correct adult value).

> **Your preview already computed the right curve. 0.180 @ 16y → 0.136 @ 25y is exactly the peak-and-settle
> the literature describes. The mechanism did the right thing; only my label was wrong.** **The adult VTA
> baseline is the post-adolescent settle, and the bump is a feature.**

## 3. ★ What this requires of the S57 MECHANISM — check it before building

**The other four nodes are monotonic (low→high→plateau). `VTA` is NOT — it is low→peak→settle.** **Does
`a053a9d`'s `maturation(schedule, age)` support a non-monotonic schedule — a curve that rises, peaks, and
comes back down — or only a saturating rise?**

- **If the scaffold curve families include a peaked/overshoot shape** (or one can be composed), `VTA` maps to
  it, adult = settle, done.
- **If the mechanism only supports monotonic saturation**, then S57 has a gap the `VTA` case just exposed —
  **and that is itself worth knowing**, because the developmental literature is full of adolescent overshoots
  (DA, synaptic density, receptor densities all peak-and-prune). **A developmental-baseline mechanism that
  can only rise-and-plateau cannot represent adolescent pruning at all.** **Register it either way: `VTA` is
  the first peak-and-settle node, and it tests whether S57 handles overshoot.**

> **This is the same shape as every other finding on this branch: a specific node measured against the
> mechanism reveals whether the mechanism is complete. `VTA` is asking S57 the overshoot question. Answer it
> before building the five, because if the mechanism needs a peaked schedule, that is a step-1 addition, not a
> step-2 curve.**

---

## 4. RULING
1. **`VTA` keeps the bump.** Curve = low (childhood) → peak ~0.18 (adolescence) → settle ~0.13–0.14 (adult).
   **The adult baseline is the settle, not the peak. My four-pacemaker "0.18 adult" was mislabelled — correct
   it to "0.18 adolescent peak."**
2. **First check the mechanism supports a non-monotonic schedule.** If yes, map `VTA` and proceed. **If no,
   that is a step-1 gap (S57 can't do overshoot) and must be built before the five curves — do not force `VTA`
   monotonic to dodge it.**
3. **The other four are unchanged and clean** (monotonic low→high→plateau; `DRN` on `pfc_low_early_high_late`,
   `LC`'s 0.15 = mature endpoint, `SNc` early-plateau, `BF-ACh` steady-rise).
4. **Then the full five-node apply → keystone across the whole trajectory → full suite + deliberate regen, on
   a confirmed machine.** Unchanged.

## 5. The disclosure this adds
**`VTA`'s adolescent DA peak is the neural substrate of adolescent reward-seeking and risk-taking.** If the
curve goes in, the model gains — for free, from a grounded maturation curve — a mechanism for **why adolescents
seek reward and risk more than children or adults.** **That is a second developmental phenomenon (alongside
the Tremblay aggression curve) that would EMERGE rather than be coded** — and it is squarely in the
sophropathy/CU study's territory (reward sensitivity, impulsivity, the developmental window of divergence).
**Flag it as a predicted emergent finding to check once the build runs: does adolescent reward-seeking rise and
fall with the VTA curve, the way aggression rose and fell with the DRN curve?**

**Everything else holds. The Tremblay result stands as ungated-but-predicted. `S58` closed. The machine and
this `VTA` mechanism-check are the two gates; the other four curves are specified and waiting.**
