"""
townprofile.py -- a town/culture profile: the demography + household composition
that together drive a settlement's spawn. This UNIFIES the two previously-
disconnected demography data points (`DemographyProfile` sized the buildings;
`HouseholdProfile` composed families but was never threaded into the spawn).

A profile is data: ship it as an editable JSON under `data/towntypes/` and a
researcher can define a new country/culture without touching code.
"""

from __future__ import annotations
from dataclasses import dataclass

from sim_viz.settlement import DemographyProfile
from sim_world.population import HouseholdProfile


@dataclass
class TownProfile:
    name: str
    demography: DemographyProfile
    household: HouseholdProfile
