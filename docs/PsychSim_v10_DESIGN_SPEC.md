# PsychSim v10 — organism design spec (physical endowment + biological sex)

**Status: grounding review PASSED; seed-mechanics review of §5 PENDING. Nothing built.** v9 path
(design → review → build). The design session verified the load-bearing citations against the
literature (Aharon, Sell) and ruled the four questions (§7); this revision folds in the five resulting
edits: O'Doherty corrected to "Beauty in a smile" 41(2):147–155; Sell *Proc R Soc B* 276:575–584 added
for the perceiver side; PH-AGILITY/PH-SENSORY out of the social channel; the percept-priors wired
**sex-conditioned** (per the evidence); keystone intact. §5 is now detailed into concrete seed edits
(E1–E7) for the mechanics review before build.

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

3. **The percept-priors themselves are sex-conditioned** (forced by the grounding review, not scope
   creep): the attractiveness reward value is a function of perceiver×bearer sex (Aharon: heterosexual
   males work to view attractive *female* faces), and formidability assessment/strength→anger is
   studied primarily in, and is more accurate for, males (Sell). So `sex` is not only a PH-SIZE mean and
   a VMHvl parameter — it also **modulates the IW-ATTRACT-REWARD and IW-FORMIDABILITY-THREAT priors**
   (E2/E4). This is what the evidence says; a flat prior would silently contradict the citation. Grounded
   direction; SCAFFOLD modulation function — detailed in §5.

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

**E2 — Derive a per-Person `physical_stimulus` dict (substrate trigger vocabulary) from the traits.**
This is the bearer's "how I present to a perceiver's senses," the exact category as a Thing's
`stimulus`:
- `PH-ATTRACT` (+ `PH-HEALTH` folded in) → an **appetitive/reward** trigger magnitude.
- `PH-MUSCLE` (primary) + `PH-SIZE` (secondary) → a **formidability/threat** trigger magnitude.
These magnitudes are **sex-conditioned** — a function of (perceiver sex × bearer sex), per Aharon
(effort-reward male→female) and Sell (formidability assessment/strength→anger studied in males). The
**direction** (there is a sex pairing) is grounded; the **modulation function and the magnitudes are
SCAFFOLD**, labelled as such. (Fallback if we want v10 minimal: wire the priors sex-neutral and flag
that as a stated simplification — but this spec proposes sex-conditioned, since v10 already carries sex
and a flat prior would silently contradict the citation.)

**E3 — Present it through `felt_response`, unchanged.** When A perceives B (same encounter path the
Arena/Things use), call `felt_response(A.engine, B.physical_stimulus, …)`. A's **own** reward / threat
circuits fire; A's approach / deference / wariness **emerges**. There is no `attract → tie` term
anywhere — the only thing wired is "this percept presents as reward/threat," which is the cited innate
prior, not an outcome.

**E4 — Two `innate_wiring_catalogue` entries (the cited priors; magnitudes SCAFFOLD, sex_conditioned).**
Same schema as the 18 existing entries (`{id, category, stimulus, target, innate_effect,
mechanism_type, default_birth_strength, present_at_birth, unlearned_evidence, confidence, caveat,
sources[]}`):
- **`IW-ATTRACT-REWARD`** — stimulus "attractive face/body (visual, IN-VIS)"; target
  "reward/appetitive (REW/OFC/NAcc)"; innate_effect "appetitive"; `default_birth_strength: weak`
  (SCAFFOLD); `present_at_birth: yes` (infant preference); `sex_conditioned: true`; unlearned_evidence
  = cross-cultural rater agreement + infant preference (Langlois 2000) and **willing-to-work-to-view**
  (Aharon 2001, the operational reward signature) + medial-OFC response (O'Doherty 2003); sources =
  [Langlois et al. 2000 *Psychol Bull* 126(3):390–423; Aharon et al. 2001 *Neuron* 32(3):537–551;
  O'Doherty et al. 2003 "Beauty in a smile," *Neuropsychologia* 41(2):147–155].
- **`IW-FORMIDABILITY-THREAT`** — stimulus "formidability cue: musculature > size (visual, IN-VIS)";
  target "defensive-threat / submission (VMHvl + defensive circuits)"; innate_effect
  "aversive/submissive"; `default_birth_strength: weak` (SCAFFOLD); `sex_conditioned: true`;
  unlearned_evidence = fast/automatic visual strength assessment (Sell Proc R Soc B, the perceiver
  side) + strength→anger/entitlement recalibration (Sell PNAS, the bearer side); sources =
  [Sell, Tooby & Cosmides 2009 *PNAS* 106(35):15073–15078; Sell et al. 2009 *Proc R Soc B*
  276:575–584].

**E5 — Bearer-side calibration (not a percept).** PH-MUSCLE/PH-SIZE also calibrate the **bearer's own**
anger/entitlement (Sell PNAS): a within-agent input raising the bearer's VMHvl reactivity / lowering
its attack threshold. A calibration parameter, SCAFFOLD magnitude, grounded direction.

**E6 — Sex as a given parameter on two circuits (no hormonal dynamics).**
- PH-SIZE distribution mean (E1).
- **VMHvl**: `sex` parameterises the Esr1-density / aggression-subdivision balance (Hashikawa 2017:
  female VMHvl carries distinct aggression vs sex subdivisions; the node is already `Esr1+/SF1` with
  Lin 2011 + Hashikawa 2017 in its `sources`). As a **given parameter**, `sex` sets a VMHvl
  reactivity/threshold factor (or the formidability→VMHvl weight) — SCAFFOLD magnitude, grounded
  direction (dimorphic). No prenatal organisation, no activational hormones.
- `sex` also feeds the sex-conditioning of E2/E4.

**E7 — Version + provenance.** `meta.version: "v10"`. Likely **no new circuits** (the traits are
percepts/inputs + parameters on existing nodes); **+2 innate_wiring_catalogue entries**; `sex` a
per-agent birth parameter. Update `gaps_register`: SCAFFOLD = all magnitudes + the sex-conditioning
function form + the physical-trait→trigger-magnitude mapping; ASSUMED-pending = the exact
sex-pairing function. Ordinal/structural tests only, never target values.

**The keystone, restated in the mechanics:** every trait becomes a `physical_stimulus` (a percept) fed
through the existing `felt_response` into the *perceiver's own* circuits; sex is a birth parameter on
distributions + VMHvl; **both population outcomes (beauty premium; CU sex ratio) are `scan_match`
objectives, never weights.** Nothing here codes a social outcome.

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
