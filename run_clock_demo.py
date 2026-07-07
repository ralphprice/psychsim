"""
run_clock_demo.py -- drive the time-clock over a childhood and read what emerges.

Drop this file in the project root (next to run_pipeline.py) and run it:

    python run_clock_demo.py

It spawns a small simulated world, advances the clock one YEAR per step for 22 years
(so a cohort of children grows up on the substrate and through the three matrices),
then prints what emerged for a few of them: their dominant drive, their standing in
the groups they belong to, and the state of their always-on executive layer.
"""

from project import ProjectSpec, spawn_universe
from sim_world import TimeController, TimeScale
from sophropathy import make_life_stepper


def main():
    # 1. spawn a world with the sophropathy extension
    uni = spawn_universe(
        ProjectSpec(name="clock_demo", target_population=80, profile="england_2021",
                    extensions=["sophropathy"], fearless_frac=0.4, seed=3),
        place_residents=False)

    # 2. build the life-stepper (it carries a .dev dict of per-child results) and
    #    hand it to the time-controller
    step = make_life_stepper(uni, seed=1)
    clock = TimeController(step)

    # 3. advance the clock. TimeScale options: REALTIME, HOUR, DAY, WEEK, MONTH, YEAR.
    #    One YEAR per step, 22 steps = a full childhood.
    clock.run(TimeScale.YEAR, steps=22)

    # 4. read what emerged for the first few children
    print("=" * 68)
    print(f"  clock advanced; {len(step.dev)} children grown up")
    print("=" * 68)
    for i, d in enumerate(step.dev.values()):
        if i >= 6:
            break
        ranks = [(m.group_id, round(m.standing, 2)) for m in d["group_matrix"].ranks(top=2)]
        ex = d["executive"]
        print(f"  child {i + 1}: dominant drive = {d['outcome']:8} | "
              f"top group standing = {ranks}")
        print(f"           executive: {ex.note() or 'developing'} "
              f"(consulted {ex.checks} times, fired {ex.fired})")
    print("=" * 68)
    print("  note: the executive is CONSULTED on every brain event (always-on) but")
    print("  FIRES only on what it has learned to monitor; in this crude world little")
    print("  is net-costly, so it rarely acts yet -- see the design document.")


if __name__ == "__main__":
    main()
