"""
gamemaster.py -- adjudicates action into world change.

The affective engine chooses a behavioural network (the mode the person acts in);
the Game-Master turns that choice, in this place and this institution, into a
world event: relationships shift, reputations move, resources change hands, and
the institution's response feeds back into the person's development (the same
consolidation and control-plasticity the engine already models, now driven by a
real institutional climate rather than a bare environment object).

This is the join between the world (Package 1) and the affective engine
(Package 2). It is deliberately rule-based and inspectable, not another model
call, so that what happens in the world is legible and reproducible.
"""

from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from affective_engine.core import clamp
from affective_engine.drives import respond_to_appraisal, is_cohesive, is_aggressive
from affective_engine.development import Environment, develop  # reuse the learning rule
from speech.acts import act_from_behaviour, SpeechChannel, SpeechAct
from speech.render import TemplateRenderer

from .world import World, Institution
from .person import Person, SocialEvent

# life-stage -> speech register (rendering band); anything else is adult
_STAGE_REGISTER = {
    "early_childhood": "child", "middle_childhood": "child",
    "adolescence": "adolescent",
}


@dataclass
class Relationship:
    familiarity: float = 0.0
    affect: float = 0.0        # -1 hostile .. +1 warm
    trust: float = 0.0


@dataclass
class Interaction:
    """A logged record of one adjudicated action."""
    step: int
    actor: str
    place: str
    behaviour: str             # the emergent action the actor took (Panksepp behaviour), not a category
    target: Optional[str]
    effect: str                # human-readable outcome
    valence: float             # environment/institution response valence


@dataclass
class Utterance:
    """One turn of a dialogic exchange: the speech-act a person emitted, what
    the hearer took it to be, the behavioural network behind it, and the
    rendered line (observer channel only -- nothing reads it back)."""
    speaker: str
    target: str
    behaviour: str             # the emergent action behind the utterance, not a category
    act: SpeechAct
    perceived_as: str          # what the hearer appraised it as
    line: str                  # rendered transcript line

    @property
    def deception_seen(self) -> Optional[bool]:
        if not self.act.deceptive:
            return None
        return self.perceived_as == self.act.intent


@dataclass
class Conversation:
    """A two-turn adjudicated encounter between two co-present people: an
    opener and the hearer's reply, plus the world Interactions each produced."""
    step: int
    place: str
    opener: Utterance
    reply: Utterance
    interactions: List[Interaction] = field(default_factory=list)

    def transcript(self) -> str:
        return f"{self.opener.line}\n{self.reply.line}"


