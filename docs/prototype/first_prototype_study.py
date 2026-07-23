import sys,os
_R="/home/ralph/psychsim"; sys.path.insert(0,os.path.join(_R,"core")); sys.path.insert(0,os.path.join(_R,"extensions")); sys.path.insert(0,_R)
from sim_experiment.lifecourse import run_life, StageEnv, LifeCourseSpec
from affective_engine import shared_root_seed, psychopathic_seed, sophropathic_seed, TraitSeed
from sophropathy.society import fearless_child_seed, typical_child_seed
from substrate.readout import _BLEND_MARGIN

# THE FIRST END-TO-END PROTOTYPE STUDY: a cohort develops through the coupled life-course loop under
# manipulated MORAL environments x RELATIONAL history, reported on the GRADED profile (never the bare label).
def spec(label, warm):
    # a two-stage moral-environment childhood (home -> school)
    return LifeCourseSpec(label, [StageEnv("home", warm, warm, warm, 32),
                                  StageEnv("school", warm, 0.7, warm, 32)])

SEEDS = {"shared_root": shared_root_seed, "fearless": fearless_child_seed, "typical": typical_child_seed,
         "sophropathic": sophropathic_seed, "psychopathic": psychopathic_seed}
ENVS = {"warm": 0.75, "harsh": 0.25}

print("="*94)
print("FIRST END-TO-END PROTOTYPE STUDY -- graded developmental profiles (corrected instrument, gate-6 clean)")
print("="*94)
hdr = "seed x env            | domain profile (sorted)                                   | label (margin)"
print(hdr); print("-"*94)
for sname, sfn in SEEDS.items():
    for ename, warm in ENVS.items():
        for rel in (False, True):
            tag = "rel" if rel else "env"
            r = run_life(sfn(), spec(f"{sname}|{ename}", warm), situation_seed=1234,
                         relational=rel, cohort_size=3, cadence=0.6)
            prof = "  ".join(f"{k[:4]}={v:.3f}" for k,v in sorted(r.profile.items(), key=lambda t:-t[1]))
            conf = "CONFIDENT" if r.margin >= _BLEND_MARGIN else "knife-edge"
            print(f"{sname:12s} {ename:4s} {tag:3s} | {prof} | {r.classification[:12]:12s} m={r.margin:.4f} {conf}")
