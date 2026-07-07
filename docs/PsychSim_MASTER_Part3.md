# PsychSim — Master Design & Build Document, Part 3 (Supplements & Addenda, continued)

*Sealed, versioned supplement to `PsychSim_MASTER.md` and Parts 1–2. Like every Part, this document
is **not** updatable once distributed — further guidance lands in a new Part, never as an edit to a
prior one. Where a section touches something already built, **reconcile, do not overwrite.** Section
numbering continues the global sequence (Parts 2 = S1–S2; this Part = S3–S6).*

This Part packages four things: the **v8 seed additions** (S3), the **proto-psychopath plugin
redesign** (S4), the **pre-8b.4 build guidance** the implementation is waiting on (S5), and the
**subcortical Allen-audit scope** (S6). The canonical substrate is now
`docs/neuralnetworks/psychsim_substrate_seed_v8.json` (supersedes v7).

---

## S3. v8 seed additions — the cognitive/mentalizing social-cognition network

### S3.1 What was added, and why it matters for the thesis

The v7 audit found the **affective-empathy** side of the social brain present (`aIns`, `dACC`, `OFC`,
the amygdala nuclei) but the **cognitive / mentalizing (theory-of-mind)** side largely absent — only
`dmPFC`. That gap is not cosmetic: **psychopathy dissociates the two systems.** The manipulative
"cold" profile is precisely *intact cognitive theory-of-mind + impaired affective empathy* — the
psychopath reads people well while not feeling their distress. v7 could not express that dissociation
(it had the affective side but not the cognitive side to leave intact). v8 adds the cognitive side, so
the CU/psychopathy manipulation can **disrupt one empathy system while sparing the other** — very
plausibly where part of the sophropath/psychopath question lives.

### S3.2 The four circuits (grounded; dynamics scaffold; new domain `social_cognition`)

Consensus mentalizing-network nodes across meta-analyses (Schurz et al. 2014; Van Overwalle 2009; Mar
2011); `dmPFC` was already present. Added:
- **`rSMG-TPJ`** — right supramarginal gyrus / temporoparietal junction: self–other distinction,
  overcoming emotional egocentricity bias, mental-state attribution. *Silani et al. 2013 (TMS-causal);
  Saxe & Kanwisher 2003; Decety & Lamm 2007; Schurz et al. 2014.*
- **`pSTS`** — posterior superior temporal sulcus: social perception (biological motion, intention
  from action, reading social interactions). *Allison, Puce & McCarthy 2000; Deen et al. 2015; Isik et
  al. 2017.*
- **`PCun-PCC`** — precuneus / posterior cingulate: self-referential processing, perspective-taking,
  integrative hub. *Cavanna & Trimble 2006; Van Overwalle 2009.*
- **`ATL-TP`** — anterior temporal lobe / temporal poles: social-semantic knowledge (person knowledge,
  social scripts). *Olson, Plaut & Ranganath 2007; Zahn et al. 2007; Frith & Frith 2006.*

All `baseline_activation`/`tau`/`homeostatic_setpoint`/weights are `# SCAFFOLD`, matching v7's cortical
circuits; confidence `Em`, evidence base human.

### S3.3 Connections (existence/direction grounded; weights scaffold)

17 edges added. The mentalizing core is reciprocal (`rSMG-TPJ ↔ dmPFC ↔ PCun-PCC`), fed by social
perception (`V-dorsal/V-ventral → pSTS → rSMG-TPJ/dmPFC`) and social semantics (`ATL-TP → dmPFC/
rSMG-TPJ`), with the affective link `aIns ↔ rSMG-TPJ`. **The load-bearing subset for the experiment**
is the amygdala→cognitive edges — `aIns → rSMG-TPJ`, `MeA → ATL-TP`, `BA → pSTS`, `BA → ATL-TP`: this
is the wiring by which a throttle on the *affective* side (amygdala/`aIns`) could leave the cognitive
network structurally intact but **under-fed** — the mechanism for "reads but doesn't feel," emergent
rather than stipulated.

### S3.4 Developmental note

The mentalizing network matures **late** — connectivity shifts from local (childhood) to long-range
frontal–posterior integration, peaking in early adulthood (~32 y). The new circuits therefore carry
**late `developmental_online_age`** (2–5 y online, `social_cortex_late` plasticity schedule) and
reinforce, not complicate, the adolescent-maturation story of S2.

### S3.5 Honesty and what remains

These circuits are the **machinery** for self–other/mentalizing that the CU deficit disrupts — not
encodings of any outcome. Their dynamics are scaffold; a given agent's callousness must still emerge
from what a lesion/throttle does to this machinery through development. Nothing here is a "callousness
circuit." Remaining cortical associates (fusiform face area, if face-specific processing is later
wanted) are optional; attitudes/beliefs remain **emergent, never seeded** (Part 2 S-series).

