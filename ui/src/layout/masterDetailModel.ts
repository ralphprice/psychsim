// Pure selection/filter logic for the MasterDetail primitive — no React, no DOM, so the tricky
// bits (clamping, filter-then-navigate consistency) are unit-testable in isolation. The component
// is a thin shell over these functions.

/** Case-insensitive substring filter on a precomputed text key. Empty query returns all. */
export function filterItems<T>(items: T[], getText: (item: T) => string, query: string): T[] {
  const q = query.trim().toLowerCase();
  if (!q) return items;
  return items.filter((it) => getText(it).toLowerCase().includes(q));
}

/**
 * Move selection within an ordered list of ids by `delta` (+1 down, -1 up), CLAMPING at the ends
 * (no wrap — predictable for keyboard users). If nothing is selected, or the current selection has
 * been filtered out of `ids`, land on the first row (moving down) or the last (moving up). Returns
 * null only for an empty list.
 */
export function moveSelection(ids: string[], current: string | null, delta: number): string | null {
  if (ids.length === 0) return null;
  const i = current ? ids.indexOf(current) : -1;
  if (i === -1) return delta >= 0 ? ids[0] : ids[ids.length - 1];
  const next = Math.min(Math.max(i + delta, 0), ids.length - 1);
  return ids[next];
}
