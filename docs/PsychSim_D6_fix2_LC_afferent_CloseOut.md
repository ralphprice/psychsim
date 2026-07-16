# D6 #2 door 1 — LC's major afferent built; the entailment PARTIALLY dissolved, and the survival is the finding

`PGi` built as ruled. The entailment dissolved under direct pain and **survived under vicarious distress** —
and the reason is the failure mode recursing one level down. Reported as-found; **door 1 only, #2 stays open.**

## Built (93→94 circuits, +4 edges; regrown)
- **`PGi`** (nucleus paragigantocellularis, `interoception_autonomic`) — the major excitatory glutamatergic
  afferent to LC (~73% of LC neurons driven; Aston-Jones et al. 1986).
- `PGi → LC` (AMPA, **strong** — from the literature's "major", not chosen to dissolve the entailment).
- **`PGi`'s afferents, available now:** `PBN → PGi`, `NTS → PGi`, `IN-SOMATO:nociception → PGi`. This is the
  justification for building it — it creates no new unafferented hub.
- **`CeA → LC` untouched at `moderate`** — it becomes minor *by anatomy*, never by re-banding.
- Domain `interoception_autonomic` — verified not temperament-reachable, so door 3 is not widened through PGi.

**Two registered items resolved:** `PBN → LC` / `NTS → LC` were never *dormant* — they were **WRONG-TARGET**.
Aston-Jones showed `PBN`/`NTS` do not project to LC (they terminate adjacent); `PGi` is their integrator. Re-marked.

## ★ The re-measure — PARTIAL dissolution (the honest, uncoded result)
Throttle `AFFECTIVE_EMPATHY` → does `LC` still collapse?

| context | before `PGi` | after `PGi` | `PGi` (intact) |
|---|---|---|---|
| threat / **direct pain** | 72% collapse | **37%** | 0.537 (nociception fires) |
| **distress / vicarious** | 73% | **64%** | 0.084 (blind) |
| rest | 54% | 44% | 0.084 |

**The entailment dissolved under direct pain** (where `PGi`'s nociceptive afferent fires, so `PGi` carries LC
when `CeA` is throttled) **but survived under distress/vicarious.** And **the vicarious context is the CU
study's context** — so door 1 is not closed for the purpose that matters.

## ★★ Why it survived — the failure mode recursed one level down (S30b)
**I completed `PGi`'s interoceptive/pain arm (`PBN`/`NTS`/nociception) but not its exteroceptive/salience arm**
— yet Aston-Jones is explicit that `PGi` integrates *"exteroceptive **and** interoceptive… arousal."* A
social-distress cue (`biological_motion`/`voice`) never reaches `PGi`, so `PGi` stays near rest (0.084) under
distress and cannot carry LC there. **The same "partial completion" I was sent to fix, one synapse further
down.** I recorded `PGi`'s set as **INCOMPLETE**, not papered over. The next grounded step (its own ruling): a
salience input to `PGi` — candidate `SC-Pv → PGi` (the biological-motion/looming salience hub). **Not added
unilaterally.**

## The failure mode's actual fix — the recording (S30)
`LC`'s afferent set is now recorded **INCOMPLETE**, remainder named: **`PrH`** (blocked on the unbuilt
vestibular/oculomotor system — building it would repeat the unafferented-hub failure *inside* the fix, S31) ·
**`preBötC-Cdh9`** (a subpopulation, with the respiratory pass — a node called `preBötC` would be the tenth
lump, and there's no oscillation substrate anyway, S32) · Barrington's nucleus · PVN dorsal cap · spinal
lamina X. *"LC now has a teaching signal" was true; "LC is afferented" was not.* Never again record a hub
complete when it is not.

## ★ A new audit category (S33) — an exclusion is a claim
Found while verifying the temperament domains: `_TEMPERAMENT_DOMAIN` excludes `FRUSTRATION` because *"the
attack circuits are net-inhibited in v8."* **The PAG split destroyed that premise** (the v9 keystone flip:
`CeA` inhibits freezing, not attack). So the exclusion's justification is **stale**, and `FRUSTRATION` may now
have leverage. The D6 audit could not catch this — it enumerated what is *in* the sets, never whether the
reasons for what is *out* still hold. **Every exclusion carries a claim; re-check its justification when its
basis moves.** `FRUSTRATION` gets its own small diagnostic — not acted on here.

## ⛔ Door 1 only — #2 stays open
- **Door 3** — the THREAT dial scales the `LC` *node* directly; `PGi` does nothing for it, so a CU agent is
  still born with a throttled teaching signal. Needs the per-function temperament model (fix #4).
- **Door 2** — the scan's `dissociation_index` still ranges over its own signature. Separate fix.
- And door 1 itself is only *partially* shut: dissolved for pain, open for vicarious (S30b). **#2 is further
  from resolved than the pain number alone would suggest — which is exactly why the line had to be held
  through the measurement.**

## ★ Unexpected: the earned negative self-cleared (a decision for the reviewer)
The full suite flagged an **unexpected success**: `test_divergence_does_not_robustly_emerge` (the earned
negative, xfailed) now **passes**. `interaction_at(500)` dropped **−0.0534 → −0.0335**, and it is
**stable/well-posed** (across durations 350/500/600: −0.0321/−0.0335/−0.0336, spread 0.0015, all < 0.05). The
self-clearing mechanism I built (`unexpected success → suite red → revisit`) fired exactly as designed.

**But it fired for `PGi`, not for the resolution condition I named** ("when the cortical brake layer is
complete… not before"). The brake layer is still 3 of 11. What happened is the **§18 direction**: each grounded
completion has shrunk the divergence — **0.0755 (saturation artifact) → 0.0534 (`dACC-GABA` brake) → 0.0335
(`PGi` afferent)** — so the earned negative now holds *more strongly*, for a grounded reason other than the one
I anticipated. This **confirms** the finding (divergence does not robustly emerge); it does not retire it.

**The decision (surfaced, not taken):** un-xfail it — assert the earned negative, which is the opposite of
retiring-by-attrition, and let it go red if a future change pushes it back over 0.05 — **or** keep it xfailed
with a resolution condition rewritten to be completion-agnostic. I lean un-xfail (an xfail on a stably-passing
test is dishonest, and the §18 arc is exactly the confirmation the earned negative was waiting for), but it is
*the earned negative*, so I hold for the ruling. **The `PGi` commit is held on this** — the suite is red only on
this unexpected success (the golden is regenerated).

## Verification
Full suite (golden regenerated if `PGi`'s tonic drive shifts the develop snapshot — a demonstrated, grounded
change); count pins 93→94; `PGi` scaffold (not a setpoint deviant); regrown. `CeA → LC` byte-untouched.
Nothing tuned.
