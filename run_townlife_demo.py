#!/usr/bin/env python3
"""
run_townlife_demo.py -- spawn a town, run the clock, and WATCH a day (or many) of life.

Automated: one command spawns the town, runs the whole clock, and writes a
self-contained web page you open and press Play. Configure it with flags:

    python run_townlife_demo.py                       # 1 day, defaults
    python run_townlife_demo.py --days 7              # a whole week
    python run_townlife_demo.py --days 3 --population 120 --tick-minutes 10
    python run_townlife_demo.py --open                # also open it in a browser

Flags:
    --days N            how many days to simulate            (default 1)
    --population N       town size                            (default 80)
    --tick-minutes N     game-minutes per step; smaller = smoother/slower to run (default 15)
    --seed N            reproducibility seed                  (default 7)
    --output FILE       output html path                     (default town_life.html)
    --open              open the page in a browser when done  (WSL/mac/linux)
"""
import argparse
import os
import subprocess
import sys

from project import ProjectSpec, spawn_universe
from sophropathy import render_townlife_html


def _open(path):
    """Best-effort open in the default browser (WSL -> Windows, mac, or linux)."""
    p = os.path.abspath(path)
    for cmd in (["explorer.exe", os.path.basename(path)],   # WSL -> Windows
                ["open", p],                                 # macOS
                ["xdg-open", p]):                            # linux
        try:
            subprocess.run(cmd, check=False,
                           cwd=os.path.dirname(p) or ".")
            return
        except FileNotFoundError:
            continue


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run and watch a PsychSim town.")
    ap.add_argument("--days", type=int, default=2)
    ap.add_argument("--population", type=int, default=80)
    ap.add_argument("--tick-minutes", type=int, default=15, dest="tick")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--output", default="town_life.html")
    ap.add_argument("--open", action="store_true")
    args = ap.parse_args(argv)

    print(f"spawning town (pop {args.population}, seed {args.seed})...")
    uni = spawn_universe(
        ProjectSpec(name="Ashcombe", target_population=args.population,
                    profile="england_2021", extensions=["sophropathy"],
                    fearless_frac=0.4, seed=args.seed),
        place_residents=False)

    print(f"running the clock for {args.days} day(s) at {args.tick}-min ticks...")
    path = render_townlife_html(uni, days=args.days, tick_minutes=args.tick,
                                seed=1, path=args.output)

    size = os.path.getsize(path) // 1024
    print(f"done -> {path} ({size} KB). Open it and press Play "
          f"(scroll = zoom, drag = pan, slider = scrub).")
    if args.open:
        _open(path)


if __name__ == "__main__":
    main()
