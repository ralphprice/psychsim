# Expression Phase A — close-out: the floor was held by an artifact; the real element restores it at its grounded rate

## The headline
**The v9 neutral floor was passing for the wrong reason.** It held because `CeA→PAG (−,0.70)` tonically
suppressed a **lumped** node — while CeA's own citation (Tovote 2016) puts it on the **freezing** column.
**CeA does not project to dPAG at all.** The model was restraining attack with a projection that, in the real
anatomy, restrains nothing of the sort.

It did **not** mean aggression was coded — the `CeA→HYPdm` half stands, untouched, at 0.000. It meant **the
check that would have caught it was not checking.** The floor's *logic* was right; its *mechanism* was luck.

**What actually restrains dPAG at rest had never been asked** — because the artifact was answering it.

## The missing element (principle 1: instability = a missing pathway)
**`dPAG-GABA`** — the tonically-active local GABAergic gate. [Stempel & Evans et al. 2024, *Current Biology*](https://pmc.ncbi.nlm.nih.gov/articles/PMC7617961/) (DOI 10.1016/j.cub.2024.05.068):
- VGAT⁺ dPAG neurons fire **tonically in the absence of synaptic input** — autonomous, like the LC pacemaker.
- They are the **major source of inhibition to the VGluT2⁺ (output) dPAG neurons**.
- **Their activity sets the escape threshold** (dips at escape onset, peaks at termination).

**Baseline grounded from the electrophysiology, set before looking at the floor** (the LC pacemaker ruling,
verbatim): `baseline_activation` is the **no-synaptic-input** relaxation target, and the intrinsic rate
measured **under synaptic blockade is 6.2 ± 0.84 Hz**; against the dPAG strong-drive reference (silicon-probe
high-firing population, **32.2 ± 7.0 Hz**) → **6.2/32.2 ≈ 0.19**. **Setpoint paired to it** (principle 10).

## The result — at the grounded rate, whatever it gives
| | |
|---|---|
| `dPAG` at rest | **0.0000** |
| independent check | the paper reports VGluT2⁺ **essentially silent** at rest (0.11 ± 0.068 Hz; 92.8% < 0.04 Hz ⇒ ≈0.003 normalised). **The model matches it without being asked to.** |
| `test_neutral_no_aggression_leak` | **passes** |
| `test_plain_threat_still_avoids` | **passes** |
| `test_pathway_is_behaviourally_efficacious_and_maturationally_restrained` | **passes** (adult → `restrain`) |
| battery | **44/44** |

**Proof the mechanism carries it** (silence-the-element-and-it-runs-hot): silence `dPAG-GABA` → `dPAG` leaks
**0.0000 → 0.0202**. The floor is held **by the tonic gate at its grounded rate** — not by CeA, not by a number
chosen to restore it.

**The provocation flip was the same finding, not a second one** — one cause with the floor flip, and it
resolved with the real element. Never characterised (principle 6 extended).

## Independently validated: one architecture, every column
The same source states the general rule: *"Disinhibition of the PAG has been suggested as a mechanism for
initiating other instinctive behaviours, such as vocalisations and freezing, with inhibitory long-range
projections from forebrain regions inhibiting local GABAergic circuits within the PAG."* That is
**`CeA → vlPAG-GABA` arrived at independently, from a different literature, stated as the architecture.** The
Phase A build is the special case; this is the rule. (Registered for Phase B: `PAG-PANIC` very likely needs its
own gate — vocalisation is named as disinhibition-initiated.)

## The DRN flag retired by the target cell — the third target-cell resolution this phase
The flag said *"PAG 5-HT 1A/2A mixed"* because the receptors have **opposite molecular effects** yet **both
inhibit escape**. The resolution is the **cell**, not the receptor:
- **`DRN → dPAG-GABA` on 5-HT2A** (Gq, **+**) → excites the gate → **net inhibition of escape**.
- **`DRN → dPAG` on 5-HT1A** (Gi, **−**) → direct hyperpolarisation → **also inhibition of escape**.

**Two receptors, opposite signs, same behavioural outcome — because they land on different cells.** The
receptor-derived-sign convention is vindicated, not strained. (The vlPAG arm's column ambiguity is unaffected
and still flagged.)

## Also built (A1–A7)
`PAG`→`vlPAG`+`dPAG` (PAG-PANIC untouched — already the third column); **`vlPAG-GABA`** (CeA + BNST both target
it — Tovote 2016 / **Hao et al. 2019**, both cited GABA-A, *not* transmitter fallback); six afferents routed with
**no weight conservation** (Rule 8 normalises each column independently); `NuAmb`→**`NuAmb-cardiac`** rename +
**`NuAmb-vocal`** added; **`NuFac`** added; keystone **re-expressed to what it protects** (CeA GABAergic; drive
byte-identical 0.70/inhibitory; target explicit) plus a new test proving the Tovote mechanism is *implemented*,
not merely cited; all six callers re-pointed; count pins re-baselined **83→88 with the delta named**.

**Edge accounting verified: 185 circuit→circuit + 28 channel→circuit + 3 pre-existing gaps = 216. Nothing lost.**

## Registered (not acted on)
- **New principle:** *a passing keystone certifies the OUTCOME, not the mechanism that produced it. An artifact
  can hold a keystone, and then the keystone certifies nothing. Always ask what is holding it.*
- **Principle 6 extended:** no behavioural characterisation from a partial assembly.
- **Domain is a throttle surface** — a construct-validity decision, not taxonomy. The self-inflicted bug
  (effectors inheriting `defensive_threat`, temperament-throttled) would have made *"low-threat agents show less
  facial expression"* true by construction — the **second** such bug caught in this arc, both before they became
  findings. **Eighth domain (motor/effector, temperament-unreachable) = Phase D prerequisite.**
- **A+B falsification narrowed** — HYPdm half survives, PAG half dissolves; conclusion stands on a narrower
  basis; the test should be re-run now the floor is honest. **B not re-opened.**
- **`dPAG-GABA` in-network runs ~2× the observed** (model 0.289 vs paper's 4.7 Hz ≈ 0.146) — and
  **directionally wrong**: the real network *dampens* this cell (6.2→4.7 Hz), ours *excites* it, because
  `DRN→dPAG-GABA` is currently its only input. Candidate missing inhibitory input. **Reported, not tuned.**
- Carried to the audit: Hao's feeding context; "anterior vlPAG" as an un-modelled sub-grain; **`SC-Pv→dPAG` at
  0.50 against a literature that calls that synapse weak** (the Point-1 threat-imminence candidate — its own
  pass, not now).
