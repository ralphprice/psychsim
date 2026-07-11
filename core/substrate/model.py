"""
model.py (substrate) -- load the v13 substrate seed into a runtime model.

The v13 seed (docs/neuralnetworks/psychsim_substrate_seed_v13.json) is the SINGLE SOURCE OF
TRUTH for substrate structure and parameters (Part 2 S1.3; Part 3 S3): 82 circuits (nucleus-
level rate units), 206 directed edges, a 25-entry innate-wiring catalogue, 9 input channels
(IN-CONSPEC), a physical-endowment table, the 8 plasticity rules, and a gaps register. v13 =
v12 + the DRN (5-HT) NODE + missing local INHIBITORY INTERNEURONS (2.1b): (1) the dorsal raphe
with receptor-signed edges -- opposite signs across targets (DRN->VMHvl/CeA 5-HT1A INHIBITORY
dampens the attack area; DRN->OFC/vmPFC/dACC 5-HT2A EXCITATORY facilitates PFC control), the
top-down loop self-limiting through a DRN-GABA (GAD2+) interneuron, DRN->VTA (5-HT1A) inhibitory,
5-HT a gating source; low-5-HT -> more provoked aggression EMERGES (a scan_match target). (2) the
DRN-GABA raphe interneuron and the vmPFC-GABA / dlPFC-GABA cortical interneurons -- the missing
local feedback inhibition that holds saturating circuits at an E/I set-point (silence any and its
target runs hot: the proof it is anatomy, not a tuned weight). dmPFC was downstream-resolved (its
interneurons scheduled for a future systematic cortical-E/I pass). v12 = v11 + the sign-convention
upgrade (2.1a); v11 = v10 + 4 Allen afferents; v10 = v9 + physical endowment. Topology byte-identical
across versions (additions / sign-only); v1-v12 archived. This module
reads the seed verbatim into typed records + indices; it supplies NO dynamics (engine.py) and
NO psychological meaning (a circuit is just an id).

Two grounded, meaning-blind derivations the seed encodes implicitly:
  * Connection SIGN (v12a). Per-edge, sign = f(source transmitter, cited dominant target receptor):
    `_receptor_sign` derives it from the receptor's G-protein/ionotropic class (params.RECEPTOR_SIGN)
    where a `dominant_receptor` is cited; otherwise `_sign` falls back to the source nucleus's
    principal transmitter (classical ionotropic glutamate+/GABA- projections). The sign is a cited
    neurochemical fact at receptor resolution, never chosen to obtain a function.
  * Input EDGES. Some seed edges have an input CHANNEL as their source (e.g. IN-GUST:sweet ->
    a circuit) -- the sensory entry points. These are kept as input_edges, driven when the
    channel is injected. A few edges reference circuits absent from the index (connectome
    incompleteness -- flagged in the seed's own gaps_register): skipped with a warning.

The only code-side additions are the SCAFFOLD numeric mappings for the seed's QUALITATIVE
fields (default_weight "low"/"moderate"/...) -- params.py.
"""

from __future__ import annotations
import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from . import params

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# v9 is the canonical substrate seed (supersedes v8): v8 + the VMHvl hypothalamic-attack area
# and its provocation->attack pathway (IN-INTERO:provocation->VMHvl, VMHvl->PAG, VMHvl->HYPdm),
# which closes the OBS-3 connectome gap (provocation could previously reach the attack effectors
# only via the GABAergic CeA, which inhibits them); the CeA->PAG/HYPdm inhibition is UNTOUCHED.
# Plus the S1.4 social innate-wiring catalogue entries (documentary). v10 = v9 + IN-CONSPEC channel +
# 3 physical-endowment edges. v11 = v10 + 4 Allen-audit subcortical afferents added existence+direction
# only, weights SCAFFOLD, signs emergent from the source transmitter (MeA->VMHvl inhibitory, LH->LHb
# excitatory, VP->LHb inhibitory [sign-fidelity caveat in gaps_register], BNST->VMHvl excitatory);
# MeA->VMHvl / BNST->VMHvl give the v9 attack node its anatomical afferents beyond the abstract
# provocation channel, and LH/VP->LHb revive the previously afferent-less lateral habenula.
# v12 = v11 + the sign-convention upgrade (2.1a): per-edge receptor-derived signs; topology unchanged,
# 3 signs re-derived (MeA->VMHvl, VP->LHb, BNST->VMHvl). v13 = v12 + the DRN (5-HT) node + 3 cortical
# inhibitory interneurons (2.1b): 78->82 circuits, 186->206 directed edges. Each version additive or
# sign-only (prior topology byte-identical). v1-v12 archived.
_SEED_PATH = os.path.join(_ROOT, "docs", "neuralnetworks", "psychsim_substrate_seed_v13.json")

