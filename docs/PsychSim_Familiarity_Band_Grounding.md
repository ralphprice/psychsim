# The IN-CONSPEC familiarity band — grounding. **The two arms are correct, and the neuroscience is decisive.**

**I researched the social-recognition circuit before naming anything, because the emergent response depends on
the routing and I will not guess it. The literature is unambiguous, the two-arm structure is confirmed and
grounded, and there is one genuine substrate-grain decision that is yours — I lay it out in §4.**

---

## 1. The circuit is real, specific, and well-characterised: dCA2 → (oxytocin / lateral septum)

**Familiar-conspecific recognition — "this individual is known, and known as safe or as a threat" — is one of
the better-mapped social circuits, centred on the dorsal CA2 hippocampal region:**

> **dCA2 is the recognition centre:** *"the dorsal CA2 region of the hippocampus enables the discrimination of
> novel from familiar conspecifics"* — it *"encodes familiarity separately from identity in an abstract, low-
> dimensional format,"* storing familiar individuals in high-dimensional representations (the memory of past
> encounters). Ventral CA1 (receiving dCA2) stores the familiar-conspecific memory.
> **★ And the decisive finding for our two arms (Kassraian et al., *Nature Neuroscience* 2024):** dCA2
> *"discriminates social threat from social safety"* and **incorporates "an abstract representation of social
> VALENCE into representations of social identity."** Silencing it *"gives rise to generalized social
> avoidance"* — the animal can no longer tell the safe individual from the threatening one, and defends against
> both.
> **The two output arms are named explicitly:** the **approach/bonding arm** runs through **oxytocin** (dCA2
> OXTR signalling, oxytocin from the **PVN**) promoting recognition and affiliative approach; the
> **aggression/avoidance arm** runs **dCA2 → lateral septum → VMHvl** (a "top-down control of aggression
> through a social memory center") and **ventral hippocampus → lateral septum** driving novelty/avoidance
> behaviour.

> **So the neuroscience says exactly what your two-arm proposal says, and says WHY: a known other is recognized
> (dCA2), that recognition carries a learned valence (safe vs threat), and the valence routes either to the
> oxytocinergic approach system or to the septo-hypothalamic defensive/aggression system. A positively-regarded
> known other and a distrusted known other are the two grounded output paths of one recognition circuit.**

## 2. What exists in the substrate (verified)

- **The recognition regions (CA2, ventral CA1, lateral septum) are NOT present as nodes** — but **HPCv
  (ventral hippocampus) IS** (currently framed as spatial threat-context, but it is anatomically the ventral-
  CA1 region that carries the social-memory story).
- **Both target systems for the two arms exist and are exactly the existing IN-CONSPEC template targets:**
  **PVN-OT** (the oxytocinergic approach/bonding target — already the destination of `IN-CONSPEC:kin_signature`)
  and **CeA** (the defensive target — already the destination of `IN-CONSPEC:formidability_cue`). The
  aggression-specific target **VMHvl** also exists.

> **This is a clean grounding: the two arms route to systems that already exist and that already receive the
> analogous IN-CONSPEC recognition cues (kin → PVN-OT for bonding; formidability → CeA for defence). The
> familiarity band is the same pattern — a recognition cue borne by a specific known other, routed to the
> approach or defence system, valued by the perceiver's own circuits.**

## 3. RULING — the two arms, grounded

- **`IN-CONSPEC:familiar_warm` → PVN-OT** (oxytocinergic approach/bonding). Mirrors `kin_signature → PVN-OT`.
  **A positively-regarded known other presents as a recognition cue that engages the perceiver's oxytocin/
  bonding system** — grounded in dCA2 OXTR → affiliative approach. Receptor/weight: mirror the `kin_signature`
  template (moderate-strong, the same receptor treatment).
- **`IN-CONSPEC:familiar_wary` → CeA** (defensive). Mirrors `formidability_cue → CeA`. **A distrusted/hostile
  known other presents as a recognition cue that engages the perceiver's defensive system** — grounded in the
  dCA2/vHPC → lateral septum → defensive/avoidance arm. Receptor/weight: mirror the `formidability_cue`
  template (low, same receptor treatment).
- **The non-negativity constraint is correctly handled by two arms** (a single channel cannot carry signed
  valence given `felt_response`'s `[0,1]` clamp). The arena constructs the cue with the P1 colouring math in
  role — **familiarity gates magnitude, the sign of stored affect selects the arm, trust modulates magnitude** —
  and routes it; the perceiver's circuits produce the response. **Valuation stays with the perceiver; only the
  recognition (a known other, warmly or warily regarded) is presented.** Emergence wall intact.

**Signs/targets are grounded, not guessed:** warm → oxytocin/approach, wary → amygdala/defence, which is the
literature's own division of the recognition circuit's output.

---

## 4. ★ The one substrate-grain decision — YOURS, because it sets a precedent

**There are two anatomically-defensible ways to add this, and the choice is about the substrate's established
grain, not about correctness. I have a recommendation but this is yours to set:**

**Option (i) — direct IN-CONSPEC edges to the valuation targets (mirror the existing template).**
`IN-CONSPEC:familiar_warm → PVN-OT` and `IN-CONSPEC:familiar_wary → CeA`, exactly as the three existing
IN-CONSPEC bands are wired (each goes straight from the cue to the valuation system, with no intervening
recognition node). **Consistent with the established grain; minimal; the recognition-memory computation is
abstracted into the cue construction (as `kin_signature`'s self-similarity computation already is).**

**Option (ii) — add an explicit dCA2 / social-recognition-memory node** that the familiarity cue routes
through, which then projects to PVN-OT (warm) and CeA/lateral-septum (wary). **Anatomically more faithful — it
represents the recognition centre as a real region — but it is a NEW node with multiple new edges, larger, and
it introduces a region the other IN-CONSPEC cues don't route through (they go direct), creating an
inconsistency unless they're also re-routed.**

> **My recommendation: (i) for this pass.** Reasons: (a) **it matches the established grain exactly** — all
> three existing IN-CONSPEC bands go direct from cue to valuation target, and the recognition computation lives
> in the cue construction (`kin_signature` is a self-similarity function computed before the channel; the
> familiarity cue is likewise computed from the stored relationship before the channel). (b) Adding a dCA2 node
> **only here** would make the familiarity cue inconsistent with its three siblings, and re-routing all of them
> through a new hippocampal node is a substrate-restructuring pass in its own right. (c) It is the minimal
> honest addition that closes the pass. **Register the explicit dCA2/vCA1/lateral-septum social-recognition-
> memory node as a later fidelity item** — it is a real region and a faithful substrate should eventually have
> it (and HPCv is already the ventral-hippocampal seed of it), but adding it belongs in a dedicated social-
> memory-anatomy pass, not bolted on here.

**This is exactly the lumping question the substrate has hit twelve times: the recognition circuit is currently
"lumped" into the cue construction + the direct edge, and the honest un-lumping (an explicit dCA2 node) is a
registered future pass, not this one. Matching the template keeps the grain consistent; the un-lumping is
deferred with the others.** But it is your call to set the precedent — if you want the faithful node now, it is
(ii), and it is larger.

---

## 5. Handoff
**Grounding delivered: two arms, `familiar_warm → PVN-OT` (oxytocin/approach, mirror `kin_signature`) and
`familiar_wary → CeA` (defence, mirror `formidability_cue`), signs and targets grounded in the dCA2 social-
recognition-memory circuit. The one decision I need back from you: (i) direct edges matching the template
[recommended, minimal, grain-consistent] or (ii) an explicit dCA2 recognition node [faithful, larger, sets a
re-routing precedent].**

**Once you confirm (i) or (ii):** add the band(s) + F1 (`accrue_relationship`) + F3 (harness fork), regrow
once, test the arena relationship-on/off diff, then F4 (`run_life` integration), test the pass claim against
the environment-only baseline. The build session's proposed order holds; F1 and F3 can be built first while
this is confirmed, as offered.

> **The familiarity band is grounded in the social-recognition-memory circuit (dCA2 → oxytocin/approach vs
> septo-defensive), the two arms are forced by both the anatomy and the non-negativity constraint, and the
> targets already exist and already receive the analogous recognition cues. The perceiver values its history
> through its own circuits; the band only presents the recognition. One grain decision is yours; the rest is
> grounded and ready.**
