import { describe, it, expect } from "vitest";
import { filterItems, moveSelection } from "./masterDetailModel";

interface Row {
  id: string;
  name: string;
}
const rows: Row[] = [
  { id: "a", name: "Alice" },
  { id: "b", name: "Bob" },
  { id: "c", name: "Carol" },
];
const text = (r: Row) => r.name;
const ids = rows.map((r) => r.id);

describe("filterItems", () => {
  it("returns all items for an empty/whitespace query", () => {
    expect(filterItems(rows, text, "")).toHaveLength(3);
    expect(filterItems(rows, text, "   ")).toHaveLength(3);
  });
  it("matches case-insensitively on a substring", () => {
    expect(filterItems(rows, text, "car").map((r) => r.id)).toEqual(["c"]);
    expect(filterItems(rows, text, "O").map((r) => r.id)).toEqual(["b", "c"]); // bOb, carOl
  });
  it("returns an empty list when nothing matches", () => {
    expect(filterItems(rows, text, "zzz")).toEqual([]);
  });
});

describe("moveSelection", () => {
  it("moves down and up by one, clamping at the ends (no wrap)", () => {
    expect(moveSelection(ids, "a", 1)).toBe("b");
    expect(moveSelection(ids, "b", -1)).toBe("a");
    expect(moveSelection(ids, "c", 1)).toBe("c"); // clamp at bottom
    expect(moveSelection(ids, "a", -1)).toBe("a"); // clamp at top
  });
  it("lands on the first (down) or last (up) row when nothing is selected", () => {
    expect(moveSelection(ids, null, 1)).toBe("a");
    expect(moveSelection(ids, null, -1)).toBe("c");
  });
  it("lands on an end when the current selection is not in the list (filtered out)", () => {
    expect(moveSelection(ids, "gone", 1)).toBe("a");
    expect(moveSelection(ids, "gone", -1)).toBe("c");
  });
  it("returns null for an empty list", () => {
    expect(moveSelection([], "a", 1)).toBeNull();
    expect(moveSelection([], null, -1)).toBeNull();
  });
});
