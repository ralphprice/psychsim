import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { ObserverReadout } from "./ObserverReadout";

// U4 with teeth at the component level: the read-out must appear EXACTLY as the observer names it —
// verbatim keys, raw numbers, no invented buckets, and the observer's own key order preserved.
// SYNTHETIC keys are used on purpose: the renderer is schema-agnostic, so its test must not embed
// (and must not depend on) the observer's actual construct names. `solo_index` is the largest value
// but not first, so it doubles as the magnitude-vs-emitted-order check.
describe("ObserverReadout (U4: verbatim)", () => {
  const observer = {
    group_one: { alpha_score: 0.7074, beta_score: 0.5462, gamma_score: 0.68 },
    solo_index: 0.8969,
    low_measure: 0.103,
    pair_metric: { first_part: 0.2, second_part: 0.0 },
  };

  it("renders the observer's keys verbatim (no Title Case, no expansion, no remap)", () => {
    render(<ObserverReadout data={observer} />);
    for (const key of ["group_one", "solo_index", "low_measure", "pair_metric", "alpha_score", "beta_score", "gamma_score", "first_part", "second_part"]) {
      expect(screen.getByText(key)).toBeInTheDocument();
    }
    // the UI must NOT prettify snake_case into Title Case, nor bucket a number
    expect(screen.queryByText(/Group One|Alpha Score/)).toBeNull();
    expect(screen.queryByText(/^(High|Moderate|Low)$/)).toBeNull();
  });

  it("shows numbers as numbers, not classified into buckets", () => {
    render(<ObserverReadout data={observer} />);
    expect(screen.getByText("0.897")).toBeInTheDocument(); // solo_index, rounded — still a number
    expect(screen.getByText("0")).toBeInTheDocument(); // second_part 0.0
  });

  it("preserves the observer's own key order (never re-sorts by magnitude)", () => {
    const { container } = render(<ObserverReadout data={observer} />);
    const keys = Array.from(container.querySelectorAll(".ro-key")).map((e) => e.textContent);
    const top = keys.filter((k) => ["group_one", "solo_index", "low_measure", "pair_metric"].includes(k ?? ""));
    expect(top).toEqual(["group_one", "solo_index", "low_measure", "pair_metric"]);
    // NOT magnitude order (which would put solo_index, the largest value, first)
    expect(top[0]).not.toBe("solo_index");
  });

  it("handles an empty / missing read-out without inventing content", () => {
    render(<ObserverReadout data={undefined} />);
    expect(screen.getByText("no read-out")).toBeInTheDocument();
  });
});
