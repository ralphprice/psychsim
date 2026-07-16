# The defensive-drive pass — diagnostic (door 1's blocker; NOTHING built; grounding surfaced)

The registered S20 item ("the defensive columns are wired for permission but not for drive") is now door 1's
blocker. Diagnosed both halves. **The first suspect is confirmed but not sufficient, and the second half needs
a cited source I can't fetch.** Surfacing before building.

## Half 1 — `vlPAG`'s drive (the freezing column reads 0.000 in every condition)
`vlPAG` afferents: `vlPAG-GABA` (⊣, the gate — the *permission*, built), `DRN` (⊣, 5-HT1A), and **`VMH` (+,
`low-moderate`) — its only excitatory drive.** `VMH` is excitation-unafferented: `MPOA` (⊣) and `MeA`.

### ★ The first suspect (S20) is CONFIRMED — and it is silently inverting the drive
`MeA → VMH` carries **receptor `None` → the transmitter fallback → sign −1** (MeA is "GABA/glutamate", the
fallback picks GABA). So **MeA *inhibits* VMH**, and with `MPOA → VMH` also inhibitory, **VMH has no excitatory
afferent at all → 0.000 → `vlPAG` = 0.000.** Meanwhile the *same source* `MeA → VMHvl` is cited **AMPA** (+).
Same nucleus, two targets, one decided and one on the fallback — and the fallback is not merely undecided, it
is **inverting the one edge that could drive the freezing column.**

### ⚠️ But grounding it is NECESSARY, NOT SUFFICIENT — the gap is deeper than one edge
Counterfactual (MeA→VMH as AMPA, a *mechanism probe, not a proposal*): VMH revives (0.000 → 0.116) **but
`vlPAG` STAYS 0.000.** `VMH → vlPAG` (`low-moderate`) is too weak to cross `vlPAG`'s `DRN` inhibition and its
gate. So the freezing column is doubly-broken:
- (a) `VMH` is dead (the `MeA → VMH` fallback), **and**
- (b) even a live `VMH` cannot drive `vlPAG` through the weak `VMH → vlPAG` synapse.

**The grounding questions (both need the anatomy, not a guess):**
1. **`MeA → VMH`'s receptor** — is the projection glutamatergic (+) or GABAergic (−)? MeA is heterogeneous;
   **do not assume symmetry with `MeA → VMHvl`'s AMPA** (the reviewer's own caution). This decides whether VMH
   can be driven at all.
2. **What actually drives `vlPAG` freezing once it is disinhibited?** Is `VMH` (the medial-hypothalamic
   defensive system) the driver, under-weighted here — or is there a missing direct excitatory afferent
   (e.g. a direct `CeA → vlPAG`, distinct from the `CeA → vlPAG-GABA` disinhibition)? The permission is built;
   the drive is not, and one weak edge from a dead node is not it.

## Half 2 — `dPAG-GABA`'s release (escape can never fire — the flight drive is blocked)
`dPAG-GABA`'s only afferent is **`DRN` (5-HT2A, +)** — which drives the gate *UP* (more escape inhibition).
**There is no projection that drives it DOWN.** So the escape gate is tonically ~0.19 and **never dips** —
whereas Stempel & Evans show VGAT⁺ activity *decreases* at escape onset (escape is **disinhibition**). Our gate
has no release, so the flight drive (`SC-Pv → dPAG`, the weak Point-1 synapse) can never cross it — the S37
finding, one level up.

**The precedent names exactly what's missing:** `vlPAG-GABA` (the freezing gate) receives **`CeA` (GABA-A, ⊣)**
and **`BNST` (GABA-A, ⊣)** — forebrain *inhibitory* projections that disinhibit freezing (its release). **The
escape gate `dPAG-GABA` has no such forebrain inhibitory afferent.** The source dPAG-GABA is grounded on names
the class: *"inhibitory long-range forebrain projections onto local PAG GABAergic circuits."*

**The grounding question:** which forebrain source disinhibits *escape* (projects inhibitory onto
`dPAG-GABA`)? It is not `CeA` (that one is on the freezing gate, Tovote). Candidate classes to research: the
medial hypothalamic defensive system / PMd, the BNST, or the amygdala via a distinct population — **grounded,
cited, not chosen by symmetry with the freezing gate.**

## What this pass is, and what it needs
Both halves are **grounding questions I cannot resolve without the anatomy** (no external access this session):
`MeA → VMH`'s receptor and `vlPAG`'s real driver (Half 1); the forebrain source of `dPAG-GABA`'s release
(Half 2). **Nothing built.** The one thing established mechanically: the `MeA → VMH` fallback is confirmed as an
inverting edge (S20's suspect), and it is necessary-but-not-sufficient — so even that fix is not a
one-edge job.

**When it lands it unblocks, in one pass:** `DEFENSIVE_OUTPUT` · `_OBS_THREAT` · `_SELF_THREAT` · `_OBS_AGGRESS`
· `vlPAG → NRA` · the escape circuit (S37) · **and door 1's visual channel** (the flight drive that `SC-Pv →
dPAG` needs). Surfacing for the grounding ruling. **Door 1 UNRESOLVED; #2 open on doors 2 and 3.**
