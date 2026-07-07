# neuraldesigner — data-driven affect authoring (core)

**Author circuits, pathways and behavioural networks as data, not code.** This
is the seam by which the affect model becomes swappable: instead of the default
circuits being hard-wired into the engine, a `NeuralLibrary` describes them
declaratively, and a `LibraryAgent` runs whatever library it is given.

This is a **core** layer. Its purpose is architectural: it lets a different
study load a different affect model without touching the engine, and it is the
route by which the platform can eventually carry *no* research content in the
core at all — the default circuits becoming just one loadable library among
possible others.

## What it provides

- **A declarative schema** — `InputFeature`, `CircuitDef`, `TriggerDef`,
  `PathwayDef`, `NetworkDef`, assembled into a `NeuralLibrary`. This describes an
  affect model as data: which appraisal features feed which circuits, how
  circuits combine into pathways, and how pathways drive behavioural networks.
- **A runtime (`LibraryAgent`, `Situation`)** — takes a library and a situation
  and produces behaviour, so an authored library is directly runnable.
- **Introspection** — a library can be inspected for its circuits, pathways and
  feedback loops (`find_loops()`), so an authored model is legible before it is
  run.
- **A worked example (`build_example_library`)** — a small authored library with
  a cascade and a loop, demonstrating the schema end to end.

## Use it

```python
from neuraldesigner import build_example_library

lib = build_example_library()
print(len(lib.circuits), "circuits,", len(lib.pathways), "pathways")
print("feedback loops:", lib.find_loops())
```

## Where it sits

A **core** layer that provides the mechanism for authoring; it does not depend
on any extension. The default affect model in `affective_engine` is the
canonical circuit set today; the planned next step is to express that set as a
loadable library here, so swapping the affect model is a data change rather than
a code change.

## Layout

```
neuraldesigner/
  library.py    the declarative schema (features, circuits, pathways, networks)
  runtime.py    LibraryAgent + Situation: run an authored library
  example.py    a worked example library (cascade + loop)
  viz.py        render a library's structure
```

See `docs/ARCHITECTURE.md` for the swap-seam design.
