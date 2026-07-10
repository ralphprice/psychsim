"""
view.py -- a READ-ONLY view of the live substrate seed for the Neural tab (UI redesign Phase 6).

The seed is the single source of truth. This view reads the STRUCTURE through load_substrate() -- the
exact loader the engine uses -- so the circuit / connection counts the UI shows cannot diverge from
the running substrate. Provenance (sources, confidence, default-weight basis) is read from the SAME
seed file, verbatim; a weight whose basis is a bare 'assumption' is flagged scaffold, so a placeholder
is never mistaken for a measured constant. There is NO write path here: this module only reads.
"""
from __future__ import annotations

import json
import os
from typing import Optional

from .model import load_substrate, _SEED_PATH, _ROOT


def _raw_seed(path: Optional[str] = None) -> dict:
    with open(path or _SEED_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def substrate_view(path: Optional[str] = None) -> dict:
    """Serialise the live seed for the UI. Structure comes via load_substrate() (== the engine);
    provenance comes from the same seed file. Read-only -- never writes, never develops an agent."""
    model = load_substrate(path)
    raw = _raw_seed(path)
    raw_circuits = {c["id"]: c for c in raw.get("circuits", [])}
    raw_conns = {
        (k.get("source_circuit"), k.get("target_circuit")): k for k in raw.get("connections", [])
    }

    circuits = []
    for cid, c in model.circuits.items():
        rc = raw_circuits.get(cid, {})
        circuits.append({
            "id": cid,
            "name": c.name,
            "domain": c.domain,
            "function": rc.get("function", ""),
            "baseline": round(c.baseline, 4),
            "tau_ms": c.tau_ms,
            "online_age": c.online_age,
            "sign": c.sign,
            "confidence": rc.get("confidence"),
            "evidence_base": rc.get("evidence_base"),
            "sources": rc.get("sources"),
        })

    connections = []
    for k in model.connections:
        rc = raw_conns.get((k.source, k.target), {})
        basis = rc.get("default_weight_basis")
        connections.append({
            "source": k.source,
            "target": k.target,
            "weight0": round(k.weight0, 4),
            "default_weight": rc.get("default_weight"),
            "basis": basis,
            # a bare assumption is a placeholder weight, not a measured constant -> SCAFFOLD in the UI
            "scaffold": basis == "assumption",
            "gating_neuromodulator": k.gating_neuromodulator,
            "confidence": rc.get("confidence"),
            "citation": rc.get("source"),  # the seed's per-connection provenance note
            "is_innate_reinforcer_link": k.is_innate_reinforcer_link,
        })

    return {
        "meta": {
            "version": model.meta.get("version"),
            "title": model.meta.get("title"),
            "n_circuits": len(model.circuits),
            "n_connections": len(model.connections),
            "source_of_truth": os.path.relpath(_SEED_PATH, _ROOT),
        },
        "circuits": circuits,
        "connections": connections,
        "domains": sorted({c.domain for c in model.circuits.values() if c.domain}),
        "gaps": list(raw.get("gaps_register", [])),
        "read_only": True,
    }