# Which SOURCE CIRCUIT produces each gating neuromodulator (R5). Resolved to real v7 circuit
# ids; the R5 modulator is that circuit's LIVE activity, never a set scalar. 'none' -> ungated.
NEUROMOD_SOURCE = {
    "NA": ["LC"], "DA": ["VTA", "SNc"], "ACh": ["BF-ACh"],
    "OT": ["PVN-OT"], "CRF": ["PVN", "BNST"],
    "5HT": ["DRN"],   # v12b: the serotonergic source (registered so 5-HT is available as an R5 gate;
    #                   the DRN direct projections are the mechanism -- no connection is 5HT-gated yet).
}


def _num_weight(qual) -> float:
    if isinstance(qual, (int, float)):
        return float(qual)
    return params.WEIGHT_QUALITATIVE.get(str(qual).strip().lower(), params.DEFAULT_WEIGHT)


def _sign(transmitters: str) -> float:
    """+1 excitatory / -1 inhibitory, from the nucleus's PRINCIPAL neurotransmitter. A leading
    'GABA...' is a GABAergic projection nucleus (inhibitory). Neurochemistry, not meaning. This is the
    FALLBACK sign (v12a): used only for a connection with no cited `dominant_receptor` -- i.e. classical
    ionotropic glutamate(+)/GABA(-) projections, where transmitter implies the receptor."""
    return -1.0 if (transmitters or "").strip().lower().startswith("gaba") else 1.0


def _receptor_sign(receptor) -> Optional[float]:
    """v12a -- a connection's sign DERIVED from its cited dominant target receptor's G-protein/ionotropic
    class (params.RECEPTOR_SIGN): the honest, finer-resolution rule (sign = f(transmitter, target
    receptor)). Parses the leading receptor token (so 'D1 (Gs, direct MSN)' -> 'D1'). Returns None for a
    missing/unknown receptor, so the caller falls back to the source's principal-transmitter sign."""
    if not receptor:
        return None
    key = str(receptor).replace("/", " ").split("(")[0].split()[0].strip() if str(receptor).strip() else ""
    v = params.RECEPTOR_SIGN.get(key)
    return None if v is None else float(v)


def _tuple2(x, default=(0.0, 1.0)) -> Tuple[float, float]:
    if isinstance(x, (list, tuple)) and len(x) == 2:
        return (float(x[0]), float(x[1]))
    return default


@dataclass
class Circuit:
    id: str
    domain: str = ""
    baseline: float = 0.05
    bounds: Tuple[float, float] = (0.0, 1.0)
    tau_ms: float = 100.0
    homeostatic_setpoint: float = 0.1
    online_age: float = 0.0
    schedule_ref: str = ""
    calibration_active: bool = True
    sign: float = 1.0                 # +1 excitatory / -1 inhibitory (from transmitters)
    name: str = ""                    # descriptive only; never read by the dynamics


@dataclass
class Connection:
    source: str                       # a circuit id
    target: str                       # a circuit id
    weight0: float = 0.3
    bounds: Tuple[float, float] = (0.0, 1.0)
    gating_neuromodulator: str = "none"
    eligibility_tau_ms: float = 1000.0
    schedule_ref: str = ""
    online_age: float = 0.0
    calibration_active: bool = True
    is_innate_reinforcer_link: bool = False
    sign: float = 1.0                 # +1 excit / -1 inhib. v12a: from the cited dominant_receptor
    #                                   (params.RECEPTOR_SIGN); falls back to the source transmitter.
    dominant_receptor: str = ""       # cited postsynaptic receptor (only where receptor-determined)


@dataclass
class InputEdge:
    """A sensory entry edge: an input CHANNEL drives a target circuit."""
    channel: str                      # e.g. "IN-GUST:sweet" or "IN-VIS"
    target: str
    weight0: float = 0.5
    online_age: float = 0.0
    calibration_active: bool = True


