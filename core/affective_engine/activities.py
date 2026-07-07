"""
activities.py -- the significant activities that fill a human life, as rich
stimulus bundles the substrate can live through (Stage 4: human-interior modelling).

Until now the developmental diet was a thin cycle of bare situations (an
opportunity, a provocation). But a life is made of ACTIVITIES -- play, sport,
learning, talking with friends, being driven to school, a family meal, screen
time, and, from adolescence, sexual activity -- each of which is not a single
trigger but a characteristic BUNDLE of them, presented together. This module gives
the substrate that richer diet, so real structure has something to emerge from.

The discipline is the same as everywhere. An Activity DESCRIBES the stimulus it
presents -- what the experience involves in the substrate's own trigger vocabulary
(play_signal, affiliation, novelty, reward_cue, thwarting, mate_cue, ...) -- NOT
what it does to the person. The person's primary systems fire to the bundle, the
dominant one drives behaviour, and the systems used are strengthened. Two children
at the same football match feel it differently (one SEEKING the goal, one FEARing
the ball) because their wiring decides, not because anything is typed in.

Activities are age-gated: they arise only in the developmental windows where they
belong (rough-and-tumble play in childhood; sport and peer talk from school age;
sexual activity only from adolescence). This is modelled abstractly -- an activity
is a bundle of neutral triggers and an age window -- and sexual activity in
particular is represented only as an age-gated bundle of the LUST/affiliation
triggers Panksepp's model already contains, never as content, and never for
children.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
import random


@dataclass
class Activity:
    """A significant life-activity as a stimulus bundle. `stimulus` is what the
    activity presents, in the substrate's trigger vocabulary; `age_min`/`age_max`
    are the developmental window in which it arises; `significance` scales how
    formative an instance is (a weighting on encounter frequency, not on effect)."""
    id: str
    name: str
    stimulus: Dict[str, float]
    age_min: float = 0.0
    age_max: float = 120.0
    significance: float = 1.0

    def available_at(self, age_years: float) -> bool:
        return self.age_min <= age_years <= self.age_max


# ---------------------------------------------------------------------------
# The vocabulary of significant activities. Bundles are scenario input -- what the
# experience involves -- chosen to be characteristic, not to force an outcome.
# ---------------------------------------------------------------------------

ACTIVITIES: List[Activity] = [
    # -- early and throughout childhood --------------------------------------
    Activity("play", "free / rough-and-tumble play",
             {"play_signal": 0.9, "safety": 0.5, "affiliation": 0.5,
              "novelty": 0.4, "reward_cue": 0.3},
             age_min=1, age_max=16, significance=1.3),
    Activity("family_meal", "a family meal",
             {"affiliation": 0.6, "comfort": 0.6, "safety": 0.5, "reward_cue": 0.4},
             age_min=0, age_max=90, significance=1.0),
    Activity("being_comforted", "being comforted when upset",
             {"comfort": 0.8, "safety": 0.7, "affiliation": 0.6},
             age_min=0, age_max=90, significance=1.0),
    Activity("exploration", "exploring somewhere new",
             {"novelty": 0.8, "reward_cue": 0.5, "safety": 0.4},
             age_min=1, age_max=90, significance=1.0),

    # -- from school age -----------------------------------------------------
    Activity("driven_to_school", "being driven / taken to school",
             {"safety": 0.6, "comfort": 0.5, "affiliation": 0.4, "novelty": 0.2},
             age_min=4, age_max=12, significance=1.0),
    Activity("learning", "a learning task that matters",
             {"novelty": 0.7, "reward_cue": 0.5, "thwarting": 0.5},
             age_min=4, age_max=90, significance=1.1),
    Activity("sport", "playing a sport / competing",
             {"play_signal": 0.6, "reward_cue": 0.6, "thwarting": 0.5,
              "affiliation": 0.5, "novelty": 0.3, "pain": 0.2},
             age_min=5, age_max=60, significance=1.2),
    Activity("talking_with_friends", "talking with friends",
             {"affiliation": 0.8, "play_signal": 0.4, "safety": 0.5,
              "reward_cue": 0.4, "novelty": 0.3},
             age_min=3, age_max=90, significance=1.2),
    Activity("screen_time", "screen / device time",
             {"reward_cue": 0.8, "novelty": 0.6},           # displaces PLAY (Panksepp)
             age_min=2, age_max=90, significance=1.0),
    Activity("peer_conflict", "a falling-out with a peer",
             {"thwarting": 0.7, "provocation_cue": 0.0, "threat": 0.3,
              "novelty": 0.2},
             age_min=3, age_max=90, significance=1.1),
    Activity("achievement", "mastering something / winning",
             {"reward_cue": 0.7, "novelty": 0.4, "affiliation": 0.3},
             age_min=3, age_max=90, significance=1.0),

    # -- from adolescence (age-gated) ----------------------------------------
    # sexual activity: represented ONLY as an age-gated bundle of the LUST /
    # affiliation triggers the model already contains -- abstract, never content,
    # never for children. Gated to adolescence onward.
    Activity("intimacy", "romantic / sexual activity",
             {"mate_cue": 0.8, "reward_cue": 0.6, "affiliation": 0.5,
              "novelty": 0.4, "safety": 0.4},
             age_min=14, age_max=90, significance=1.2),
    Activity("independence", "acting independently / taking a risk",
             {"novelty": 0.7, "reward_cue": 0.6, "thwarting": 0.4},
             age_min=12, age_max=90, significance=1.1),
    Activity("belonging_group", "belonging to a group / fitting in",
             {"affiliation": 0.8, "safety": 0.4, "reward_cue": 0.4},
             age_min=10, age_max=90, significance=1.1),

    # -- the ordinary HARD experiences a real life also contains (realism, not an
    #    outcome: a life is not all play and reward). Which system each engages,
    #    and what it does to the person, still emerges from their wiring.
    Activity("being_told_off", "being told off / disciplined",
             {"thwarting": 0.6, "threat": 0.3, "restraint": 0.4},
             age_min=1, age_max=90, significance=1.0),
    Activity("failure", "failing / being frustrated at a task",
             {"thwarting": 0.8, "novelty": 0.2},
             age_min=3, age_max=90, significance=1.0),
    Activity("rejection", "being left out / rejected by peers",
             {"separation": 0.6, "threat": 0.3, "loss": 0.3},
             age_min=4, age_max=90, significance=1.0),
    Activity("loss", "a loss / a separation (a pet, a move, a parting)",
             {"loss": 0.8, "separation": 0.6},
             age_min=2, age_max=90, significance=0.8),
    Activity("boredom_restless", "being bored / under-stimulated",
             {"novelty": 0.1, "thwarting": 0.3},
             age_min=3, age_max=90, significance=0.8),
]


def activities_for_age(age_years: float) -> List[Activity]:
    """The activities available to a person at this age -- the diet a life offers
    in this developmental window."""
    return [a for a in ACTIVITIES if a.available_at(age_years)]


def sample_activity(age_years: float, rng: random.Random) -> Activity:
    """Draw one age-appropriate activity, weighted by how significant/frequent it
    is. The living world offers a mix; which system it engages, and what that does
    to the person, emerges from their wiring."""
    pool = activities_for_age(age_years)
    if not pool:
        pool = [a for a in ACTIVITIES if a.age_min <= 1]
    return rng.choices(pool, weights=[a.significance for a in pool], k=1)[0]
