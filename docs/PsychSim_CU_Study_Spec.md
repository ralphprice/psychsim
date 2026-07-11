# PsychSim — CU-study control surface: the validated-CU-seed system

**Design specification. Status: specced, NOT to be built until the engine (v10) is complete.**
This is not a UI module. It is **how the psychopathy study is run** — the bridge that turns the
finished instrument suite (substrate · throttle module · scan controller · bank · Arena · observer)
into a conducted experiment. Its honesty constraints are therefore method constraints, not polish.

---

## 0. What this is, in one paragraph

A *validated CU seed* is a **circuit-throttle configuration that has been proven — by automated
search, against a measured signature — to produce the callous-unemotional phenotype in a developed
child**, saved as a named, transparent, editable, provenance-carrying profile that can then seed CU
children into a study town under a specified family/environment distribution. The config is
**discovered, never designed**; the name records **what it was proven to do**, never a category
assigned in advance.

---

## 1. The governing principle (why this can't be a manual preset)

We do **not** know which circuit deficit produces a CU child. That is the research question. Therefore:

- **A CU seed cannot be hand-authored.** No researcher sets "amygdala 0" and calls it CU. It must be
  *found* by search and *proven* against a measured outcome.
- **The name comes last.** A config is called `CU-Profile-A` **because it was validated** to produce a
  measured CU signature — not because we decided a circuit "is" CU. The label points at evidence.
- **The deprecated `fearless` / `fearless (calc.)` dropdown is exactly what this replaces.** Those are
  temperament presets (a low-fear *starting disposition* — a legitimate endowment) that were being
  read, wrongly, as if they seeded a CU *outcome*. A temperament is an input; CU is an outcome; naming
  a temperament preset after an outcome pre-supposes the answer. This system is the honest replacement:
  the outcome is produced by a *discovered circuit manipulation*, measured, then saved.

**A permanent CU deficit is a throttle held at (or near) 0** — a pathway disabled for life, not a
starting value that development moves off. That is what `set_throttle(circuit, 0)` already expresses.
There may be one such pathway, or two or three; **the search establishes how many and which.**

---

## 2. The backtester = the scan controller applied to a CU objective (no new tool)

**Confirmed design decision: reuse the scan controller's search directly. Build no separate tool.**
The scan controller already carries, *structurally*, every guard this needs — so the CU backtester
inherits them for free and cannot smuggle in an answer:

- objective is a **measured observer signature** or a **held-out clinical CU profile** — there is no
  slot for a hand-drawn target profile (Part 4 S8.3);
- the search **cannot touch the mechanism** — only `set_throttle` (found-not-fitted, architectural);
- **coarse-to-fine** (binary screen → graded on survivors) — the exact shape for "disable a pathway,
  then a pair, then three" (S8.4);
- **viable-first** — a throttle config that produces a non-viable child is the expected "broken"
  background, not a CU result (S8.7 + the "broken is background" ruling);
- every hit is **`candidate_hypothesis`, never `finding`** — promotion needs robustness.

The CU backtester is the scan controller with three study-specific settings:

