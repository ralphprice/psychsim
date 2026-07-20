# S57 step 2 — the per-node curves, and a **correction to point 2 before it becomes a wrong curve**

**The mechanism (`a053a9d`) is right, and the `DRN` 0.30-adult-on-a-childhood-curve → 0.047-at-age-2 →
0.30-by-10 resolution is exactly the prediction. But your point 2, as framed, would have produced the WRONG
curve, and I nearly confirmed it in passing. Here is the correction, because it decides every shape.**

---

## 1. ★ The correction: the human 5-HT trajectory is NOT a simple low→high rise

**You recorded: "the model's `DRN` baseline is the functional 5-HT output (matures UP), not the raw firing
rate." The direction is right for the FUNCTIONAL BRAKE but wrong for TISSUE LEVELS, and the distinction is the
whole mechanism:**

> **Tissue 5-HT in humans PEAKS in the first two years, then DECLINES to adult levels.**
> *"Peak serotonin levels occur during the first two years in humans"* (biorxiv 2023, citing the human
> literature). In rodents: *"levels of 5-HT peak within the first postnatal week, after which they decline,
> reaching adult levels at around P15"* (Hohmann 1988).

**So at the TISSUE level the curve is high→low — the OPPOSITE of what point 2 says.** If we ground `DRN`'s
baseline to tissue 5-HT, we get a HIGH age-2 value, the keystone breaks HARDER, and the model says toddlers
have an adult-plus 5-HT brake. **That is backwards.**

**What actually matures UP is the FUNCTIONAL 5-HT1A-MEDIATED BRAKE, and the mechanism is specific:**
> The immature DRN has **"lack of 5-HT1A autoreceptor response, and lack of GABA synaptic activity"** (J
> Neurosci 2014). And the aggression-relevant arm is **cortical**: the C-LHPA longitudinal PET work locates
> the deficit in **orbitofrontal 5-HT synthesis** and frames it as *"reduced top-down control"* (Booij/Tremblay
> 2010, PMC2889822) — a **cortical** 5-HT action that depends on the protracted maturation of 5-HT innervation
> to frontal cortex (*"maturation of 5-HT innervation is protracted... P21 in rodents,"* PMC5440475).

> **The resolution: the model's `DRN` baseline is neither tissue 5-HT nor raw firing. It is the FUNCTIONAL
> INHIBITORY EFFICACY of the 5-HT system on the aggression circuit — which is gated by (a) 5-HT1A autoreceptor
> maturation and (b) 5-HT innervation of frontal cortex, BOTH of which mature UP across childhood while tissue
> levels fall.** **The brake matures up because the RECEPTOR-AND-CIRCUIT machinery matures up, not because the
> transmitter rises.** That is why your low→high direction is right for the model's purposes — but for a
> reason that must be recorded correctly, or the next person grounds it to tissue levels and inverts it.

**Confirmed, with the mechanism attached. Build the `DRN` baseline as functional-brake-efficacy, low→high,
gated by autoreceptor + cortical-innervation maturation — NOT tissue level.**

---

## 2. The per-node curves — scaffold-family mapping, with mature-age per node

**You are authorized to map to the existing scaffold curve families** (curve *shapes* are already scaffold in
the model; `pfc_low_early_high_late` is the precedent). **What I am grounding is the DIRECTION and the
MATURE-AGE per node — the load-bearing parameters — not authoring new curve shapes.**

