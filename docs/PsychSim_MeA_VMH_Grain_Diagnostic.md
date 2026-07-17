# `MeA`/`VMH` grain diagnostic — both edges, keystone-bound (NOTHING built; surface first)

The tenth and eleventh lumps, brought as one pass as ruled. The grain test passes for both nodes; both edges
are wrong, each in a different way; and the keystone risk is real but small. **Nothing built.**

## 1. The grain test — both nodes pass
| lump | subpopulations | transmitter | target | function | separable? |
|---|---|---|---|---|---|
| **`MeA`** | **MePV** | glutamatergic | VMHdm (our `VMH`) | predator defence (cat-odor) | **yes** — opposite tx, |
| | **MePD** | GABAergic | VMHvl (our `VMHvl`) | reproduction / aggression | opposite target, opposite function |
| **`VMH`** | **core** | glutamatergic | projects out (the drive) | defensive output | **yes** — the shell |
| | **shell** | GABAergic | inhibits the core | local gate | *gates* the core |

Both meet the grain test (different development/transmitter/projection). The `MeA` "GABA/glutamate" and `VMH`
"glutamate/GABA" transmitter fields *are* the lumps written into the data.

## 2. The two edges — each wrong, each differently
### `MeA → VMH` (the predator/defence edge; drives `vlPAG` freezing)
Currently **sign −1** (typing-order fallback: "GABA/glutamate" → GABA; S44). **Grounded value: MePV →
VMHdm is GLUTAMATERGIC → +1.** This is the sign flip that gives `VMH` (and thus `vlPAG`) its excitatory drive.
**Necessary but not sufficient** — the counterfactual (as +) revived `VMH` to 0.116 but `vlPAG` stayed 0.000;
Q2 (`vlPAG`'s real driver / the `VMH → vlPAG` band) is a separate pass, re-run *after* the node is settled.

### `MeA → VMHvl` (the aggression edge; keystone-bound)
Currently **`AMPA`, +1, w0 = 0.10.** Probably the **`CeA → vlPAG-GABA` architecture in disguise**: MePD is
GABAergic and `VMHvl`'s shell is GABAergic, so the aggression route is very likely
**`MePD (GABA) → VMHvl-shell (GABA) → disinhibits the VMHvl core`** — *right outcome, wrong mechanism*, the v9
keystone-flip's exact shape on a keystone edge. A direct GABAergic `MeA → VMHvl` would be *backwards* (it would
suppress attack); the disinhibition architecture is what makes MeA pro-aggression.

## 3. Keystone risk — real but SMALL (verify on build, don't fear it)
The aggression keystone (OBS-3) is driven by **`IN-INTERO:provocation → VMHvl`**, not by MeA. `MeA → VMHvl` is
**w0 = 0.10** — a minor additive input. So re-grounding it (to shell-disinhibition) is **low-risk** for the
keystone, which rides on provocation and on `CeA → vlPAG-GABA`/`HYPdm` at 0.70 (untouched). **But the keystone
must be re-run on the rebuilt node** — fixing one sign inside a lump is exactly how the `CeA→PAG` artifact
happened, so the guard is: build the grain, re-run the keystone, and it must hold on the *mechanism*, not just
the number.

## 4. The build options (for the ruling — I will not choose the depth alone)
- **(A) Minimal — re-ground the two edges, no node split.** `MeA → VMH` sign → glutamatergic (+); `MeA →
  VMHvl` → a `VMHvl-GABA` shell interneuron (the disinhibition architecture), like `vlPAG-GABA`. Adds one gate
  circuit (`VMHvl-GABA`), flips one sign, re-mechanises one keystone edge. *Smallest change that fixes both
  edges' mechanisms.*
- **(B) Full split — `MeA → MePV`/`MePD`, `VMH → core`/`shell`, `VMHvl → core`/`shell`.** Anatomically honest,
  but 3–5 new circuits and a re-wire of every `MeA`/`VMH`/`VMHvl` edge — a large build, and most of those edges
  are not on the fallback (so not obviously wrong). **Grain-test-passing is a reason to queue a split, not to
  do it now** (the standing rule: splits are queued, not automatic).

**My lean: (A).** It fixes the two *demonstrably wrong* edges (a typing-order sign and a wrong mechanism) at
their real grain (the shell interneuron), without splitting nodes whose other edges are not implicated. The
full `MeA`/`VMH`/`VMHvl` split is a registered candidate (the lump census, S43) — queued, its own pass. **But
this is the keystone-bound call the ruling reserved; surfacing both.**

## Carried
Q2 (`vlPAG`'s driver) re-runs after (A) or (B) settles the node. The `MeA → VMHvl` keystone edge must pass the
keystone *on mechanism* after re-grounding. `MPOA`/`BNST`/`HYPdm`/`PVN` (the other dangerous census sources)
each get their own grain pass — their fallback signs are also typing-order (S44). **Nothing built; door 1
visual `TRUE BY ANATOMY`, auditory live; #2 open on doors 2 and 3.**