1. **Objective — the CU signature, measured.** Either *search-for-effect* (maximise a measured CU
   read-out the observer computes — passive-avoidance/punishment-learning deficit, the
   reads-but-doesn't-feel dissociation, low-affiliation read-outs — per-signature, never a composite)
   or *search-for-match* (match a **held-out, provenance-validated clinical CU profile** loaded from
   `data/field/`). **The target is a measured signature or external data — never a profile we drew
   that says "this is what CU looks like."** This is the single most important honesty line in the
   whole feature (see §6).
2. **Target age.** The age at which the signature is measured — researcher-set, any age, **~18 by
   default** (the child has developed far enough for the CU phenotype to be assessable). The backtester
   develops each candidate child to the target age, then measures.
3. **Family / environment distribution** (§4) — the spawn context the candidate develops in.

The backtester then runs the scan's coarse-to-fine search over the throttleable set, develops each
candidate to the target age in the specified family context, measures the CU signature, and returns —
per the scan's existing contract — the config(s) that maximise it (or best match the held-out profile),
each labelled `candidate_hypothesis` with its trajectory and provenance. **Your hypothesis (one
pathway, or two–three, reducing affect toward zero) is tested by this, not assumed.** If a single
throttle produces the signature, the screen finds it; if it takes three, the focused search finds that;
if it's something unpredicted, that is the more interesting result.

---

## 3. What a validated CU seed STORES

**Confirmed: a throttle config applied to a standard newborn** — not a pre-grown agent. The child
develops *from* the deficit in the specified context, so the outcome is re-measured every run and never
frozen. A saved seed is:

```
CUSeed {
  name:            "CU-Profile-A"          # neutral handle (§5)
  throttle_config: { <circuit_id>: <0..100>, ... }   # the manipulation (intact=100)
  family_context:  <FamilyDistribution>    # §4 — travels WITH the config
  target_age:      18.0                     # where it was validated
  provenance: {                             # §6 — non-optional, the reason it earns the name
    objective:         "<measured signature name>" | "match:<held-out pattern id>"
    signature_value:   <measured magnitude at validation>
    intact_baseline:   <same signature in the intact control>
    robustness:        <seed-robustness + scaffold-perturbation status>
    status:            "candidate_hypothesis"    # NEVER "finding" from the backtester
    corroboration:     false                       # a saved seed never self-certifies
    scan_trajectory:   <ref>                        # the landscape it was found in
    substrate_version: "v11"                         # the seed the validation ran on (below)
    date, world_seed
  }
}
```

Applied at spawn: a **standard newborn** + `set_throttle(config)` + developed in `family_context`.
Nothing pre-grown; nothing edited.

**Substrate-version dependency (design-session ruling — the 5-HT caveat).** The provenance carries the
`substrate_version` it was validated on. A CU seed validated **before the serotonergic (dorsal/median
raphe, 5-HT) node is in** must be marked **`aggression_regulation: "provisional — validated on pre-5-HT
substrate"`**. Rationale (§6): 5-HT is the principal aggression/impulsivity-regulating neuromodulator, so
any *aggression-regulation* conclusion drawn on a substrate missing it is provisional until re-validated on
the post-5-HT substrate. Non-aggression signatures (physical-endowment, sex-ratio, reward/affiliation
deficits) are not gated by this. So: **the study apparatus may be built and exercised now; its
aggression-regulation findings do not become non-provisional until the raphe node lands and the seed is
re-validated.**

---

## 4. Family / environment distribution (required for a real CU study)

A proper CU study needs the child seeded into a **specified** family and social context, not a default.
The seeding function exposes these as **spawn-context parameters**, distinct from the throttle config:

- **number of siblings** (and birth order, if wanted)
- **socio-economic status**
- family structure, and the other environmental variables a CU study requires

**Honesty line (this is the one that protects your whole thesis).** These are **perturbation-pattern
distributions, NEVER coded effects.** "Low SES" configures *what stimuli the developmental environment
presents* (resource scarcity, stress perturbations, fewer enrichment `Things`) — it is **not** a coded
"low SES → worse outcome." Whether the environment *interacts* with the throttle to shape the CU
outcome must **emerge and be measured**, never be wired. This is the same discipline that has governed
environment throughout: the environment presents patterns; the substrate's own response is what the
study *discovers*. It is exactly what lets the CU study investigate gene-environment interaction rather
than assume it — the core commitment of the thesis. Any line that maps a family variable directly to an
outcome is the violation; the family variables map only to the perturbation stream the child develops
in.

The family_context travels **with** the throttle config in a saved seed, because a CU seed is "this
circuit deficit *in* this developmental context" — both are needed to reproduce the study condition.

---

## 5. Naming, viewing, editing (where categories could re-enter — and don't)

**Confirmed: neutral handle + transparent, inspectable config.**

- **Name:** a neutral label — `CU-Profile-A`, `CU-Profile-B`. Not a circuit list crammed into a name;
  not a free-text outcome claim.
- **Viewable:** opening `CU-Profile-A` shows the **actual config** — `amygdala 0, hippocampus 20, …` —
  plus the provenance (which signature it was validated against, the value, the intact baseline, the
  robustness status). The meaning lives in the transparent config, not the name.
- **Loadable + editable:** load a profile, tweak the throttles, and **save as a new profile** — but an
  edited config is **unvalidated until re-run through the backtester.** A profile's `CU-` prefix and
  its provenance are only earned by validation; a hand-edited derivative carries
  `status: "unvalidated — re-run to validate"` until it passes. Editing generates a *candidate*, not a
  validated seed.
- **The `CU` in the name records evidence, not assumption.** It means "this config was *proven* to
  produce the measured CU phenotype," and the provenance that proves it travels with it. It is never a
  category we assigned to a circuit.

Optional light metadata in the display (not the name) may summarise the config (e.g. a short
"amygdala↓ hippocampus↓" tag) — but the authoritative content is the full config + provenance panel.

---

## 6. THE honesty line (restated, because it is the study's method)

The backtester's objective is where the CU study could accidentally **prove its own premise**, so this
is enforced structurally, not by discipline:

- **Allowed objectives:** (a) maximise a **measured** CU signature the observer computes over emergent
  behaviour (per-signature, never a composite); (b) match a **held-out, provenance-validated** clinical
  CU profile from external data (never used to build the mechanism).
- **Forbidden:** any hand-drawn "CU target profile" the search optimises toward. If we tell the search
  what CU looks like and it finds a config that reproduces our description, we have proven nothing —
  the config is circular. The scan controller **has no slot for a drawn target**; the CU backtester
  inherits that. Do not add one.
- **The measured-vs-designed distinction, concretely:** we measure whether the CU *phenotype* (the
  passive-avoidance deficit, the felt-empathy collapse, the behavioural signature) **emerges** from the
  circuit deficit. We never tell the substrate what CU *is*. A saved seed is honest because the phenotype
  it produces was *measured to emerge*, not *specified*.
- **Intact control is mandatory.** Every candidate's CU signature is reported **relative to the intact
  (all-throttles-100) baseline** — the CU deficit is the *contrast*, not the raw magnitude (the same
  control-arm discipline as the 2×2 and the scan).
- **A saved seed is `candidate_hypothesis`, and `corroboration: false` from the backtester.** Whether a
  discovered CU config is a real finding is a researcher's judgment over robustness and (for
  search-for-match) held-out corroboration — the backtester never certifies its own result. A CU seed
  becomes a *validated tool for running the study*; the *scientific claim* that "this circuit deficit
  causes CU" is a separate, human, evidence-weighed conclusion.

