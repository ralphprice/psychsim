# `IN-AUD → COCH` — the raw auditory channel; startle fires for the first time (own pass)

Built as ruled: the one edge the input-surface audit predicted. **Startle fires for the first time in the
model's existence.** Measured all five consequences honestly — three land, two do not, and the two that don't
are a separate, named gap.

## Built (95 circuits, +1 input edge; regrown; golden UNCHANGED)
**`IN-AUD → COCH`** — the raw auditory channel, the analogue of `IN-VIS → RET` (band `moderate-strong`,
`anatomy`, inherited from the template). Audition was **the only modality without a raw input channel** (S42):
vision has `IN-VIS→RET`, olfaction `IN-OLF→OB`, vestibular `IN-VESTIB→VN`, interoception `IN-INTERO→NTS` — but
the only auditory input was `IN-AUD:voice→A1-belt`, a feature channel landing in cortex, so `COCH` was
completely unafferented and the whole subcortical relay was dead.

## The five consequences — measured, honestly
| # | consequence | result |
|---|---|---|
| 1–2 | **the subcortical chain lights + STARTLE FIRES** | ✅ sudden sound → `COCH` 0.680 → `StN` 0.657 → `CeA` **0.921** (rest 0.472). `PB-STARTLE` fires for the first time. |
| 3 | auditory threat reaches `SC-Pv` | ✅ `IN-AUD → COCH → AUD-brainstem` 0.579 → `SC-Pv` 0.315 (the escape paper: SC receives visual **and auditory** threat). |
| 4 | the cry reaches the IC | ❌ **the cry bypasses** — `IN-AUD:voice → A1-belt` (cortex); `COCH` stays 0.050. |
| 5 | door 1's auditory half closes | ❌ **not by this edge** — the cry doesn't reach `SC-Pv`/`PGi`/`LC`. |

**Three land, two do not — and the two are one gap: the cry's INJECTION DEPTH.** The cry is injected as
`IN-AUD:voice → A1-belt` (cortex), so it bypasses the subcortical relay this edge lit. `IN-AUD → COCH` fixes
**startle and generic auditory salience**; it does **not** route the cry — that needs the cry to also enter
subcortically (or `PGi`'s auditory arm, `IC → PGi`, which is itself unbuilt — S38). Registered, not
papered over.

## "If a startle test passes, ask what's holding it" (the freezing-floor rule, applied)
Startle fires via the **grounded** cascade `COCH → StN → CeA` (+ `COCH → AUD-brainstem → SC-Pv → CeA`). What
holds the *magnitude* (`CeA` 0.921, near ceiling): `CeA` is a saturating hub, so per §18 the magnitude is
**provisional-upward** — the *existence* of startle (CeA rises sharply under sudden sound) is the solid claim,
its size is not. Not a corpse-passes-the-floor situation: the positive behaviour genuinely emerged from
grounded anatomy that had no input before.

## Verification
95 circuits / +1 input edge / 0 dangling; regrown; **golden UNCHANGED** (the childhood curriculum injects no
generic `IN-AUD` cue that reaches `COCH`, so development is unaffected). Count pins unchanged (no new circuit;
`input_edges` still > 15). **The suite carries exactly ONE expected red — the freezing-floor positive half
(the Q2 gap, `8c9cce6`); a `failures=1` that is that test is green-modulo-Q2, any other failure is a
regression.**

## Order
Q2 — `vlPAG`'s drive on the settled node (turns the freezing floor red → real) → door 1's auditory half (the
cry's injection depth + `PGi`'s `IC → PGi` arm) → the channel gaps (`PB-LOOMING` the escape trigger, `PR-SALT`,
`PR-HOMEOSTATIC`, predator-odor, `IN-PROPRIO`). **Door 1: visual `TRUE BY ANATOMY` (measured), auditory live.
#2 open on doors 2 and 3.**
