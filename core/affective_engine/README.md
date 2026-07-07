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

- **Circuits** — leaky-integrator drives (THREAT, ANXIETY, SEEKING, FRUSTRATION,
  CARE, SOCIAL_LOSS, and two regulatory circuits, CONTROL and
  INSTRUMENTAL_CONTROL) computed from an `Appraisal` of a situation.
- **Behavioural networks** — the modes a person can act in: affiliative warmth,
  strategic prosociality, cool instrumental boldness, reactive aggression,
  callous exploitation, fearful withdrawal. Each is driven by a weighted mix of
  circuits, with an arbitration step that settles on the dominant one.
- **Trait seeds** — dispositions as parameter sets (`shared_root_seed`,
  `sophropathic_seed`, `psychopathic_seed`, and others), so two agents can differ
  only in temperament and let the environment do the rest.
- **A development rule (`develop`)** — a childhood lived in an environment shifts
  conscience-control plasticity and network access, with plasticity declining
  with developmental age. Supports **graded (sigmoid) affordances** so outcome
  boundaries can be smooth rather than knife-edge at 0.5.
- **Episodic memory** — a memory stream that primes appraisal from similar past
  episodes, so history shapes behaviour by a second, bounded pathway alongside
  development.
- **An outcome classifier (`classify`)** — reads behaviour on a probe battery and
  labels the outcome sophropathic / intermediate / psychopathic. Psychopathy is
  scored by the **callous-exploitative core** (exploiting, or being unmoved by, a
  *vulnerable other*), not by reactive aggression and not by pursuing a victimless
  reward.

## Use it

```python
from affective_engine import (AffectiveAgent, shared_root_seed,
                               warm_firm_home, harsh_inconsistent_home,
                               develop, classify)

agent = AffectiveAgent(seed=shared_root_seed())
develop(agent, harsh_inconsistent_home(), graded=True)
print(classify(agent).classification)      # e.g. "psychopathic"
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
  core.py           appraisal, circuits, networks, trait seeds, the language actuator stub
  agent.py          the AffectiveAgent: tick, settle, arbitrate
  development.py    the development rule (+ graded affordances) and the classifier
  memory.py         the episodic memory stream and appraisal priming
  demo.py           developmental separation from one seed across two homes
```

See `docs/ARCHITECTURE.md` for how the engine sits under the world, experiment,
visualiser and explorer.
