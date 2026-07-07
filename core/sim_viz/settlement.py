"""
settlement.py -- generate a settlement from a spec (the "spawn a town" engine).

Given how many of each building a community has -- so many homes, offices,
schools, shops, a pub -- plus cars, this lays out a grid town: a street network,
plots along the streets, buildings placed on them (commercial toward the centre,
housing toward the edges, larger civic buildings given room), greenery and a
park in the gaps, and vehicles on the roads. The result is a CityMap the existing
compositor renders with any tileset.

This is generic town-building: it produces the *place*. Binding a population into
it -- households in the homes, pupils in the school, workers in the offices, and
the relational ties among them -- is a separate step (the population generator),
so each building is given a stable `place` name here for that step to attach to.

Deliberately simple and rough: a regular grid, not organic growth. It is a
starting point to be revised, and it lays out and renders a town today.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math
import random

from .mapmodel import CityMap, Placement, Actor


# ---------------------------------------------------------------------------
# The catalogue of building types (extensible)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class BuildingType:
    """A kind of building a settlement can contain: its render tile, footprint, and
    where it prefers to sit (big civic buildings need a 2x2 central plot; commercial
    goes central; homes fall to the outer plots)."""
    tile: str
    footprint: Tuple[int, int] = (1, 1)
    placement: str = "central"              # "big" | "central" | "outer"


# Existing types keep their historical tile/footprint/placement, so existing specs are
# byte-for-byte unchanged. New civic types (hospital, clinic, place of worship, market)
# extend the catalogue; a study or a data-file town-type profile chooses how many of each.
BUILDING_TYPES: Dict[str, BuildingType] = {
    "school":    BuildingType("building_school", (2, 2), "big"),
    "sports":    BuildingType("building_sports", (2, 2), "big"),
    "hospital":  BuildingType("building_hospital", (2, 2), "big"),
    "civic":     BuildingType("building_institution", (1, 1), "central"),
    "office":    BuildingType("building_workplace", (1, 1), "central"),
    "clinic":    BuildingType("building_clinic", (1, 1), "central"),
    "shop":      BuildingType("building_shop", (1, 1), "central"),
    "market":    BuildingType("building_market", (1, 1), "central"),
    "worship":   BuildingType("building_worship", (1, 1), "central"),
    "cafe":      BuildingType("building_cafe", (1, 1), "central"),
    "pub":       BuildingType("building_pub", (1, 1), "central"),
    "apartment": BuildingType("building_apartment", (1, 1), "central"),
    "home":      BuildingType("building_home", (1, 1), "outer"),
}
_DEFAULT_BT = BuildingType("building_institution", (1, 1), "central")


# ---------------------------------------------------------------------------
# The spec
# ---------------------------------------------------------------------------

@dataclass
class SettlementSpec:
    """What a community consists of. Counts of buildings, plus cars; a study or a
    demography profile supplies the numbers (e.g. a village: 1 school, 2 offices,
    40 homes, 4 shops, 1 pub, ~100 cars)."""
    name: str = "Settlement"
    homes: int = 40
    apartments: int = 0
    offices: int = 2
    schools: int = 1
    shops: int = 4
    pubs: int = 1
    cafes: int = 0
    sports: int = 0
    civic: int = 0
    cars: int = 0
    trees: int = 0                # extra scatter trees; 0 -> auto
    block: int = 4                # plots per block edge (between roads)
    green_blocks: int = 1         # whole blocks reserved as parks
    seed: int = 0
    extra: Dict[str, int] = field(default_factory=dict)   # counts of EXTRA building types
    #                                                       (hospital, clinic, worship, market, ...)

    def building_bill(self) -> List[Tuple[str, str, Tuple[int, int]]]:
        """(place_prefix, tile, footprint) for every building, larger first. The named
        counts come first in their historical order (so existing specs are unchanged),
        then any EXTRA data-driven building types."""
        bill: List[Tuple[str, str, Tuple[int, int]]] = []
        named = (("school", self.schools), ("sports", self.sports),
                 ("civic", self.civic), ("office", self.offices),
                 ("shop", self.shops), ("cafe", self.cafes),
                 ("pub", self.pubs), ("apartment", self.apartments),
                 ("home", self.homes))
        for kind, count in named:
            bt = BUILDING_TYPES[kind]
            for _ in range(int(count)):
                bill.append((kind, bt.tile, bt.footprint))
        for kind, count in self.extra.items():
            bt = BUILDING_TYPES.get(kind, _DEFAULT_BT)
            for _ in range(int(count)):
                bill.append((kind, bt.tile, bt.footprint))
        return bill


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

def _grid_size(spec: SettlementSpec) -> Tuple[int, int, List[int], List[int]]:
    """Choose a grid that fits the buildings, and the road rows/cols."""
    bill = spec.building_bill()
    cells_needed = sum(fp[0] * fp[1] for _, _, fp in bill)
    # perimeter plots per block ~ 4*block - 4; plus reserved green blocks
    plots_per_block = max(1, 4 * spec.block - 4)
    blocks_needed = math.ceil(cells_needed / (plots_per_block * (1 - 0.0)))
    blocks_needed += spec.green_blocks
    blocks_side = max(2, math.ceil(math.sqrt(blocks_needed)))
    step = spec.block + 1                       # block + one road lane
    span = blocks_side * step + 1               # +1 for the closing road
    margin = 2
    size = span + 2 * margin
    road_lines = [margin + i * step for i in range(blocks_side + 1)]
    return size, size, road_lines, road_lines


def _is_road(x: int, y: int, road_cols: List[int], road_rows: List[int]) -> bool:
    return x in road_cols or y in road_rows


def _adjacent_to_road(x: int, y: int, road_cols, road_rows, size) -> bool:
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < size and 0 <= ny < size and _is_road(nx, ny, road_cols, road_rows):
            return True
    return False


def generate_settlement(spec: SettlementSpec) -> CityMap:
    """Lay out a town from the spec and return a CityMap ready to render. Each
    building carries a stable `place` name (e.g. 'home_7', 'school_0') for a
    population step to bind agents to."""
    rng = random.Random(spec.seed)
    size, _, road_cols, road_rows = _grid_size(spec)
    m = CityMap(name=spec.name, cols=size, rows=size)
    m.fill_terrain("terrain_grass")

    # 1. roads: lay the street grid; pavement fringes read as plots
    for y in range(size):
        for x in range(size):
            if _is_road(x, y, road_cols, road_rows):
                cross = x in road_cols and y in road_rows
                m.roads.append(Placement(tile=("road_cross" if cross else "road_straight_ns"),
                                         x=x, y=y))
                m.set_terrain(x, y, "terrain_pavement")

    # 2. reserve whole blocks as parks (interior filled with park terrain)
    blocks = []
    for i in range(len(road_cols) - 1):
        for j in range(len(road_rows) - 1):
            blocks.append((road_cols[i] + 1, road_rows[j] + 1,
                           road_cols[i + 1] - 1, road_rows[j + 1] - 1))
    rng.shuffle(blocks)
    park_cells = set()
    for b in blocks[:spec.green_blocks]:
        x0, y0, x1, y1 = b
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                m.set_terrain(x, y, "terrain_park")
                park_cells.add((x, y))

    # 3. buildable plot cells: adjacent to a road, not a road, not park.
    #    Sort by distance from the centre so commercial can go central, homes out.
    cx, cy = size / 2, size / 2
    buildable = []
    for y in range(size):
        for x in range(size):
            if _is_road(x, y, road_cols, road_rows) or (x, y) in park_cells:
                continue
            if _adjacent_to_road(x, y, road_cols, road_rows, size):
                d = (x - cx) ** 2 + (y - cy) ** 2
                buildable.append((d, x, y))
    buildable.sort()                                    # central first
    central = [(x, y) for _, x, y in buildable]

    used: set = set()
    occupied: Dict[Tuple[int, int], str] = {}

    def _free(x, y):
        return (0 <= x < size and 0 <= y < size and (x, y) not in used
                and not _is_road(x, y, road_cols, road_rows)
                and (x, y) not in park_cells)

    def _place_2x2(x, y):
        return all(_free(x + dx, y + dy) for dx in range(2) for dy in range(2))

    # 4. place buildings: larger (2x2) civic first from central plots, then the
    #    rest; commercial stays central, homes fall to the outer plots.
    bill = spec.building_bill()

    def _placement(kind):
        return BUILDING_TYPES.get(kind, _DEFAULT_BT).placement
    big = [b for b in bill if _placement(b[0]) == "big"]
    small_central = [b for b in bill if b[2] == (1, 1) and _placement(b[0]) == "central"]
    small_outer = [b for b in bill if b[2] == (1, 1) and _placement(b[0]) == "outer"]

    counts: Dict[str, int] = {}

    def _name(prefix):
        n = counts.get(prefix, 0)
        counts[prefix] = n + 1
        return f"{prefix}_{n}"

    # 2x2 buildings: scan central plots for a free 2x2 block
    for prefix, tile, fp in big:
        for (x, y) in central:
            if _place_2x2(x, y):
                m.objects.append(Placement(tile=tile, x=x, y=y, footprint=(2, 2),
                                           place=_name(prefix)))
                for dx in range(2):
                    for dy in range(2):
                        used.add((x + dx, y + dy))
                break

    # small central (commercial) from the innermost free plots outward
    def _place_small(queue, order):
        idx = 0
        for prefix, tile, fp in queue:
            while idx < len(order) and not _free(*order[idx]):
                idx += 1
            if idx >= len(order):
                break
            x, y = order[idx]; idx += 1
            m.objects.append(Placement(tile=tile, x=x, y=y, footprint=(1, 1),
                                       place=_name(prefix)))
            used.add((x, y))

    _place_small(small_central, central)
    _place_small(small_outer, list(reversed(central)))   # homes from the edges in

    # 5. greenery: trees on some remaining buildable plots + all park cells
    remaining = [(x, y) for (_, x, y) in buildable if (x, y) not in used]
    rng.shuffle(remaining)
    n_trees = spec.trees or max(6, len(remaining) // 3)
    for (x, y) in remaining[:n_trees]:
        m.objects.append(Placement(tile=rng.choice(["prop_tree", "prop_bush", "prop_hedge"]),
                                    x=x, y=y))
        used.add((x, y))
    for (x, y) in list(park_cells)[:max(1, len(park_cells) // 2)]:
        if _free(x, y):
            m.objects.append(Placement(tile=rng.choice(
                ["prop_tree", "prop_bench", "prop_flowerbed", "prop_playground"]),
                x=x, y=y))

    # 6. street furniture on some pavement corners
    for (x, y) in [(rc + 1, rr) for rc in road_cols[:-1] for rr in road_rows][: max(2, spec.homes // 10)]:
        if 0 <= x < size and 0 <= y < size and not _is_road(x, y, road_cols, road_rows):
            if _free(x, y):
                m.objects.append(Placement(tile="prop_streetlight", x=x, y=y))
                used.add((x, y))

    # 7. cars on the road network
    road_cells = [(x, y) for y in range(size) for x in range(size)
                  if _is_road(x, y, road_cols, road_rows)]
    rng.shuffle(road_cells)
    car_tiles = ["vehicle_car_a", "vehicle_car_b", "vehicle_car_c"]
    for i, (x, y) in enumerate(road_cells[:spec.cars]):
        m.actors.append(Actor(sprite=rng.choice(car_tiles), x=x, y=y,
                              agent_id=f"car_{i}"))

    return m


def settlement_inventory(m: CityMap) -> Dict[str, int]:
    """Count what was placed, by place-prefix -- to check the spec was met."""
    inv: Dict[str, int] = {}
    for p in m.objects:
        if p.place:
            prefix = p.place.rsplit("_", 1)[0]
            inv[prefix] = inv.get(prefix, 0) + 1
    inv["cars"] = sum(1 for a in m.actors if a.sprite.startswith("vehicle"))
    people = sum(1 for a in m.actors if a.sprite.startswith("char"))
    if people:
        inv["residents_shown"] = people
    return inv


# ---------------------------------------------------------------------------
# Demography -- turn a target population into a spec via ratios
# ---------------------------------------------------------------------------

@dataclass
class DemographyProfile:
    """Ratios that turn a single target (a community of ~N people) into a full
    building inventory. Defaults are anchored to real 2021 figures for England
    (sources noted), so a spawned settlement is demographically convincing; swap
    in a specific ONS area later for an exact match.

    Sources: household size 2.41 and age structure (under-16 ~18.6%, working-age
    16-64 62.9%, 65+ 18.4%) -- ONS Census 2021, England. Car availability 1.2
    per household -- DfT National Travel Survey 2021 (12 cars per 10 households
    in England). Average primary school ~280 pupils -- DfE / Good Schools Guide,
    England."""
    mean_household: float = 2.41       # people per dwelling (ONS 2021, England)
    child_frac: float = 0.186          # aged under 16 (ONS 2021)
    working_age_frac: float = 0.629    # aged 16-64 (ONS 2021)
    elderly_frac: float = 0.184        # aged 65+ (ONS 2021, England)
    employment_rate: float = 0.75      # share of working-age in work (~ONS)
    cars_per_home: float = 1.2         # DfT NTS 2021 (England)
    avg_primary_pupils: int = 280      # DfE/GSG average primary school (England)
    primary_share_of_children: float = 0.5   # ~ages 4-11 of the 0-15 band
    workers_per_office: int = 18       # employees a small local workplace holds
    people_per_shop: float = 700.0     # residents a convenience shop serves
    people_per_pub: float = 1200.0     # residents a pub serves (declining nationally)
    local_work_share: float = 0.45     # share of employed who work locally (rest commute)
    # outdoor space: settlement type + tenure drive garden access and size.
    # ~12% of GB households have no garden (21% in London, near-universal rural);
    # owner-occupiers are mostly houses, social renters far more often flats (ONS).
    settlement_type: str = "suburban"                  # rural / suburban / inner_city
    garden_prob_by_tenure: Dict[str, float] = field(
        default_factory=lambda: {"owner": 0.92, "private_rent": 0.75, "social_rent": 0.60})
    garden_area_multiplier: float = 1.0                # scales garden probability by area type
    garden_size_scale: float = 1.0                     # relative garden size by area type
    # civic buildings, by residents served. Defaults are large, so a small town/village
    # gets NONE (no village hospital); a denser or different-culture profile sets its own.
    # ILLUSTRATIVE placeholders -- replace with real per-country data when available.
    people_per_hospital: float = 90000.0
    people_per_clinic: float = 12000.0
    people_per_worship: float = 2500.0
    people_per_market: float = 30000.0


# a few named starting profiles
ENGLAND_2021 = DemographyProfile()                     # suburban baseline
RURAL_VILLAGE = DemographyProfile(mean_household=2.45, cars_per_home=1.45,
                                  people_per_shop=500.0, people_per_pub=800.0,
                                  local_work_share=0.35, settlement_type="rural",
                                  garden_area_multiplier=1.05, garden_size_scale=1.4)
INNER_CITY = DemographyProfile(mean_household=2.30, cars_per_home=0.8,
                               people_per_shop=500.0, people_per_pub=700.0,
                               local_work_share=0.55,
                               settlement_type="inner_city",
                               garden_area_multiplier=0.62, garden_size_scale=0.5,
                               garden_prob_by_tenure={"owner": 0.70, "private_rent": 0.45,
                                                      "social_rent": 0.35})


def spec_for_population(target_people: int, profile: Optional[DemographyProfile] = None,
                        name: str = "Settlement", seed: int = 0) -> SettlementSpec:
    """Size a SettlementSpec to house ~target_people, with buildings in the
    profile's real-world ratios -- so 'a village of 200' becomes a defensible
    inventory rather than a guess. A community always gets at least one school,
    one shop and one workplace so it is self-contained and runnable."""
    p = profile or ENGLAND_2021
    homes = max(1, round(target_people / p.mean_household))
    primary_children = target_people * p.child_frac * p.primary_share_of_children
    schools = max(1, round(primary_children / p.avg_primary_pupils))
    local_workers = target_people * p.working_age_frac * p.employment_rate * p.local_work_share
    offices = max(1, round(local_workers / p.workers_per_office))
    shops = max(1, round(target_people / p.people_per_shop))
    pubs = max(1, round(target_people / p.people_per_pub))
    cars = round(homes * p.cars_per_home)
    green = 2 if p.settlement_type == "inner_city" else 1   # denser areas: more public parks
    # civic buildings by residents served (0 for small towns)
    extra: Dict[str, int] = {}
    for kind, per in (("hospital", p.people_per_hospital), ("clinic", p.people_per_clinic),
                      ("worship", p.people_per_worship), ("market", p.people_per_market)):
        n = round(target_people / per) if per and per > 0 else 0
        if n > 0:
            extra[kind] = n
    return SettlementSpec(name=name, homes=homes, offices=offices, shops=shops,
                          pubs=pubs, schools=schools, sports=1 if target_people > 1500 else 0,
                          cars=cars, green_blocks=green, seed=seed, extra=extra)
