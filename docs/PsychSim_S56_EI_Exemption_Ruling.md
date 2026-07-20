# S56 — how the E-I loops persist: RULING. **Exempt the 8 limbs. And a correction to my own ruling.**

**First, a correction that is mine to own: I told you to govern the loops by "the existing homeostatic rule."
You traced that the existing rule (R4-HOMEO) is a firing-RATE homeostat that scales a circuit's incoming
weights UNIFORMLY — it does not distinguish excitatory from inhibitory and does not preserve an E-I ratio.
Applying it to the loops would erode the grounded balance along with everything else. So my instruction was an
over-specification that is not available as stated. You were right not to build it. Here is the corrected
ruling.**

---

## 1. What actually erodes the grounded weights (your trace, confirmed)

I read the two rules. Your diagnosis is exact:
- **R8 competitive normalisation is the main culprit.** `normalise_incoming` holds a circuit's total incoming
  drive at a target (`max(1.0, n×0.5)`), rescaling all incoming weights when the sum exceeds it. `CeA-GABA` has
  two incoming (PVN-OT + the new `CeA → CeA-GABA`), so setting the new edge to 1.0 pushes the sum over target
  and **the grounded edge is renormalised away (1.0 → 0.472).** Confirmed.
- **R4-HOMEO is a firing-rate homeostat**, not an E-I homeostat: `homeo_factor = 1 − rate·(activity − setpoint)`
  scales ALL incoming weights of a circuit uniformly toward a *firing-rate* set-point. **It does not preserve
  an E-I ratio** — it would scale the loop limbs along with everything else. Confirmed: "use the existing rule"
  cannot do what my ruling asked.
- **Hebbian/BCM `dw`** also acts on the limbs.

**The literature I cited (inhibitory plasticity holding the E/I ratio at a set-point) describes a DIFFERENT
mechanism from the model's rate homeostat. So my ruling conflated "the biology's E-I homeostat" with "the
model's existing homeostatic rule" — they are not the same. That conflation is the error, and it is corrected
here.**

## 2. The decision — (1) exempt the 8 limbs, NOT (2) add an E-I-ratio homeostat

**Both would work. The ruling is (1), and the reason is the same discipline that governed the VTA dependency:
do not add a load-bearing new mechanism to buy a capability nothing currently needs.**

**The key fact that decides it: the model's afferent load is developmentally FIXED.** The number of afferents a
node has does not change during a life — the connectome is structural. So:
- **Holding the grounded, load-scaled weight IS holding the grounded E-I ratio**, because the load it was
  scaled to is constant. There is no drift in the ratio to correct — only the eroding rules pushing the weight
  off its grounded value.
- **The dynamic tracking that (2) would add** — an E-I homeostat that re-derives the inhibitory return against
  the node's *measured* excitatory drive — **only earns its complexity if the excitatory load CHANGES**, so the
  inhibition must chase it. **In the current model, load doesn't change, so (2)'s self-correction corrects
  nothing that happens.** It is a more faithful mechanism for a situation the model doesn't currently contain.

> **This is the VTA lesson exactly: (2) is a real, more-faithful mechanism (Vogels/Sprekeler dynamic E-I
> tracking), and its dependency-like appeal is strong — but adding it now buys a self-correction for
> load-change that the model never undergoes, at the cost of a new rule in the plasticity layer that governs
> the ENTIRE substrate. A more load-bearing change to buy an unused capability. Do not build it this pass.**

**RULING: (1) — exempt the 8 recurrent E-I loop limbs (the `node → gate` drive and `gate → node` return of
dlPFC, vmPFC, dACC, CeA) from the eroding rules (R8 normalisation, R4 uniform scaling, and Hebbian `dw`), so
they hold their grounded load-scaled values through development. Since load is developmentally fixed, holding
the grounded weight holds the grounded ratio. This is the minimal, grounded expression of "actively maintained
rather than eroded," and it is a designation change, not a new mechanism.**

## 3. The refinement that keeps (1) honest — it is a STRUCTURAL designation, grounded, not an arbitrary exemption

**An exemption from plasticity must not read as "we froze the weights we wanted." It must be a grounded
structural designation, and it is:**

