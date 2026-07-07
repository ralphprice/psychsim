import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)   # repo root, for `import project`

"""Data-file-first town/culture profiles: JSON round-trips to the Python constants (so
built-in spawns are unchanged), int-key coercion works, and a different household
composition actually threads through populate() (which the old spawn path ignored)."""
import unittest

from config.loader import load_town_profiles
from sim_viz.settlement import (ENGLAND_2021, RURAL_VILLAGE, INNER_CITY,
                                spec_for_population, generate_settlement)
from sim_world import populate
from sim_world.population import HouseholdProfile


class TestTownProfiles(unittest.TestCase):
    def test_builtin_json_equals_constants(self):
        tps = load_town_profiles()
        for name, const in (("england_2021", ENGLAND_2021),
                            ("rural_village", RURAL_VILLAGE),
                            ("inner_city", INNER_CITY)):
            self.assertEqual(tps[name].demography, const)          # demography faithful
            self.assertEqual(tps[name].household, HouseholdProfile())  # household = default

    def test_child_count_weights_keys_coerced_to_int(self):
        hh = load_town_profiles()["england_2021"].household
        self.assertTrue(all(isinstance(k, int) for k in hh.child_count_weights))
        self.assertEqual(sorted(hh.child_count_weights), [1, 2, 3, 4])

    def test_household_profile_threads_through_populate(self):
        # a socially-rented-heavy composition yields fewer owner households -- proving
        # household_profile is actually applied (the old spawn path never passed it).
        sett = spec_for_population(160, ENGLAND_2021, name="t", seed=5)
        city = generate_settlement(sett)

        def owner_frac(hp):
            pop = populate(city, seed=5, household_profile=hp)
            ten = [h.tenure for h in pop.households]
            return ten.count("owner") / max(1, len(ten))

        default = owner_frac(HouseholdProfile())
        social_heavy = owner_frac(HouseholdProfile(
            tenure_weights={"owner": 0.10, "private_rent": 0.10, "social_rent": 0.80}))
        self.assertGreater(default, social_heavy)

    def test_civic_buildings_scale_with_size(self):
        from sim_viz.settlement import (spec_for_population, generate_settlement,
                                        settlement_inventory)
        self.assertEqual(spec_for_population(300, ENGLAND_2021).extra, {})   # village: none
        big = spec_for_population(120000, ENGLAND_2021)
        self.assertGreater(big.extra.get("hospital", 0), 0)                  # city: a hospital
        self.assertGreater(big.extra.get("worship", 0), 0)
        inv = settlement_inventory(generate_settlement(big))                 # and they get placed
        self.assertGreater(inv.get("worship", 0), 0)
        self.assertGreater(inv.get("hospital", 0), 0)

    def test_culture_profile_differs_from_england(self):
        tps = load_town_profiles()
        self.assertIn("traditional_town", tps)
        tt, eng = tps["traditional_town"], tps["england_2021"]
        self.assertGreater(tt.demography.mean_household, eng.demography.mean_household)
        self.assertLess(tt.demography.people_per_worship, eng.demography.people_per_worship)

    def test_venues_for_handles_civic_buildings(self):
        from project import ProjectSpec, spawn_universe
        from sophropathy.world import venues_for
        uni = spawn_universe(ProjectSpec(name="t", target_population=8000,
                                         profile="england_2021", extensions=["sophropathy"],
                                         seed=5), place_residents=False)
        venues = venues_for(uni.city, uni.population)
        worship = [o.place for o in uni.city.objects
                   if o.place and o.place.startswith("worship")]
        self.assertTrue(worship)                      # 8000 people -> some places of worship
        self.assertIn(worship[0], venues)             # each gets a venue (drawn in plan-view)


if __name__ == "__main__":
    unittest.main(verbosity=2)
