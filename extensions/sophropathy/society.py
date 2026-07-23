"""
society.py -- families, dispositions, and the parent -> environment mechanism.

The platform raises one child at a time in a given environment. The staged
programme needs two things on top of that:

  1. A distinction between the child dispositions the programme studies:
       - a TYPICAL child (ordinary fear/affiliation) -- the control;
       - a FEARLESS child (the shared root disposition: attenuated threat/fear,
         undeveloped control) -- the "proto-psychopath / sophropathic" child,
         whose adult outcome the environment decides.

  2. Parents who are themselves dispositional, and whose disposition SHAPES the
     caregiving environment their children grow up in. This is the mechanism that
     lets stages 6-7 model a psychopathic or sophropathic *parent*: the parent's
     capacity for warmth (CARE) and conscience-linked self-command (CONTROL)
     determine the warmth, structure and recognition the child experiences.

Nothing here is fitted to data. The mappings are transparent, illustrative, and
are the things Stage 5 calibrates against the human studies.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from affective_engine import (TraitSeed, shared_root_seed,
                              shared_root_calculating_seed,
                              sophropathic_seed, psychopathic_seed)
from affective_engine.development import Environment, clamp


# ---------------------------------------------------------------------------
# Child dispositions
# ---------------------------------------------------------------------------

def typical_child_seed() -> TraitSeed:
    """The control child: ordinary threat/fear and affiliation, an undeveloped
    control circuit. Because fear is intact, a harsh upbringing tends to make
    this child anxious or withdrawn rather than callous -- the differential-
    susceptibility contrast with the fearless child."""
    return TraitSeed(
        "typical_child",
        gains={"THREAT": 0.50, "ANXIETY": 0.50, "SEEKING": 0.60,
               "FRUSTRATION": 0.50, "CARE": 0.55, "SOCIAL_LOSS": 0.50,
               "CONTROL": 0.40, "INSTRUMENTAL_CONTROL": 0.35},
    )


def fearless_child_seed() -> TraitSeed:
    """The proto-psychopath / sophropathic child: the shared root disposition.
    Its adult outcome is decided by development."""
    return shared_root_seed()


def fearless_calculating_child_seed() -> TraitSeed:
    """A fearless child high in cold instrumental temperament (the variant that,
    raised harshly, tends to the calculated rather than reactive outcome)."""
    return shared_root_calculating_seed()


CHILD_SEEDS = {
    "typical": typical_child_seed,
    "fearless": fearless_child_seed,
    "fearless_calculating": fearless_calculating_child_seed,
}


# ---------------------------------------------------------------------------
# Parent dispositions
# ---------------------------------------------------------------------------

def normal_parent_seed() -> TraitSeed:
    """A balanced, developed adult -- the ordinary parent."""
    return TraitSeed(
        "normal_parent",
        gains={"THREAT": 0.40, "ANXIETY": 0.40, "SEEKING": 0.60,
               "FRUSTRATION": 0.45, "CARE": 0.55, "SOCIAL_LOSS": 0.50,
               "CONTROL": 0.62, "INSTRUMENTAL_CONTROL": 0.40},
    )


PARENT_SEEDS = {
    "normal": normal_parent_seed,
    "sophropathic": sophropathic_seed,
    "psychopathic": psychopathic_seed,
}


# ---------------------------------------------------------------------------
# The parent -> caregiving environment mapping (the intergenerational mechanism)
# ---------------------------------------------------------------------------

def parent_to_environment(parent: TraitSeed, name: Optional[str] = None) -> Environment:
    """Derive the caregiving environment a parent provides from their capacity for warmth (CARE) and
    conscience-linked self-command (CONTROL).

    ★★ CLAIM WITHDRAWN -- SCAFFOLD, NOT A GROUNDED MECHANISM (prototype item 2b). This is a hand-authored
    trait->environment mapping and it carries THREE banned patterns the honesty wall forbids:
      1. THREE invented coefficients (1.3, 0.4, 0.6) map disposition straight to warmth/structure/recognition
         -- scalars chosen, not grounded.
      2. THE PARENT IS NEVER AN AGENT. A grounded transmission would instantiate the parent, let it DEVELOP
         from its own temperament and rearing, and let its EMERGENT caregiving BEHAVIOUR create the child's
         environment (wire what the agent perceives; behaviour emerges). Here disposition -> environment is a
         direct formula with no agent, no development, no behaviour.
      3. PARENT_SEEDS feeds psychopathic_seed / sophropathic_seed -- documented DEVELOPED END-STATES (outcome
         categories, core.py) -- in as a CAUSAL INPUT: the outcome-category-as-primitive violation.
    CONSEQUENCE: the Stage-6/7 intergenerational-TRANSMISSION CLAIM ("dispositional parents transmit outcome
    via the environment they create") is NOT a grounded emergent result and is WITHDRAWN. The stages still RUN
    as a scaffold demonstration, clearly marked; no thesis claim rests on them until grounded.
    GROUNDING PATH (registered, a future pass, NOT a prototype blocker): parent-as-agent -- the parent develops
    and acts, and the child's Environment EMERGES from the parent's caregiving behaviour, not a coefficient.
    The coefficients below are SCAFFOLD and are left only so the scaffold stages execute; they are not a claim.
    """
    care = parent.gains.get("CARE", 0.4)
    control = parent.gains.get("CONTROL", 0.4)
    warmth = clamp(1.3 * care)         # SCAFFOLD (withdrawn claim -- see docstring)
    structure = clamp(control)         # SCAFFOLD
    recognition = clamp(0.4 * warmth + 0.6 * structure)   # SCAFFOLD
    return Environment(name or f"{parent.name}_parenting",
                       warmth=warmth, structure=structure, recognition=recognition)


# ---------------------------------------------------------------------------
# Family types as direct environments (stages 2-5)
# ---------------------------------------------------------------------------

FAMILY_ENVIRONMENTS: Dict[str, Environment] = {
    "caring": Environment("caring", warmth=0.90, structure=0.85, recognition=0.85),
    "balanced": Environment("balanced", warmth=0.65, structure=0.60, recognition=0.60),
    "dysfunctional": Environment("dysfunctional", warmth=0.20, structure=0.25, recognition=0.15),
}


# ---------------------------------------------------------------------------
# Family and society
# ---------------------------------------------------------------------------

@dataclass
class Family:
    """A family: a caregiving environment (either a family-type environment, or
    one derived from a parent's disposition) and an optional child disposition."""
    family_type: str
    environment: Environment
    parent_seed: Optional[TraitSeed] = None
    child_seed: Optional[TraitSeed] = None


@dataclass
class Society:
    name: str
    families: List[Family] = field(default_factory=list)

    def environment_profile(self) -> Dict[str, float]:
        """Mean warmth/structure across the society -- a crude 'balance' read."""
        n = max(1, len(self.families))
        return {
            "families": len(self.families),
            "mean_warmth": sum(f.environment.warmth for f in self.families) / n,
            "mean_structure": sum(f.environment.structure for f in self.families) / n,
        }
