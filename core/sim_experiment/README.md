# sim_experiment — the experiment framework (core)

**The experimental-manipulation layer — the part that turns the platform into a
study.** It manipulates the two things the programme is about, runs whole life
courses at scale, and reads the outcome from behaviour.

This is a **core** layer, built on the world and the affect engine. It supplies
the *mechanism* for running factorials; the specific research design that uses
it lives in an extension.

## The two manipulations

1. **Trait configuration** (`conditions.SEED_FACTORY`) — which disposition an
   agent is seeded with. The scientific comparison holds the fearless *root*
   disposition fixed and lets the environment do the work.
2. **Moral / developmental environment** (`conditions.CONDITIONS`) — the life
   course an agent is raised through: childhood (home + school), the transition
   (further education / first job), and adulthood (an occupational role), each
   with its own warmth / structure / recognition and duration. Presets contrast
   *warm-firm-throughout*, *harsh-inconsistent-throughout*, and — the interesting
   ones — *harsh-home-then-warm-turn* and *warm-home-then-harsh-world*.

## What it runs

`run_life` raises one seeded agent through the stages of a life course, carrying
the *same person* across all of them so the trajectory is continuous, and returns
the classified outcome (with an optional stage-by-stage trace). `run_factorial`
crosses every seed with every condition, runs each cell across many random seeds,
and aggregates — reporting the share of seeds giving each outcome, so
between-seed variation is a reported quantity rather than noise averaged away.

## What it finds (illustrative)

With the shared fearless disposition held fixed:

| life course | outcome |
|---|---|
| warm-firm throughout | **sophropathic** |
| harsh-inconsistent throughout | **psychopathic** |
| harsh home → warm turn later | **intermediate** (partial rescue only) |
| warm home → harsh adult world | **intermediate** (early start protects) |

The two mixed-timing conditions are the point. A warm turn *after* a harsh
childhood lifts the trajectory out of a psychopathic outcome but cannot reach
full sophropathy, because plasticity declines with developmental age and the
sensitive period has passed. A warm childhood followed by a harsh adult world
leaves a durable conscience-control circuit that prevents a full psychopathic
outcome even as the loss of prosocial affordances erodes strategic prosociality.
**When** the environment is warm or harsh matters, not only whether it is — a
counterfactual no real cohort can run: same disposition, different life, measured
impact.

## Use it

```python
from sim_experiment import run_life, run_factorial, seeds, conditions

r = run_life(seeds()["shared_root"], conditions()["harsh_home_then_warm_turn"], trace=True)
print(r.stage_trace, "=>", r.classification)

fr = run_factorial(n_runs=30)
print(fr.table())
```

## Honest scope

A *functional* model whose warrant is behavioural; parameters are illustrative
and are *calibrated* in the programme to the human studies (Study 2 for homes,
Study 5 for classrooms). With the illustrative parameters the cells are
near-deterministic — that is honest, not manufactured; the runner reports genuine
between-seed variance wherever the calibrated, noisier parameters produce it. A
simulation generates hypotheses; it is not evidence about people.

## Layout

```
sim_experiment/
  lifecourse.py     run one whole life across staged environments
  conditions.py     the two manipulations: seeds x moral life courses
  batch.py          the factorial runner with seed replication + aggregation
  demo.py           the factorial report + one traced life
```

See `docs/ARCHITECTURE.md`.
