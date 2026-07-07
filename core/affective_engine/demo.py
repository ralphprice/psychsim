"""
demo.py -- the developmental-separation experiment.

Takes ONE identical circuit-seed (the shared root disposition), raises two
agents from it in two different moral environments, and shows the trajectory
fork.  This is the programme's central developmental claim, running in code:
same disposition, different history, different reachable repertoire, different
outcome -- and the branch point is the growth of the conscience-linked control
circuit and the accessibility of a strategic-prosociality network.
"""

from __future__ import annotations
from typing import List, Tuple

from .core import shared_root_seed
from .agent import AffectiveAgent
from .development import (Environment, warm_firm_home, harsh_inconsistent_home,
                         develop, classify)


def raise_agent(env: Environment, n_episodes: int = 48):
    agent = AffectiveAgent(seed=shared_root_seed())
    develop(agent, env, n_episodes=n_episodes)
    return agent, classify(agent)


def _bar(x: float, width: int = 22) -> str:
    filled = int(round(max(0.0, min(1.0, x)) * width))
    return "#" * filled + "-" * (width - filled)


def report(n_episodes: int = 48) -> str:
    seed = shared_root_seed()
    a_env, b_env = warm_firm_home(), harsh_inconsistent_home()
    a_agent, a_out = raise_agent(a_env, n_episodes)
    b_agent, b_out = raise_agent(b_env, n_episodes)

    L: List[str] = []
    W = L.append
    W("=" * 70)
    W("  DEVELOPMENTAL-SEPARATION EXPERIMENT")
    W("  One identical disposition, two moral environments.")
    W("=" * 70)
    W("")
    W(f"  Shared root seed: '{seed.name}'")
    W(f"    boldness  = attenuated THREAT ({seed.gains['THREAT']:.2f}) "
      f"/ ANXIETY ({seed.gains['ANXIETY']:.2f})")
    W(f"    affiliation= CARE ({seed.gains['CARE']:.2f}) "
      f"SOCIAL_LOSS ({seed.gains['SOCIAL_LOSS']:.2f})  (partly attenuated)")
    W(f"    CONTROL   = {seed.gains['CONTROL']:.2f}  (weak / undeveloped at start)")
    W(f"    INSTRUMENTAL_CONTROL = {seed.gains['INSTRUMENTAL_CONTROL']:.2f}")
    W("")
    W("-" * 70)

    for tag, env, agent, out in [("A", a_env, a_agent, a_out),
                                 ("B", b_env, b_agent, b_out)]:
        W(f"  AGENT {tag}  --  raised in: {env.name}")
        W(f"     (warmth {env.warmth:.2f} | structure {env.structure:.2f} "
          f"| recognition {env.recognition:.2f})")
        W("")
        W("     emergent drive-profile (strength of each primary system):")
        for k, v in sorted(out.profile.items(), key=lambda x: -x[1]):
            W(f"        {k:<10} {v:5.2f}  |{_bar(v)}|")
        W(f"     dominant system: {out.dominant.value}")
        W("")
        W("")
        W(f"     >>> CLASSIFIED OUTCOME: {out.classification.upper()}")
        W("-" * 70)

    W("")
    W("  READING:")
    W("  Both agents began from the IDENTICAL disposition and met the IDENTICAL")
    W("  stream of situations. They differ only in how their environment")
    W("  responded. The warm, firm, recognising home grew the conscience-linked")
    W("  control circuit and made strategic prosociality reachable; the harsh,")
    W("  inconsistent home did neither and instead consolidated the exploitative")
    W("  and reactive repertoire. The branch point is mechanistic and visible.")
    W("=" * 70)
    return "\n".join(L)


if __name__ == "__main__":
    print(report())


def three_way_summary(n_episodes: int = 48) -> str:
    """Same root disposition, three destinations: the sophropath, the reactive
    (unsuccessful) psychopath, and the calculated (successful) psychopath -- the
    distinction the forensic tradition collapses."""
    from .core import shared_root_calculating_seed

    rows = [
        ("sophropath",
         AffectiveAgent(seed=shared_root_seed()), warm_firm_home()),
        ("psychopath / reactive (unsuccessful)",
         AffectiveAgent(seed=shared_root_seed()), harsh_inconsistent_home()),
        ("psychopath / calculated (successful)",
         AffectiveAgent(seed=shared_root_calculating_seed()), harsh_inconsistent_home()),
    ]
    L = ["", "=" * 74,
         "  THREE DESTINATIONS FROM ONE DISPOSITION",
         "  (environment builds conscience-control; temperament sets instrumental control)",
         "=" * 74, ""]
    header = (f"  {'target':38} {'ctrl':>5} {'ictrl':>6} {'strat':>6}  "
              f"{'provocation response':22}")
    L.append(header)
    L.append("  " + "-" * 70)
    for target, agent, env in rows:
        develop(agent, env, n_episodes=n_episodes)
        o = classify(agent)
        result = o.classification            # the emergent dominant primary system
        prof = " ".join(f"{k[:4]}:{v:.2f}" for k, v in sorted(
            o.profile.items(), key=lambda kv: -kv[1])[:3])
        L.append(f"  {target:38} {prof}")
        L.append(f"       -> dominant system: {result}")
    L.append("  " + "-" * 70)
    L.append("  The conscience-linked CONTROL circuit (built by warm, firm,")
    L.append("  recognising care) makes the sophropath; with it weak, the level of")
    L.append("  cold INSTRUMENTAL control decides whether the psychopathy is")
    L.append("  reckless-and-reactive or calm-and-calculated. Note the behavioural")
    L.append("  tell: only the reactive subtype rages under provocation.")
    L.append("=" * 74)
    return "\n".join(L)
