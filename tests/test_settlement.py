import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))

"""The settlement generator (spawn a town from a spec), the demography profile
(a target population -> a building inventory via ratios), and the population
generator (fill the town with households, pupils, workers and relational ties)."""
import unittest

from sim_viz import (SettlementSpec, generate_settlement, settlement_inventory,
                     DemographyProfile, spec_for_population, ProceduralTileset,
                     render_svg)
from sim_world import populate, Population, HouseholdProfile


class TestSettlementGenerator(unittest.TestCase):
    def test_spec_is_met(self):
        spec = SettlementSpec(homes=40, offices=2, schools=1, shops=4, pubs=1,
                              sports=1, cars=50, seed=1)
        m = generate_settlement(spec)
        inv = settlement_inventory(m)
        self.assertEqual(inv["home"], 40)
        self.assertEqual(inv["office"], 2)
        self.assertEqual(inv["school"], 1)
        self.assertEqual(inv["shop"], 4)
        self.assertEqual(inv["cars"], 50)

    def test_buildings_never_sit_on_roads(self):
        m = generate_settlement(SettlementSpec(homes=20, seed=2))
        road_cells = {(p.x, p.y) for p in m.roads}
        for o in m.objects:
            self.assertNotIn((o.x, o.y), road_cells, f"{o.place or o.tile} on a road")

    def test_deterministic(self):
        a = generate_settlement(SettlementSpec(homes=25, seed=3))
        b = generate_settlement(SettlementSpec(homes=25, seed=3))
        self.assertEqual([(o.tile, o.x, o.y) for o in a.objects],
                         [(o.tile, o.x, o.y) for o in b.objects])

    def test_renders(self):
        m = generate_settlement(SettlementSpec(homes=15, cars=10, seed=4))
        svg = render_svg(m, ProceduralTileset())
        self.assertIn("<svg", svg[:200])
        self.assertIn("polygon", svg)


class TestDemography(unittest.TestCase):
    def test_target_population_gives_ratioed_inventory(self):
        spec = spec_for_population(200, DemographyProfile())
        # ~200 people at 2.4/home -> ~83 homes; ratios give the rest
        self.assertGreater(spec.homes, 60)
        self.assertLess(spec.homes, 100)
        self.assertGreaterEqual(spec.schools, 1)
        self.assertGreaterEqual(spec.shops, 1)
        self.assertGreater(spec.cars, 0)

    def test_bigger_target_more_homes(self):
        self.assertLess(spec_for_population(100).homes, spec_for_population(400).homes)


class TestPopulation(unittest.TestCase):
    def setUp(self):
        self.city = generate_settlement(SettlementSpec(homes=30, offices=2, schools=1,
                                                       shops=3, pubs=1, seed=5))
        self.pop = populate(self.city, seed=5)

    def test_every_home_has_a_household(self):
        homed = {h.home for h in self.pop.households}
        homes = {o.place for o in self.city.objects if o.place and o.place.startswith("home")}
        self.assertEqual(homed, homes)

    def test_children_are_pupils_and_adults_work(self):
        children = sum(len(h.children) for h in self.pop.households)
        self.assertEqual(len(self.pop.pupils), children)
        self.assertGreater(sum(len(w) for w in self.pop.workplaces.values()), 0)

    def test_relational_ties_are_wired(self):
        kinds = {t.pair.kind for t in self.pop.society.ties}
        # at least parent-child ties exist wherever there are children
        if any(h.children for h in self.pop.households):
            self.assertIn("parent-child", kinds)
        self.assertGreater(len(self.pop.society.ties), 0)

    def test_summary_counts(self):
        s = self.pop.summary()
        self.assertEqual(s["people"], self.pop.size())
        self.assertEqual(s["adults"] + s["children"] + s["teachers"], s["people"])



class TestSocioEconomicHomes(unittest.TestCase):
    """Socio-economics governs room-sharing and home size: most children have
    their own room, sharing is concentrated in lower-SES tenures, and wealthier
    homes have spare rooms (more comfort)."""

    def setUp(self):
        city = generate_settlement(SettlementSpec(homes=400, offices=5, schools=2,
                                                  shops=4, seed=8))
        self.pop = populate(city, seed=8)

    def test_socioeconomics_tenure_mix(self):
        from collections import Counter
        ten = Counter(h.tenure for h in self.pop.households)
        self.assertIn("owner", ten); self.assertIn("social_rent", ten)
        # owner-occupier is the majority tenure (EHS ~64%)
        self.assertGreater(ten["owner"] / len(self.pop.households), 0.5)

    def test_most_children_do_not_share(self):
        child_hh = [h for h in self.pop.households if h.children]
        sharing = [h for h in child_hh if h.child_bedrooms < len(h.children)]
        self.assertLess(len(sharing) / len(child_hh), 0.35)   # majority own rooms

    def test_sharing_concentrated_in_lower_ses(self):
        def rate(tenure):
            hh = [h for h in self.pop.households if h.children and h.tenure == tenure]
            if not hh:
                return 0.0
            return sum(h.child_bedrooms < len(h.children) for h in hh) / len(hh)
        self.assertGreater(rate("social_rent"), rate("owner"))

    def test_wealthier_homes_have_more_spare_rooms(self):
        owner_spare = sum(h.spare_rooms for h in self.pop.households if h.tenure == "owner")
        social_spare = sum(h.spare_rooms for h in self.pop.households if h.tenure == "social_rent")
        self.assertGreater(owner_spare, social_spare)

    def test_comfort_tracks_ses(self):
        import statistics as st
        owner = st.mean(h.comfort for h in self.pop.households if h.tenure == "owner")
        social = st.mean(h.comfort for h in self.pop.households if h.tenure == "social_rent")
        self.assertGreater(owner, social)


class TestHouseholdComposition(unittest.TestCase):
    """Household composition follows ONS proportions: childless homes, 1/2/3/4
    child families, with bedroom-sharing rising in larger/poorer families."""

    def setUp(self):
        city = generate_settlement(SettlementSpec(homes=300, offices=4, schools=1,
                                                  shops=3, seed=9))
        self.pop = populate(city, seed=9)

    def test_mix_of_family_sizes_including_larger_families(self):
        from collections import Counter
        sizes = Counter(len(h.children) for h in self.pop.households)
        self.assertGreater(sizes.get(0, 0), 0)         # childless homes exist
        self.assertGreater(sizes.get(1, 0), 0)
        self.assertGreater(sizes.get(2, 0), 0)
        # some 3+ child families appear
        self.assertGreater(sum(sizes.get(k, 0) for k in (3, 4)), 0)

    def test_child_household_share_near_ons(self):
        child_hh = sum(1 for h in self.pop.households if h.children)
        frac = child_hh / len(self.pop.households)
        self.assertGreater(frac, 0.18)
        self.assertLess(frac, 0.42)                    # ONS ~30%

    def test_larger_families_share_bedrooms(self):
        # at least one family has fewer child bedrooms than children (sharing)
        sharing = [h for h in self.pop.households
                   if h.children and h.child_bedrooms < len(h.children)]
        self.assertTrue(sharing)
        for h in sharing:
            self.assertGreaterEqual(h.child_bedrooms, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
