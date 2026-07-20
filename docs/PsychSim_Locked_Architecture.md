# PsychSim — THE LOCKED ARCHITECTURE
### The model is a coupled body-brain loop that records. Build it out top-down.

**This replaces the layer-ladder framing (substrate → learning → representation → …), which I drew as if the
brain were a stack of cognitive faculties. It is not. The model is the architecture YOU described, and it is
already substantially built. This document locks it and gives the top-down build-out.**

---

## 1. THE ARCHITECTURE — one sentence, then the diagram

**A person is a brain bound to a body; the body's sensory apparatus is the only aperture to the world; other
people are perceived through that aperture and expressed to through it; and every exchange is recorded in the
matrices, which IS the person developing.**

```
        ┌─────────────────────── THE WORLD / THE GROUP ───────────────────────┐
        │                                                                      │
        │   ┌── PERSON A ──────────────┐          ┌── PERSON B ──────────────┐ │
        │   │                          │          │                          │ │
        │   │   ┌─ BODY (boundary) ─┐  │          │  ┌─ BODY (boundary) ─┐   │ │
        │   │   │ sensory apparatus │◄─┼──signal──┼──┤ expression        │   │ │
   ARC1 │   │   │ (IN-* channels)   │  │          │  │ (face/voice/…)    │   │ │  ARC3
        │   │   └─────────┬─────────┘  │          │  └─────────▲─────────┘   │ │
        │   │             ▼            │          │            │             │ │
        │   │   ┌─ BRAIN (substrate) ─┐│          │┌─ BRAIN (substrate) ────┐│ │
   ARC2 │   │   │ perceive→appraisal  ││          ││  affect→social_act     ││ │  ARC2
        │   │   │ affect (D6/D7 core) ││          ││  (emergent behaviour)  ││ │
        │   │   │ interoceptive loops ││          ││                        ││ │
        │   │   │  = FEELING itself   ││          ││                        ││ │
        │   │   └─────────┬───────────┘│          │└────────────────────────┘│ │
        │   │             ▼            │          │                          │ │
        │   │   ┌─ EXPRESSION ────────┐│          │                          │ │
   ARC3 │   │   │ face/voice/gesture ─┼┼──signal──┼──► B's sensory apparatus  │ │  ARC1
        │   │   └─────────────────────┘│          │                          │ │
        │   │             │            │          │                          │ │
        │   └─────────────┼────────────┘          └──────────────────────────┘ │
        │                 ▼                                                     │
        │   ┌─ THE RECORD (matrices) ──────────────────────────────────────┐   │
   ARC4 │   │ environment_matrix · group_matrix · relations · norms ·      │   │
        │   │ self_reflection · timeline  →  THIS IS THE PERSON DEVELOPING  │   │
        │   └──────────────────────────────────────────────────────────────┘   │
        └──────────────────────────────────────────────────────────────────────┘

  The exchange = A's ARC3 (expression-out) becomes B's ARC1 (perception-in), and back.
  Development   = ARC4: every exchange leaves a trace that changes who each person is.
```

---

## 2. WHAT EXISTS — the honest map, per arc (verified against the repo today)

**The loop is far more built than the "climb" framing implied. The pieces are all present; the frontier is
their FIDELITY and their COUPLING, not their existence.**

| arc | what it is | what exists | maturity |
|---|---|---|---|
| **ARC 1 — perception-in** | world → sensory apparatus → appraisal | **9 input channels** (`IN-VIS/AUD/OLF/GUST/SOMATO/PROPRIO/VESTIB/INTERO/CONSPEC`); `Person.perceive()` turns world state into an `Appraisal` the brain acts on | **substantial** — channels exist; `IN-CONSPEC` (conspecific = other-people channel) is the key social aperture |
| **ARC 2 — the brain** | appraisal → affect → emergent behaviour | **the 96-region substrate**; `AffectiveAgent`; the reactive/affective core (D6/D7); interoceptive loops that ARE feeling; `social_act()` produces emergent `SocialBehaviour` | **strong** — this is what the whole descent built and hardened |
| **ARC 3 — expression-out** | affect → face/voice/gesture → signal in world | **the L7 expression apparatus** (NuFac, M1-face, PMC-l, the vocal effectors, Mc); **a `speech` module** (`acts.py`, `faithfulness.py`, `render.py`) | **substantial** — the transmitting side of the aperture; L7 built the effectors, speech adds verbal |
| **ARC 4 — the record** | exchange → trace → development | **the whole `sim_world`**: `environment_matrix`, `group_matrix`, `relations`, `norms`, `self_reflection`, `timeline`, `person`, `population`, `daily`, `gamemaster` | **present, least mature** — the matrices exist; the question is whether the exchange truly lands and truly records-as-development |

> **The reframe this forces: the model is NOT missing a cognitive layer. It is a loop with all four arcs
> present, and the real work is making each arc — and especially the COUPLING (A's expression → B's
> perception) and the RECORD (does the trace change the person) — more faithful.**

---

## 3. ★ THE FRONTIER — stated in the model's own terms, not a borrowed theory's

**The honest frontier is not "representation" as an abstract faculty. It is two specific fidelity questions:**

