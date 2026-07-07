"""
demo.py -- a day in the life, in the world.

Builds a home/school/workplace world, puts one person in it (seeded with the
shared root disposition), and walks them through a short sequence of places and
social episodes -- showing, at each step, the mode the affective engine selects,
what the Game-Master makes of it in the world, and how relationships, reputation
and the person's episodic memory accumulate. This is Package 1 (world) driving
Package 2 (the affective engine) end to end.
"""

from __future__ import annotations
from typing import List

from affective_engine import shared_root_seed
from .builder import build_world
from .person import Person, SocialEvent
from .gamemaster import GameMaster


# a scripted little day: (destination place, social event or None)
DAY = [
    ("home", SocialEvent("morning at home", "parent",
                         {"social_valence": 0.6, "goal_relevance": 0.3})),
    ("street", None),
    ("classroom", SocialEvent("offered cooperation", "classmate",
                              {"reward": 0.5, "social_valence": 0.5, "goal_relevance": 0.6})),
    ("playground", SocialEvent("provoked by a peer", "bully",
                               {"provocation": 0.8, "social_valence": -0.7,
                                "goal_relevance": 0.6, "controllability": 0.3})),
    ("classroom", SocialEvent("a chance to cheat, unobserved", None,
                              {"reward": 0.8, "goal_relevance": 0.7,
                               "other_distress": 0.4, "controllability": 0.2})),
    ("street", None),
]


def run_day(warm: bool = True) -> str:
    preset = dict(home_warmth=0.90, home_structure=0.85) if warm \
        else dict(home_warmth=0.20, home_structure=0.25)
    w = build_world(**preset)
    gm = GameMaster(w)

    w.institutions["Family"].add_member("alex", "child")
    w.institutions["School"].add_member("alex", "pupil")
    alex = Person("alex", "Alex", shared_root_seed())
    w.place_agent("alex", "home")

    L: List[str] = []
    W = L.append
    W("=" * 72)
    W(f"  A DAY IN THE WORLD  --  home climate: {'warm & firm' if warm else 'harsh & inconsistent'}")
    W("=" * 72)
    W(f"  {'place':<11} {'institution':<9} {'event':<28} -> mode")
    W("  " + "-" * 68)
    for dest, event in DAY:
        # move if adjacent, else place directly (the scripted route is valid)
        if not w.move_agent("alex", dest):
            w.place_agent("alex", dest)
        inst = w.governing_institution("alex")
        inst_kind = inst.kind if inst else "-"
        inter = gm.run_episode(alex, event)
        label = event.kind if event else "(just present)"
        W(f"  {dest:<11} {inst_kind:<9} {label:<28} -> {inter.network}")
    W("  " + "-" * 68)
    W("")
    W("  world state after the day:")
    W(f"     reputation(Alex)      = {gm.reputation.get('alex', 0.5):.2f}")
    for (a, b), r in gm.relationships.items():
        W(f"     relationship {a}->{b:<9} affect {r.affect:+.2f}  trust {r.trust:+.2f}")
    W(f"     episodic memory       : {alex.mind.memory.summary()}")
    W("=" * 72)
    return "\n".join(L)


if __name__ == "__main__":
    print(run_day(warm=True))
    print()
    print(run_day(warm=False))
