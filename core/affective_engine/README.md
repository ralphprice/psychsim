# affective_engine — the affect mechanism (core)

**A functional, circuit-level model of emotional and mental process for
generative-agent simulation** — the novel research contribution at the heart of
the platform, and the layer everything else is built to situate, manipulate,
visualise and explore.

This is a **core** layer. It is *functional, not biophysical*: inspired by
circuit-level affective neuroscience, it is not a simulation of neurons. Its
warrant is behavioural — it reproduces the developmental divergences the
programme is about.

## What it provides

- **The behaviour engine** — the circuit **substrate** (`core/substrate/`, ~82
  nucleus-level circuits loaded by `load_substrate`) is the live engine;
  `AffectiveAgent` wraps it and runs it per tick. *(The earlier leaky-integrator
  Panksepp 7-drive engine, `drives.py`, and the outcome-category **behavioural
  networks** + arbitration step were **retired and removed** — see the honesty
  note in `core.py`. THREAT / ANXIETY / SEEKING / … survive only as temperament
  **gain biases**, not as circuits.)*
- **Trait seeds** — dispositions as parameter sets (`shared_root_seed` and others):
  temperament gains plus the valence-engine endowment, so two agents can differ
  only in temperament and let the environment do the rest.
- **A development rule (`develop`)** — a childhood lived in an environment shifts
  plasticity with developmental age, so outcome divergence is **produced by the life
  lived, not stipulated**.
- **Episodic memory** — a memory stream that primes appraisal from similar past
  episodes, so history shapes behaviour by a second, bounded pathway alongside
  development.
- **A descriptive read-out (`classify`)** — reads the emergent substrate
  (`read_mind`) and reports which domain dominates. It is **measurement, not a
  driver, and attaches NO verdict**; the study's outcome constructs are computed
  separately by the observer read-out (`observer.py`), over emergent behaviour,
  never fed back.

## Use it

```python
from affective_engine import (AffectiveAgent, shared_root_seed,
                               harsh_inconsistent_home, develop, classify)

agent = AffectiveAgent(seed=shared_root_seed())
develop(agent, harsh_inconsistent_home())
readout = classify(agent)      # DESCRIPTIVE read-out of the emergent substrate -- no verdict
```

## Honest scope

- **Functional, not biophysical.** Its warrant is behavioural, not neural.
- **Illustrative, not fitted.** Every parameter is illustrative; every number the
  engine prints is computed by the mechanism from those parameters, not an
  empirical estimate and not invented. Calibration to the human studies is a
  named, pending step.
- **A simulation generates hypotheses; it is not evidence about people.**

## Layout

```
affective_engine/
  core.py           appraisal, trait seeds, and affect primitives
  agent.py          the AffectiveAgent: wraps the circuit substrate; tick, settle
  development.py    the development rule and the descriptive read-out (classify)
  memory.py         the episodic memory stream and appraisal priming
  demo.py           developmental separation from one seed across two homes
```

See `docs/ARCHITECTURE.md` for how the engine sits under the world, experiment,
visualiser and explorer.
