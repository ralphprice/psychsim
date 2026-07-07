#!/usr/bin/env python3
"""
run_pipeline.py -- exercise the whole platform + extension, end to end.

Core (universal):     world, affect engine, neural designer, experiment,
                      visualiser, edge explorer.
Extension (research): the sophropathy family/parent model and seven stages.
"""
import sys, os
_R = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_R, "core"))
sys.path.insert(0, os.path.join(_R, "extensions"))


def main():
    print("#" * 78)
    print("  PSYCHSIM -- universal life-course simulation platform + sophropathy extension")
    print("#" * 78)

    print("\n[CORE 1] affect engine -- developmental separation (one seed, two homes):")
    from affective_engine.demo import report as eng
    print(eng().splitlines()[-2])

    print("\n[CORE 2] world -- a person living a day across home/school/workplace:")
    from sim_world.demo import run_day
    print("  " + [l for l in run_day(warm=True).splitlines() if "reputation" in l][0].strip())

    print("\n[CORE 3] neural designer -- an authored library with a cascade and a loop:")
    from neuraldesigner import build_example_library
    lib = build_example_library()
    print(f"  {len(lib.circuits)} circuits, {len(lib.pathways)} pathways, "
          f"loops: {lib.find_loops()}")

    print("\n[CORE 4] experiment -- trait x moral-environment factorial (modal outcomes):")
    from sim_experiment import run_factorial
    fr = run_factorial(n_runs=6)
    for c in fr.cells[:4]:
        print(f"  {c.seed_name:22} x {c.condition_label:28} -> {c.modal_classification}")

    print("\n[CORE 5] edge explorer -- warmth x structure phase map (graded):")
    from bifurcation import Config, phase_map_2d, boundary_cells
    pm = phase_map_2d(Config(graded=True), "warmth", 0, 1, "structure", 0, 1, nx=11, ny=11)
    print(f"  basins {pm.region_counts()} | separatrix {len(boundary_cells(pm))} cells")

    print("\n[CORE 6] visualiser -- render a town from the world (placeholder tiles):")
    from sim_viz.demo import build_demo_city
    from sim_viz import render_svg
    world, m, ov, alex = build_demo_city()
    svg = render_svg(m, overlays=ov)
    print(f"  rendered {m.cols}x{m.rows} town, {len(svg)} bytes SVG, "
          f"Alex@{world.location_of('alex')} state={alex.mind.dominant}")

    print("\n[EXTENSION] sophropathy -- the seven-stage programme (key contrasts):")
    from sophropathy import run_stage3, run_stage4
    s3, s4 = run_stage3(n=8), run_stage4(n=8)
    d3 = [c for c in s3.conditions if "dysfunctional" in c.label][0].modal
    d4 = [c for c in s4.conditions if "dysfunctional" in c.label][0].modal
    print(f"  dysfunctional home: typical child -> {d3}   |   fearless child -> {d4}")
    print(f"  (differential susceptibility: same home, different disposition, different fate)")

    print("\n[CORE 7] language layer -- speech-acts wired into the world (two agents converse):")
    from speech import TemplateRenderer, evaluate
    from sim_world import build_world, Person, GameMaster, SocialEvent
    from affective_engine.core import psychopathic_seed, sophropathic_seed
    fscore = evaluate(TemplateRenderer())
    w2 = build_world()
    cal = Person("cal", "Cal", psychopathic_seed(), birth_day=-9000)
    ann = Person("ann", "Ann", sophropathic_seed(), birth_day=-9000)
    w2.place_agent("cal", "street"); w2.place_agent("ann", "street")
    gm2 = GameMaster(w2, seed=6)
    # a reward with a vulnerable other present -- the opening a psychopath exploits
    opp = SocialEvent(kind="opportunity", source_id="ann",
                      appraisal_overrides={"reward": 0.8, "other_distress": 0.7,
                                           "threat": 0.0})
    convo = gm2.converse(cal, ann, topic="the money", event=opp)
    seen = convo.opener.deception_seen
    print(f"  faithfulness gate: act={fscore['act']:.2f} reg={fscore['register']:.2f} "
          f"artic={fscore['articulacy']:.2f} (.90/.80/.80)")
    print(f"  {convo.opener.line}")
    print(f"  {convo.reply.line}")
    print(f"  Cal settled on {convo.opener.network} behind an affiliative surface; "
          f"Ann {'saw through it' if seen else 'took it at face value'} and "
          f"answered with {convo.reply.network}.")
    print("  What Cal SAYS is produced by the network it settled on; what Ann HEARS "
          "drives hers -- the model, not the words, does the causal work.")

    print("\n[EXTENSION] criminogenic justice -- does the system make its subjects?")
    from justice import run_comparison, JusticeParams
    from affective_engine.development import Environment
    base = Environment("near-boundary", 0.36, 0.36, 0.34)
    early = JusticeParams(base_detect=0.85, warn_at=1, charge_at=2, convict_at=3,
                          warmth_per_level=0.14, structure_per_level=0.16,
                          recognition_per_level=0.14)
    resourced = Environment("well-resourced", 0.45, 0.47, 0.43)
    off_d, on_d = run_comparison(n_children=30, base_env=base)                 # default
    _,     on_e = run_comparison(n_children=30, base_env=base, params=early)   # aggressive
    _,     on_r = run_comparison(n_children=30, base_env=resourced, params=early)  # far off
    print(f"  near-boundary child, labelling OFF      -> psychopathic "
          f"{off_d.shares()['psychopathic']:.0%}   (baseline)")
    print(f"  near-boundary, default labelling ON     -> psychopathic "
          f"{on_d.shares()['psychopathic']:.0%}")
    print(f"  near-boundary, aggressive labelling ON  -> psychopathic "
          f"{on_e.shares()['psychopathic']:.0%}   (dose-response: harder, earlier contact -> more)")
    print(f"  well-resourced child, aggressive ON     -> psychopathic "
          f"{on_r.shares()['psychopathic']:.0%}   (distance from the edge protects; no fabrication)")
    print("  a hypothesis about the mechanism -- never evidence about people.")

    print("\n[CORE 8] functioning world -- a rule-based day, and local social rules:")
    print("  (the core is neutral machinery; the study's world is an extension)")
    from sim_world import Person, Inhabitant, assess
    from affective_engine.core import sophropathic_seed
    from sophropathy.world import (build_home, build_school, child_routine,
                                   run_study_day, NORMS, BOISTEROUS, DISRUPTIVE,
                                   CONSIDERATE)
    venues = {"Home": build_home(warmth=0.9), "School": build_school()}
    alex = Inhabitant(Person("alex", "Alex", sophropathic_seed()),
                      child_routine("Home", "School"))
    log = run_study_day(venues, {"alex": alex}, hours=range(7, 11))
    for r in log.records:
        print(f"  {r.hour:02d}:00 {r.area:11} {r.activity:12} -> [{r.network}]")
    print("  local social rules -- the same conduct, read by place:")
    for cat in (BOISTEROUS, CONSIDERATE):
        cells = []
        for area in ("classroom", "playground", "workplace", "community"):
            lvl, dep = assess(cat, NORMS[area])
            cells.append(f"{area}={lvl.name.lower()}" + ("*" if dep else ""))
        print(f"    {cat:11}: " + "   ".join(cells))
    print("  access is respect for a boundary, not a lock: a staff room admits "
          "teachers, a bedroom its occupant. No offence framing anywhere.")

    print("\n[CORE 9] the relational fabric of a functioning society:")
    from sim_world import (Society, interact, PARENT_CHILD, TEACHER_PUPIL,
                           BOSS_EMPLOYEE, COLLEAGUES, TEAMMATES, CAPTAIN_PLAYER,
                           COMMUNITY)
    from affective_engine.core import sophropathic_seed as _ok, psychopathic_seed as _px
    def _m(seed): return Person("x", "x", seed).mind
    ties = [PARENT_CHILD, TEACHER_PUPIL, BOSS_EMPLOYEE, COLLEAGUES,
            TEAMMATES, CAPTAIN_PLAYER, COMMUNITY]
    soc = Society()
    minds = {}
    for i, pr in enumerate(ties):
        soc.add(f"h{i}", f"l{i}", pr, standing=0.55, strain=0.3)  # start strained
        minds[(f"h{i}", f"l{i}")] = (_m(_ok()), _m(_ok()))
    start = soc.cohesion()
    for _ in range(4):
        for t in soc.ties:
            interact(t, *minds[(t.higher, t.lower)])
    print(f"  ordinary members, all ties: cohesion {start:.0%} -> {soc.cohesion():.0%} "
          f"(a working society repairs strain)")
    # the study's perturbation: an exploitative disposition in a senior role
    soc2 = Society(); t2 = soc2.add("Boss", "Emp", BOSS_EMPLOYEE, standing=0.6, strain=0.1)
    hm, lm = _m(_px()), _m(_ok())
    for _ in range(5):
        interact(t2, hm, lm)
    print(f"  same boss-employee tie, senior party pressing an advantage: "
          f"-> {t2.state()} (strain {t2.strain:.2f})")
    print("  the core registers strain and repair; WHY a tie strains -- the "
          "disposition, and its meaning -- is the study's reading.")

    print("\n[EXTENSION] the loop closed -- a childhood LIVED IN THE WORLD -> an outcome:")
    from sophropathy import (build_home, build_school, raise_in_world,
                             fearless_child_seed, typical_child_seed)
    from collections import Counter as _C
    _school = build_school()
    _warm = build_home("Warm", warmth=0.9, structure=0.85)
    _harsh = build_home("Harsh", warmth=0.2, structure=0.25)
    for _cl, _sf in [("fearless child", fearless_child_seed),
                     ("typical child ", typical_child_seed)]:
        for _hl, _home in [("warm-firm home", _warm), ("harsh home", _harsh)]:
            _outs = [raise_in_world(_sf(), _home, _school, situation_seed=700 + k).classification
                     for k in range(6)]
            _m = _C(_outs).most_common(1)[0]
            print(f"    {_cl} x {_hl:14} -> {_m[0]:14} ({_m[1]}/6)")
    print("  the outcome is PRODUCED by the life lived, not set -- so every later")
    print("  refinement to homes, schools, ties or norms is observable in the result.")

    print("\n[CORE 10] spawn a settlement from a spec, and populate it as a society:")
    from sim_viz import spec_for_population, generate_settlement, settlement_inventory
    from sim_world import populate
    spec = spec_for_population(200, name="Ashcombe", seed=11)
    city = generate_settlement(spec)
    pop = populate(city, seed=11)
    print(f"  'village of ~200' -> {settlement_inventory(city)}")
    s = pop.summary()
    print(f"  populated: {s['people']} people in {s['households']} households "
          f"({s['children']} children/pupils, {s['adults']} adults), "
          f"{s['ties']} relational ties wired")
    print("  the place is generated and rendered; the society is bound into it and "
          "its lives can be run.")

    print("\n[CORE 11] controlling the passing of time -- real time up to years:")
    from sim_world import TimeController, TimeScale
    from project import ProjectSpec, spawn_universe
    from sophropathy import make_stepper, make_life_stepper
    uni = spawn_universe(ProjectSpec(name="Ashcombe", target_population=140,
                                     extensions=["sophropathy"], fearless_frac=0.2,
                                     seed=5), place_residents=False)
    tc = TimeController(make_stepper(uni, seed=1))
    rt = tc.run(TimeScale.REALTIME, steps=3)
    print("  real time (interaction by interaction):")
    for p in rt:
        for e in p.events:
            if e.kind == "interaction":
                print(f"    {e.text}"); break
    print("  one clock, many speeds: watch sims tick by tick, or advance by day, "
          "week, month or year.")

    print("\n[CORE 12] advancing the clock AGES THE POPULATION to outcomes:")
    life = make_life_stepper(uni, seed=1)
    tc2 = TimeController(life)
    grew_up = 0
    for yr in range(1, 22):
        p = tc2.run(TimeScale.YEAR, steps=1)[0]
        ms = [e for e in p.events if e.kind == "milestone"]
        grew_up += len(ms)
        if ms and yr % 5 == 0:
            from collections import Counter
            reached = Counter(e.text.split(": ")[-1] for e in ms)
            print(f"    year {yr}: {grew_up} grown up so far, this year {dict(reached)}")
    from collections import Counter
    dist = Counter(d["outcome"] for d in life.dev.values() if d["done"])
    print(f"  each child lived their days to a classified outcome: {dict(dist)}")
    print("  (illustrative model behaviour as the mechanism runs -- NOT evidence "
          "about people; real results come from the study's data.)")

    print("\n" + "#" * 78)


if __name__ == "__main__":
    main()
