import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

"""The project startup: real-demography ratios, and spawning a universe (a
settlement populated as a society) for a named project with selected extensions."""
import unittest
from sim_viz import spec_for_population, ENGLAND_2021, RURAL_VILLAGE
from project import (ProjectSpec, spawn_universe, available_extensions,
                     available_profiles)


class TestDemographyRatios(unittest.TestCase):
    def test_household_size_drives_homes(self):
        # ONS 2021 England: 2.41 people/home -> ~415 homes for 1000 people
        spec = spec_for_population(1000, ENGLAND_2021)
        self.assertAlmostEqual(spec.homes, round(1000 / 2.41), delta=2)

    def test_cars_match_dft_ratio(self):
        spec = spec_for_population(1000, ENGLAND_2021)
        self.assertAlmostEqual(spec.cars, round(spec.homes * 1.2), delta=1)

    def test_small_community_is_self_contained(self):
        # a village always gets at least a school, a shop and a workplace
        spec = spec_for_population(200, ENGLAND_2021)
        self.assertGreaterEqual(spec.schools, 1)
        self.assertGreaterEqual(spec.shops, 1)
        self.assertGreaterEqual(spec.offices, 1)

    def test_school_provision_scales(self):
        # a town large enough needs more than one primary school
        small = spec_for_population(500, ENGLAND_2021).schools
        big = spec_for_population(8000, ENGLAND_2021).schools
        self.assertGreaterEqual(big, small)
        self.assertGreater(big, 1)


class TestProjectSpawn(unittest.TestCase):
    def test_dropdown_lists_extensions_and_profiles(self):
        exts = available_extensions()
        self.assertIn("sophropathy", exts)
        self.assertIn("england_2021", available_profiles())

    def test_spawn_builds_a_populated_universe(self):
        uni = spawn_universe(ProjectSpec(name="P", target_population=250, seed=1))
        s = uni.summary()
        self.assertGreater(s["society"]["people"], 150)
        self.assertGreaterEqual(s["inventory"]["home"], 80)
        self.assertGreater(s["society"]["ties"], 0)

    def test_deterministic(self):
        a = spawn_universe(ProjectSpec(name="P", target_population=200, seed=5))
        b = spawn_universe(ProjectSpec(name="P", target_population=200, seed=5))
        self.assertEqual(a.summary()["society"]["people"],
                         b.summary()["society"]["people"])

    def test_sophropathy_extension_perturbs_the_population(self):
        on = spawn_universe(ProjectSpec(name="P", target_population=250,
                                        extensions=["sophropathy"], seed=3))
        off = spawn_universe(ProjectSpec(name="P", target_population=250,
                                         extensions=[], seed=3))
        def threat(u):
            return [round(u.population.persons[c].mind.gain.get("THREAT", 0), 2)
                    for hh in u.population.households for c in hh.children]
        self.assertNotEqual(threat(on), threat(off))



class TestGardensBySettlementType(unittest.TestCase):
    """Garden access and size vary by settlement type AND tenure (ONS)."""

    def _garden_rate(self, profile_name):
        uni = spawn_universe(ProjectSpec(name="P", target_population=400,
                                         profile=profile_name, seed=6))
        hh = uni.population.households
        return sum(h.garden for h in hh) / len(hh)

    def test_rural_more_gardens_than_inner_city(self):
        self.assertGreater(self._garden_rate("rural_village"),
                           self._garden_rate("inner_city"))

    def test_owner_more_likely_to_have_garden_than_social_renter(self):
        uni = spawn_universe(ProjectSpec(name="P", target_population=500, seed=6))
        def rate(t):
            hh = [h for h in uni.population.households if h.tenure == t]
            return sum(h.garden for h in hh) / len(hh) if hh else 0
        self.assertGreater(rate("owner"), rate("social_rent"))

    def test_some_homes_have_no_garden(self):
        uni = spawn_universe(ProjectSpec(name="P", target_population=400,
                                         profile="inner_city", seed=6))
        self.assertTrue(any(not h.garden for h in uni.population.households))


if __name__ == "__main__":
    unittest.main(verbosity=2)
