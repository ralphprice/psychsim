# PsychSim — calibration and validation plan (valence/motivation subsystem)

*How the scaffold numbers get set, and how we test that the model's behaviour concords with the
constructs — the decisive gate the thesis rests on. Companion to the design doc, code-change map, and
build instructions.*

---

## 1. The central methodological principle (read first)

The model is only worth anything if its psychological results **emerge** rather than being fitted in.
That imposes a hard separation that the rest of this plan protects:

- **Calibration tunes low-level mechanism** — the shape of taste hedonics, a fear-extinction rate, the
  dopamine RPE signature, arousal/HRV dynamics, maturation timings — against physiology, the
  neuroscience literature, and the thesis's own studies.
- **Validation tests high-level emergent phenomena** — adolescent risk-taking curves, the negativity
  bias, approach–avoidance conflict, differential susceptibility, and above all the sophropath/
  psychopath divergence — on data and phenomena the calibration did **not** target.
- **Never tune a parameter to hit a validation target.** If we adjusted the numbers until the
  sophropath/psychopath split came out right, the model would demonstrate nothing. The split, and the
  other targets, must fall out of mechanism calibrated on *other* grounds. This is the single rule
  that separates a result from an artefact.

This mirrors what the codebase already assumes ("Stage 5 calibrates against the human studies…
nothing here is fitted to data") and the thesis's own honesty wall.

---

## 2. The parameter inventory (what is scaffold)

Everything below is a placeholder to be set by §3, collected in one params module (per the build
instructions):

- **State vector (App. A):** per-variable set-points; `fixed` vs `allostatic` designation; drive-
  function shape/curvature; drive weights `w_k`.
- **Innate perturbations (App. B):** the gain on each hardwired sensor→variable link; the per-cue
  **learning-rate multipliers** for prepared learning.
- **Learning (App. C):** `BETA` (valence scale), `GAMMA` (discount), `ALPHA` (learning rate),
  `LAMBDA` (eligibility); the model-free/model-based arbitration weight.
- **Selection (App. F):** decision thresholds; accumulation rates; Go/NoGo and STN-hold strengths;
  softmax temperature; the tonic-dopamine operating point (inverted-U).
- **Matrices (App. 3/4):** Dunbar slot sizes and decay rates; the salience→slot mapping; the pooled-
  prior blend weight.
- **Development (§6):** circuit onset ages; plasticity/critical-period windows; the executive-
  maturation curve; the epigenetic early-window sensitivity.
- **Endowment (§5):** the *ranges and covariances* of the temperament parameters across the population
  (including the atypical/proto-disposition region — App. E).

---

## 3. Calibration — sources and procedure

Given the model's **functional-illustrative** scope, calibration is mostly *range- and shape-based*
(getting dynamics and orderings right), not precise point-fitting. Two levels:

**3a. Low-level mechanism → physiology and the neuroscience literature.** Set the mechanistic
parameters so the components behave qualitatively as documented: taste hedonics (innate liking/
rejection), fear acquisition/extinction asymmetry and time-course, the dopamine RPE signature
(shift from outcome to predictor), arousal/HRV stress-recovery dynamics, the maturation gradient
timing (reward early, prefrontal into the mid-20s), and the opioid/oxytocin social-reward gating
(e.g. a naltrexone-analogue manipulation should *reduce* modelled social reward — a check drawn from
Løseth et al. 2024). Use the verified reference set for target behaviours; where only a direction is
known, calibrate to the direction, not a number.

**3b. Developmental mappings → the thesis's own studies.** The parent→environment and
environment→outcome mappings (`parent_to_environment`, the develop loop) are what Study 5 calibrates
against the human data (Studies 2–3). Fit the *shape* of these mappings (e.g. how caregiving warmth/
structure relate to executive-control development) to the study data, holding the mechanism from 3a
fixed.

**Procedure:** calibrate 3a first (component behaviour), then 3b (developmental mappings), then
**freeze**. Record every calibration target and its source. Anything not pinned by 3a/3b is left at a
neutral default and enters the sensitivity analysis (§5).

---

## 4. Validation — the concordance gate

Validation runs the **observer read-outs** (Appendix D) — the simulated agent "takes the same tests"
as human participants — and compares emergent behaviour to human patterns, on phenomena **not used in
calibration**.

**4a. The validation-target battery** (each a runnable probe from the build instructions):
- the **sophropath/psychopath divergence** and its **childhood emergence** (the primary test) — the
  same proto-disposition reaching adaptive vs antisocial outcomes under warm-firm vs harsh-
  inconsistent development, matching the thesis's documented pattern;
- **differential susceptibility** (fearless child diverges by environment; typical child internalises
  under adversity);
- **adolescent risk-taking** (a curvilinear bump that resolves with executive maturation);
- the **negativity bias** ("bad is stronger than good" in learning and impression formation);
- the **ambivalent-bond** signature (approach–avoidance conflict, sustained arousal, its destructive
  behavioural pull);
- **"a punishment for one is a reward for another"** (the same event, opposite valence across
  endowments).

**4b. Types of validity to establish:**
- *Construct* — do the observer read-outs (triarchic dimensions, CU traits, punishment/passive-
  avoidance learning, aggression type) map onto the human constructs with the expected structure?
- *Predictive* — does the model reproduce patterns **not** used to calibrate it (held-out phenomena)?
- *The emergence requirement* — for each target, confirm the outcome was **not** coded (e.g. show the
  divergence appears only through temperament × environment, disappears if either is neutralised).

**4c. What counts as passing.** A target passes if the *qualitative* pattern and *ordering* match the
human data and emerge without being fitted. Given scaffold numbers, we are testing shapes and
directions, not effect sizes — claiming more would overreach the model's scope.

---

## 5. Robustness and mechanistic checks

Because the numbers are scaffold, robustness *is* the evidence:

- **Sensitivity analysis / parameter sweeps.** Vary each scaffold parameter across a plausible range
  and check whether the validation-target phenomena **persist**. **Robust emergence** (phenomena hold
  across ranges) is strong support; **knife-edge** phenomena (appear only at one tuning) are suspect
  and must be flagged, not reported as findings.
- **Ablation.** Remove a mechanism and confirm the predicted deficit appears — knock out the opioid
  social channel → social reward collapses; remove the executive brake → impulsivity/ persistence of
  prepotent responses; flatten the maturation gradient → no adolescent bump. This is mechanistic
  validation that the phenomena come from the parts we claim.
- **Dose/manipulation checks.** Analogue manipulations should move behaviour in the documented
  direction (naltrexone→less social reward; higher tonic dopamine→more impulsive selection).

---

## 6. Methodological guards (against circularity and researcher degrees of freedom)

- **Pre-register** the validation targets, the observer-read-out operationalisations, and the
  **calibrate-on-X / validate-on-Y split** before running validation.
- **No tuning to targets.** Parameters are set only by §3; validation is read-only. If a target fails,
  that is a *result about the model*, not a cue to adjust numbers.
- **Hold-out.** Calibrate on some studies/phenomena, validate on independent ones; never both on the
  same data.
- **Report failures.** Publish where the model does *not* reproduce the human pattern — the honest and
  informative outcome, and a guard against selective reporting.
- **Falsifiability.** State in advance what would disconfirm the model (e.g. if the sophropath/
  psychopath divergence required coding the outcome; if the biases only appeared at a single knife-
  edge tuning; if ablating a claimed mechanism left its phenomenon intact).

---

## 7. What success and failure look like (honest criteria)

- **Success:** the validation-target phenomena emerge, in the right direction and ordering, from
  mechanism calibrated on independent grounds; they are robust across scaffold-parameter ranges;
  ablations behave as predicted; and the sophropath/psychopath divergence tracks the thesis's
  childhood-divergence data **without the outcome being coded**.
- **Failure (equally informative):** a target requires tuning-to-fit, is knife-edge, survives ablation
  of its claimed mechanism, or contradicts the human data. Any of these is reported as a limitation
  and, where possible, traced to the responsible assumption.

---

## 8. Honesty ledger and connection to the thesis

- Calibration sets **mechanism**, validation tests **emergence** — kept strictly apart; nothing is
  tuned to produce the psychological result.
- The plan is **range/shape-based**, matching the model's functional-illustrative scope (App. A.5,
  and the substrate review): we claim the model reproduces *patterns*, not *magnitudes*.
- Calibration ties to **Studies 2–3–5** and the developmental mappings the codebase already flags for
  Stage-5 calibration; validation ties to the thesis's construct instruments (Study 1–4).
- Every scaffold number remains labelled until calibrated, and every calibration target is recorded
  with its source — so a reader can see exactly what was fitted and what emerged.
