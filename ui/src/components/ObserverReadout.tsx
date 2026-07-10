// ObserverReadout — renders the observer's read-out VERBATIM (constraint U4). It walks whatever
// key→value tree the observer emits and shows it EXACTLY as named: keys are printed as-is (no Title
// Casing, no abbreviation expansion, no key remapping), numbers are shown as numbers (never bucketed
// into High/Moderate/Low, never colour-coded good/bad), and object keys keep the observer's own
// order (never re-sorted by magnitude, which would read as a ranking). If a label is unreadable,
// that is a signal to fix the OBSERVER's naming, not to prettify it here.
//
// The renderer is deliberately schema-agnostic: it must not know WHICH keys the observer emits. It
// renders the tree it is given, which is what keeps it honest as the observer's output evolves — and
// is why neither this component nor its test names any specific construct.

function formatNumber(n: number): string {
  if (Number.isInteger(n)) return String(n);
  // show the number at a legible precision — a display choice, not a classification
  return n.toFixed(3);
}

function ReadoutValue({ value }: { value: unknown }) {
  if (value === null || value === undefined) return <span className="ro-null">—</span>;
  if (typeof value === "number") return <span className="ro-num">{formatNumber(value)}</span>;
  if (typeof value === "boolean" || typeof value === "string")
    return <span className="ro-scalar">{String(value)}</span>;
  if (Array.isArray(value)) {
    return (
      <span className="ro-array">
        {value.map((v, i) => (
          <ReadoutValue key={i} value={v} />
        ))}
      </span>
    );
  }
  // object: render each key in the observer's own order (Object.entries preserves insertion order)
  return (
    <div className="ro-group">
      {Object.entries(value as Record<string, unknown>).map(([k, v]) => (
        <div className="ro-row" key={k}>
          <span className="ro-key">{k}</span>
          <ReadoutValue value={v} />
        </div>
      ))}
    </div>
  );
}

export function ObserverReadout({ data }: { data: unknown }) {
  if (data === null || data === undefined) return <div className="ro-empty">no read-out</div>;
  return <ReadoutValue value={data} />;
}
