"""
engine.py (substrate) -- the dynamical substrate engine ("make v7 live", Part 2 S2).

A leaky-integrator rate model over the v7 circuits/connections (S2.2). Each LIVE circuit is a
rate unit relaxing toward its net input; a two-switch live set (developmental_online_age +
calibration_active, S2.3) gates which circuits/connections participate, so the maturation
gradient falls out of the data. Per step, the live connections update by the composed 8-rule
plasticity (plasticity.py), with R5's neuromodulator supplied as a source CIRCUIT's live
output. Circuits are only rate units -- the update references no circuit's meaning.

Standalone (8a): this engine produces circuit ACTIVITY; it is not wired into the valence
engine or the live sim yet (that unification is 8b). Acceptance here is mechanistic (S2.6).
"""

from __future__ import annotations
from typing import Dict, List, Optional

from . import params
from . import plasticity as P
from .model import SubstrateModel, load_substrate


class SubstrateEngine:
    def __init__(self, model: Optional[SubstrateModel] = None, age_years: float = 25.0):
        self.model = model or load_substrate()
        self.age_years = age_years
        m = self.model
        # dynamical state (initialised at the age-appropriate baseline -- S57)
        self.activation: Dict[str, float] = {cid: self._baseline_at_age(c) for cid, c in m.circuits.items()}
        self.theta: Dict[str, float] = {cid: self._baseline_at_age(c) for cid, c in m.circuits.items()}
        self.mean_activity: Dict[str, float] = {cid: self._baseline_at_age(c) for cid, c in m.circuits.items()}
        self.weight: List[float] = [c.weight0 for c in m.connections]
        self.eligibility: List[float] = [0.0] * len(m.connections)
        self.external: Dict[str, float] = {}
        self.channel_drive: Dict[str, float] = {}
        # THROTTLE (Part 3 S4.1): a graded 0..1 HYPOFUNCTION on a circuit -- it still fires but
        # drives its targets more weakly (output gain 1-fraction), and its connections cannot
        # fully learn back to normal (a plasticity ceiling). The study manipulation; NOT an
        # outcome weight. Applied to an otherwise-ordinary substrate; what it produces is measured.
        self.throttle: Dict[str, float] = {}
        # per-agent per-circuit INPUT-reactivity gain (default 1.0 via .get). v10 E5/E6: an agent's
        # own physical strength + sex bias its VMHvl reactivity -- how strongly it responds to its
        # drive. Multiplies the circuit's driven input, NOT its baseline, so it cannot add a standing
        # drive. Neutral-floor: at v10 provocation was VMHvl's only input, so the floor held BY
        # CONSTRUCTION; v11 added VMHvl afferents (MeA/BNST), whose neutral net is negligible, so the
        # floor now holds BEHAVIOURALLY (neutral -> restrain; residual ~0). A calibration on the
        # competition, never a determinant of output. Not an outcome weight; what it produces is measured.
        self.reactivity: Dict[str, float] = {}
        self._silent: List[int] = [0] * len(m.connections)
        self.exp_count: List[int] = [0] * len(m.connections)   # relevant experiences (S10.1)
        self._coactive_flag: List[bool] = [False] * len(m.connections)
        self.pruned: List[bool] = [False] * len(m.connections)
        self._step_i = 0
        self._refresh_live()

    def _baseline_at_age(self, c) -> float:
        """S57 -- the age-appropriate baseline. `c.baseline` is the ADULT/mature target; a
        circuit whose tonic rate MATURES postnatally (the neuromodulator pacemakers -- the
        four-pacemaker table) carries a `baseline_schedule_ref`, and its effective baseline is
        the adult value scaled by the SAME maturation curve that matures a circuit's functional
        contribution (immature -> adult, from onset). Exactly parallel to how a schedule_ref
        gives an edge a maturing WEIGHT (pfc_low_early_high_late). No schedule -> the static
        baseline, unchanged. This is the missing field: the substrate had developmental_online_age
        (onset) and plasticity/maturation curves, but no maturing BASELINE -- so a neuromodulator
        whose tonic rate develops (DRN's scaffold-low was standing in for exactly this) could not
        be represented. ★ DRN SEMANTICS (counterintuitive -- record correctly or the next person
        inverts the curve): the DRN baseline here is the FUNCTIONAL INHIBITORY EFFICACY of the
        5-HT system on the aggression circuit, which matures UP across childhood -- NOT tissue 5-HT
        (which PEAKS in the first two postnatal years and DECLINES to adult; Hohmann 1988), and NOT
        raw firing. It matures up because the RECEPTOR-AND-CIRCUIT machinery matures up: 5-HT1A
        autoreceptor response + 5-HT innervation of frontal cortex (top-down inhibitory control)
        both develop late, while transmitter level falls. That is why DRN maps to
        pfc_low_early_high_late -- the frontal inhibitory-control maturation curve -- a GROUNDED
        identification (same curve, same reason as the PFC), not a convenient pick."""
        if c.baseline_schedule_ref:
            return c.baseline * P.maturation(c.baseline_schedule_ref, self.age_years, c.online_age)
        return c.baseline

    # -- the two-switch live set (S2.3) -----------------------------------
    def set_age(self, age_years: float) -> None:
        self.age_years = age_years
        self._refresh_live()

    def _refresh_live(self) -> None:
        m = self.model
        self.live_circuit = {
            cid: (c.calibration_active and c.online_age <= self.age_years)
            for cid, c in m.circuits.items()
        }
        self.live_conn = [
            (k.calibration_active and k.online_age <= self.age_years
             and self.live_circuit.get(k.source, False)
             and self.live_circuit.get(k.target, False))
            for k in m.connections
        ]

    def live_circuits(self) -> List[str]:
        return [cid for cid, on in self.live_circuit.items() if on]

    # -- external drive (via a circuit, or an input channel) --------------
    def inject(self, circuit_id: str, drive: float) -> None:
        self.external[circuit_id] = drive

    def inject_channel(self, channel_id: str, drive: float) -> None:
        """Drive a sensory input channel (e.g. 'IN-GUST' or 'IN-GUST:sweet'); prefix-matched
        to the seed's channel->circuit input edges."""
        self.channel_drive[channel_id] = drive

    def _edge_drive(self, edge_channel: str) -> float:
        best = 0.0
        for key, d in self.channel_drive.items():
            if edge_channel == key or edge_channel.startswith(key):
                best = max(best, d)
        return best

    def clear_inputs(self) -> None:
        self.external = {}
        self.channel_drive = {}

    # -- throttle (the study manipulation, S4.1) --------------------------
    def set_throttle(self, circuit_id: str, fraction: float) -> None:
        """Throttle a circuit's OUTPUT by `fraction` in [0,1] (0 = normal, 1 = silent output).
        A graded reactivity/output hypofunction, from birth; its connections also gain a
        plasticity ceiling so a throttled pathway stays weak."""
        self.throttle[circuit_id] = max(0.0, min(1.0, fraction))

    def _gain(self, circuit_id: str) -> float:
        return 1.0 - self.throttle.get(circuit_id, 0.0)

    # -- input-reactivity gain (v10 E5/E6 physical calibration) -----------
    def set_reactivity(self, circuit_id: str, gain: float) -> None:
        """Set a circuit's INPUT-reactivity gain (>0; 1.0 = normal). Scales how strongly the circuit
        responds to its drive, NOT its resting level -- a calibration on the competition, applied at
        birth from the agent's physical endowment. Distinct from throttle (which weakens OUTPUT)."""
        self.reactivity[circuit_id] = max(0.0, float(gain))

    # -- R5 modulator: a neuromodulator SOURCE CIRCUIT's live output ------
    def neuromod_output(self, nmod: str) -> float:
        """The R5 modulator scalar for a connection gated by `nmod`. It is the mean live
        activation of that neuromodulator's SOURCE CIRCUIT(S) -- a circuit output, never a
        value set from an outcome. 'none' (ungated) and unresolved sources -> 1.0."""
        if not nmod or nmod == "none":
            return 1.0
        srcs = self.model.neuromod_source.get(nmod, [])
        live = [self.activation[s] * self._gain(s)
                for s in srcs if self.live_circuit.get(s, False)]
        if not live:
            return 1.0                       # unresolved/offline source -> ungated (flagged)
        return sum(live) / len(live)

    def neuromod_teaching(self, nmod: str) -> float:
        """The PHASIC teaching signal that gates R5 consolidation: the neuromodulator SOURCE CIRCUIT(S)'
        activation ABOVE their running baseline (`mean_activity`), floored at 0. A tonically-elevated
        source (e.g. CeA holding LC up) yields NO tonic teaching signal -- a teaching signal is a
        DEVIATION ('something salient happened NOW'), not a standing level, and it naturally habituates
        as the baseline catches up to a sustained input. This is the same phasic principle behaviour
        selection already uses (`_phasic_drive`: tonic cancels so hub circuits don't swamp). 'none'
        (ungated) and unresolved/offline sources -> 1.0, exactly as `neuromod_output`."""
        if not nmod or nmod == "none":
            return 1.0
        srcs = [s for s in self.model.neuromod_source.get(nmod, [])
                if self.live_circuit.get(s, False)]
        if not srcs:
            return 1.0
        dev = sum((self.activation[s] - self.mean_activity[s]) * self._gain(s)
                  for s in srcs) / len(srcs)
        return max(0.0, dev)

    # -- one integration + plasticity step (S2.2 / S2.4) ------------------
    def step(self, dt_ms: float = None) -> None:
        dt = params.DT_MS if dt_ms is None else dt_ms
        m = self.model
        a = self.activation

        # 1) leaky-integrator update (synchronous): new activation from current inputs
        new_a = dict(a)
        for cid, c in m.circuits.items():
            if not self.live_circuit[cid]:
                continue
            inp = self.external.get(cid, 0.0)
            # circuit -> circuit input, signed PER CONNECTION (v12a: from the cited dominant target
            # receptor; else the source nucleus's principal transmitter)
            for j in m.incoming.get(cid, ()):
                if self.live_conn[j] and not self.pruned[j]:
                    k = m.connections[j]
                    src = k.source
                    # v14: a phasic/adapting edge transmits the source's DEVIATION above its running
                    # baseline (mean_activity), floored at 0 -- for edges whose transmitter release is
                    # phasic, not tonic (e.g. CeA-CRF->LC: CRF release fires on the event and adapts, it
                    # does not clamp LC at CeA's plateau level). Same deviation the phasic teaching signal
                    # uses. A tonic edge transmits the absolute level, as before.
                    drive = (a[src] - self.mean_activity[src]) if k.phasic_drive else a[src]
                    if drive < 0.0:
                        drive = 0.0
                    inp += (k.sign * self.weight[j]
                            * drive * self._gain(src))    # throttle: weak output drive
            # sensory input edges (channel -> circuit), driven when the channel is injected
            for e in m.incoming_channel.get(cid, ()):
                edge = m.input_edges[e]
                if edge.calibration_active and edge.online_age <= self.age_years:
                    inp += edge.weight0 * self._edge_drive(edge.channel)
            # E5/E6: scale the DRIVEN input by the per-circuit reactivity gain (default 1.0). The
            # baseline-relaxation term is separate, so a raised gain amplifies response to drive
            # (provocation) without lifting the resting level -- the neutral floor holds.
            r = self.reactivity.get(cid)
            if r is not None and r != 1.0:
                inp *= r
            da = (dt / c.tau_ms) * (-(a[cid] - self._baseline_at_age(c)) + inp)
            lo, hi = c.bounds
            new_a[cid] = P.clamp_weight(a[cid] + da, lo, hi)
        self.activation = new_a

        # 2) BCM threshold tracks each circuit's own recent activity
        for cid in m.circuits:
            if self.live_circuit[cid]:
                self.theta[cid] = P.update_theta(self.theta[cid], new_a[cid])
                self.mean_activity[cid] = 0.99 * self.mean_activity[cid] + 0.01 * new_a[cid]

        # 3) per-connection plasticity: R3-BCM -> eligibility -> R5-gate -> R6-eta
        # PERF: the R5 teaching signal depends ONLY on (nmod, activation, mean_activity, gains), all of
        # which are fixed for the whole plasticity loop (activation was replaced in step 1, mean_activity
        # updated in step 2, both BEFORE this loop). So neuromod_teaching(nmod) is constant across the ~265
        # connections that share a neuromodulator -- memoise it per step instead of recomputing per edge.
        # Byte-identical by construction: same function, same inputs, cached; verified on a fixed seed.
        _teach: Dict[str, float] = {}
        for j, k in enumerate(m.connections):
            if not self.live_conn[j] or self.pruned[j]:
                continue
            a_pre = new_a[k.source] * self._gain(k.source)       # throttle: weak pre-drive
            a_post = new_a[k.target]
            corr = P.bcm_term(a_pre, a_post, self.theta[k.target])
            self.eligibility[j] = P.decay_eligibility(self.eligibility[j], dt,
                                                      k.eligibility_tau_ms) + corr
            nmod = k.gating_neuromodulator
            mod = _teach.get(nmod)
            if mod is None:
                mod = _teach[nmod] = self.neuromod_teaching(nmod)  # R5: PHASIC teaching signal (once per nmod/step)
            # S10.1: experience-decreasing plasticity. The nth relevant EXPERIENCE (episode, not
            # step -- committed once per settle()) of this connection carries ~1/n weight
            # (running average), so the developed weight naturally rigidifies -- no separate
            # stabiliser. This step only FLAGS co-activity; settle() commits the experience.
            if a_pre > params.EXP_COACTIVE_THRESHOLD and a_post > params.EXP_COACTIVE_THRESHOLD:
                self._coactive_flag[j] = True
            n = self.exp_count[j]
            exp_factor = max(params.EXP_PLASTICITY_FLOOR, 1.0 / n) if n > 0 else 1.0
            dw = P.consolidate(self.eligibility[j], mod,
                               P.eta(k.schedule_ref, self.age_years)) * exp_factor   # R6 x 1/n
            w = P.clamp_weight(self.weight[j] + dw, k.bounds[0], k.bounds[1])   # R8 clamp
            thr = max(self.throttle.get(k.source, 0.0), self.throttle.get(k.target, 0.0))
            if thr > 0.0:                                          # plasticity ceiling (S4.1)
                w = min(w, k.bounds[1] * (1.0 - thr))
            self.weight[j] = w
            self._silent[j] = self._silent[j] + 1 if w < params.PRUNE_BELOW else 0

        # 4) R4-HOMEO (slow): scale incoming weights toward the firing-rate set-point
        if self._step_i % params.HOMEO_EVERY == 0:
            for cid, c in m.circuits.items():
                if not self.live_circuit[cid]:
                    continue
                f = P.homeo_factor(self.mean_activity[cid], c.homeostatic_setpoint)
                for j in m.incoming.get(cid, ()):
                    if self.live_conn[j] and not self.pruned[j]:
                        self.weight[j] = P.clamp_weight(self.weight[j] * f,
                                                        *m.connections[j].bounds)

        # 5) R8 competitive normalisation of incoming weights (slow clock)
        if params.NORMALISE and self._step_i % params.HOMEO_EVERY == 0:
            for cid in m.circuits:
                idxs = [j for j in m.incoming.get(cid, ())
                        if self.live_conn[j] and not self.pruned[j]]
                if len(idxs) > 1:
                    normed = P.normalise_incoming([self.weight[j] for j in idxs])
                    for j, w in zip(idxs, normed):
                        self.weight[j] = w

        # 6) R7-STRUCT (slow clock): prune long-silent weights (adding is a flagged extension)
        if self._step_i and self._step_i % params.STRUCT_EVERY == 0:
            for j in range(len(m.connections)):
                if not self.pruned[j] and self._silent[j] >= params.PRUNE_AFTER:
                    self.pruned[j] = True
                    self.weight[j] = 0.0

        self._step_i += 1

    def settle(self, ticks: int = 20, dt_ms: float = None) -> None:
        """Run several ticks as ONE lived experience/episode: connections co-active during it
        accrue one 'relevant experience' (S10.1), so plasticity decreases per episode, not per
        integration step."""
        self._coactive_flag = [False] * len(self.model.connections)
        for _ in range(ticks):
            self.step(dt_ms)
        for j, hot in enumerate(self._coactive_flag):
            if hot:
                self.exp_count[j] += 1

    # -- read-outs (measurement only) -------------------------------------
    def activity(self, circuit_id: str) -> float:
        return self.activation.get(circuit_id, 0.0)

    def snapshot(self) -> Dict[str, float]:
        return dict(self.activation)
