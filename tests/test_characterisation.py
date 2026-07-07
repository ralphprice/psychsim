import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""Phase 0 (PsychSim_MASTER build) -- CHARACTERISATION BASELINE.

A parity safety net for the valence/motivation migration. It snapshots the *current*
behaviour of the developmental read-outs (develop -> probe -> classify) across the study
seeds x canonical environments, plus one deterministic call into each of the three
matrices, and compares against a committed golden file.

This does NOT assert that any behaviour is correct -- only that it does not change
unnoticed while the substrate/valence engine is migrated behind the stable interfaces.
Later phases that intentionally change these read-outs regenerate the golden WITH A NOTE
(set PSYCHSIM_REGEN_CHAR=1) and record the change in the commit.
"""

import json
import random
import unittest

from affective_engine.core import (shared_root_seed, sophropathic_seed,
                                    psychopathic_seed)
from affective_engine.agent import AffectiveAgent
from affective_engine.development import (develop, probe, classify,
                                          warm_firm_home, harsh_inconsistent_home)
from affective_engine.drives import Brain, System
from sophropathy.society import typical_child_seed

from sim_world import Society, interact, PARENT_CHILD, Person
from sim_world.group_matrix import Group, GroupMatrix, group_encounter
from sim_world.environment_matrix import Thing, EnvironmentMatrix, encounter

_GOLDEN_DIR = _O.path.join(_ROOT, "tests", "characterisation")
_GOLDEN = _O.path.join(_GOLDEN_DIR, "baseline.json")

# fixed everywhere so the whole snapshot is reproducible
_TEMPERAMENT_SEED = 4242
_SIT_SEED = 20260704
_PROBE_SEED = 999

_SEEDS = {
    "typical_child": typical_child_seed,
    "shared_root": shared_root_seed,
    "sophropathic": sophropathic_seed,
    "psychopathic": psychopathic_seed,
}
_ENVS = {"warm_firm": warm_firm_home, "harsh_inconsistent": harsh_inconsistent_home}


def _round(x, n=4):
    return round(float(x), n)


def _develop_snapshot() -> dict:
    """develop -> probe -> classify for every seed x environment."""
    out = {}
    for seed_name, seed_fn in _SEEDS.items():
        for env_name, env_fn in _ENVS.items():
            ag = AffectiveAgent(seed_fn(), temperament_seed=_TEMPERAMENT_SEED)
            develop(ag, env_fn(), situation_seed=_SIT_SEED)
            readout = classify(ag)
            out[f"{seed_name}|{env_name}"] = {
                "probe": probe(ag, situation_seed=_PROBE_SEED),
                "classification": readout.classification,
                "profile": {k: _round(v) for k, v in sorted(readout.profile.items())},
            }
    return out


def _relations_snapshot() -> dict:
    soc = Society()
    tie = soc.add("Pat", "Sam", PARENT_CHILD, standing=0.5, strain=0.4)
    hm = Person("h", "h", sophropathic_seed()).mind
    lm = Person("l", "l", psychopathic_seed()).mind
    for _ in range(6):
        interact(tie, hm, lm)
    return {"strain": _round(tie.strain), "standing": _round(tie.standing),
            "state": tie.state()}


def _group_snapshot() -> dict:
    brain = Brain.from_temperament(random.Random(1))
    gm = GroupMatrix()
    mem = gm.membership("team", "team")
    team = Group("team", "a team", "team", cohesion=0.6, norm_strength=0.6)
    for et in ("acceptance", "cooperation", "competition", "acceptance",
               "cooperation", "rejection", "acceptance", "cooperation"):
        group_encounter(brain, team, mem, et, age_years=12)
    return {"belonging": _round(mem.belonging), "standing": _round(mem.standing),
            "encounters": mem.encounters}


def _environment_snapshot() -> dict:
    brain = Brain.from_temperament(random.Random(1),
                                   reactivity_bias={System.SEEKING: 0.9,
                                                    System.FEAR: 0.2})
    m = EnvironmentMatrix()
    treat = Thing("treat", "a treat", "food", {"reward_cue": 0.9})
    for _ in range(5):
        encounter(brain, treat, m)
    bond = m.bond("treat")
    return {"attraction": _round(bond.attraction), "aversion": _round(bond.aversion),
            "state": bond.state()}


def build_snapshot() -> dict:
    return {
        "develop": _develop_snapshot(),
        "relations": _relations_snapshot(),
        "group": _group_snapshot(),
        "environment": _environment_snapshot(),
    }


class TestCharacterisationBaseline(unittest.TestCase):
    def test_matches_committed_baseline(self):
        snap = build_snapshot()
        if _O.environ.get("PSYCHSIM_REGEN_CHAR") or not _O.path.isfile(_GOLDEN):
            _O.makedirs(_GOLDEN_DIR, exist_ok=True)
            with open(_GOLDEN, "w", encoding="utf-8") as fh:
                json.dump(snap, fh, indent=2, sort_keys=True)
            self.skipTest("characterisation golden (re)generated; commit it")
        with open(_GOLDEN, encoding="utf-8") as fh:
            golden = json.load(fh)
        self.assertEqual(snap, golden,
                         "current behaviour diverged from the committed characterisation "
                         "baseline; if intentional, regenerate with PSYCHSIM_REGEN_CHAR=1 "
                         "and note it in the commit")


if __name__ == "__main__":
    unittest.main()
