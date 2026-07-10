// Pure helpers for MatrixTab's per-field editor. The matrix metadata gives field NAMES but not
// TYPES, so we infer each field's type from an example value (an existing item of the same kind, or
// the item being edited) and coerce the string edit-buffer back to that type on save. Kept pure (no
// React) so the coercion — the part that silently corrupts data if wrong — is unit-testable alone.

export type Buffer = Record<string, string>;
export type Item = Record<string, unknown>;

/** Values that need a JSON textarea rather than a plain input. */
export function isComplex(v: unknown): boolean {
  return typeof v === "object" && v !== null;
}

/** Stringify one field value for the edit buffer (pretty JSON for objects, String otherwise). */
export function toBufferValue(v: unknown): string {
  if (isComplex(v)) return JSON.stringify(v, null, 2);
  return v === undefined || v === null ? "" : String(v);
}

/** Build the edit buffer for an item over the given field list. */
export function initBuffer(item: Item, fields: string[]): Buffer {
  const b: Buffer = {};
  for (const f of fields) b[f] = toBufferValue(item[f]);
  return b;
}

/** Coerce a buffer string back to the type of `template` (the current/example value). Throws on
 *  invalid JSON for a complex template so the caller can surface an error rather than save garbage. */
export function coerceValue(raw: string, template: unknown): unknown {
  if (isComplex(template)) return JSON.parse(raw); // object / array
  if (typeof template === "number") {
    const n = Number(raw);
    return Number.isNaN(n) ? 0 : n;
  }
  if (typeof template === "boolean") return raw === "true";
  return raw; // string (also the default when the template field is absent)
}

/** Reconstruct a typed item from the buffer, taking per-field types from `template`. */
export function buildItem(buf: Buffer, template: Item, fields: string[]): Item {
  const out: Item = {};
  for (const f of fields) out[f] = coerceValue(buf[f] ?? "", template[f]);
  return out;
}

/** A blank item for the "+ New" form: blank values carrying the right JS types (inferred from an
 *  example item of the same kind, when there is one), with the id field always a string. */
export function blankItem(fields: string[], example: Item | undefined, idField: string): Item {
  const out: Item = {};
  for (const f of fields) {
    const t = example?.[f];
    if (isComplex(t)) out[f] = Array.isArray(t) ? [] : {};
    else if (typeof t === "number") out[f] = 0;
    else if (typeof t === "boolean") out[f] = false;
    else out[f] = "";
  }
  out[idField] = "";
  return out;
}