| node | direction | mature-age (human) | scaffold family | firmness |
|---|---|---|---|---|
| **DRN** (5-HT functional brake) | **low → high** | **~adolescence** (protracted; frontal 5-HT innervation matures latest) | **`pfc_low_early_high_late`** — same shape, same reason (both are frontal-maturation-gated inhibitory control) | **FIRM** — direction and mechanism both grounded above |
| **LC** (NA) | low → high | ~childhood–adolescence | a low-early-high-late family | MODERATE — LC matures postnatally; human timescale less precisely pinned. **`LC`'s existing 0.15 = the mature endpoint** (resolves S58). |
| **SNc** (DA, motor) | low → high | **~early, then stable** (motor DA consolidates P30–50 rodent → early-childhood human) | an early-plateau family | MODERATE — direction firm (immature bursty → adult pacemaker), early mature-age |
| **VTA** (DA, reward) | low → high | **~adolescence** (reward DA is the classic late-maturing system) | a low-early-high-late family | MODERATE — direction firm; **the adolescent reward-DA peak is well-established** and the curve should carry the adolescent bump if the family allows |
| **BF-ACh** | low → high | **~childhood** (linear P10→adult in rodent) | a steady-rise family | FIRM direction (the linear-rise result is direct), MODERATE mature-age |

**The one that is load-bearing — `DRN` — is the one that is FIRM**, because its curve is not a free choice:
it is the frontal-inhibitory-control maturation curve, which is exactly `pfc_low_early_high_late`, which the
model already uses for the PFC's own maturation. **`DRN` and the PFC mature on the same schedule for the same
reason (frontal top-down inhibitory control), so mapping `DRN` to that existing family is a GROUNDED
identification, not a convenient pick.** **I did not choose it to pass the keystone; I chose it because the
aggression-relevant 5-HT action IS a frontal-cortical inhibitory-control mechanism and that is the curve
frontal inhibitory control follows.**

---

## 3. DISCLOSURES
1. **`DRN` mature-age drives the keystone.** I have set it to adolescence on the frontal-maturation ground.
   **The keystone must be checked to hold across the *whole* curve, not just at age 2** — the young→aggress
   half at 2, the decline through childhood (Tremblay), the adult restraint. **If it holds at 2 but not the
   trajectory, the curve is wrong, not the keystone.** (S57's prediction is the whole Tremblay curve, not one
   point.)
2. **Tissue-vs-functional is now on record** (§1). Anyone re-grounding `DRN` must not use tissue 5-HT.
3. **SNc early / VTA late** is a real dissociation (motor DA consolidates early, reward DA matures into
   adolescence) — **do not give them the same curve** even though both are DA. Two different mature-ages.
4. **Human timescales are coarser than rodent.** All mature-ages are order-of-magnitude (early-childhood /
   childhood / adolescence), not precise. **Mark the whole table "direction firm, mature-age approximate."**
   The mechanism is robust to mature-age precision; only `DRN`'s needs to be early-enough-at-2, which
   adolescence-mature comfortably satisfies (0.047 at 2 on that curve).

---

## 4. RULING
1. **Apply the five curves** with the directions and mature-ages above; **`DRN` → `pfc_low_early_high_late`**
   (the grounded identification), the others to their families. **`LC`'s 0.15 = mature endpoint (S58 closed).**
2. **Record the tissue-vs-functional distinction (§1) in the seed** as `DRN`'s baseline-semantics note — it is
   the reason the curve is low→high and it is counterintuitive.
3. **Re-run the keystone across the whole developmental trajectory** — not a point check. **The finding, if it
   emerges: the Tremblay curve (aggression peaks ~2–3, declines) falls out of a grounded 5-HT-brake maturation
   curve.** That is the prediction S57 exists to test.
4. **The golden moves substantially** (all development changes) — **full suite, deliberate regen, the moment
   the machine is confirmed.** **Do not gate on a partial suite for a five-node developmental change** — this
   is a bigger move than the deletion, and the deletion already taught us the partial-gate is not enough.
5. **Do not build until the machine is up** (step 3's blocker is real and yours). **The curves are specified and
   waiting; nothing is guessed.**

**`DRN` 0.05 → its curve's age-appropriate value, mechanism-grounded; keystone predicted green across the
trajectory; freezing floor unchanged by this pass (it is a different defect). The reviewer-literature queue is
now empty of the pacemaker work — what remains (S56, `VMH→vlPAG` band, opioid, `noci→PBN`) is grounding I still
owe, but none blocks this build.**
