# PsychSim v10 — organism design spec (physical endowment + biological sex)

**Status: grounding review PASSED; seed-mechanics review PASSED with four required corrections, now
applied. Awaiting the final pre-build check. Nothing built.** v9 path (design → review → build). The
four seed-mechanics corrections folded into §5: (1) perceiver-side formidability routes to
**defensive-threat / CeA (submission), NOT VMHvl** — seeing strength makes you defer, not attack;
(2) sex-conditioning moved to **E4 (the perceiver's prior weight), not E2 (the bearer's stimulus)** —
the dimorphism is in valuation; (3) **E6 sex sets a VMHvl baseline-reactivity factor, not an on/off
gate** — aggression reachable in both sexes, the CU ratio measured not encoded; (4) **E5 gains the
neutral-floor guard** — `strong × neutral → restrain` proves the calibration didn't code
"strong→aggressive." Plus: the two new IN-VIS triggers (`attractive_face`, `formidability_cue`) are
stated as a perception-vocabulary extension, and verified against v9 — reward/defensive target nodes
exist but `IN-VIS` reaches neither today, so E4's two priors are **new connectome edges** (not new
circuits), each grounded.

---

## 1. Scope (what v10 is, and is not)

**In.** Two declared-or-assumed-but-unwired things from the §6 Phase-8 findings, wired together as one
reviewed seed pass:

1. **Physical endowment** — the seed's 7-attribute `physical_endowment` table (PH-ATTRACT, PH-SIZE,
   PH-MUSCLE, PH-AGILITY, PH-HEALTH, PH-SENSORY, PH-TEMPERAMENT), currently declared but unpopulated
   (`endowment.py` reads `getattr(seed, "physical", {})`, which does not exist) and unread.
2. **Biological sex** — as a **given input parameter** (chromosomal/gonadal sex), the variable the seed
   already presupposes (PH-SIZE `normal(mean_by_age_sex, sd)`; VMH "gonadal-steroid gated"), currently
   absent from the code entirely.

**Out (explicitly, this pass).**
- **No prenatal/hormonal machinery.** Sex is a *given parameter* that sets distributions and circuit
  parameters directly; we do **not** model prenatal androgenic organisation or activational hormonal
  modulation. (The earlier §6.2 escalation floated those; this pass is deliberately narrower.)
- **No genetics.** No MAOA/OXTR/methylation markers. If they ever enter, it is as parameters on
  substrate/plasticity, never as a marker that assigns an outcome — a separate future pass.
- **No gender as social construct.** Where sex-differentiated social responding appears, it must emerge
  from the matrices; it is never a coded role.

---

## 2. The design keystone (why this can't encode the answer)

The honest form for every physical trait is the same, and it is the one the whole project already
uses for Things: **a physical trait is a STIMULUS PROPERTY of the bearer — something another agent
perceives — and the response emerges from the *perceiver's own* circuits, never from a coded
trait→outcome weight.**

