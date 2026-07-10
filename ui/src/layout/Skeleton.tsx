// SkeletonList — placeholder bars shown while a panel's data loads, instead of a bare "Loading…".
// role=status + aria-label announces the load to a screen reader; the bars themselves are decorative.
// The shimmer is disabled by the global prefers-reduced-motion rule.

const WIDTHS = ["w80", "w60", "w40", "w80", "w60", "w40"] as const;

export function SkeletonList({ rows = 5, label = "Loading" }: { rows?: number; label?: string }) {
  return (
    <div className="skeleton-list" role="status" aria-label={label} aria-busy="true">
      {Array.from({ length: rows }, (_, i) => (
        <div key={i} className={`skeleton skeleton-row ${WIDTHS[i % WIDTHS.length]}`} aria-hidden="true" />
      ))}
    </div>
  );
}
