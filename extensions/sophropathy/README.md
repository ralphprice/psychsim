# sophropathy — the reference extension

**The seven-stage experimental programme, and the family/society model it needs
— a staged design that builds from a balanced society up to fearless children
raised by dispositional parents.**

This is an **extension**: it is built on the core (`affective_engine`,
`sim_world`, `sim_experiment`), and the core knows nothing about it. It is the
research-specific content of the sophropathy programme; a different study would
be a different extension, reusing the core unchanged.

## What it adds to the core

1. **A family / society model (`society.py`)** — families and populations, and
   the distinction between the child dispositions the programme studies: the
   **typical** child (ordinary fear and empathy — the control) and the
   **fearless** child (the shared root disposition: attenuated threat/fear,
   undeveloped conscience-control — the "proto-psychopath / sophropathic" child,
   whose adult outcome development decides).

2. **The parent → environment mechanism** — parents who are themselves
   dispositional, and whose disposition *shapes the caregiving environment* their
   children experience: warmth grows with the parent's capacity to care (CARE),
   structure with their conscience-linked self-command (CONTROL). This closes the
   loop that lets stages 6–7 model a psychopathic or sophropathic *parent*.

## The seven stages (`stages.py`)

| Stage | What it does | The design role |
|---|---|---|
| **1** | A balanced, functioning society (ordinary parents, caring homes) | The perfect-condition **reference** |
| **2** | A mix of caring, balanced and dysfunctional family types | Introduce **imbalance** — the environmental landscape |
| **3** | Typical children developed across those family types | The **control** |
| **4** | Fearless children across those family types | The **core manipulation** |
| **5** | The same, with family/child parameters calibrated to the human studies | **Faithful modelling** (placeholder until data) |
| **6** | Psychopathic/sophropathic **parents** raising typical children | The **parent → environment → child** pathway |
| **7** | Those parents raising fearless children | The **full gene × environment interaction** |

## What it shows (illustrative parameters)

- **Stage 3 vs 4 — differential susceptibility.** In a dysfunctional home the
  *typical* child reaches an *intermediate* outcome (conduct/dysregulation, but
  empathy intact — it does not exploit the vulnerable), while the *fearless*
  child reaches the full *psychopathic* outcome. In caring homes both do well.
  The fearless disposition is uniquely sensitive to the family environment — for
  good and ill.
- **Stage 6 vs 7 — transmission through environment.** The *same* psychopathic
  parent leaves a typical child at *intermediate* but drives a fearless child to
  *psychopathic*: same parent, opposite outcome, transmitted through the
  environment the parent creates. A sophropathic parent yields good outcomes for
  both.

These are the designed contrasts, and they emerge from the mechanism rather than
being stipulated.

## Use it

```python
from sophropathy import run_stage3, run_stage4

s3, s4 = run_stage3(n=20), run_stage4(n=20)
# typical vs fearless child in a dysfunctional home:
print([c.modal for c in s3.conditions if "dysfunctional" in c.label])  # intermediate
print([c.modal for c in s4.conditions if "dysfunctional" in c.label])  # psychopathic
```

## An honest note on the model (please read)

- **The classifier is scored by the callous-exploitative core**, not by reactive
  aggression and not by pursuing a victimless reward: psychopathy is exploiting,
  or being unmoved by, a *vulnerable other*. Reactive aggression with intact
  empathy is conduct/dysregulation, not psychopathy. This refinement — first made
  in this extension — is now back-ported into the core engine, so all layers
  agree; it is both more faithful to the callous-unemotional literature and what
  makes the typical/fearless contrast meaningful.
- **Stage 5 calibration is a placeholder.** The family-type prevalences and child
  profiles are clearly marked `PLACEHOLDER` and must be replaced with the
  findings of Study 2 (family environments) and Study 5 (child profiles) before
  the stage carries any empirical weight. The structure is ready; the numbers are
  not claimed.
- **Everything is computed, nothing is fitted or invented.** The parameters are
  illustrative; the outcomes are outputs of the mechanism, not empirical findings
  about people. A simulation generates hypotheses for the human studies to test;
  it is not evidence about humans.
- **The parent → environment mapping is a transparent modelling choice**, not a
  measured relationship; it is one of the things the human studies calibrate.


## The world-driven childhood (the closed loop)

`lived.py` (`raise_in_world`) raises a child by living a childhood in a home and school built here: each situation the child meets moving through the world -- weighted toward the testing moments a conscience is built in -- feeds the core's validated `develop_step`, with the plasticity-gating environment derived from the home's warmth and structure and how the parent-child tie is going. The classifier reads the adult outcome. A fearless child becomes sophropathic in a warm-firm home and psychopathic in a harsh one; a typical child resists psychopathy in the same harsh home. The outcome is produced by the life lived, not set -- a test-bed in which later refinements to the world become observable in the result. It is deliberately rough and will be improved.

## Layout

```
extensions/sophropathy/
  society.py    child & parent dispositions; parent -> environment; families & society
  stages.py     the seven stages, each a runnable configuration
```

Runs as part of `python run_pipeline.py`. See `docs/ARCHITECTURE.md`.