Concretely: agent B's attractiveness/size/health become entries in a **physical-stimulus percept**
(the analogue of a Thing's `stimulus` dict). When A perceives B, that percept is presented to A's
substrate in the substrate's own trigger vocabulary; A's reward / threat / affiliation circuits fire;
A's deference, approach, or wariness **emerges**. There is no `attractive → tie +0.3` anywhere — that
would be an authored social outcome, the exact encoded effect the project forbids.

**What is cited, and what is measured.** For each entry, the citation grounds the **intrinsic
property** being wired (e.g. "attractive faces are intrinsically rewarding to a perceiver," with a
neural mechanism). The citation is **never** for the population outcome the wiring should reproduce
(the beauty premium; the sex ratio in CU traits). Those outcomes are **search-for-match objectives
for the scan controller** — a hit is corroboration, a miss a real sufficiency finding.

- **Grounded** = literature gives the mechanism/direction (cited).
- **Scaffold** = literature gives direction but not magnitude → a labelled placeholder weight, same
  status as every other seed default.
- **Flag** = evidence for an intrinsic-property prior is thin/contested → say so; the design session
  decides whether it goes in or waits. Do not manufacture a citation to fill a slot.

---

## 3. Physical endowment — entry by entry

| attribute | intrinsic-property prior (what is wired) | citation(s) | wiring form | measured-not-coded outcome | status |
|---|---|---|---|---|---|
| **PH-ATTRACT** | attractive faces are intrinsically rewarding to a perceiver; agreement is cross-cultural and present pre-verbally (infants prefer attractive faces); perceivers **work (keypress) to view** attractive faces — the operational reward signature — and viewing activates reward circuitry (NAcc, medial OFC) | Langlois et al. 2000, *Psychol Bull* 126(3):390–423 (DOI 10.1037/0033-2909.126.3.390); Aharon et al. 2001, *Neuron* 32(3):537–551 (DOI 10.1016/S0896-6273(01)00491-3, PMID 11709163); O'Doherty et al. 2003, **"Beauty in a smile,"** *Neuropsychologia* 41(2):147–155 | a small innate reward-prior from the "attractive-face" percept → the **perceiver's** REW/OFC circuits | the "beauty premium" (attractive people gain more standing / positive treatment) | **grounded ✓ verified** |
| **PH-SIZE** | body size is a (secondary) formidability cue; observers assess it fast/automatically and it calibrates the bearer's own anger/entitlement; sex-dimorphic in distribution | Sell, Tooby & Cosmides 2009, *PNAS* 106(35):15073–15078 (DOI 10.1073/pnas.0904312106, PMID 19666613); Sell et al. 2009, *Proc R Soc B* 276:575–584 | percept channel (formidability) → **perceiver's** defensive-threat/submission; and a calibration input to the bearer's own threat/entitlement | size→dominance-route / rank correlation | **grounded ✓ verified** |
| **PH-MUSCLE** | **upper-body strength is the PRIMARY formidability variable** (assessment privileges musculature over height/weight); stronger individuals are more anger-prone and feel more entitled | Sell/Tooby/Cosmides 2009 *PNAS* (bearer recalibration); Sell et al. 2009 *Proc R Soc B* 276:575–584 (perceiver's fast visual strength assessment) | primary formidability channel (PH-SIZE secondary) | conflict-prevailing / entitlement outcome | **grounded ✓ verified** |
| **PH-HEALTH** | facial cues of health (symmetry, averageness) contribute to perceived attractiveness/mate-value — a component of the PH-ATTRACT channel, not a separate one | Rhodes et al. 2007, *Perception* 36(8):1244–1252 (DOI 10.1068/p5712); Thornhill & Gangestad `[secondary — verify locator]` | folds into the attractiveness percept (a contributor) | mate-value / attractiveness outcome | **grounded (folds into PH-ATTRACT)** |
| **PH-TEMPERAMENT** | reactive/affective temperament — **already** the existing `TraitSeed` temperament seed (fear/threat reactivity priors). Not a new physical channel. | — (existing substrate) | already wired | — | **covered — no new work** |
| **PH-AGILITY** | motor coordination is a **bearer capacity** (affects whether the bearer's own actions succeed), not a social cue others read. No grounded "graceful → liked" prior — inventing one would be the forbidden invented-category. | — | **not a social percept** | — | **RULED OUT of the social channel** (deferred bearer-capacity: a ceiling on motor-action success, a later pass) |
| **PH-SENSORY** | sensory acuity is an **input gain on what the bearer perceives** — the opposite direction from a social cue. | — | **not a social percept** | — | **RULED OUT of the social channel** (deferred bearer-capacity: possible input-channel gain, only if trivially cheap; not v10 social scope) |

**Resolved (design-session ruling): PH-AGILITY and PH-SENSORY are OUT of the social channel.** Applying
the keystone test strictly — is there an intrinsic property others *perceive and respond to*? — neither
qualifies: agility is a bearer motor capacity, sensory acuity an input gain, both the wrong direction
for a social cue. Manufacturing a "graceful people are liked" prior would be exactly the invented
category the project forbids, and the evidence for it is thin-to-absent. They may return in a **later
pass** as bearer-capacity parameters (PH-SENSORY as an input-channel gain; PH-AGILITY as a motor-success
ceiling) — a different mechanism from "how others respond." v10 stays focused on the social-percept
traits (ATTRACT, SIZE, MUSCLE, HEALTH) + sex. Flagging the two as thin, and their exclusion, is the
process working — not a gap.

---

## 4. Biological sex — a given input parameter

Sex enters as a **given parameter** (not via hormones this pass). It parameterises exactly two things
the seed already assumes:

1. **PH-SIZE distribution** — `normal(mean_by_age_sex, sd)`. Sex selects the age×sex mean. (Body-size
   dimorphism is uncontested; the citation is anthropometric norms, not an outcome.)
2. **VMHvl parameterisation** — the ventrolateral VMH is the canonical sexually dimorphic nucleus:
   Esr1/ERα-expressing neuron density differs by sex, and the female VMHvl carries anatomically and
   molecularly distinct aggression vs sex subdivisions. Our v9 VMHvl carries **no** sex parameterisation
   at all; v10 sets its parameters by the given sex.
   - Hashikawa et al. 2017, *Nat Neurosci* 20:1580–1590 `[DOI 10.1038/nn.4644]` — Esr1+ VMHvl controls
     female aggression; two subdivisions (aggression VMHpvlm, sex VMHpvll). **Already in the v9 citation
     list.**
   - Lin et al. 2011, *Nature* 470:221–226 (DOI 10.1038/nature09736) — VMHvl as the aggression locus;
     attack-activated neurons are inhibited during mating (opponent populations).

3. **The percept-priors are sex-conditioned — on the perceiver's PRIOR WEIGHT (E4), not the bearer's
   stimulus (E2)** (grounding review): the dimorphism is in the *perceiver's valuation* (Aharon:
   heterosexual males work to view attractive *female* faces), not in the face itself — B isn't "more
   attractive to everyone." So `sex` modulates the **effective weight** of the two new innate edges
   (`IW-ATTRACT-REWARD`, `IW-FORMIDABILITY-SUBMIT`), while the bearer's `physical_stimulus` magnitude
   stays a pure bearer property. Grounded direction; SCAFFOLD modulation function — detailed in §5 E4.

**The honesty line (non-negotiable).** Sex as a **substrate parameter** is *in*: body-size distribution
and VMHvl Esr1/subdivision parameterisation, set by the given sex. Whether that sex-differentiated
substrate **yields the observed sex ratio in CU/psychopathy traits** is **measured, never assumed**. A
model in which sex raises CU likelihood *by construction* has encoded the answer — exactly as coding
environment→divergence would have. So there is **no** `sex → CU +x` term anywhere. Instead:

> **Scan objective (search-for-match):** "Does a sex-differentiated substrate — nothing about outcomes
> encoded — reproduce the observed sex ratio in CU traits against held-out field data?" A hit corroborates
> the substrate's sufficiency; a miss is a real, publishable sufficiency finding. This is a
> `scan_match` objective, provenance-validated, exactly like the CU-punishment objective.

---

## 5. How it lands in the seed — concrete seed edits (for seed-mechanics review before build)

The plumbing already exists and is reused, not invented:
- `TraitSeed.physical: Dict[str,float]` is **already a field** (`core.py`), passed through to
  `Endowment.physical` (`endowment.py`) — but never populated and never read. v10 populates + reads it.
- `felt_response(engine, stimulus_dict, age_years, …)` is the **exact vetted path** a Thing's
  `stimulus` dict already takes to drive a *perceiver's* substrate (`environment_matrix.py:173`;
  `arena.py:267`). v10 feeds a bearer's physical-stimulus through the same call. No new perception path.

**E1 — Populate `TraitSeed.physical` at spawn (v10 seeding).** Sample PH-ATTRACT, PH-MUSCLE, PH-SIZE,
PH-HEALTH from the `physical_endowment` distributions; add a per-agent **`sex`** (given at birth, M/F).
PH-SIZE draws from `normal(mean_by_age_sex, sd)` — `sex` resolves the mean. **PH-AGILITY / PH-SENSORY
are NOT sampled into the social channel this pass** (§3 ruling — deferred bearer-capacity parameters).

**E2 — Derive a per-Person `physical_stimulus` dict — a PURE BEARER property (sex-NEUTRAL magnitudes).**
This is "how B physically presents to a perceiver's senses," the exact category as a Thing's
`stimulus`. It does **not** depend on who is looking — B's musculature is B's musculature:
- `PH-ATTRACT` (+ `PH-HEALTH` folded in) → an **`attractive_face`** trigger (visual), magnitude = B's
  attractiveness.
- `PH-MUSCLE` (primary) + `PH-SIZE` (secondary) → a **`formidability_cue`** trigger (visual),
  magnitude = B's formidability.
Magnitudes SCAFFOLD. **Sex-conditioning lives at E4, not here** (design-session ruling): the dimorphism
is in the *perceiver's valuation*, not in the bearer's face — B isn't "more attractive to everyone,"
the *response* varies by perceiver.

*Trigger-vocabulary extension (stated explicitly):* there is no `attractive_face` or `formidability_cue`
trigger today. v10 **adds these two IN-VIS triggers** to the perception vocabulary. This extends
perception, it is not an arbiter — each new trigger becomes exactly one grounded innate edge (E4), the
same way `IN-GUST:sweet` is a trigger with an innate `→NAc-shell` edge.

**E3 — Present it through `felt_response`, unchanged.** When A perceives B (the Arena/Things encounter
path), call `felt_response(A.engine, B.physical_stimulus, …)`. A's **own** reward / defensive circuits
fire; A's approach / deference / wariness **emerges**. No `attract → tie` term — the only wired thing
is "this percept drives this perceiver's reward/defensive channel," the cited innate prior.

**E4 — Two `innate_wiring_catalogue` entries = two NEW connectome EDGES (into existing nodes; weights
SCAFFOLD; sex-conditioned ON THE WEIGHT).** Verified against v9: the reward and defensive target nodes
exist, but `IN-VIS` drives only `SC-Pv` today, so each of these is a **new edge**, not a new circuit —
a real connectome addition with its own grounding, on the `IN-GUST:sweet→NAc-shell` template. Same
schema as the 18 existing entries:
- **`IW-ATTRACT-REWARD`** — edge **`IN-VIS:attractive_face → NAc-shell`** (and `→OFC`); innate_effect
  "appetitive"; `default_birth_strength: weak` (SCAFFOLD); `present_at_birth: yes`; **`sex_conditioned`
  applies to this edge's effective weight** (perceiver×bearer — the dimorphism is in valuation, per
  Aharon); unlearned_evidence = cross-cultural agreement + infant preference (Langlois 2000) +
  **willing-to-work-to-view** (Aharon 2001, the operational reward signature; NAcc) + medial-OFC
  response (O'Doherty 2003); sources = [Langlois et al. 2000 *Psychol Bull* 126(3):390–423; Aharon et
  al. 2001 *Neuron* 32(3):537–551; O'Doherty et al. 2003 "Beauty in a smile," *Neuropsychologia*
  41(2):147–155].
