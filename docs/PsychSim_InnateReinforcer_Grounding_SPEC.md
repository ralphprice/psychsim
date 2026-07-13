# PsychSim — Innate-Reinforcer Grounding (the first Point-1 grounding)

**Design specification. Status: SPEC ONLY — nothing built. For researcher review.**
This is the **first research-grounded innate-strength grounding (Point-1)**, so it sets the precedent and
the methodology for every Point-1 grounding after it. It grounds the **8 innate-reinforcer edges** that
the uniform-0.5 start flattened from their `moderate-strong` innate value — each with its **own
per-edge citation** for that reinforcer's documented innate strength. It lands as one unit with the
uniform-start change (they are a unit: the blank start is only a *working* substrate once the innate
reinforcers carry their documented strength).

---

## 0. Why this exists (the diagnostic finding it resolves)

The uniform-start diagnostic returned **Outcome 1** (the substrate self-organizes from a blank uniform
start — HSO's optimizer was never needed). But the diagnostic also surfaced, exactly as the handover's
§2.1/§6 anticipated, that the uniform null **flattened a specific, principled class of edges: the innate
reinforcers.** These are the hardwired primary-reinforcer wiring (sweet=reward, pain=threat,
bitter=aversion, suffocation=threat, hunger=appetitive, loud-onset=startle) — **present and strong from
birth, non-plastic by design.** The uniform 0.5 wrongly flattened 8 of them from their `moderate-strong`
value; because they are non-plastic input edges, **nothing in development restores them** (experience
cannot produce an *innate* prior). The lost `paired>unpaired` learning discrimination is the *reward
instance* of this catalogue-wide under-service.

**This is the clean Point-1 signal:** a primary reinforcer is, by definition, "genuinely innate strength
experience-from-a-blank-start cannot produce." So the honest fix is to ground these edges' innate
strength **from the research** (an educated guess from the literature — never a convenience fit), NOT to
raise the global operating point (0.7) to make the learning test pass (which would be choosing the whole
substrate's operating point for an outcome — forbidden).

---

## 1. Scope (the 8 edges — ruled: the demonstrably-weakened class, not just the 2 tested)

Ground the **8 innate-reinforcer edges whose original band was `moderate-strong` and which the uniform
0.5 demonstrably weakened.** Grounding only the 2 reward edges the learning test needs would leave 6
known-wrong edges in the substrate solely because no test watches them — the latent-failure trap.
They are one class with one demonstrated finding (innately strong, flattened, unrecoverable-because-non-
plastic); grounding the class consistently is the honest application, grounding only the tested pair is
the convenience application.

**In scope (8):**
| # | edge | reinforcer class | plastic? | role in mechanism |
|---|---|---|---|---|
| 1 | `IN-GUST:sweet → VTA` | reward (DA-teaching) | non-plastic input | US drives the DA teaching signal — **carries the paired>unpaired discrimination** |
| 2 | `IN-GUST:sweet → NAc-shell` | reward (hedonic) | non-plastic input | US → hedonic reward readout — **discrimination** |
| 3 | `IN-SOMATO:nociception → LA` | nociceptive threat | non-plastic input | pain US → threat/aversive-learning amygdala |
| 4 | `IN-SOMATO:nociception → CeA` | nociceptive threat | non-plastic input | pain US → threat-output amygdala |
| 5 | `IN-GUST:bitter → CeA` | gustatory aversion | non-plastic input | bitter US → innate aversion |
| 6 | `IN-INTERO:CO2_acidosis → CeA` | interoceptive threat | non-plastic input | suffocation-alarm US → fear |
| 7 | `IN-INTERO:nutritive_state → LH` | appetitive drive | non-plastic input | hunger US → feeding drive |
| 8 | `COCH → StN` | acoustic startle | **plastic** | loud-onset US → startle (the one plastic edge — see §3) |

**NOT in scope:** the other 11 innate-reinforcer edges, which were `moderate` (≈0.5) originally — the
uniform 0.5 did NOT demonstrably weaken them (null matches prior value). They are **recorded as "null
matches prior value, no demonstrated under-service — grounded only if a future diagnostic implicates
them."** We do not ground on speculation (their prior `moderate` was itself hand-set, so "null agrees
with prior" is not proof either is correct — but absent a demonstrated under-service, we leave them). We
ground only where the null is *demonstrably* wrong.

---

## 2. The grounding methodology (the precedent — per-edge, cited)

For EACH edge: (1) name it by its **mechanistic role** (done, §1 — not chosen by weight-search); (2) cite
the literature establishing **that reinforcer's innate strength** (below); (3) set the grounded value
from the citation as an **educated guess from research** (§4). The *class* is grounded consistently; the
*values and citations are per-edge*. **This is grounding, not a catalogue-wide bump** — each value has
an external, edge-specific justification, and its effect on function (learning discrimination) is a
downstream consequence, not the reason for the value.

### 2.1 Per-edge literature grounding (innate strength documented)
- **Reward pair (1, 2) — `sweet → VTA` / `sweet → NAc-shell`:** the sweet→reward pathway is documented as
  a **robust, hardwired primary reinforcer**. Sweet is "unavoidably and intrinsically laden with reward
  value"; innate attraction is present from first exposure (stereotyped neonatal facial reactions);
  sweet-evoked dopamine release in ventral striatum occurs even without post-ingestive signals; the
  ponto-VTA projection is anatomically "robust." *Sources:* Neurobiology of Sensation and Reward (NCBI
  Bookshelf, taste chapter); Boughter et al. 2019 (robust caudal-PBN→dorsal-VTA projection); Berridge &
  Kringelbach 2008; Ventura & Mennella 2011 (innate sweet preference). → **strong innate reinforcer.**
- **Nociceptive-threat pair (3, 4) — `nociception → LA` / `→ CeA`:** the spino-parabrachio-amygdaloid
  pathway is a **hardwired "general alarm system"** relaying innate threat; PBel→CeAl produces "strong
  depolarization" of amygdala neurons; CGRP-PBel neurons are critical for relaying the aversive
  unconditioned stimulus to CeA. *Sources:* Han et al. 2015 (CGRP-PBN→CeA relays the US, defensive
  responses + threat memory on stimulation); the parabrachio-CeA "general alarm" pain-sensitization work
  (Neuropsychopharmacology 2023 / bioRxiv 2023). → **strong innate reinforcer.**
- **Gustatory-aversion (5) — `bitter → CeA`:** bitter is a **hardwired innate rejection** signal ("bitter
  rejection is an innate response commonly seen in mammals," neonatal negative facial expressions); sweet
  and bitter are "hardwired circuits encoding innate responses" with "strong" amygdala feedback. *Sources:*
  Jin et al. 2021 (Top-Down Control of Sweet and Bitter, *Cell* — "hardwired circuits," strong amygdala
  feedback); innate bitter-rejection review (PMC6312290). → **strong innate reinforcer.**
- **Interoceptive-threat (6) — `CO2_acidosis → CeA`:** the amygdala is a **direct chemosensor for
  CO2/acidosis that elicits innate fear** — "evolution positioned a sensor for hypercarbic acidosis in
  the amygdala"; rising CO2 forewarns suffocation, "a terrifying situation that demands sensitive
  detection." *Source:* Ziemann et al. 2009 (*Cell*, The Amygdala is a Chemosensor that Detects CO2 and
  Acidosis to Elicit Fear). → **strong innate reinforcer.**
- **Appetitive drive (7) — `nutritive_state → LH`:** the LH is the classic **hardwired "hunger
  motivational system"**; hunger/AgRP→LH drives "strong and long-lasting" appetitive and consummatory
  feeding "crucial for survival." *Sources:* Morgane 1961 (*Nature*, hunger motivational system in LH);
  the LH-feeding-circuits review (PMC6195675, "strong and long-lasting" appetitive responses). → **strong
  innate reinforcer.**
- **Acoustic startle (8) — `COCH → StN`:** the acoustic startle reflex is a **hardwired short-latency
  "survival mechanism of alarm"**; the cochlear-root-neuron → PnC pathway "mediates fast neurotransmission"
  and is obligatory for startle (lesions abolish it). *Sources:* Lee et al. 1996 (*J Neurosci*, obligatory
  CRN→PnC primary startle pathway); Gómez-Nieto et al. 2014 (CRN-PnC fast neurotransmission). → **strong
  innate reinforcer** (but note §3 — this edge is plastic).

**Every value below traces to one of these edge-specific citations.** No value is set because it makes a
test pass.

---

## 3. The one subtlety — edge 8 (`COCH → StN`) is PLASTIC, the other 7 are not

7 of the 8 are non-plastic input edges (the primary-reinforcer priors — they *should* be non-plastic and
innately set; that is what a hardwired reinforcer is). Edge 8 (`COCH → StN`) is **plastic**. This matters:
- For the 7 non-plastic edges, the grounded innate value is *load-bearing and permanent* — development
  cannot change it, so the grounded starting value IS the operating value. Grounding is essential.
- For edge 8 (plastic), development *can* move it — so grounding its start is less critical (experience
  could partly compensate). But it is the same class (a documented innate startle prior), so for
  consistency it gets the same grounded start; its plasticity then operates from the grounded value.
- **Flag for review:** should edge 8 be grounded like the others (consistency — it's the same innate
  class), or left uniform (it's plastic, so experience handles it)? Lean: **ground it** — it's a
  documented innate reinforcer of the same class, and consistency of the class-grounding is the honest
  rule; its plasticity operating from a grounded start is fine. But it's the one genuinely-optional case.

---

## 4. The values (grounded, not tuned)

All 8 edges were originally `moderate-strong`. The honest grounded value is the one the *original band
encoded* — i.e. restore the `moderate-strong` innate strength that the uniform null flattened, now
**justified by the per-edge citations** (§2.1) rather than by the original hand-set band. Concretely:
- Set each of the 8 edges' starting weight to the **`moderate-strong` value** (the same numeric the band
  mapped to — the diagnostic showed these were 0.7 before flattening), now grounded as "documented strong
  innate reinforcer, cited per §2.1."
- **This is not re-hand-setting the weight to 0.7 for convenience** — it is grounding it to the innate
  strength the literature documents (strong primary reinforcer), which happens to be the `moderate-strong`
  band. The justification is the citation, not the number; the number follows from "strong innate
  reinforcer."
- **Do NOT tune the value to optimise the learning metric.** The value is "documented strong innate
  reinforcer" (per citation); if learning discrimination returns as a consequence, good (it should — the
  reward pair's DA teaching signal is restored); if some edge needs a *different* strength to match its
  citation (e.g. a reinforcer documented as *very* strong vs. moderately strong), ground it to *that*,
  per the source — not to what the metric wants.

---

## 5. Verification (functional consequence, not target)

- **Learning discrimination restored:** with the reward pair (1, 2) grounded, `test_paired` should pass
  (paired > unpaired) — as a **downstream consequence** of the restored DA teaching signal, NOT because
  the value was chosen for it. Report it as a consequence.
- **The other 6 edges:** verify they carry their grounded innate strength (the threat/aversion/appetitive/
  startle priors are present at strength). No specific test may exercise them today — that's expected;
  they're grounded because the principle implicates them, and their correctness is anatomical (documented
  strength) not test-demonstrated.
- **Full suite green at operating point 0.5** — the uniform-start value stays 0.5 (the R8 normalization
  equilibrium `len×0.5`, principled — §operating-point finding); the innate reinforcers are grounded on
  top of it. The suite goes green because the substrate now both self-organizes (uniform start) AND
  carries its innate priors (grounded reinforcers) — the honest unit.
- **v9 closure, functional invariants:** still hold (they held throughout the diagnostic).
- **NO result is a target** — learning discrimination returning is a consequence of grounded anatomy; no
  emergent pattern is preserved or chased.

---

## 6. What lands, and how (the unit)

**One commit (red-tree discipline):** the uniform-start change (all weights → 0.5) and the 8 grounded
innate-reinforcer edges land **together**, suite green at 0.5 — because committing the uniform start alone
lands a deliberately-red tree (`test_paired` fails until the reward pair is grounded), and we never land a
known-red tree. They are genuinely a unit: the blank start is a *working* substrate only once the innate
reinforcers carry their documented strength.

**Reviewed before landing:** since this is the precedent-setting first Point-1 grounding, the grounding is
**surfaced for reviewer review before the joint commit** — the per-edge values *and* their per-edge
citations (not just "learning passed"). The reviewer checks that **each value traces to a citation about
that edge** (the methodology), not merely that the suite is green.

**Ledger:** `docs/hso/uniform_start_and_innate_grounding.md` — Outcome 1 (uniform-start self-organization),
the operating-point finding (0.5 = R8 equilibrium, a scaffold governing activity level, grounds
biologically if ever needed), and the 8 per-edge innate-reinforcer groundings with citations.

---

## 7. Scope boundary (what this is NOT)
- **NOT the whole innate-reinforcer catalogue** — only the 8 demonstrably-weakened edges; the 11 `moderate`
  ones are recorded, not grounded (no demonstrated under-service).
- **NOT a global operating-point change** — 0.5 stays (principled); the fix is per-edge innate grounding,
  not a bump to 0.7.
- **NOT HSO** — HSO stays shelved (Outcome 1 confirmed it's not needed). This is uniform-start + innate
  grounding, no homeostatic optimizer.
- **NOT epigenetic spawn-state modification** — that remains the deferred layer scoped to the CU study
  (recorded, not built).
- **NOT re-grounding other assumption-basis weights** — the 74 `assumption` weights become plastic under
  uniform-start and self-organize; only the innate-reinforcer priors (which are non-plastic and must be
  innately set) need grounding. The broader weight-grounding question is settled by Outcome 1 (plasticity
  differentiates them); only the innate priors are the exception.

---

*This is the first Point-1 grounding: it grounds the 8 innate-reinforcer edges the uniform null flattened,
each cited to that reinforcer's documented innate strength, establishing the per-edge grounding
methodology. It lands as one unit with the uniform-start change (suite green at 0.5), reviewed before the
joint commit. Nothing is built until the researcher approves. HSO stays shelved; the operating point stays
the principled 0.5; no result is a target.*
