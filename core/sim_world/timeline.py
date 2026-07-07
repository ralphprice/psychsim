"""
timeline.py -- controlling the passing of time (core).

One clock, many speeds. At the fine end it runs in REAL TIME: you watch sim-people
interact tick by tick. At the coarse end it fast-forwards, advancing by day, week,
month or year and surfacing the events that happened over that span at that
granularity. The same underlying event stream is simply shown at the chosen
resolution -- individual interactions when close up, rolled-up summaries when the
clock is racing ahead.

The controller is generic: it drives a `world_step(clock, minutes)` callback that
advances the simulation by a span of simulated minutes and returns the events
that occurred. A study supplies that callback (what an interaction is, what counts
as an event); the core provides the clock, the scales, the pacing, and the
bucketing of events into periods. Optional real-time pacing lets a live view feel
like time actually passing.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Callable, Dict, List, Optional
import time as _time

# a simple, revisable calendar
MIN_PER_HOUR = 60
HOURS_PER_DAY = 24
DAYS_PER_WEEK = 7
DAYS_PER_MONTH = 30
DAYS_PER_YEAR = 365
MIN_PER_DAY = MIN_PER_HOUR * HOURS_PER_DAY


class TimeScale(IntEnum):
    """A step size, valued in simulated minutes -- from a single interaction tick
    (real time) up to a year at a stride."""
    REALTIME = 1                          # ~one interaction tick
    MINUTE = 1
    HOUR = MIN_PER_HOUR                    # 60
    DAY = MIN_PER_DAY                      # 1,440
    WEEK = MIN_PER_DAY * DAYS_PER_WEEK     # 10,080
    MONTH = MIN_PER_DAY * DAYS_PER_MONTH   # 43,200
    YEAR = MIN_PER_DAY * DAYS_PER_YEAR     # 525,600


SCALE_NAMES = {TimeScale.REALTIME: "real time", TimeScale.HOUR: "hour",
               TimeScale.DAY: "day", TimeScale.WEEK: "week",
               TimeScale.MONTH: "month", TimeScale.YEAR: "year"}


@dataclass
class Instant:
    """A point in simulated time, addressable at any granularity."""
    total_minutes: int

    @property
    def minute(self) -> int: return self.total_minutes % MIN_PER_HOUR
    @property
    def hour(self) -> int: return (self.total_minutes // MIN_PER_HOUR) % HOURS_PER_DAY
    @property
    def day(self) -> int: return self.total_minutes // MIN_PER_DAY
    @property
    def week(self) -> int: return self.day // DAYS_PER_WEEK
    @property
    def month(self) -> int: return self.day // DAYS_PER_MONTH
    @property
    def year(self) -> int: return self.day // DAYS_PER_YEAR

    def label(self) -> str:
        d = self.day
        y, rem = divmod(d, DAYS_PER_YEAR)
        mo, dd = divmod(rem, DAYS_PER_MONTH)
        return (f"Y{y+1} M{mo+1} D{dd+1} {self.hour:02d}:{self.minute:02d}")


@dataclass
class Event:
    """Something that happened at a moment -- an interaction, a strain, a repair,
    a developmental milestone. A study decides what to emit."""
    at: int                               # total simulated minutes
    kind: str                             # e.g. 'interaction', 'strain', 'milestone'
    who: str = ""
    text: str = ""
    data: Dict = field(default_factory=dict)


@dataclass
class Period:
    """One advance of the clock: the span covered, the events in it, and a
    summary appropriate to the scale (each event when close up; rolled-up counts
    when fast-forwarding)."""
    scale: TimeScale
    start: Instant
    end: Instant
    events: List[Event]

    def summary(self, max_notable: int = 6) -> str:
        if self.scale <= TimeScale.HOUR:
            return "\n".join(f"  {Instant(e.at).label()}  {e.text}" for e in self.events) \
                or "  (quiet)"
        from collections import Counter
        c = Counter(e.kind for e in self.events)
        head = ", ".join(f"{n} {k}{'s' if n != 1 else ''}" for k, n in c.most_common())
        notable = [e.text for e in self.events if e.kind in ("milestone", "rupture")]
        line = f"  {self.start.label()} .. {self.end.label()}: {head or 'quiet'}"
        shown = notable[:max_notable]
        extra = len(notable) - len(shown)
        tail = "".join(f"\n    * {t}" for t in shown)
        if extra > 0:
            tail += f"\n    * ... and {extra} more"
        return line + tail


class SimClock:
    def __init__(self) -> None:
        self.total_minutes = 0

    @property
    def now(self) -> Instant:
        return Instant(self.total_minutes)

    def advance(self, minutes: int) -> Instant:
        self.total_minutes += int(minutes)
        return self.now


class TimeController:
    """Runs the simulation forward at a chosen scale, bucketing the events each
    advance produces into periods. `world_step(clock, minutes) -> List[Event]`
    must advance the world by `minutes` of simulated time and return what
    happened; the controller advances the clock in step with it."""

    def __init__(self, world_step: Callable[["SimClock", int], List[Event]]):
        self.clock = SimClock()
        self.world_step = world_step
        self.events: List[Event] = []

    def step(self, scale: TimeScale) -> Period:
        start = self.clock.now
        before = self.clock.total_minutes
        evs = self.world_step(self.clock, int(scale))
        if self.clock.total_minutes == before:        # step_fn didn't move the clock
            self.clock.advance(int(scale))
        self.events.extend(evs)
        return Period(scale, start, self.clock.now, evs)

    def run(self, scale: TimeScale, steps: int = 1,
            on_period: Optional[Callable[[Period], None]] = None,
            realtime: bool = False, speed: float = 1.0,
            seconds_per_sim_minute: float = 0.02) -> List[Period]:
        """Advance `steps` times at `scale`. If `realtime`, pace each step so wall
        time tracks simulated time (scaled by `speed` -- higher is faster). Calls
        `on_period` for each period as it completes."""
        periods: List[Period] = []
        for _ in range(steps):
            p = self.step(scale)
            periods.append(p)
            if on_period:
                on_period(p)
            if realtime and speed > 0:
                _time.sleep(min(2.0, int(scale) * seconds_per_sim_minute / speed))
        return periods
