"""
bifurcation -- an edge-condition explorer for the life-course simulation.

Maps the parameter space to find the separatrix: the edge conditions where a
fearless disposition bifurcates between the sophropathic and psychopathic basins.
Nothing here presupposes where the boundary is; the tools reveal it.
"""
from .config import Config, run_config, RunResult, make_seed
from .sweep import (Sweep1D, sweep_1d, PhaseMap, phase_map_2d,
                    boundary_cells, bisect_edge)

__all__ = ["Config", "run_config", "RunResult", "make_seed",
           "Sweep1D", "sweep_1d", "PhaseMap", "phase_map_2d",
           "boundary_cells", "bisect_edge"]
__version__ = "0.1.0"
