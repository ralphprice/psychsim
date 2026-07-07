"""
sim_viz -- the visualisation layer of the simulation platform.

Builds the map data model, renders it to SVG with a swappable tileset (a
placeholder renderer now; the real AI PNG tiles later), and binds to sim_world so
buildings are places, roads are the place-graph, and sims carry their current
behavioural-network state. Implements Parts V and VI of the graphics spec.
"""
from .iso import TILE_W, TILE_H, cell_to_screen
from .mapmodel import CityMap, Placement, Actor
from .procedural import ProceduralTileset
from .floorplan import render_settlement_plan, render_building_plan
from .settlement import (SettlementSpec, generate_settlement, settlement_inventory,
                         DemographyProfile, spec_for_population,
                         ENGLAND_2021, RURAL_VILLAGE, INNER_CITY)
from .tileset import (Tileset, PlaceholderTileset, PngTileset, TileArt,
                      default_manifest)
from .compositor import render_svg, save_svg, Overlays, NETWORK_COLOUR
from .binding import (Layout, build_map, add_people, overlays_from_state,
                      PLACE_TILE)

__all__ = [
    "TILE_W", "TILE_H", "cell_to_screen",
    "CityMap", "Placement", "Actor",
    "Tileset", "PlaceholderTileset", "PngTileset", "ProceduralTileset", "render_settlement_plan", "render_building_plan", "SettlementSpec", "generate_settlement", "settlement_inventory", "DemographyProfile", "spec_for_population", "ENGLAND_2021", "RURAL_VILLAGE", "INNER_CITY", "TileArt", "default_manifest",
    "render_svg", "save_svg", "Overlays", "NETWORK_COLOUR",
    "Layout", "build_map", "add_people", "overlays_from_state", "PLACE_TILE",
]
__version__ = "0.1.0"