1. **Does the exchange CLOSE?** When A expresses (ARC3), does that signal actually enter B's sensory apparatus
   (ARC1) and move B's affect (ARC2)? Or is `social_act` currently adjudicated by the world abstractly,
   without literally passing through the other agent's perception? **This is the coupling question — the "great
   exchange mechanism."** `IN-CONSPEC` existing is the promising sign; whether A's expression drives B's
   `IN-CONSPEC` is the thing to verify.
2. **Does the record shape DEVELOPMENT?** When an exchange lands, does the trace in the matrices actually change
   who the person is going forward — their memory, their expectations, their future behaviour? **This is the
   memory-as-lived-experience question.** The matrices recording is necessary; the matrices *feeding back into
   the substrate* is what makes it development rather than a logbook.

> **These two — coupling and record-feedback — are the model's real growth edges, and they are exactly what
> "our window on the mind" requires: you watch the mind by watching the loop run and accumulate over a
> lifetime. Everything else (imitation, learning, habit, morality) is a BEHAVIOUR of this loop running, not a
> separate module to build.**

---

## 4. THE BUILD DISCIPLINE — top-down, accuracy-increasing, no rabbit holes

**You asked for a solid architecture to build out top-down — filling the whole model to greater accuracy each
step, not descending into detail. Here is the discipline:**

> **Every build pass makes the WHOLE loop more faithful, not one arc deeper. We do not perfect an arc before
> moving on; we raise the fidelity of the complete loop, then raise it again.** This is the opposite of the D6
> descent (which went deep on one column). The substrate needed that depth because it is the grounded
> foundation. The loop does NOT — it needs breadth-first fidelity, because its value is the whole cycle
> turning, and a perfect ARC3 coupled to an empty ARC4 is worth nothing.

**The top-down passes, each raising whole-loop fidelity:**

| pass | what it makes more faithful | the test (S35 — a claim, not completion) |
|---|---|---|
| **P1 — close the exchange** | ARC3→ARC1 coupling: A's expression literally enters B's perception | Two agents in a room: does A's emotional display measurably move B's affective state through B's sensory channel? |
| **P2 — the record feeds back** | ARC4→ARC2: the matrix trace changes the person | Does an agent behave differently toward someone it has a recorded history with, vs a stranger? |
| **P3 — the exchange accumulates** | ARC4 over time: repeated exchanges become relationship/development | Over many days, do stable relationships and divergent individual histories EMERGE from the accumulated record? |
| **P4 — the self-aware loop** | expression as input to the SELF (self_reflection): a person perceives their own acts | Does an agent's own expression/behaviour update its self-model (the `self_reflection` arc)? |
| **P5+ — fidelity of each arc** | richer perception, richer expression, richer needs — as needed | each raises realism; none is opened until a claim needs it |

**The rule that prevents spiral:** a pass opens only when the previous pass's CLAIM is demonstrable, and each
pass targets whole-loop fidelity. **We are not building faculties; we are turning the crank and making the
whole cycle more lifelike each turn.** The substrate-hardening backlog (S56 etc.) is drawn from ONLY when a
loop-pass's claim specifically needs it — otherwise it waits.

---

## 5. WHAT I NEED TO VERIFY NEXT (the honest precondition for P1)

Before locking P1 as the first build, one diagnostic — because the architecture above is mapped from module
NAMES and I should confirm the SEAMS:

- **Does `social_act` (A's output) connect to `perceive`/`IN-CONSPEC` (B's input)?** i.e. is the exchange
  already wired, partly wired, or adjudicated abstractly by the `gamemaster` without passing through the other
  brain? **This single question decides whether P1 is "wire the coupling" or "deepen an existing coupling."**
- **Do the matrices already feed back into the substrate, or only record?** decides whether P2 is "build the
  feedback" or "strengthen it."

**These are two file-reads (`gamemaster.py`/`daily.py` for the exchange, `self_reflection.py`/`person.py` for
the record-feedback). Say the word and I read them and report — then we lock P1 with its exact scope, and start
turning the crank top-down.**

---

## 6. THE RELABELING (for the register, so we stop defending a ladder)
- **The "layers/ladder" (D2–D7) is RETIRED as an architecture.** It was a build-ORDER for the substrate, and
  the substrate is essentially built. **The architecture is the four-arc loop.**
- **D6/D7 = ARC 2 (the brain), done and hardened.** The substrate-hardening backlog belongs to ARC 2.
- **The climb is retired.** The forward plan is the **top-down loop-fidelity passes (P1…)**.
- **"Representation/D3" is not a rung** — it is a property that emerges as the record (ARC4) feeds back and
  accumulates. It gets built as P2/P3, in the model's own terms (the record shaping the person), not as an
  abstract faculty.

> **The model is a window on the mind: a body-bound brain, perceiving and expressing through its sensory
> aperture, exchanging with other such minds through the world, and BECOMING someone through the accumulated
> record of those exchanges. That is the architecture. It is built in skeleton. We now turn the crank
> top-down, making the whole more faithful each pass — and the honesty wall still governs every arc: the
> behaviour emerges, it is never scripted.**
