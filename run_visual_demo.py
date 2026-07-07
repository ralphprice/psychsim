"""
run_visual_demo.py -- the clock and the graphics, wired together.

Ages a population on the time-clock, then renders the aged world: the settlement
laid out, each child placed near their home and coloured by their EMERGENT dominant
drive, each home tinted by its parenting climate. Drop this in the project root and:

    python run_visual_demo.py

It writes aged_town.svg -- open it in VS Code (right-click the tab -> Open Preview)
or in a web browser.
"""
from collections import Counter
from project import ProjectSpec, spawn_universe
from sim_world import TimeController, TimeScale
from sophropathy import make_life_stepper, render_aged_town


def main():
    uni = spawn_universe(
        ProjectSpec(name="visual_demo", target_population=80, profile="england_2021",
                    extensions=["sophropathy"], fearless_frac=0.4, seed=3),
        place_residents=False)
    step = make_life_stepper(uni, seed=1)
    TimeController(step).run(TimeScale.YEAR, steps=22)     # age the population

    path, m, ov = render_aged_town(uni, step, path="aged_town.svg")
    print(f"wrote {path}: {m.cols}x{m.rows} town, {len(m.actors)} children placed")
    print(f"emergent drives on the map: {dict(Counter(ov.actor_state.values()))}")
    print("open aged_town.svg in VS Code (right-click tab -> Open Preview) or a browser")


if __name__ == "__main__":
    main()