- **The biological justification is explicit and cited:** E-I balance is **homeostatically maintained at a
  set-point, not left to use-dependent modification** (the Vogels/Gerstner inhibitory-plasticity result; the
  invariant CA3-CA1 E/I ratio; "E-I balance must be dynamically maintained throughout life"). **The recurrent
  E-I loop limbs are therefore homeostatically-clamped STRUCTURAL weights — held at their grounded ratio —
  rather than use-dependent plastic edges. That is what the biology does; the exemption makes the model do it.**
- **Record it as a structural designation in the plasticity layer:** these 8 limbs are marked as
  homeostatically-maintained (E-I-clamped), with the grounding note (detailed-balance, load-scaled from the
  dACC reference) and the biological citation. **So a future reader sees a grounded designation ("E-I balance
  is actively maintained"), not an unexplained exemption.** This is the same discipline as the deletion-into-
  the-gap-register: a change to the substrate's rules is recorded with its justification, never left bare.
- **The exemption is SPECIFIC:** only these 8 limbs, only from the eroding rules. Every other edge remains fully
  plastic. **The E-I loops are the one structure biology holds homeostatically; nothing else is touched.**

## 4. Register (2) as the future mechanism IF load ever becomes variable

**(2) is not wrong — it is premature.** Register it: **if a future pass makes afferent load developmentally
variable** (e.g. synaptic pruning/growth that changes a node's afferent count during a life, or an explicitly
developing connectome), **then the fixed-weight exemption (1) no longer holds the ratio, and the true E-I-ratio
homeostat (2) becomes necessary** — inhibition would then have to dynamically track the changing excitation.
**Until load changes, (1) is correct and (2) is over-engineering. Registered as the mechanism that (1)'s
validity depends on load-invariance, and that becomes required if that assumption breaks.**

## 5. This completes Stage 1

**With the exemption, the grounded E-I balance persists into the adult substrate for the first time — which is
what Stage 1's grounding always required and never had.** The grounded relation (detailed balance, load-scaled)
AND its developmental persistence (the exemption) are the two halves of one grounding, now both in place.
**Stage 1 is complete when this lands.**

---

## 6. Handoff

**Implement (1): exempt the 8 recurrent E-I loop limbs (dlPFC/vmPFC/dACC/CeA, each `node → gate` and
`gate → node`) from R8 normalisation, R4 uniform scaling, and Hebbian `dw` — holding their grounded load-scaled
values through development. Record them as homeostatically-maintained structural weights with the grounding
note and the biological citation (E-I balance is actively maintained at a set-point, not use-dependent). The
exemption is specific to these 8 limbs; all other edges stay plastic. Keep the Stage-2 CeA edge (subsumed — it
is one of the 8). Regrow, gate ONCE on the final form.**

**Then re-measure all four outcomes on the developed agent — the first meaningful test, because the adult now
carries the grounded balance: (a) aggression recruits HYPdm/dPAG? (b) freezing floor fires? (c) the coupling
test — do freezing and aggression trade off (promoting Lump #13) or both resolve (deferring it)? (d) OFC
residual (ruling Stage 3), and no classification flips. Report all four plus the coupling verdict.**

**Register: (2) the true E-I-ratio homeostat as the mechanism required IF a future pass makes afferent load
developmentally variable (until then, (1) suffices and (2) is over-engineering); and the correction that the
model's R4-HOMEO is a rate homeostat, not an E-I homeostat (so "the existing homeostatic rule" does not
preserve E-I balance — my earlier ruling's error, now corrected).**

> **My ruling said "use the existing homeostatic rule"; you traced that the existing rule is a rate homeostat
> that would erode the balance, not hold it. Corrected: the E-I loops are held by EXEMPTION from the eroding
> rules — grounded because E-I balance is homeostatically maintained not use-dependent, and sufficient because
> the model's load is developmentally fixed so a held weight is a held ratio. The dynamic E-I homeostat is the
> right mechanism only if load ever changes; registered for that, not built now. This completes Stage 1 — the
> grounded balance finally persists into the adult. Build it, gate once, measure the developed agent, and the
> coupling question the whole staging has circled becomes answerable at last.**
