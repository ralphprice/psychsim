"""justice -- optional criminogenic-justice extension (labelling dynamics).

Becker (1963), Lemert (1967) rendered as a runnable, sweepable mechanism:
detection -> contact ladder -> labelled environment -> development. Outputs
are hypotheses about the mechanism, never evidence about people.
"""
from .system import (JusticeParams, JusticeSystem, ContactEvent,
                     develop_with_justice, LABEL_NAMES)
from .experiment import run_comparison, report, CohortResult

from modular import Module

# Discoverable as a platform module. This is an ANALYSIS layer: it does not alter the
# spawned population (child_source=None), so selecting it changes nothing about the spawn;
# its OFF/ON comparison is run via `run_comparison`/`report`.
MODULE = Module(
    name="justice",
    title="Criminogenic justice (labelling)",
    description="A sweepable model of how justice-system contact degrades a child's "
                "developmental environment. Analysis layer; does not alter the spawned "
                "population.",
    child_source=None,
    default_params={},
)

