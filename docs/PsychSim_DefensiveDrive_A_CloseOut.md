# Defensive-drive (A) — the MeA/VMH re-grounding built; keystone holds on the mechanism; the freezing floor is trivially held

Built (A) as ruled: the two edges re-grounded at their real grain, the shell interneuron added, the keystone
re-run on the mechanism, the lump's cost and the predator-odor channel gap disclosed. **And the honest catch:
the sign flip revived the driver but not the output — `vlPAG` still doesn't fire (Q2), so the freezing floor is
held by an absence, not a mechanism.** Reported, not papered over.

## Built (94→95 circuits, +2/−1 edges; regrown)
- **`MeA → VMH` sign RE-GROUNDED to glutamatergic (+1)** — MePV→VMHdm is glutamatergic (cat-odor predator
  defence). The fallback had it at **−1 purely by transmitter-field typing order** (`"GABA/glutamate"` → GABA;
  S44), silently suppressing the defensive column. This revives `VMH` (0.000 → 0.116).
- **`VMHvl-GABA`** — the shell interneuron, the twin of `vlPAG-GABA` (scaffold baseline, `structural_element`,
  recurrent-E-I class — no rate forced; bands inherited byte-for-byte).
- **`MeA → VMHvl-GABA` (GABA-A, −)** replacing the old `MeA → VMHvl` AMPA-direct edge: **`MePD (GABA) → shell
  → disinhibits the core`** — the `CeA → vlPAG-GABA` disinhibition architecture, right outcome by the right
  mechanism now (the AMPA-direct was right-outcome-wrong-mechanism, the v9-flip shape).
- **`VMHvl-GABA → VMHvl` (GABA-A, −)** — the shell inhibits the core (band inherited from `vlPAG-GABA → vlPAG`).

The receptor convention gives sign **per edge**, so `MeA` is glutamatergic to `VMH` *and* GABAergic to
`VMHvl-GABA` simultaneously, both right — while the node stays lumped (see the cost, below).

## The aggression keystone — HELD, on the mechanism
- neutral → VMHvl 0.000 (no leak); provocation → **VMHvl 0.725 → dPAG 0.361, HYPdm 0.173** (attack effectors
  recruited). `test_aggression_pathway` passes in full.
- **The mechanism, not just the number:** `MeA` tonically crushes the shell (`VMHvl-GABA` → 0), so `VMHvl` is
  tonically disinhibited and fires on its own provocation drive — a *weaker* MeA contribution than the old
  direct +0.10, so the keystone rides on `provocation → VMHvl` + `CeA → effectors` at 0.70 (byte-untouched), as
  it should. Re-run and interrogated per the discipline; it holds because the driver is provocation, not MeA.

## ★ The honest catch — the freezing floor is held by an ABSENCE (the v9 lesson, obeyed)
The ruling's premise was *"this is the first time vlPAG can fire."* **Measured, it is not yet:** the sign flip
revived `VMH` (the driver) but `vlPAG` still reads **~0.008** in every condition — `VMH → vlPAG` (low-moderate)
is too weak to cross `vlPAG`'s DRN inhibition and gate. **So freezing still cannot fire (Q2, its own pass).**

I built the freezing-floor guard (`TestFreezingFloor`: neutral & conspecific → no freezing) **and flagged it
exactly:** it passes **trivially, because the output is dead, not because a floor restrains it** — *a floor
that has never existed is not a floor that has held* (the aggression floor once held on a lumping artifact;
this is the same shape). It becomes a **real** floor — one that could be violated — only when Q2 gives `vlPAG`
its drive. The guard documents the requirement and will start to bite when the column lives. **Asked what holds
it; the answer is Q2, not a mechanism.**

## Disclosed in-seed (S45), not the commit message
- **The lump's COST:** `MeA` is functional-but-unresolved. MePV and MePD fire **together** (one activation), so
  a predator cue and a conspecific cue drive **both** routes. This stays until the input surface can separate
  them.
- **The predator-odor CHANNEL GAP:** MePV is *defined* by predator-odor response, but `MeA ← PIR, V-ventral`
  only — no predator channel. **This is why `MeA` cannot be split** (MePV/MePD would be undrivable-apart — the
  `PrH` block, the third recursion), and it is why (B) was unbuildable, not merely large. Joins the input-
  surface gaps (S42); the input-surface audit predicted it before it was needed.

## Verification
`test_aggression_pathway` green (keystone on mechanism + freezing floor); count pins 94→95; `VMHvl-GABA`
correctly scaffold (reconciliation passes); regrown; full suite (golden regenerated if the sign flip's revived
`VMH` shifts the develop snapshot — a grounded, demonstrated change). `CeA → effectors` byte-untouched at 0.70.

## Order
`IN-AUD → COCH` (its own pass, own clearance — startle fires for the first time) → **Q2: `vlPAG`'s drive** (the
`VMH → vlPAG` band, on the now-settled node — this is what makes the freezing floor real) → door 1's auditory
half → the channel gaps (`PB-LOOMING` the escape trigger, `PR-SALT`, `PR-HOMEOSTATIC`, predator-odor,
`IN-PROPRIO`). **Door 1: visual `TRUE BY ANATOMY` (measured), auditory live. #2 open on doors 2 and 3.**
