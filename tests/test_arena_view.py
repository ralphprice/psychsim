import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""The Arena UI server seam (arena_view): the JSON views + run-and-serialise the ARENA tab uses.

Mechanistic + HONESTY checks only -- the behaviour itself is tested in test_arena.py; here we test
that the seam exposes DEFINED content (no hollow labels), temperament as PARAMETERS (not outcome
names), the structural escape (never a tag), the emergent-relationship honesty, the 2-5 instrument
bound surfacing, and determinism preserved through the seam."""

import json
import unittest
import arena_view as av


def _payload(*slots, env="one_house", seed=7, shared=3.0, years=6.0):
    return {"micro_env": env, "seed": seed, "shared_hours": shared, "childhood_years": years,
            "slots": list(slots)}


class TestDefinedContentOnly(unittest.TestCase):
    def test_environments_are_the_four_defined_with_structural_escape(self):
        envs = av.environments()
        self.assertEqual({e["id"] for e in envs},
                         {"one_room", "one_house", "house_garden", "office"})
        for e in envs:
            self.assertEqual(e["escape"], len(e["present"]))       # escape is STRUCTURAL (a count)
            self.assertTrue(all(isinstance(p, str) for p in e["present"]))

    def test_no_valence_or_stressful_tag_anywhere_in_the_env_view(self):
        # the honesty wall: an environment is its present Things, never a coded aversiveness label
        blob = repr(av.environments()).lower()
        for banned in ("stress", "aversive", "valence", "hostile", "scary"):
            self.assertNotIn(banned, blob)

    def test_sources_expose_temperament_as_parameters_not_outcome_names(self):
        src = av.sources()
        self.assertEqual(src["kinds"], ["newborn", "grown", "banked"])
        # temperament = the gain DIMS (circuits/parameters), never outcome-named presets
        self.assertIn("THREAT", src["gain_dims"])
        self.assertIn("SEEKING", src["gain_dims"])
        blob = repr(src["gain_dims"]).lower()
        for banned in ("fearless", "typical", "psychopath", "callous"):
            self.assertNotIn(banned, blob)

    def test_banked_ids_empty_without_a_bank(self):
        self.assertEqual(av.sources(None)["banked_ids"], [])

    def test_relationships_are_honest_empty_not_hollow_labels(self):
        rel = av.relationships()
        self.assertEqual(rel["defined"], [])                      # no named configs defined yet
        self.assertTrue(rel["substrate"])                         # the emergent substrate is described
        self.assertIn("emerge", rel["substrate"].lower() + rel["note"].lower())


class TestRunSeam(unittest.TestCase):
    def test_run_composes_and_serialises_a_trace(self):
        out = av.run(_payload({"slot_id": "A", "source": "newborn"},
                              {"slot_id": "B", "source": "newborn"}))
        self.assertTrue(out["records"])
        self.assertIn("viable", out)
        self.assertIn("peak_activation", out)
        self.assertIn("act_counts", out)
        self.assertEqual(out["agent_ids"], ["A", "B"])
        r0 = out["records"][0]
        for k in ("episode", "age", "acts", "max_act", "drift", "strain"):
            self.assertIn(k, r0)

    def test_temperament_gains_are_accepted_as_parameters(self):
        out = av.run(_payload({"slot_id": "X", "source": "newborn", "gains": {"THREAT": 0.8}},
                              {"slot_id": "Y", "source": "newborn"}, env="one_room"))
        self.assertTrue(out["records"])

    def test_roster_bound_surfaces_as_valueerror(self):
        with self.assertRaises(ValueError):
            av.run(_payload({"slot_id": "solo", "source": "newborn"}))   # <2 -> S12.2 guard
        self.assertEqual(av.roster_bounds()["min"], 2)
        self.assertEqual(av.roster_bounds()["max"], 5)

    def test_banked_slot_without_bank_is_a_clear_error(self):
        with self.assertRaises(ValueError):
            av.run(_payload({"slot_id": "A", "source": "newborn"},
                            {"slot_id": "K", "source": "banked", "bank_id": "x"}), )

    def test_run_output_is_json_serialisable_with_string_strain_keys(self):
        # the trace keys tie-strain by a PAIR TUPLE; the seam must remap to 'a|b' strings, or the
        # HTTP layer's json.dumps blows up (regression: it did, caught by the live end-to-end test).
        out = av.run(_payload({"slot_id": "A", "source": "newborn"},
                              {"slot_id": "B", "source": "newborn"}))
        json.dumps(out)                                  # must not raise
        for r in out["records"]:
            for k in r["strain"]:
                self.assertIsInstance(k, str)

    def test_determinism_preserved_through_the_seam(self):
        p = _payload({"slot_id": "A", "source": "newborn"}, {"slot_id": "B", "source": "newborn"})
        a = av.run(dict(p, slots=list(p["slots"])))
        b = av.run(dict(p, slots=list(p["slots"])))
        # same seed -> identical per-episode acts (the regression-harness property, through the seam)
        self.assertEqual([r["acts"] for r in a["records"]], [r["acts"] for r in b["records"]])


if __name__ == "__main__":
    unittest.main()