### S3.6 Wiring v8 in

v8 supersedes v7 as the canonical substrate; the substrate engine (`core/substrate/`, per Part 2 S1.2)
should load v8. New circuits/connections gate on by their `developmental_online_age` exactly like the
rest — no engine change, just the newer seed.

---

## S4. The proto-psychopath plugin — redesign to a lesion/throttle module

This **redirects** the study plugin. Drop the inherited multi-seed design (`sophropathic_seed` /
`psychopathic_seed` as distinct adult profiles) entirely — separate outcome-seeds smuggle the answer
into the setup. The researcher's design is stricter and cleaner:

### S4.1 The manipulation (the independent variable)

Apply, from birth, a **throttle (0–100%)** — not a binary switch — to a circuit or a **combination**
of circuits/connections in the affective/empathy network, on an otherwise-ordinary newborn substrate.
A throttle, not a lesion, because psychopathy-relevant dysfunction is *hypofunction*, not absence
(a total lesion overshoots toward Klüver–Bucy); and because a graded reactivity deficit is
biophysically ordinary (malfunctioning dendritic integration → a cell that still fires but needs more
to drive it and drives its targets more weakly). The throttle acts on **nodes** (a gain on a circuit's
reactivity/output) *and* **connections** (a scaling of an edge's weight, optionally with a
plasticity ceiling so a throttled pathway stays weak and *cannot fully learn back to normal*).

**The switch/throttle set** is the affective/empathy network named by the researcher, now all present
in v8: amygdala subnuclei (`LA`/`BA`/`CeA`/`ITC`/`MeA`), insula (`aIns`/`mIns`/`pIns`), cingulate
(`dACC`/`dmPFC`), PFC (`vmPFC`/`vlPFC`/`dlPFC`/`OFC`), hippocampus (`HPCv`), the mentalizing network
(`rSMG-TPJ`/`pSTS`/`PCun-PCC`/`ATL-TP`), and the **connections among them**. The module sweeps
throttle settings (e.g. 0/25/50/100) over single levers first, then combinations.

### S4.2 The read-out (the dependent variable)

The observer layer (App. D) measures the **callous-unemotional (CU) profile** in the developing child
— lack of empathic response to distress cues, absent remorse/guilt signals, shallow/deficient
emotion, an uncaring attitude, reckless/fearless behaviour, and — the sharpest, most measurable — the
**inversion/failure of the punishment response** (a passive-avoidance/aversive-conditioning probe:
does the child fail to learn from punishment, as CU children do?). Operationalised to whatever
instrument the thesis uses (ICU; DSM-5 limited-prosocial-emotions specifier). **All output, none
seeded.**

### S4.3 The honesty line (the researcher's own correction, held)

The lesion/throttle is a **mechanism**, not the answer. What a given throttle combination produces —
whether any yields the CU profile, and what develops afterward — is **observed, not assumed.** No
cause is stipulated (not environment, not anything); no outcome is seeded. A run "produces a
proto-psychopath" iff the child *manifests the CU profile as measured*. What that child becomes later,
and whether any diverge toward sophropathy vs psychopathy, stays strictly downstream and unassumed.

### S4.4 What v8 buys the design

Because v8 now carries both empathy systems, the sweep can throttle the **affective** side
(amygdala/`aIns`) while leaving the **cognitive** mentalizing network structurally intact — the
"reads but doesn't feel" manipulation — and see whether the CU profile emerges. That dissociation was
impossible in v7.

---

## S5. Pre-8b.4 build guidance (the answer the implementation is waiting on)

The 8b.3 report was exemplary in its honesty: it correctly distinguished *mechanisms that emerge*
(DA-gated conditioning, emergent behaviour, weak developmental restraint) from *signature phenomena
not yet demonstrated*, and stopped at invariant 6. Here is the ruling.

### S5.1 The reframe: the phenomena aren't failing to emerge — they haven't been tested

The core phenomena aren't *failing*; the **endowment → substrate-difference → development → behaviour
loop that would produce and test them isn't built over the substrate yet.** So the honest status is
"mechanisms sound; signature phenomena not yet tested," not "don't emerge." That sets the next move:
build the loop, run it, and let the result — either way — be the finding.

### S5.2 The decision

**Yes — build the core-phenomena demonstrations over the substrate now, with the legacy in place, and
pause for 8b.4 only once they visibly emerge (or are shown not to).** Invariant 6 forbids retiring the
legacy until the substrate reproduces; scientific honesty forbids concluding before testing. This is
the make-or-break phase, and it belongs before the irreversible step.