- **`IW-FORMIDABILITY-SUBMIT`** — edge **`IN-VIS:formidability_cue → CeA`** (defensive-threat →
  submission/wariness via CeA→PAG). **NOT VMHvl** (design-session ruling: seeing a strong opponent
  makes you *defer*, not attack — the attack area is the bearer's own, E5). innate_effect
  "aversive/submissive"; `default_birth_strength: weak` (SCAFFOLD); **`sex_conditioned` on the weight**;
  unlearned_evidence = fast/automatic visual strength assessment (Sell *Proc R Soc B*, the perceiver
  side); sources = [Sell et al. 2009 *Proc R Soc B* 276:575–584; Sell, Tooby & Cosmides 2009 *PNAS*
  106(35):15073–15078].

**E5 — Bearer-side calibration + the neutral-floor guard (the one smuggle-risk).** PH-MUSCLE/PH-SIZE
calibrate the **bearer's own** anger/entitlement (Sell PNAS: strength→anger-proneness): `sex`-neutral
here, a within-agent bias raising the bearer's VMHvl **baseline reactivity**. **Guard (required):** this
is a calibration input to the attack circuit's *competition*, **never a determinant of its output** —
strength biases VMHvl's starting gain, but whether the bearer aggresses must still win the basal-ganglia
race against the executive brake and the defensive channels, under actual provocation. **Test (same
shape as the v9 neutral control):** `strong × neutral (unprovoked) → restrain` (the neutral floor holds)
AND `strong × provocation → more aggress than weak × provocation`. The differential is the finding; the
neutral floor **proves it is not coded "strong→aggressive."** If raising strength alone (no provocation)
produces aggression, E5 has become a coded outcome and fails.

**E6 — Sex as a given parameter (no hormonal dynamics): a baseline-reactivity FACTOR, not a gate.**
- PH-SIZE distribution mean (E1).
- **VMHvl**: `sex` sets a VMHvl **baseline-reactivity factor** — Hashikawa 2017 shows Esr1+ VMHvl is
  necessary for aggression **in both sexes**, with a higher male baseline and differing subdivisions.
  So this is **not** "male = aggression-on, female = off" (that would overstate it and encode a
  sex→aggression outcome); it is a baseline-gain difference, with **aggression fully reachable in both
  sexes under provocation** (the v9 pathway intact). SCAFFOLD magnitude, grounded direction
  (male>female baseline). No prenatal organisation, no hormones.
- `sex` also parameterises the E4 edge weights (perceiver valuation).
- **Honesty line:** whether this baseline difference yields the observed **CU sex ratio** must still
  **emerge and be measured** (`scan_match`) — it is never the *reason* the parameter is set.

**E7 — Version + provenance.** `meta.version: "v10"`. **No new circuits** (reward, defensive, VMHvl
nodes all exist — verified). **Two NEW EDGES** (`IN-VIS:attractive_face→NAc-shell/OFC`;
`IN-VIS:formidability_cue→CeA`), each = one `innate_wiring_catalogue` entry with its own grounding;
**+2 IN-VIS triggers**; `sex` a per-agent birth parameter (PH-SIZE mean + VMHvl factor + E4 weights).
Update `gaps_register`: SCAFFOLD = all magnitudes, the sex-conditioning function form, the
trait→trigger-magnitude mapping; the two new edges are cited but weak/assumption-basis until better
sourced. Ordinal/structural tests only, never target values.

**The keystone, restated in the mechanics:** every trait becomes a `physical_stimulus` (a bearer
percept) fed through the existing `felt_response` into the *perceiver's own* circuits — attractiveness
to reward, another's formidability to **defensive submission** (not attack); the bearer's own strength
calibrates the bearer's attack circuit but **cannot fire it without provocation** (neutral-floor guard);
sex is a birth parameter (distribution means, VMHvl baseline factor, perceiver-valuation weights);
**both population outcomes (beauty premium; CU sex ratio) are `scan_match` objectives, never weights.**
Nothing here codes a social outcome.

---

## 6. Build sequence (after this spec is reviewed + the citations checked)

1. Design-session **grounding review** of §3/§4 entry by entry (verify each DOI; rule on the
   PH-AGILITY/PH-SENSORY flags; confirm the sex scope).
2. Seed edits (v10): `physical_endowment` populated; percept channel; innate-wiring entries; sex
   parameters. Test-gated, ordinal/structural asserts only, never target values.
3. `endowment.py` wired to read `TraitSeed.physical`; perception plumbing (reuse the Arena/Thing
   percept path).
4. **Scan objectives** for the two measured outcomes (beauty premium; sex-ratio-in-CU) as
   `scan_match` targets against provenance-validated held-out field data.
5. Full suite green; honesty wall held (no coded trait→outcome); sync per phase.

---

## 7. Review status

**Grounding review — PASSED (design session, verified against the literature).** PH-ATTRACT
(Langlois/Aharon/O'Doherty, with O'Doherty corrected to "Beauty in a smile," 41(2):147–155) ✓;
PH-SIZE/PH-MUSCLE (Sell PNAS + Sell *Proc R Soc B*) ✓; PH-HEALTH → attractiveness (Rhodes) ✓; sex scope
(given-parameter only) ✓; both outcomes as `scan_match` objectives, not weights ✓. PH-AGILITY /
PH-SENSORY ruled OUT of the social channel ✓. The sex-conditioning of the percept-priors is folded in
(§4.3, §5 E2/E4).

**Now open: seed-mechanics review of §5 (E1–E7)** — the concrete edits above, before build. Points I most
want checked: the `physical_stimulus → trigger-vocabulary` mapping (E2) and whether the sex-pairing
modulation belongs at E2 (the stimulus magnitude) or E4 (the prior weight); the VMHvl sex parameter form
(E6); and that E5's bearer-side calibration doesn't smuggle an outcome. Once the mechanics are cleared,
this goes to build (test-gated, ordinal-only), then Step 6 (Allen audit, fresh), then the study.
