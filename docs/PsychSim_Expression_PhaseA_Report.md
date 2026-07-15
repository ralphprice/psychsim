# Expression Phase A — built; the split FLIPPED the v9 behavioural keystone (HOLDING commit)

Phase A is built as ruled. The battery was re-run. **It flipped a prior behavioural finding — reporting it,
not tuning around it.** Holding the commit for the ruling.

## Built (83→87 circuits, 214→216 seed edges; byte-additive, nothing removed but the lumped parent)
- **A1 `PAG` split** → **`vlPAG`** (passive coping: freezing/quiescence) + **`dPAG`** (active coping:
  flight/escape). Bandler & Shipley 1994; Tovote 2016. **`PAG-PANIC` untouched** — it already self-declares as
  the separate vocalisation column.
- **A2/A3 six afferents routed as ruled** — each takes the band its own anatomy supports; **no conservation, no
  invented ratio** (the lumped 0.50 was a placeholder, not a measurement; Rule 8 normalises each column's
  afferent set independently).
- **A4 `NuAmb` renamed → `NuAmb-cardiac`** (nothing moved; its two cited cardiac afferents intact) + **`NuAmb-vocal` ADDED** (compact/semicompact, laryngeal — it had no existence in the model).
- **A5 `NuFac` ADDED** (the convergence point; Kuypers 1958, Morecraft 2004).
- **A6 keystone re-expressed** to what it protects — **passes**. Plus a new test proving the Tovote mechanism is
  *implemented*, not merely cited — **passes**.
- **A7 all six callers re-pointed** (`aggress` affordance, `DEFENSIVE_OUTPUT`, `_OBS_THREAT`, `_OBS_AGGRESS`,
  `_SELF_THREAT`, `_DISTRESS_DISPLAY`→vlPAG per ruling).

### Both target cells, grounded and brought for signing (as A2 required)
| edge | target | sign | citation |
|---|---|---|---|
| `CeA → vlPAG-GABA` | vlPAG GABAergic interneurons | −1 via **cited GABA-A** (0.70 unchanged) | Tovote 2016 — *the paper the edge already cited and did not implement* |
| `BNST → vlPAG-GABA` | vlPAG GABAergic interneurons | −1 via **cited GABA-A** (0.50 unchanged) | **Hao et al. 2019 Cell Rep** — BNST/LH GABAergic long-projections onto anterior-vlPAG GABAergic cells |

**Not signed off the transmitter fallback**, as instructed. **Disclosed:** Hao establishes the projection and
target cell in a **feeding** context (**anterior** vlPAG); this edge's function here is generic defensive
"anatomy" — the *target cell* is grounded, the functional context differs. **"Anterior vlPAG" is a further
sub-grain our single `vlPAG` node lumps — audit item, not acted on.**

### Two things caught in build
- **A domain bug, self-inflicted:** `NuAmb-vocal`/`NuFac` initially inherited `defensive_threat` from the PAG
  template — which **is** temperament-throttled, so a low-THREAT temperament would have throttled the facial
  motor nucleus. Fixed to `interoception_autonomic` (the effector limb).
- **Domain flag (registered):** they are **branchiomotor**, not autonomic. The model has **no motor/effector
  domain**, and Phase A adds none. `interoception_autonomic` is in scan's `_THROTTLEABLE_DOMAINS` and feeds
  domain-mean read-outs — so **"throttle interoception" would also throttle the face/voice**: a
  construct-validity hazard of exactly the registered class.
- **Edge accounting verified:** 185 circuit→circuit + 28 channel→circuit + 3 pre-existing gaps = 216. **Nothing
  silently lost.**

## THE FINDING — the v9 neutral floor depended on the lumping
**Battery: the CU study passes in full** (punishment learning, dissociation, reads-but-doesn't-feel), **social
passes in full** (incl. `generic_threat_drives_avoidance_not_aggression`), **behaviour, learning, plasticity,
neuromodulator discipline all pass**, and **both keystone-guard tests pass**. **Three behavioural tests flipped:**

| test | was | now |
|---|---|---|
| `test_neutral_no_aggression_leak` | aggress < 1e-06 | **0.00506** |
| `test_plain_threat_still_avoids` | aggress < 1e-06 | **0.00479** |
| `test_pathway_is_behaviourally_efficacious_and_maturationally_restrained` | adult → `restrain` | **`aggress`** |

**Mechanism, pinned.** At rest: `CeA=0.517` → crushes `vlPAG-GABA` to `0.000` → `vlPAG=0.000`. But
**`dPAG=0.026`, and CeA does not project to dPAG at all.**

- **Before:** `aggress` read the **lumped `PAG`**, which `CeA→PAG (−, 0.70)` **tonically suppressed** (CeA rests
  ~0.5). The floor held because CeA sat on a node that contained the attack column.
- **After:** `aggress` reads **`dPAG`** — whose afferents are `SC-Pv(+)`, `VMHvl(+)`, `DRN(−)`. **No CeA.**
  Because **CeA's own cited projection (Tovote 2016) is to the FREEZING column (vlPAG), not the attack column.**

**So: the v9 claim "CeA is the dominant inhibitor of both attack effectors (`CeA→PAG`/`HYPdm`)" is half
artifact.** The **`HYPdm` half stands** — `CeA→HYPdm (−, 0.70)` is untouched and `HYPdm=0.000` at rest. The
**`PAG` half was column-confusion**: CeA inhibits *freezing*, not *attack*. The neutral floor was resting on a
node that lumped two opposite columns — **the lumping was doing the work.**

**This also bears on the A+B falsification** ("damping CeA disinhibits attack", which killed the ruled B fix
with clean data). That mechanism ran through `CeA→PAG` **and** `CeA→HYPdm`. The HYPdm half survives; **the PAG
half dissolves.** The conclusion (B breaks the keystone) is unchanged in direction but its stated mechanism was
partly the lumping. Recorded.

**Magnitude:** the leak is ~0.005 — the resting level of an unsuppressed `dPAG`. The test asserts `< 1e-06`,
i.e. *exactly zero*. The provocation flip rides the same leak over an already-thin margin (that keystone was
`restrain` at aggress 0.193 against a ~0.22 threshold).

## Two structural-count pins (mechanical, not behavioural)
`test_loads_the_v9_substrate` and `test_live_set_gates_by_age` assert `len(circuits) == 83`. The connectome
legitimately grew to **87**. These are state pins on connectome size — mechanical re-baseline, but **I have not
touched them either**, pending the ruling.

## The decision I need
The suite cannot be green while a committed test asserts `aggress < 1e-06`, which is now **false for a grounded
reason**. Per the ruling I have not tuned around it. So:
1. **The neutral floor** — is `aggress ≈ 0.005` at rest **acceptable emergent leak** (re-express the floor to
   what it protects: *no aggression without provocation*, i.e. provocation-specific, not literally zero)? Or is
   an unsuppressed `dPAG` at rest **a missing inhibitory element** (principle 1) — i.e. is something that
   should tonically restrain the attack column absent? *I lean the latter being the real question: the floor
   was held by a lumping artifact, so the question "what actually restrains dPAG at rest?" has never been
   asked.* **I will not answer it by re-pointing CeA→dPAG — that would be inventing anatomy to restore a
   result.**
2. **The provocation flip** — re-prove or re-characterise?
3. **The two count pins** — re-baseline 83→87?

Nothing committed. **The SC-Pv Point-1 threat-imminence finding is recorded in-seed and NOT acted on**, as
ruled.