@dataclass
class SubstrateModel:
    circuits: Dict[str, Circuit]
    connections: List[Connection]
    input_edges: List[InputEdge]
    innate_wiring: List[dict]
    input_channels: List[dict]
    physical_endowment: List[dict]
    plasticity_rules: List[dict]
    gaps_register: List
    meta: dict = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    incoming: Dict[str, List[int]] = field(default_factory=dict)          # target -> [conn idx]
    incoming_channel: Dict[str, List[int]] = field(default_factory=dict)  # target -> [input_edge idx]
    neuromod_source: Dict[str, List[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.incoming = {}
        for i, c in enumerate(self.connections):
            self.incoming.setdefault(c.target, []).append(i)
        self.incoming_channel = {}
        for i, e in enumerate(self.input_edges):
            self.incoming_channel.setdefault(e.target, []).append(i)
        self.neuromod_source = {}
        needed = {c.gating_neuromodulator for c in self.connections} - {"none", None}
        for nmod in sorted(needed):
            srcs = [cid for cid in NEUROMOD_SOURCE.get(nmod, []) if cid in self.circuits]
            self.neuromod_source[nmod] = srcs
            if not srcs:
                self.warnings.append(
                    f"gating neuromodulator '{nmod}' has no source circuit in v7; its gated "
                    f"connections are treated as ungated (flagged, never a set scalar).")


def load_substrate(path: Optional[str] = None) -> SubstrateModel:
    """Load v7 into a SubstrateModel. Never raises on soft data issues -- they are warnings."""
    with open(path or _SEED_PATH, "r", encoding="utf-8") as fh:
        d = json.load(fh)

    circuits: Dict[str, Circuit] = {}
    for c in d.get("circuits", []):
        circuits[c["id"]] = Circuit(
            id=c["id"], domain=c.get("domain", ""), name=c.get("name", ""),
            baseline=float(c.get("baseline_activation", 0.05)),
            bounds=_tuple2(c.get("activation_bounds")),
            tau_ms=float(c.get("time_constant_tau_ms", 100.0)),
            homeostatic_setpoint=float(c.get("homeostatic_setpoint", 0.1)),
            online_age=float(c.get("developmental_online_age", 0.0) or 0.0),
            schedule_ref=c.get("plasticity_coeff_schedule_ref", ""),
            calibration_active=bool(c.get("calibration_active_default", True)),
            sign=_sign(c.get("transmitters", "")),
        )

    channel_ids = {ch.get("id") for ch in d.get("input_channels", [])}

    def is_channel(src: str) -> bool:
        return src.startswith("IN-") or src.split(":")[0] in channel_ids

    connections: List[Connection] = []
    input_edges: List[InputEdge] = []
    warnings: List[str] = []
    for k in d.get("connections", []):
        src, tgt = k.get("source_circuit"), k.get("target_circuit")
        if tgt not in circuits:
            warnings.append(f"edge {src}->{tgt}: unknown target circuit (connectome gap); skipped.")
            continue
        w0 = _num_weight(k.get("default_weight", "moderate"))
        online = float(k.get("developmental_online_age", 0.0) or 0.0)
        active = bool(k.get("calibration_active_default", True))
        if src in circuits:
            # v12a: sign from the cited dominant target receptor (finer resolution); if none is cited,
            # fall back to the source nucleus's principal-transmitter sign (classical ionotropic edges).
            recv = k.get("dominant_receptor", "") or ""
            rsign = _receptor_sign(recv)
            sign = rsign if rsign is not None else circuits[src].sign
            connections.append(Connection(
                source=src, target=tgt, weight0=w0, bounds=_tuple2(k.get("weight_bounds")),
                gating_neuromodulator=str(k.get("gating_neuromodulator", "none") or "none"),
                eligibility_tau_ms=float(k.get("eligibility_trace_tau_ms", 1000.0) or 1000.0),
                schedule_ref=k.get("plasticity_coeff_schedule_ref", ""),
                online_age=online, calibration_active=active,
                sign=sign, dominant_receptor=str(recv),
                is_innate_reinforcer_link=bool(k.get("is_innate_reinforcer_link", False))))
        elif is_channel(src):
            input_edges.append(InputEdge(channel=src, target=tgt, weight0=w0,
                                         online_age=online, calibration_active=active))
        else:
            warnings.append(f"edge {src}->{tgt}: unknown source circuit (connectome gap); skipped.")

    return SubstrateModel(
        circuits=circuits, connections=connections, input_edges=input_edges,
        innate_wiring=list(d.get("innate_wiring_catalogue", [])),
        input_channels=list(d.get("input_channels", [])),
        physical_endowment=list(d.get("physical_endowment", [])),
        plasticity_rules=list(d.get("plasticity_rules", [])),
        gaps_register=list(d.get("gaps_register", [])),
        meta=d.get("meta", {}), warnings=warnings)
