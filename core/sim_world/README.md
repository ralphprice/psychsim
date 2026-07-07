# sim_world — world & agents (core)

**The world and agent architecture: places, objects, institutions,
memory/history, time, the Game-Master, and now dialogic interaction —
integrated with the affective-circuit engine.**

This is a **core** layer. Where the affect engine gives a person an emotional
interior, this layer gives them a world to live in: somewhere to be, other
people to act on and talk to, institutions whose climate shapes them, and time
across which they age.

## What it provides

- **A places graph** — a home, a school (classroom, playground), a workplace, and
  public space, wired together so movement is local (you can only go somewhere
  adjacent). Places hold objects with affordances.
- **Institutions** — a family, a school, an employer, a peer group — each with a
  climate (warmth, structure) and an incentive regime (reward for cooperation,
  sanction for defection). The institution governing a person depends on where
  they are.
- **Embodied people** — each `Person` *is* an affective agent: it owns an
  `AffectiveAgent` mind, has a body/needs proxy the engine reads, ages on the
  developmental clock, has a life stage, and a `perceive` method that turns the
  local world state into the appraisal the engine acts on.
- **The Game-Master** — turns the mode the engine chooses into world change:
  relationships shift, reputation moves, and the institution's response feeds the
  same validated development rule the engine uses. It is rule-based and
  inspectable, not a model call, so the world is legible and reproducible.
- **Dialogic interaction (`GameMaster.converse`)** — two co-present people hold a
  two-turn encounter: the speaker emits the speech-act its settled network makes,
  the hearer appraises the *act it perceives* (not the words) and answers, and
  both acts are adjudicated into the world and written to each mind's memory.
  This is where the language layer joins the living simulation — deception
  included, resolved by a seeded roll grounded in the hearer's vigilance.
- **Two clocks** — a fine interaction clock (social episodes) and a coarse
  developmental clock (aging and life-stage transitions).

## How the world and the affect engine join

```
   world                                 affect engine
   -----                                 -------------
   Person.perceive(world, event)  --->   Appraisal
                                         AffectiveAgent.settle(appraisal)
   GameMaster.adjudicate(person,  <---   dominant behavioural network
                         network)
      relationships, reputation,
      institution response valence --->  memory + development
```

A childhood lived across the world's institutions drives the *same* development
the engine models from a bare environment — verified in the tests:
`institution_to_environment(family)` raised warm-and-firm yields a sophropathic
outcome; raised harsh-and-inconsistent yields a psychopathic one. The world does
not re-implement cognition; it *situates* it.

## Use it

```python
from sim_world import build_world, Person, GameMaster, SocialEvent
from affective_engine import shared_root_seed, psychopathic_seed, sophropathic_seed

world = build_world(home_warmth=0.90, home_structure=0.85)
gm = GameMaster(world, seed=7)

alex = Person("alex", "Alex", shared_root_seed())
world.place_agent("alex", "classroom")
inter = gm.run_episode(alex, SocialEvent("offered cooperation", "classmate",
                       {"reward": 0.5, "social_valence": 0.5, "goal_relevance": 0.6}))
print(inter.network, gm.reputation["alex"])

# a dialogic encounter between two co-present people
cal = Person("cal", "Cal", psychopathic_seed(), birth_day=-9000)
ann = Person("ann", "Ann", sophropathic_seed(), birth_day=-9000)
world.place_agent("cal", "street"); world.place_agent("ann", "street")
opp = SocialEvent("opportunity", "ann",
                  {"reward": 0.8, "other_distress": 0.7, "threat": 0.0})
convo = gm.converse(cal, ann, topic="the money", event=opp)
print(convo.transcript())   # Cal's exploit voiced as warmth; Ann's reply
```

## Local norms — the mechanism, not the values

`norms.py` adds the point no map-style world captures: **the same conduct is not
acceptable everywhere.** The core carries only the *machinery*: a place holds a
**norm profile** mapping a study-defined behaviour category to how acceptable it
is there, on a neutral symmetric scale (encouraged … unacceptable). An act is
assessed by looking up its category in the local profile; acting below what a
place expects is a **norm departure**, with a magnitude, and witnessing one
colours an observer's appraisal. The core names **no categories** and ships **no
profiles** — what any conduct *means*, and what each place expects, are supplied
by a study. This keeps the instrument neutral: it does not presume that any
behaviour is prosocial, disruptive, or anything else, still less an offence.

## Interiors, access, and a functioning day

A place is no longer only a bare node. `interior.py` gives it an **interior** of
areas an agent moves through, connected by **access** rules — open, restricted to
certain roles, or closed (a private room, a members-only space, a hard boundary
are all configurations; the universal feature is *who may enter where*, and thus
respect for the boundaries one is granted). Each area holds **affordance-objects**
whose actions carry **preconditions** (a role present and attending, being
observed or unobserved) and an **effect**: the appraisal imposed on the actor,
which is what the affective engine then acts on. `daily.py` runs a **rule-based
day** (not autonomous planning): a routine puts each agent in a place doing an
activity, and the engine decides *how* they act; a `categorise` seam lets a study
supply how behavioural networks map onto its own categories.

The core ships **no venues, routines or categories** — a home, a school, a
workplace, and the conduct and social rules they involve, are supplied by a
study. The reference sophropathy study provides them in
`extensions/sophropathy/world.py`: a home with a family interior and an optional
shared sibling bedroom, a school with an orderly classroom and a permissive
playground, an adult workplace, a community setting, a symmetric social category
set with a positive pole (warmth, cooperation, restraint) as first-class as any
departure, and the matching local norms. Another study would replace that module
entirely.

## The relational fabric of a functioning society

`relations.py` adds what a society *is*, not what a study supplies: the standing
relationships any society has by definition — parent–child, teacher–pupil,
colleague–colleague, teammate–teammate, captain–player, a community group, an
employer and an employee. Each is a directed **tie** carrying a role-pair, a
**power differential**, and a **relational state** that registers **strain and
repair** — because a working society *notices* when a relationship is upheld and
when it is strained, and that felt strain is exactly what social norms and
restraint exist to manage. Both parties act through the affective engine on
appraisals coloured by the tie (power, standing, strain); **reciprocity and
restraint are the functioning default** — the senior party exercises authority
with care, the other responds with respect, and the tie holds and repairs. When
either side presses an advantage or disengages, the tie is strained, and a
cohesive society repairs low strain over time. `Society.cohesion()` reads the
share of ties upheld. This is normal social functioning, so it is core; the core
registers *that* a relationship worked or was strained, and attaches no judgement
of character to it. *Why* a tie strains — a particular disposition, and what its
strain-patterns mean developmentally — is the perturbation a study introduces,
and lives in an extension.

## Layout

```
sim_world/
  world.py          places graph, objects, institutions, the two-rate clock
  person.py         the embodied person: mind, body, age, life stage, perception
  gamemaster.py     adjudicates modes into world change; dialogic converse
  interior.py       interiors: areas, affordance-objects, access rules (neutral)
  daily.py          the rule-based day loop (machinery only)
  norms.py          the local-norm mechanism (no categories of its own)
  relations.py      the society's standing ties: strain, repair, cohesion
  builder.py        assembles a home/school/workplace world (+ presets)
  demo.py           a day in the world
```

Depends on the affect engine and the speech layer; nothing in the core forbids
that (both are core). See `docs/ARCHITECTURE.md`.
