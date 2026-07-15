# Emotional Expression (Level 5) — code diagnostic (NOTHING built; surfacing before any build)

Answers to the §8 questions, against the connectome at `0aa9285`. **Headline: the reference's prediction is
confirmed and is worse than "no expression system" — the emotional motor system EXISTS and is ENTIRELY
UNEFFERENTED. Every one of its nodes is a dead end. And the CU expression payoff (§6) is not currently
testable at all.**

## Q1 — Is PAG afferented as the expression hub? YES (6 afferents) — but the sign tension is real
| afferent | sign | receptor | w |
|---|---|---|---|
| `CeA→PAG` | **−** | *(none cited — transmitter fallback: CeA is GABAergic)* | 0.70 |
| `BNST→PAG` | + | (fallback) | 0.50 |
| `SC-Pv→PAG` | + | (fallback) | 0.50 |
| `VMH→PAG` | + | (fallback) | 0.35 |
| `VMHvl→PAG` | + | (fallback) | 0.85 |
| `DRN→PAG` | − | 5-HT1A | 0.50 |

So PAG has excitatory limbic drive (BNST/VMH/VMHvl/SC-Pv) — but **the amygdala's drive is INHIBITORY**, where
§2.1 puts the amygdala among PAG's *excitatory* controls. **This is the same shape as the CeA→LC problem**
(CeA is GABAergic, so its excitatory drive of a brainstem target must be a distinct cited projection — CRF-R1
there). **But it collides with a committed keystone:** `test_cea_to_attack_effectors_still_inhibitory_and_unchanged`
asserts `CeA→PAG` is inhibitory at *byte-exactly* 0.70 (the v9 aggression result rides on it). **Not resolvable
unilaterally — surfaced, not touched.**

## Q2 — Is PAG-PANIC connected downstream? **NO. It is a dead end.**
`PAG-PANIC` (in-seed: *"the infant-cry/protest output"*): afferents `MPOA(−), PVN-OT(+), dACC(+), SEPT(−)` +
channel `IN-INTERO:contact_loss`; **efferents: NONE**. The cry output exists, is driven — and **drives
nothing**. This is the **mirror** of the PVN-OT/LC gap: **unefferented**, not unafferented. The reference was
right to say check both directions.

## Q3 / Q5 — Does any cortical route reach the expression effectors? What would a display be read from?
**The entire emotional motor system is unefferented:**
| circuit | in | out | |
|---|---|---|---|
| `PAG` | 6 | **0** | dead end |
| `PAG-PANIC` | 4 | **0** | dead end |
| `NuAmb` | 2 | **0** | dead end |
| `SympOut` | 1 | **0** | dead end |
| `HYPdm` | 3 | 1 | → PVN |
| `IML` | 3 | 1 | → SympOut (→ nothing) |

**There is nothing to read a display from.** The EMS produces no output whatsoever. And `NuAmb` — the
vocalisation/laryngeal effector, the thing that would actually *make the cry* — is driven **only by PVN(+) and
NTS(+)**, i.e. autonomics. **`PAG→NuAmb` is MISSING**: the canonical vocalisation pathway, PAG's own defining
output (§2: "PAG lesions cause complete mutism"), does not exist. The hub of the emotional motor system is not
connected to the motor system.

**Only ONE cortical route reaches an expression hub: `dACC→PAG-PANIC (+)`** — and it is **excitatory**. That
matches §2 (ACC *instructs* PAG to vocalise) but it is an instruction, **not** a suppressor. `OFC` and `aIns`,
which §2 also has instructing PAG, reach it **not at all**.

## Q4 — Does anything inhibit PAG from premotor/motor cortex? **NO — and there is no motor cortex.**
Inhibitory afferents to PAG/PAG-PANIC are `CeA→PAG`, `DRN→PAG`, `MPOA→PAG-PANIC`, `SEPT→PAG-PANIC` — **all
limbic/subcortical, none volitional**. Stronger: **`M1`, premotor/lateral-premotor, `SMA`, and the facial
nucleus are ABSENT from the model entirely** (83 circuits; none of them present). So:
- **No volitional pathway** → no posing, no displays-without-feeling.
- **No volitional suppressor** → §2.1's *"volitional system descending from lateral premotor cortices that can
  suppress"* has no substrate.
- **We have built an agent with pathological laughing/crying**, exactly as the reference predicted — except it
  cannot even laugh or cry, because the output is unefferented.

`preSMA` (the in-seed *"motor inhibition interface (to STN)"*) is the one candidate — but it goes **only to
STN**. It brakes **action selection**, not expression. `vlPFC→preSMA→STN` is a complete action brake with **no
expression branch**.