### S5.3 Prioritise the core divergence, incrementally

The sophropath/psychopath divergence is the thesis's heart, and it depends on the loop — **not** on
the two gaps. Build the **minimal** loop for it first: the S4 proto-psychopath manipulation (throttle
the affective-empathy circuitry) on a standard newborn, run through a developmental environment,
CU/behaviour **measured** by the observer layer. Test whether divergence appears; surface the result;
*then* the other phenomena (ambivalent-bond conflict, negativity bias, differential susceptibility),
which share the loop. Learn early whether the core claim holds before investing in the full battery.

### S5.4 The two mechanism-gap rulings (circuit-level; not blocking the divergence)

- **Continuous maturation (adolescent bump).** Approved as diagnosed: feed the late-maturing schedules
  into the executive's **control capacity / gain**, not just plasticity, so restraint keeps
  strengthening into the mid-20s. This is an **engine** change (how it reads the schedules), not a
  seed change; honesty-clean (age enters as a rate; the bump *emerges* from late control × early
  reward). Needed for the adolescent-risk phenomenon, **not** the divergence.
- **DA/satiety state-dependence.** Do **not** scale DA by the computed drive-reduction `r` — that
  breaches R5 (the modulator must be a circuit *output*, and `r` is a computed value). Implement it as
  **circuit modulation**: an interoceptive deficit/hunger circuit (`LH`/arcuate/visceral interoception)
  modulating the primary-reinforcer reward link / VTA excitability, so a sated agent's `sweet→VTA`
  drive is attenuated (biologically, hypothalamic gating of VTA DA). If v8 lacks the deficit→VTA
  modulatory connection, that is a **flagged further seed edit** (a new Part, once authorised) — not
  in this v8, which is the four mentalizing circuits only. Needed for the motivational/homeostatic
  phenomena, **not** the divergence.

Wire both as **scoped sub-steps for their own phenomena**; do the divergence loop first, which needs
neither.

### S5.5 Honesty checkpoints for the divergence loop (where the answer can be smuggled in)

- The proto-psychopath difference is a **throttle on temperament/substrate circuitry** (S4), **not** an
  outcome-category weight. No `callousness=high`.
- Developmental environments are **perturbation patterns**, **not** stipulated valences/outcomes.
- Development is the **meaning-blind plasticity running forward**; nothing intervenes to steer the
  outcome.
- The outcome is **measured by the observer read-out** (CU/triarchic metrics over emergent behaviour),
  **not** read from a coded category.
- The test: does the throttled newborn, developed out, manifest the CU/antisocial signature — and do
  different runs/conditions diverge? Emerges, or it's a finding.

### S5.6 The honest-negative stance, and cadence

If the phenomena do **not** fall out of the biological rule, **surface it** — do not force it with a
coded arbiter, a shadow learner, or a tuned parameter that hands over the outcome. An honest negative
here is itself a real result: it bears on whether a circuit disruption plus development is *sufficient*
to produce the CU/psychopathy profile. Cadence: build the divergence loop (+ the two gaps as scoped
sub-steps), test incrementally, sync, and **hold before 8b.4** for the design-session phenomena review
— the review that decides whether the substrate reproduces the thesis's core claim. Do not retire the
legacy until it does, or until it's shown it doesn't.

---

## S6. Subcortical audit against the Allen connectome — scope (distinct task; size before starting)

The comprehensive-connectome idea cashes out as a bounded, one-off coverage pass for the
**subcortical/limbic** circuits only (mouse↔human homology holds there; cortical/social stays
literature-based per S3). What it involves:
1. **Map** the seed's ~40 subcortical nuclei to the **Allen CCF** ontology (a lookup table; flag human
   nuclei with no clean mouse equivalent).
2. **Pull** projection data per source from the Allen Mouse Brain Connectivity Atlas (API at
   connectivity.brain-map.org or bulk download) — it returns **projection density**, not functional
   weights.
3. **Threshold & filter** to meaningful projections (density cutoff is a recorded judgement).
4. **Diff** against the seed's connections → candidate missing subcortical projections.
5. **Human cross-check** each candidate before adding (subcortical homology is good, not perfect).
6. **Propose** additions as existence/direction only — **weights and dynamics stay scaffold**.

- **Effort:** a real data task (region mapping + API/bulk pull + matrix processing + per-edge human
  cross-check) — on the order of days, not a one-click import.
- **Bound:** subcortical/limbic only; supplies wiring existence/direction, never function or dynamics.
- **Payoff:** systematic, quantified subcortical coverage vs. the piecemeal current set — worth doing
  once, not a standing dependency. Deliverable: a candidate-connection list (in a new Part) for
  authorisation.
