# S56 Stage 2 — **build the one-edge loop closure, but understand precisely what it can and cannot fix.**

**The build session's diagnosis is structurally correct and its recommendation is right — but I verified the
CeA output structure and found a tension that changes what we should EXPECT from the one-edge fix, and makes
the measurement afterward decisive for whether Lump #13 is deferred or promoted. Here is the ruling.**

---

## 1. The one-edge diagnosis is confirmed

Verified: **CeA has the return limb (`CeA-GABA → CeA`, strong) but NOT the drive limb (`CeA → CeA-GABA` is
absent).** `CeA-GABA` is driven only by `PVN-OT` (feedforward) — exactly the feedforward-blindness. The three
cortical gates have closed loops; CeA uniquely has only the return. **So closing the loop with a single
`CeA → CeA-GABA` excitatory edge — load-scaled under Stage 1's detailed-balance relation, clamping to 1.0 at
CeA's ~15 afferents (the same honest ceiling as dlPFC) — gives CeA the drive-proportional self-brake its
siblings have and it alone lacks. That is a real, grounded, structurally-consistent fix, and it is the correct
Stage 2.**

## 2. ★ But the verification found the tension: the lump COUPLES the two defects through opposite-signed outputs

**This is the part that changes the expectation, and it is why the build session's own observation ("the
one-edge fix doesn't give selection") matters more than a scope nicety:**

```
CeA -> vlPAG-GABA (GABA-A, inhibitory) -> vlPAG    [Tovote: CeA DISINHIBITS vlPAG → MORE CeA = MORE freezing]
CeA -> HYPdm      (inhibitory)                       [CeA SUPPRESSES HYPdm    → MORE CeA = LESS aggression]
```

**The two standing defects run through CeA outputs of OPPOSITE behavioural sign:**
- **The freezing floor needs MORE effective CeA drive to vlPAG** (to disinhibit the freezing column).
- **The aggression output needs LESS CeA suppression of HYPdm** (to release the attack drive).

> **In a LUMPED CeA, these are the SAME activation. A single self-brake that lowers CeA uniformly — which is
> exactly what the one-edge loop closure does — would help release HYPdm (good for aggression) but
> SIMULTANEOUSLY reduce the drive to vlPAG-GABA's inhibition... i.e. it lowers CeA's disinhibition of freezing
> (bad for the floor). The one-edge fix cannot cleanly fix both, because in a single-node CeA the freezing
> drive and the HYPdm suppression are one quantity pulling in two behavioural directions.**

**This is the precise mechanistic reason CeA needs SELECTION, not just gain.** Winner-take-all CeA (CEl→CEm)
exists in biology exactly so that the freezing mode and the aggression mode are DIFFERENT CeA output states,
not the same activation. The model's lump makes them inseparable. **So the one-edge closure fixes the
SATURATION (the runaway) but not the COUPLING (the shared activation) — and the coupling is what stands between
a de-saturated CeA and fixing BOTH defects.**

## 3. RULING — build the one-edge closure as Stage 2; let the measurement rule Lump #13's priority

**Build the one-edge loop closure. It is the correct minimal, grounded Stage 2 — but its role is now sharper:
it is the fix that will TELL US whether the two defects are separable without un-lumping.**

1. **Build `CeA → CeA-GABA`** (load-scaled, detailed-balance relation, clamps to 1.0 — the same grounded
   relation and the same honest ceiling as Stage 1's dlPFC). This de-saturates CeA: gives it the
   drive-proportional self-brake its siblings have.
2. **Gate on the full suite and measure the four outcomes — but read (a) and (b) TOGETHER, as the coupling
   test:**
   - **(a) does aggression recruit HYPdm/dPAG?** (de-saturation should release HYPdm)
   - **(b) does the freezing floor fire?** — **and critically, does releasing HYPdm come AT THE COST of the
     freezing drive?** If (a) improves but (b) regresses or stalls, **that is the coupling biting — the
     evidence that a lumped CeA cannot serve both modes, and that Lump #13 (CEl/CEm un-lumping) is REQUIRED,
     not optional.**
   - **(c) what OFC residual remains** (ruling Stage 3).
   - **(d) no classification flips** (a substrate-selection fix should not change outcomes).
3. **The measurement determines Lump #13's priority:**
   - **If de-saturation resolves BOTH defects** (aggression recruits HYPdm AND the floor fires) → the coupling
     was not binding at these activation levels; the one-edge fix suffices; Lump #13 stays a deferred fidelity
     pass.
   - **If de-saturation trades one for the other** (HYPdm releases but the floor stalls/regresses, or vice
     versa) → **the coupling is binding, and Lump #13 is promoted from deferred to the required next step** —
     because only separating CeA into CEl/CEm output modes can let freezing and aggression be different CeA
     states. **This would be the measurement promoting the un-lumping, exactly as the harsh-mirror measurement
     promoted S56 itself.**

> **This is the honest structure: the one-edge closure is correct and minimal and worth building, AND it is the
> diagnostic that reveals whether the lump must be resolved now. We do not pre-emptively un-lump (the lumping
> discipline — the dCA2 node, the twelve prior lumps, all deferred until measurement demanded them). We build
> the minimal grounded fix, and we let the coupling — if it bites — promote Lump #13 on evidence. Either way
> the one-edge fix is the right next build; the question is only whether it is sufficient, and the measurement
> answers it.**

## 4. Why not un-lump now (the lumping discipline holds)

The full CEl/CEm un-lumping re-routes 18 afferents and 6 outputs — a dedicated substrate-restructuring pass
(Lump #13). **Per the discipline applied twelve times (and to the dCA2 recognition node two passes ago): un-
lumping is its own deliberate pass, opened when measurement demands it, not bolted onto a gain fix.** The
one-edge closure is the grounded, structurally-consistent, minimal Stage 2. **If the measurement shows the
coupling blocks one defect, Lump #13 opens next with a clear mandate; if not, it stays deferred. The
measurement decides — which is the whole point of staging.**

---

## 5. Handoff

**Build Stage 2: the single `CeA → CeA-GABA` excitatory edge, load-scaled under Stage 1's detailed-balance
relation (clamps to 1.0 at CeA's ~15 afferents — the heaviest node, same honest ceiling as dlPFC). This
de-saturates CeA. Regrow (it is a connectome change), gate on the full suite.**

**Measure the four outcomes, reading (a) and (b) together as the coupling test: if de-saturation releases HYPdm
AND fires the floor, the one-edge fix suffices and Lump #13 stays deferred; if it trades one defect for the
other, the coupling is binding and Lump #13 (CEl/CEm un-lumping) is promoted to the required next step. Report
all four, and the coupling verdict.**

**Register: CeA as the heaviest node (~15 afferents) hitting the ceiling clamp (same as dlPFC); the CeA
saturation/coupling finding (the two defects run through opposite-signed CeA outputs, inseparable while
lumped); and Lump #13 (CEl/CEm un-lumping) as deferred-pending-the-Stage-2-measurement.**

> **Stage 2 is the one-edge loop closure — grounded in the same detailed-balance relation as Stage 1, giving
> CeA the self-brake its siblings have and it uniquely lacks. It fixes CeA's saturation. Whether it fixes both
> standing defects depends on whether the lump's coupling of freezing-drive and aggression-suppression binds —
> and the measurement after this build is exactly what reveals that, promoting the CEl/CEm un-lumping on
> evidence if the coupling holds. Build the minimal grounded fix; measure the coupling; let it rule Lump #13.**
