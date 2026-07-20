# PsychSim — D6 BRANCH: consolidated open-threads register
### Assembled 2026-07-18, mid-branch. Supersedes the L7-exit register's D6 section ONLY.
### The return-path register (v3) still governs the overall spine; this refines the D6 node it left open.

> **Why this exists:** the D6 branch has generated ~20 rulings since the L7-exit register was written, and its
> open state is scattered across all of them. This is the single act-from ledger. **Everything here is in the
> file's vocabulary** (`circuit` = region, `connection`/`edge` = pathway) for paper-trail continuity.

---

## SUBSTRATE STATE AT THIS WRITE
- **96 circuits, 239 connections** (was 93/231 at L7 exit; +3 circuits, +9 connections, −1 the first deletion).
- **Added this branch:** `Mc` (freezing effector) · `PGi` (LC integrator) · `COCH`/`IN-AUD` (auditory raw
  channel). **Corrected:** `MeA→VMH` sign, `MeA→VMHvl-GABA`, `VMH→vlPAG` receptor, `MeA→ATL-TP` sign.
  **Removed:** `MeA→ATL-TP` (into the gap register, `a11c588`).
- **Suite: 541 tests, ONE authorized red** (freezing floor's positive half — now four scaffold terms).
- **`DRN` at 0.05 `UNGROUNDED — pending`; aggression keystone green + annotated.**

---

## TIER 0 — BLOCKING, NOT OPTIONAL (close these before the branch advances)

| # | item | status | who |
|---|---|---|---|
| **0.1** | **Full 541-suite confirmation of the `MeA→ATL-TP` deletion** | **committed but NOT confirmed-closed.** Targeted gate only (OOM). S64 stays open with this as its explicit gate. **The precedent is "deletion + full-suite," not "deletion + whatever the machine bore."** | build session, once machine clears |
| **0.2** | **The crash — identify before fixing** | diagnosis (external `www-data` fleet) is **plausible but unconfirmed from here.** Read-only checks named in chat (`ps aux --sort=-%mem`, `free -h`, `dmesg \| grep -i "killed process"`). **If PsychSim is not in the OOM log, the fleet theory is a red herring and we're debugging a different crash.** Fix in your control if real: `.wslconfig` cap + single-worker suite. | Ralph |

---

## TIER 1 — THE REVIEWER'S, NEEDS NO MACHINE

| # | item | detail |
|---|---|---|
| **1.1** | **★ The four-pacemaker grounding table** | `DRN`, `VTA`, `SNc`, `BF-ACh` — **adult tonic rate AND developmental trajectory, as ONE table.** #1 and #2 of the tonic sweep are one question per node (*what is the adult rate, and does it mature?*) — neither half is buildable alone, both are literature. **Nothing builds until it's in.** After it, we know whether S57 (the developmental-baseline mechanism) serves one node or five — mechanism vs over-engineering. **Mine to run on your call; the crash does not block it.** |

---

## TIER 2 — QUEUED BUILD WORK (needs grounding I shouldn't guess; ordered)

| # | item | the question, and why it waits |
|---|---|---|
| **2.1** | **`DRN` baseline** | Grounded from 1.1's table. **Expected to leave the freezing floor RED** and re-attribute it — principle 2: freezing was resting on two scaffold values cancelling (low brake × low drive). Ground the brake, the drive's arbitrariness shows. |
| **2.2** | **`VMH→vlPAG`'s BAND** | Now exposed as load-bearing and ungrounded (was hidden while the brake was also scaffold). **The sole excitatory driver of the freezing column. Ground it — do NOT crank it.** Sign is correct (glutamatergic core projects; GABAergic shell is local). |
| **2.3** | **S57 — developmental trajectory for neuromodulator baselines** | Its own pass, IF 1.1 shows more than one node needs it. `baseline_activation` is static; the substrate models circuit onset + plasticity but not a maturing tonic rate. The mechanism `DRN`'s scaffold-low was standing in for. |
| **2.4** | **S56 — the gate family calibration (NINE nodes, not four)** | `DRN-GABA, vlPAG-GABA, dACC-GABA, dlPFC-GABA, vmPFC-GABA, CeA-GABA, ITC, PAG-PANIC-GABA, VMHvl-GABA` — all share one brake band + baseline regardless of afferent load. **`dlPFC` has nine excitatory afferents and saturates to 1.0 against its own brake.** The question is not "what number stops it saturating" but **"should an E-I loop's inhibition scale with drive, and does ours?"** Family-wide, grounded. |
| **2.5** | **`vlPAG-GABA`'s afferent set** | The **selector** (freezing vs flight); ours has 2 (`CeA`, `BNST`); the literature says it integrates many. **Enumerate the cited set, record INCOMPLETE with the remainder named** (LC/PGi pattern, 3rd instance). |
| **2.6** | **The opioid system** | Four circuits name opioids in prose (`vlPAG`, `dPAG`, `NAc-shell`, `PAG-PANIC`); **no opioid circuit exists.** Dense μ-opioid on `vlPAG-GABA` is the cited release. **`PAG-PANIC`'s soothing arm wants the same system — one circuit, two registers. Its own pass, not a footnote.** |
| **2.7** | **`noci→PBN`** | The missing afferent that makes `PBN` inert (why it's not a viable `vlPAG` driver). Register S55. |
| **2.8** | **The two `LA` receptor pins** | `LA→BA`, `LA→CeA` — load-bearing on the keystone, +1 correct (LA projects glutamatergically). **Cheap grounding, no sign question, whenever wanted.** |

---

## TIER 3 — DOORS 2 & 3 (diagnosed, NOT designed — and door 3 gates the CU study)

| # | item | detail |
|---|---|---|
| **3.1** | **Door 1, auditory half** | (b) the `AUD-brainstem`/IC grain FIRST — a cry reaching `SC-Pv→CeA→LC` is amygdala-obligate (the direct-pain-37% trap); the non-amygdala route is `IC→PGi→LC`. (a) the Arena's cry-presentation depth is worthless without (b). **Door 1 visual = TRUE BY ANATOMY, closed. This is the remaining half.** |
| **3.2** | **Door 2 — the scan's self-search** | `dissociation_index = cog − aff`, maximised over a set containing both. **The search returns its own manipulation.** Not yet designed. |
| **3.3** | **★ Door 3 — the temperament dial reaches `LC`'s node directly, on every agent, at seed time** | Low threat IS the CU temperament → **every CU agent is born with a throttled teaching signal.** Needs the **per-function temperament model.** **THIS IS THE ONE THAT DECIDES WHETHER THE CU STUDY CAN MAKE ITS CENTRAL CLAIM.** Not a line written toward it. |

---

## TIER 4 — REGISTERED, NOT THIS BRANCH

- **S65 — the `basis: assumption` census** (provenance sibling of the fallback-sign census; one-line query;
  may reframe "grounded connectome" the way Q1 reframed "grounded baselines"). **Do not run this pass.**
- **The lump census** (12 known; `MeA`'s remaining fallback connections — `MeA→MPOA`, `MeA→BNST` SPLIT-BLOCKED
  — at the top). Feeds the 209-connection audit.
- **The input-surface gaps:** `PB-LOOMING` (the escape trigger the model CITES and cannot fire — escape has
  never happened) · `PB-STARTLE` · `PR-SALT` · `PR-HOMEOSTATIC` · `IN-PROPRIO` (S23, no agency claim until it
  lands) · predator odor (blocks the `MeA` split).
- **The §18 systemic-conditions widening** (for the master doc + thesis limitations): the one-number baseline
  layer (S61) · the nine-node gate scaffold · effect-sizes-biased-upward (now a measured law) · cortical brake
  layer 3 of 11 · the typing-order hazard (S44) · Form 3 is a class, 1 of 5 fixed.
- **The four split candidates** (`NuFac` upper/lower = highest thesis value, the Duchenne signature) · the
  reactivity/regulation fusion (registered above the CU study) · CeA operating point · S28 autonomic cost of
  suppression.

---

## WHAT CLOSES D6 (the stopping rule, made concrete)
**D6 closes when its CLAIMS are testable, NOT when the substrate is finished** (S35). Concretely, in order:
1. **The freezing column works** — 1.1 → 2.1 → 2.2 → 2.5 (driver grounded, selector afferented, output present
   via `Mc`). The floor turns from an expected red into a held one.
2. **Door 3 is designed** — the per-function temperament model. The CU study's central claim becomes makeable.
3. **The read-out tail is fixed** — `DEFENSIVE_OUTPUT`, `_OBS_THREAT`, `_SELF_THREAT` (all self-clear when
   `vlPAG` fires), `AFFECTIVE_EMPATHY`'s hollow (3/5 — the study's primary instrument), the executive conflation.

**Then the climb resumes at D4 → D3 (the purpose) → D2 → v14 Phases 3-5 → the 209-connection audit → the CU
study.**

---

### The two findings to carry up the climb (don't lose them under the mechanism work)
1. **A psychological theory emerged from the connectome** — Gross's reappraisal/suppression fell out of where
   two routes land. The model did the thing it exists to do.
2. **The honest wall held at the substrate's single worst point** — 161 ungrounded signs → one under pressure
   → carrying a thesis label → the accidental sign was the CORRECT one, and a fitted model would have had the
   other. **The strongest evidence the substrate isn't reverse-engineered from its answer, and it landed on
   the study's output.**
