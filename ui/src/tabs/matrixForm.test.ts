import { describe, it, expect } from "vitest";
import { isComplex, toBufferValue, initBuffer, coerceValue, buildItem, blankItem } from "./matrixForm";

describe("matrixForm helpers", () => {
  it("isComplex distinguishes objects/arrays from scalars", () => {
    expect(isComplex({})).toBe(true);
    expect(isComplex([])).toBe(true);
    expect(isComplex(0)).toBe(false);
    expect(isComplex("x")).toBe(false);
    expect(isComplex(null)).toBe(false);
  });

  it("toBufferValue stringifies scalars plainly and objects as JSON", () => {
    expect(toBufferValue(0.8)).toBe("0.8");
    expect(toBufferValue("parent")).toBe("parent");
    expect(toBufferValue(null)).toBe("");
    expect(toBufferValue({ a: 1 })).toBe(JSON.stringify({ a: 1 }, null, 2));
  });

  it("initBuffer covers exactly the field list", () => {
    const buf = initBuffer({ kind: "parent-child", power: 0.8, stimulus: { warmth: 1 } }, [
      "kind",
      "power",
      "stimulus",
    ]);
    expect(buf.kind).toBe("parent-child");
    expect(buf.power).toBe("0.8");
    expect(buf.stimulus).toContain("warmth");
  });

  it("coerceValue coerces back to the template's type", () => {
    expect(coerceValue("0.8", 0)).toBe(0.8); // number template
    expect(coerceValue("parent", "x")).toBe("parent"); // string template
    expect(coerceValue("true", false)).toBe(true); // boolean template
    expect(coerceValue('{"warmth":2}', {})).toEqual({ warmth: 2 }); // object template
  });

  it("coerceValue guards a non-numeric string against a number template", () => {
    expect(coerceValue("", 0)).toBe(0);
    expect(coerceValue("abc", 0)).toBe(0);
  });

  it("coerceValue throws on invalid JSON for a complex template (so save can surface it)", () => {
    expect(() => coerceValue("{not json}", {})).toThrow();
  });

  it("buildItem reconstructs a typed item from the buffer + a type template", () => {
    const template = { kind: "parent-child", higher: "parent", lower: "child", power: 0.8 };
    const buf = { kind: "mentor-mentee", higher: "mentor", lower: "mentee", power: "0.5" };
    expect(buildItem(buf, template, ["kind", "higher", "lower", "power"])).toEqual({
      kind: "mentor-mentee",
      higher: "mentor",
      lower: "mentee",
      power: 0.5, // coerced number, not the string "0.5"
    });
  });

  it("blankItem carries the example's types with blank values, id field a string", () => {
    const example = { id: "g1", name: "club", size: 12, stimulus: { warmth: 1 } };
    expect(blankItem(["id", "name", "size", "stimulus"], example, "id")).toEqual({
      id: "",
      name: "",
      size: 0,
      stimulus: {},
    });
  });

  it("blankItem falls back to empty strings when there is no example", () => {
    expect(blankItem(["kind", "power"], undefined, "kind")).toEqual({ kind: "", power: "" });
  });
});