## Q6 — Is the regulation network wired to anything expressive? **Essentially no.**
`dlPFC →` MDthal, S2-PPC, Caud-assoc, vmPFC, NAc-core, dmPFC, dlPFC-GABA — nothing expressive.
`vlPFC →` preSMA, STN, ITC — action brake only. `dmPFC →` LA, BA, rSMG-TPJ, PCun-PCC. `OFC →` NAc-core, VTA,
dlPFC, DRN, DRN-GABA. `aIns →` dACC, CeA, OFC, PBN, PVN, rSMG-TPJ. **`dACC →` dlPFC, PAG-PANIC(+)** — the sole
expressive link, excitatory. The regulation network can stop an **act**; it has no path to stop a **display**.

## Q7 — What is age-gated? **The trajectory would emerge for free — the schedules are already there.**
| | online_age | schedule |
|---|---|---|
| `PAG` / `PAG-PANIC` / `NuAmb` | **0.0** | brainstem_low_flat / affiliation_early |
| `CeA` | 0.0 | cea_moderate |
| `STN` | 1.0 | bg_moderate |
| `OFC` / `aIns` | 3.0 | pfc_low_early_high_late / insula_anterior_late |
| **`preSMA`** | **4.0** | **pfc_low_early_high_late** |
| `vlPFC` / `dACC` | 5.0 | pfc_low_early_high_late |
| `dlPFC` | 6.0 | pfc_low_early_high_late |
| `dmPFC` | 8.0 | pfc_low_early_high_late |

**Expression hubs are online at birth and flat; every candidate suppressor comes online at 4–8y on
PFC-protracted maturation.** That is Thompson's trajectory (§5) already encoded — newborn expresses
uncontrollably, control arrives late and keeps maturing. **The developmental trajectory of suppression needs no
new schedule; it needs a pathway for the existing schedules to act on.**

## §9 CONSTRUCT-VALIDITY CHECK — run before any expression claim. **It fails.**
- `AFFECTIVE_EMPATHY` (the CU study's instrument) = `(LA, BA, CeA, MeA, aIns)`
- `_DISTRESS_DISPLAY` (what we call the "shown" state) = `(CeA, PAG, BA)`
- **Overlap = {CeA, BA} — the throttle contains 2 of the 3 display nodes.**

**So the §6 payoff is NOT currently testable.** "CU agents show blunted involuntary expression" probed with
this throttle is **true by construction** — the manipulation contains the read-out. This is the §4 trap again,
caught *before* it became a finding. It is also the deeper reason the current display is wrong: **we read
affect and call it expression**, so the affect throttle inevitably "explains" the display.

## The two re-homed branches (§9) — they do close here, mechanically
Both were symptoms of `_DISTRESS_DISPLAY` reading the **felt** state:
- **Chronic-distress invisibility** — measured: bearer at CeA=1.000 displays 0.474 → 0.000 by tick 800.
  That is an artifact of phasic-differencing a *limbic* signal to fake a display. A real expression system
  has its own dynamics and its own suppression; adaptation would be a property of the **motor** pathway, not a
  subtraction we perform on affect.
- **Contagion-loop damping** — the loop is currently damped *only* by that same subtraction.
**Neither can be resolved while the display is a read of affect. They close with the expression system, or are
consciously re-homed.**

## Summary of the gap (sharpened from §7)
1. **The EMS is unefferented end-to-end** — PAG, PAG-PANIC, NuAmb, SympOut all 0-out. Not "no expression
   read-out": **no expression output at all.**
2. **`PAG→NuAmb` missing** — the hub is not connected to the vocal effector; PAG's defining output absent.
3. **No volitional pathway** — M1/premotor/SMA/facial nucleus absent entirely.
4. **No volitional suppressor** — nothing inhibits PAG from motor cortex (which doesn't exist).
5. **No audience-sensitivity** — ties/status/proximity reach nothing expressive.
6. **Suppressor age-gating already present** — the trajectory is free once a pathway exists.
7. **`CeA→PAG` sign tension vs the v9 aggression keystone** — same shape as CeA→LC, but keystone-bound.
8. **Construct validity fails** — the instrument contains the read-out; §6 is untestable as-is.

**Nothing built. Surfacing for the decision.** The biggest open question I will not answer alone: this level
implies **adding a motor/premotor + facial-nucleus limb** (new circuits, not just edges) — the largest
structural addition since the arc began — and it touches a committed keystone (Q1). That is a scope/sequencing
call.
