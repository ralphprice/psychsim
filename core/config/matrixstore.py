"""
matrixstore.py -- generic view/add/edit/delete over the three interface matrices'
DEFINITION sets, persisted as data files. The runtime *traces* (a person's Memberships,
Bonds, Ties) are emergent and read-only; what a researcher curates is the definitions:
the Groups that exist, the Things the world contains, the social role-pairs.

CRUD operates on the JSON data files directly (as dicts), so this imports no matrix
module (no cycle). Edits take effect on the next spawn/respawn for groups and things;
social role-pairs are import-cached, so they take effect on a server restart.
"""

from __future__ import annotations
import json
import os
from typing import Dict, List

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _d(*p):
    return os.path.join(_ROOT, "data", *p)


# each matrix kind: its canonical editable file, the list key inside it, the id field,
# and the editable fields (for a generic editor UI).
MATRIX_SPECS: Dict[str, dict] = {
    "environment": {"path": _d("things", "childhood.json"), "list_key": "things",
                    "id_field": "id", "label": "environment (things)",
                    "fields": ["id", "name", "kind", "stimulus", "inherited_aversion",
                               "inherited_attraction", "frequency"]},
    "group": {"path": _d("groups", "groups.json"), "list_key": "groups",
              "id_field": "id", "label": "groups",
              "fields": ["id", "name", "kind", "size", "cohesion", "status", "norm_strength"]},
    "social": {"path": _d("social", "ties.json"), "list_key": "ties",
               "id_field": "kind", "label": "social (role-pairs)",
               "fields": ["kind", "higher", "lower", "power"]},
}


def _read(spec):
    if not os.path.isfile(spec["path"]):
        return {}, []
    with open(spec["path"]) as f:
        doc = json.load(f)
    if isinstance(doc, list):
        return {}, list(doc)
    return doc, list(doc.get(spec["list_key"], []))


def _write(spec, doc, items):
    doc = dict(doc)
    doc[spec["list_key"]] = items
    os.makedirs(os.path.dirname(spec["path"]), exist_ok=True)
    with open(spec["path"], "w") as f:
        json.dump(doc, f, indent=2)


def kinds() -> Dict[str, dict]:
    """Metadata for each matrix kind (label, editable fields, id field)."""
    return {k: {"label": v["label"], "fields": v["fields"], "id_field": v["id_field"]}
            for k, v in MATRIX_SPECS.items()}


def list_items(kind: str) -> List[dict]:
    return _read(MATRIX_SPECS[kind])[1]


def upsert_item(kind: str, item: dict) -> dict:
    """Add a new definition item, or update an existing one by its id field."""
    spec = MATRIX_SPECS[kind]
    idf = spec["id_field"]
    if not str(item.get(idf, "")).strip():
        raise ValueError(f"item is missing its id field '{idf}'")
    doc, items = _read(spec)
    for i, it in enumerate(items):
        if it.get(idf) == item[idf]:
            items[i] = {**it, **item}
            _write(spec, doc, items)
            return items[i]
    items.append(item)
    _write(spec, doc, items)
    return item


def delete_item(kind: str, item_id: str) -> bool:
    """Remove a definition item by id. True if something was removed."""
    spec = MATRIX_SPECS[kind]
    idf = spec["id_field"]
    doc, items = _read(spec)
    kept = [it for it in items if it.get(idf) != item_id]
    _write(spec, doc, kept)
    return len(kept) < len(items)
