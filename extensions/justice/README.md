# justice — the criminogenic-justice extension

**Labelling theory as a runnable, sweepable mechanism.** Contact with the
justice system attaches a label, and the label degrades the developmental
environment a child subsequently grows in — less access to ordered institutions,
stigma from adults and peers, fewer legitimate routes to recognition. If the
hypothesis holds, part of the forensic "criminal psychopath" phenotype is
*manufactured* by the very system that studies it; if it does not, switching the
mechanism on barely moves the outcome distribution.

This is an **extension** (optional), built on the core. It makes the
criminogenesis question *runnable*; it does not answer it. Every constant is an
explicit, sweepable assumption, and nothing it produces is evidence about people
— outputs are hypotheses about how such a mechanism *would* behave in given
parameter ranges. It renders Becker (1963) and Lemert (1967) as mechanism.

## What it provides

- **`JusticeParams`** — the mechanism as parameters: detection rate, severity by
  offence type, the contact ladder (warned → charged → convicted), and how much
  warmth, structure and recognition each label level costs. Everything is a dial.
- **`JusticeSystem`** — tracks one child's contact history, rolls seeded
  detection on visible antisocial acts read from the agent's memory, escalates
  the ladder, and derives the *labelled environment* the next segment of
  childhood is lived in.
- **`develop_with_justice`** — runs development in segments, re-deriving the
  labelled environment between them. With `justice=None` it reduces *exactly* to
  plain segmented development, so the ON/OFF comparison isolates the mechanism.
- **`run_comparison`** — grows the *same* cohort twice (identical trait seeds,
  situation streams and randomness), once OFF and once ON, so any shift in the
  outcome distribution is attributable to labelling alone.

## What it finds (illustrative)

The mechanism has genuine dynamic range and does not fabricate. Near the outcome
separatrix, aggressive early labelling manufactures the psychopathic outcome in
up to 100% of children, dose-responsive in detection rate, label severity and
timing; a child clear of the boundary is unmoved even under aggressive
labelling. Because contact accrues only *after* a child offends, the mechanism
also predicts its own timing signature: criminogenic effects should be strongest
for *early* system contact.

## Use it

```python
from justice import run_comparison, JusticeParams
from affective_engine.development import Environment

base = Environment("near-boundary", 0.36, 0.36, 0.34)
early = JusticeParams(base_detect=0.85, warn_at=1, charge_at=2, convict_at=3,
                      warmth_per_level=0.14, structure_per_level=0.16,
                      recognition_per_level=0.14)
off, on = run_comparison(n_children=30, base_env=base, params=early)
print(off.shares()["psychopathic"], "->", on.shares()["psychopathic"])
```

## Honest scope

Simplifications are stated in the source: label effects act only through the
three environment channels the development rule already has (deviant-peer
exposure is subsumed, imperfectly, in the warmth/structure degradation);
offence visibility is treated as binary by situation kind; and the ladder does
not decay, which is the strong form of the labelling claim and therefore an
*upper bound* on the mechanism, not an estimate of it. Outputs are hypotheses
about the mechanism, never evidence about people.

## Layout

```
extensions/justice/
  system.py       JusticeParams, JusticeSystem, develop_with_justice
  experiment.py   the ON/OFF cohort comparison + report
```

Runs as part of `python run_pipeline.py`. See `docs/ARCHITECTURE.md`.
