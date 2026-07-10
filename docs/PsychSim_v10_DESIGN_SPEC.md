# PsychSim v10 — organism design spec (physical endowment + biological sex)

**Status: FIRST DRAFT for design-session review. Nothing here is built.** This follows the v9 path
(design → review → build): the design session checks the grounding **entry by entry** against the
real citations before any of it enters the seed. Where I have not verified the exact DOI string, it
is marked `[DOI to verify]` — I would rather flag than manufacture one.

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
| **PH-ATTRACT** | attractive faces are intrinsically rewarding to a perceiver; agreement is cross-cultural and present pre-verbally (infants prefer attractive faces); viewing them activates the perceiver's reward circuitry (NAcc, medial OFC) | Langlois et al. 2000, *Psychol Bull* 126(3):390–423 `[DOI 10.1037/0033-2909.126.3.390 — verify]`; Aharon et al. 2001, *Neuron* 32(3):537–551 `[DOI 10.1016/S0896-6273(01)00491-3 — verify]`; O'Doherty et al. 2003, *Neuropsychologia* `[cite+DOI to verify]` | a small innate reward-prior from the "attractive-face" percept channel → the **perceiver's** REW/OFC circuits | the "beauty premium" (attractive people gain more standing / positive treatment) | **grounded** |
| **PH-SIZE** | body size is a formidability cue; observers assess it (fast, automatic) and it calibrates the bearer's own anger/entitlement; sex-dimorphic in distribution | Sell, Tooby & Cosmides 2009, *PNAS* 106(35):15073–15078 `[DOI 10.1073/pnas.0904312106]` | percept channel (formidability) → **perceiver's** defensive-threat/submission circuits; and a calibration input to the bearer's own threat/entitlement | size→dominance-route / rank correlation | **grounded** |
| **PH-MUSCLE** | upper-body strength is the core formidability variable (≈ PH-SIZE's mechanism); stronger individuals are more anger-prone and feel more entitled | Sell, Tooby & Cosmides 2009 (as above); Sell et al. 2009 *"human anger face"* / formidability-assessment line `[cite+DOI to verify]` | same channel as PH-SIZE (formidability cue) | conflict-prevailing / entitlement outcome | **grounded** |
| **PH-HEALTH** | facial cues of health (symmetry, averageness) contribute to perceived attractiveness/mate-value — largely a component of the PH-ATTRACT channel, not a separate one | Rhodes et al. 2007, *Perception* 36(8):1244–1252 `[DOI 10.1068/p5712 — verify]`; Thornhill & Gangestad `[cite+DOI to verify]` | folds into the attractiveness percept (a contributor, not its own weight) | mate-value / attractiveness outcome | **grounded (folds into PH-ATTRACT)** |
| **PH-TEMPERAMENT** | reactive/affective temperament — **already** the existing `TraitSeed` temperament seed (fear/threat reactivity priors). Not a new physical channel. | — (existing substrate) | already wired | — | **covered — no new work** |
| **PH-AGILITY** | is there an intrinsic property *others respond to*? Agility is a bearer motor capacity, not obviously a perceived social cue. | — | (bearer capacity at most; no clear percept channel) | — | **FLAG — thin; likely defer or bearer-capacity-only** |
| **PH-SENSORY** | sensory acuity is a bearer perceptual capacity (an input gain on what the bearer perceives), not a "how others respond" cue. | — | (could set the bearer's own input-channel gain; not a social percept) | — | **FLAG — thin as a social trait; possible bearer input-gain only** |

**Open question for the design session (PH-AGILITY / PH-SENSORY):** the honest keystone is "a trait
others *perceive*." Agility and sensory acuity don't obviously present a social percept — they are
bearer capacities. Options: (a) leave them out this pass; (b) wire them only as bearer-side capacities
(sensory acuity as input-channel gain; agility unused) with that limitation stated; (c) find a
grounded perceived-cue prior I've missed. I lean (a)/(b) and flag rather than force a social effect.

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
   - Lin et al. 2011, *Nature* 470:221–226 `[DOI 10.1038/nature09736]` — VMHvl as the aggression locus;
     attack-activated neurons are inhibited during mating (opponent populations).

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

## 5. How it lands in the seed (v10 mechanics — sketch, for review before detailing)

1. **`TraitSeed.physical`** gets populated (it is read but never set today) from the seed's
   `physical_endowment` distributions, with `sex` as a parameter on the sex-dependent ones (PH-SIZE).
2. **A physical-stimulus percept**: the bearer's PH-ATTRACT / PH-SIZE / PH-HEALTH become a small
   `stimulus`-style dict carried on the person, presented to a *perceiver's* substrate when they
   encounter the bearer (the same trigger-vocabulary channel Things and the Arena already use — reuse,
   don't invent).
3. **`innate_wiring_catalogue` entries** (the cited priors): "attractive-face percept → perceiver
   reward" (Langlois/Aharon); "formidability percept → perceiver defensive-threat/submission" (Sell).
   Each with confidence + evidence_base + sources, and a **scaffold** flag on the magnitude.
4. **Sex parameters** on PH-SIZE's distribution and on the VMHvl circuit's Esr1/subdivision parameters
   (Hashikawa/Lin), as given-parameter values — no hormonal dynamics.
5. **Version bump v9 → v10**, circuit/edge counts updated, `gaps_register` updated (what's still
   scaffold, what's still assumed).

None of this codes a social outcome: every entry is a percept + a prior on the *perceiver's* own
circuits, or a distribution/circuit parameter. The outcomes (beauty premium, sex ratio) are scan
objectives.

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

## 7. What I need from the design session (this review)

1. **Verify the grounding** entry by entry — especially the DOIs I flagged `[verify]`, and whether the
   PH-ATTRACT mechanism claim (Aharon/O'Doherty reward-circuit activation) is the right anchor for "an
   intrinsic reward prior," vs. something stronger.
2. **Rule on PH-AGILITY / PH-SENSORY** — leave out, bearer-capacity-only, or a grounded cue I missed.
3. **Confirm the sex scope** — given-parameter only (PH-SIZE mean + VMHvl parameters), no hormonal
   machinery, this pass.
4. **Confirm the two outcomes are scan objectives**, not coded — the beauty premium and the CU sex
   ratio as `scan_match` targets, never weights.

Once reviewed, I'll detail §5 into concrete seed edits and take it to build.
