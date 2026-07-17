# `dACC-GABA` — CLEARED (`2eb5087`). Phase C released.

**Verified against `origin/main`:** 90 circuits / 226 edges. `dACC-GABA` baseline **0.05**, setpoint 0.1,
`structural_element: True`, domain `executive` (throttleable — and correctly excluded by the property, not the
domain). `BA → dACC` untouched at `moderate-strong`/anatomy/AMPA. Both xfails carry their **resolution
conditions in the test**, with the self-clearing mechanism written into the comment:
*"xfail clears → unexpected success → suite RED → revisit."* Exactly as ruled.

---

## 1. ★ The byte-identical loop is the most important line in this commit

```
dlPFC      -> dlPFC-GABA   w=moderate         recep=AMPA     basis=anatomy
dlPFC-GABA -> dlPFC        w=moderate-strong  recep=GABA-A   basis=anatomy
dACC       -> dACC-GABA    w=moderate         recep=AMPA     basis=anatomy
dACC-GABA  -> dACC         w=moderate-strong  recep=GABA-A   basis=anatomy
```

**Byte-identical, verified.** And that is not tidiness — **it is the reason the result is trustworthy.**

The brake reduced the divergence 0.0755 → 0.0534. **The obvious objection to that is: you chose a brake
strength that made the number fall.** The answer is now structural rather than rhetorical: **the bands were
INHERITED from the structural twin, not selected. Nobody could have picked them to produce that reduction,
because nobody picked them at all.**

**That is the strongest form of the anti-tuning discipline the project has produced: not "we didn't tune it,"
but "there was no degree of freedom in which to tune it."** Record the pattern — **when a new element has a
structural twin, inherit its bands byte-for-byte and say so. It converts a defence into a fact.**

---

## 2. My reachability probe was badly posed — recording it

I traced which affective sources can reach the display effectors and got answers like
`BA → CeA → HYPdm → PVN → Pituitary → AdrenalCortex → HPCv → LA → BA → NAc-core → VP → VTA → OFC → dlPFC →
vmPFC → DRN → dACC → NuFac`. **In a 226-edge recurrent graph, reachability is trivially true and depth-first
search returns whatever branch it tried first. The question is never "is there a path" — it is "is there a
short functional one."** My probe answered a question worth nothing. **Fourth self-correction this arc; noted
in the same spirit as the others.**

**But absences survive a bad probe, and three of them are real:**
```
vlPAG     -> NuFac   NO PATH
dPAG      -> NuFac   NO PATH
PAG-PANIC -> NuFac   NO PATH
```

---

## 3. ★ The modality dissociation is ARCHITECTURAL, not competitive — and Phase D is its test

**No PAG column reaches the face by any path. The face is reachable only via `dACC`.** So:

> **"Separation drives the voice; pain drives the face" is not two drives competing for a shared effector and
> one winning. It is two drives on SEPARATE LIMBS WITH NO CROSSTALK.**

**It is still emergent — nobody wired "separation → voice", and it fell out of two grounded edges landing on
different limbs. But it is currently GUARANTEED by an absence, and a dissociation guaranteed by an absence is
a weaker claim than a dissociation that survives contact.** State it that way in the record; do not let it
harden into "the model shows a modality dissociation."

**And the test already exists in the plan.** Phase D's grounded route is *"cortico-bulbar fibers to the
**face, mouth, tongue, larynx and pharynx** motoneurons"* — **it reaches BOTH effectors.** So **Phase D
introduces the crosstalk, and if the dissociation survives it, it becomes a real finding rather than an
architectural one.** Register it as a Phase D measurement, not a Phase C claim.

---

## 4. Phase C — released

**`_DISTRESS_DISPLAY` reads the EFFECTORS** (`NuFac`, `NuAmb-vocal`) — never the affective circuits. Present
on the channels the effectors reach: face → visual (`IN-CONSPEC`/`face_like`), cry → **auditory** (`IN-AUD`).
Closes chronic-distress invisibility and contagion damping **at source**. Dissolves the construct-validity
overlap — **do not touch the throttle set.**

**⚠️ Carry these disclosures into the re-measurement — the display is not a neutral instrument yet:**
- **`vicarious < direct` must be RE-DERIVED, not preserved.** It was measured off the fake display. **If it
  no longer holds, report that.** It would be the easiest thing in the world to quietly keep a result we are
  fond of.
- **The vocal half runs on `PAG-PANIC` and `dPAG` only — `vlPAG → NRA` is grounded and DORMANT** (the freezing
  column has no drive). So the display currently under-reads any distress routed through freezing.
- **The facial half runs on `BA → dACC → NuFac` alone**, in a cortex where 8 of 11 nodes are still unbraked.
- **Effect sizes are biased upward** (§18). Report magnitudes with that caveat attached; the *existence* of an
  effect is the safer claim than its size.

---

## Carried
The defensive columns wired for permission not drive (`MeA → VMH` fallback is the first suspect;
`dPAG-GABA`'s missing release is the same pass) · the cortical brake layer at 3 of 11 · the capacity measure
at matched demand · the read-out audit (two live cases) · the divergence at 0.0534 pending the brake layer ·
`dPAG` dl/l split · `dACC` cognitive/motor split · `PAG-PANIC`'s own gate · `PAG-PANIC` = dm identification ·
preBötC + respiratory rhythm · the inspiratory PAG route · `SC-Pv → dPAG` 0.50 Point-1 candidate ·
scan-vs-signature disjointness · the reactivity/regulation fusion.
