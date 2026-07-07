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
        # dynamical state
        self.activation: Dict[str, float] = {cid: c.baseline for cid, c in m.circuits.items()}
        self.theta: Dict[str, float] = {cid: c.baseline for cid, c in m.circuits.items()}
        self.mean_activity: Dict[str, float] = {cid: c.baseline for cid, c in m.circuits.items()}
        self.weight: List[float] = [c.weight0 for c in m.connections]
        self.eligibility: List[float] = [0.0] * len(m.connections)
        self.external: Dict[str, float] = {}
        self.channel_drive: Dict[str, float] = {}
        self._silent: List[int] = [0] * len(m.connections)
        self.pruned: List[bool] = [False] * len(m.connections)
        self._step_i = 0
        self._refresh_live()

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

    # -- R5 modulator: a neuromodulator SOURCE CIRCUIT's live output ------
    def neuromod_output(self, nmod: str) -> float:
        """The R5 modulator scalar for a connection gated by `nmod`. It is the mean live
        activation of that neuromodulator's SOURCE CIRCUIT(S) -- a circuit output, never a
        value set from an outcome. 'none' (ungated) and unresolved sources -> 1.0."""
        if not nmod or nmod == "none":
            return 1.0
        srcs = self.model.neuromod_source.get(nmod, [])
        live = [self.activation[s] for s in srcs if self.live_circuit.get(s, False)]
        if not live:
            return 1.0                       # unresolved/offline source -> ungated (flagged)
        return sum(live) / len(live)

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
            # circuit -> circuit input, signed by the SOURCE nucleus's projection type
            for j in m.incoming.get(cid, ()):
                if self.live_conn[j] and not self.pruned[j]:
                    src = m.connections[j].source
                    inp += m.circuits[src].sign * self.weight[j] * a[src]
            # sensory input edges (channel -> circuit), driven when the channel is injected
            for e in m.incoming_channel.get(cid, ()):
                edge = m.input_edges[e]
                if edge.calibration_active and edge.online_age <= self.age_years:
                    inp += edge.weight0 * self._edge_drive(edge.channel)
            da = (dt / c.tau_ms) * (-(a[cid] - c.baseline) + inp)
            lo, hi = c.bounds
            new_a[cid] = P.clamp_weight(a[cid] + da, lo, hi)
        self.activation = new_a

        # 2) BCM threshold tracks each circuit's own recent activity
        for cid in m.circuits:
            if self.live_circuit[cid]:
                self.theta[cid] = P.update_theta(self.theta[cid], new_a[cid])
                self.mean_activity[cid] = 0.99 * self.mean_activity[cid] + 0.01 * new_a[cid]

        # 3) per-connection plasticity: R3-BCM -> eligibility -> R5-gate -> R6-eta
        for j, k in enumerate(m.connections):
            if not self.live_conn[j] or self.pruned[j]:
                continue
            a_pre, a_post = new_a[k.source], new_a[k.target]
            corr = P.bcm_term(a_pre, a_post, self.theta[k.target])
            self.eligibility[j] = P.decay_eligibility(self.eligibility[j], dt,
                                                      k.eligibility_tau_ms) + corr
            mod = self.neuromod_output(k.gating_neuromodulator)   # R5: circuit output
            dw = P.consolidate(self.eligibility[j], mod,
                               P.eta(k.schedule_ref, self.age_years))  # R6
            w = P.clamp_weight(self.weight[j] + dw, k.bounds[0], k.bounds[1])   # R8 clamp
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
        for _ in range(ticks):
            self.step(dt_ms)

    # -- read-outs (measurement only) -------------------------------------
    def activity(self, circuit_id: str) -> float:
        return self.activation.get(circuit_id, 0.0)

    def snapshot(self) -> Dict[str, float]:
        return dict(self.activation)