class GameMaster:
    def __init__(self, world: World, seed: int = 20260705) -> None:
        self.world = world
        self.relationships: Dict[Tuple[str, str], Relationship] = {}
        self.reputation: Dict[str, float] = {}
        self.log: List[Interaction] = []
        self.conversations: List[Conversation] = []
        self._rng = random.Random(seed)         # seeds deception-detection rolls
        self._renderer = TemplateRenderer()

    # -- relationships -----------------------------------------------------
    def rel(self, a: str, b: str) -> Relationship:
        return self.relationships.setdefault((a, b), Relationship())

    # -- the core adjudication --------------------------------------------
    def adjudicate(self, person: Person, resp,
                   event: Optional[SocialEvent] = None) -> Interaction:
        """Commit the consequences of `person`'s emergent action `resp` (a drives.Response).
        The world keys on FEATURE read-outs of the act (is_cohesive/is_aggressive) and on the
        emergent action itself (`resp.behaviour`) -- never on an outcome-category label
        (honesty migration #2)."""
        world = self.world
        place = world.location_of(person.agent_id) or "?"
        inst = world.governing_institution(person.agent_id)
        target = event.source_id if event else None
        behaviour = resp.behaviour

        # 1. relational and reputational effect of the act
        effect, drep = self._effect_of(behaviour)
        self.reputation[person.agent_id] = clamp(
            self.reputation.get(person.agent_id, 0.5) + drep, 0.0, 1.0)
        if target is not None:
            r = self.rel(person.agent_id, target)
            r.familiarity = clamp(r.familiarity + 0.1)
            if is_cohesive(resp):              # appetitive/affiliative act -> warms the tie
                r.affect = clamp(r.affect + 0.15, -1.0, 1.0)
                r.trust = clamp(r.trust + 0.1)
            elif is_aggressive(resp):          # RAGE-driven act -> strains the tie
                r.affect = clamp(r.affect - 0.2, -1.0, 1.0)
                r.trust = clamp(r.trust - 0.15)

        # 2. the institution's response valence (warmth of the climate),
        #    which is what development consumes
        valence = 0.0
        if inst is not None:
            valence = clamp(2.0 * inst.warmth - 1.0, -1.0, 1.0)

        interaction = Interaction(world.clock.interaction_step, person.agent_id,
                                  place, behaviour, target, effect, valence)
        self.log.append(interaction)
        world.clock.tick()
        return interaction

    def _effect_of(self, behaviour: str) -> Tuple[str, float]:
        """Map an EMERGENT ACTION (a Panksepp behaviour, not a category) to a world effect and
        a reputation delta. Whether an action reads as prosocial or antisocial is the observer's
        job (observer.py); this table only describes what each act does in the world."""
        table = {
            "nurture": ("supports and bonds", +0.05),
            "play": ("plays warmly", +0.04),
            "court": ("courts", +0.03),
            "approach": ("acts toward a goal", +0.02),
            "aggress": ("lashes out", -0.10),
            "avoid": ("withdraws", -0.01),
            "seek_comfort": ("seeks comfort", -0.01),
        }
        return table.get(behaviour, ("acts", 0.0))

    # -- one social episode ------------------------------------------------
    def run_episode(self, person: Person,
                    event: Optional[SocialEvent] = None) -> Interaction:
        """Perceive -> choose a mode (affective engine) -> adjudicate -> record
        to the person's episodic memory."""
        appraisal = person.perceive(self.world, event)
        resp = respond_to_appraisal(person.mind, appraisal)
        person.mind.dominant = resp.behaviour  # reflect the substrate's emergent action for inspection
        interaction = self.adjudicate(person, resp, event)

        # write the lived event to the person's episodic memory (the emergent action, not a category)
        importance = clamp(max(appraisal.threat, appraisal.provocation,
                               appraisal.reward, appraisal.other_distress))
        person.mind.memory.add(appraisal.label, appraisal, resp.behaviour,
                               interaction.valence, importance)
        return interaction

    # -- helpers for dialogic interaction ----------------------------------
    def _register_for(self, person: Person) -> str:
        try:
            return _STAGE_REGISTER.get(person.life_stage(self.world).value, "adult")
        except Exception:
            return "adult"

    def _articulacy_for(self, person: Person) -> float:
        """Rendering-only fluency knob; younger speakers render less fluently.
        Carries no causal weight -- it never touches appraisal."""
        return {"child": 0.3, "adolescent": 0.6}.get(self._register_for(person), 0.7)

    def _vigilance_of(self, hearer: Person, speaker_id: str) -> float:
        """How likely the hearer is to see through a deceptive act. Grounded in
        engine and relational state: a threat-primed mind and low trust in the
        speaker both raise vigilance. Detection itself is a seeded roll in the
        speech channel -- this only sets its probability."""
        threat = hearer.mind.gain.get("THREAT", 0.3)
        threat_norm = clamp((threat - 0.20) / 0.70)
        trust = self.rel(hearer.agent_id, speaker_id).trust
        return clamp(0.25 + 0.45 * threat_norm + 0.30 * (1.0 - trust))

    def _one_turn(self, chan: SpeechChannel, speaker: Person, hearer: Person,
                  appr, topic: str) -> Tuple[Utterance, "Appraisal"]:
        """Speaker settles on a network, emits the act that network makes, the
        hearer perceives it (seeded), and we return the utterance plus the
        appraisal the hearer should now be run on."""
        resp = respond_to_appraisal(speaker.mind, appr)
        intensity = clamp(0.35 + 0.5 * max(appr.provocation, appr.threat,
                                           appr.reward, appr.other_distress))
        act = act_from_behaviour(resp.behaviour, speaker.agent_id, hearer.agent_id,
                                 intensity=intensity,
                                 register=self._register_for(speaker),
                                 articulacy=self._articulacy_for(speaker),
                                 topic=topic,
                                 tick=self.world.clock.interaction_step)
        heard_appr = chan.exchange(act, self._vigilance_of(hearer, speaker.agent_id),
                                   self._rng)
        perceived = chan.acts[-1][1]
        line = self._renderer.transcript_line(act, perceived, self._rng)
        # the speaker records having acted; the hearer records below, in its turn
        i = self.adjudicate(speaker, resp,
                            SocialEvent(kind=act.intent.lower(),
                                        source_id=hearer.agent_id))
        speaker.mind.memory.add(appr.label, appr, resp.behaviour, i.valence,
                                clamp(max(appr.threat, appr.provocation,
                                          appr.reward, appr.other_distress)))
        return Utterance(speaker.agent_id, hearer.agent_id, resp.behaviour, act,
                         perceived, line), heard_appr

    def converse(self, actor: Person, target: Person, topic: str = "it",
                 event: Optional[SocialEvent] = None) -> Conversation:
        """A dialogic encounter between two co-present people. The actor
        perceives the situation and speaks; the target appraises the ACT it
        heard (not the words) and answers; both acts are adjudicated into the
        world and written to each mind's memory. This is where the language
        layer joins the living simulation: what an agent says is produced by
        the network it settled on, and what it hears drives the network it
        settles on next -- deception included, resolved by a seeded roll."""
        if actor is target:
            raise ValueError("a person cannot converse with themselves")
        world = self.world
        place = world.location_of(actor.agent_id) or "?"
        chan = SpeechChannel()

        # actor opens from its reading of the situation
        a_appr = actor.perceive(world, event)
        opener, heard = self._one_turn(chan, actor, target, a_appr, topic)

        # target replies to what it actually heard (the perceived act)
        reply, _ = self._one_turn(chan, target, actor, heard, topic)

        convo = Conversation(world.clock.interaction_step, place, opener, reply,
                             [self.log[-2], self.log[-1]])
        self.conversations.append(convo)
        return convo


def institution_to_environment(inst: Institution) -> Environment:
    """Bridge: express an institution's climate as the developmental Environment
    the affective engine's `develop` rule already understands, so a childhood
    lived across real institutions drives the same, validated learning."""
    recognition = inst.warmth * inst.structure   # recognising care needs both
    return Environment(inst.name, warmth=inst.warmth, structure=inst.structure,
                       recognition=recognition)