---

## 7. Spawn integration

- Validated CU seeds appear in the **spawn dropdown** (replacing the deprecated `fearless` presets),
  each shown by its neutral name with the config + provenance inspectable on selection.
- Selecting one seeds children with that throttle config, in that family_context, into the study town —
  as many as the study design calls for (the ~4% base-rate point applies: a study town may seed a
  realistic fraction).
- The throttle-panel UI (deferred, ships with this) is where a config is *manually explored* before
  being handed to the backtester to *validate* — manual exploration proposes, the backtester proves,
  the save records. Manual configs are never saved as validated CU seeds without passing the backtester
  (§5).

---

## 8. How it composes with what's built

- **Throttle module** — the manipulation surface (`set_throttle`, `develop_and_measure`). Built.
- **Scan controller** — *is* the backtester, applied to a CU objective. Built. No new search tool.
- **Observer** — computes the measured CU signatures the objective maximises. Built.
- **Bank** — the pattern for save/load/provenance of a discovered artifact (a CU seed is to a config
  what a banked agent is to a developed state: saved, reloadable, never edited-then-passed-off).
- **Arena / society spawn** — where seeded CU children are developed and studied.
- **This spec** — the control surface that ties them into "run the CU study."

**Sequencing:** build **after v10 is complete** (the engine must be finished — physical endowment +
sex are part of what a CU child develops with, and the sex-ratio question is itself a CU-study target).
Then this is the **first study run** — the bridge from instrument suite to research.

---

## 9. Open questions for the researcher (before build, not now)

1. **The CU signature set** — which measured observer read-outs *are* the CU phenotype for validation?
   (Passive-avoidance/punishment-learning deficit + reads-but-doesn't-feel + low-affiliation is the
   current triad; confirm/extend. Per-signature, and convergence-across-signatures is the stronger
   result.)
2. **Held-out clinical CU profiles** — for search-for-match, these are yours to supply, properly
   sourced, with the `not_used_in_calibration` provenance. (The ICU / relevant CU instruments.)
3. **Family/environment variable set** — the full list a proper CU study needs (siblings, SES, and
   what else), and each one's **perturbation-pattern** definition (what stimuli it configures) — since
   they enter as patterns, never coded effects.
4. **Target-age default and the assessment battery at that age** — ~18 confirmed as default; confirm
   the signature is assessed once at target age vs. across a developmental window.
