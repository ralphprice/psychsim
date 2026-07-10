import { describe, it, expect } from "vitest";
import { render, screen, within } from "@testing-library/react";
import { NeuralViewContent } from "./NeuralView";
import type { NeuralView as NeuralViewT } from "../types";
// U2/U3: the Neural tab must be structurally incapable of writing. Import the component's own source
// text (Vite ?raw) and assert no write path exists — not a convention, a fact about the code.
import src from "./NeuralView.tsx?raw";

const view: NeuralViewT = {
  meta: {
    version: "v9",
    title: "seed",
    n_circuits: 2,
    n_connections: 2,
    source_of_truth: "docs/neuralnetworks/psychsim_substrate_seed_v9.json",
  },
  circuits: [
    { id: "LA", name: "Lateral amygdala", domain: "defensive_threat", function: "fear learning", baseline: 0.05, tau_ms: 200, online_age: 0.3, sign: 1, confidence: "E", evidence_base: "human+animal", sources: "LeDoux 2000" },
    { id: "CeA", name: "Central amygdala", domain: "defensive_threat", function: "output", baseline: 0.05, tau_ms: 150, online_age: 0.3, sign: -1, confidence: "Em", evidence_base: "animal", sources: "Ref X" },
  ],
  connections: [
    { source: "LA", target: "CeA", weight0: 0.3, default_weight: "low", basis: "assumption", scaffold: true, gating_neuromodulator: "none", confidence: "E", citation: "assumption note", is_innate_reinforcer_link: false },
    { source: "sensory_thalamus", target: "LA", weight0: 0.4, default_weight: "moderate", basis: "anatomy", scaffold: false, gating_neuromodulator: "NA", confidence: "E", citation: "anatomy note", is_innate_reinforcer_link: false },
  ],
  domains: ["defensive_threat"],
  gaps: ["Default weights are assumptions until better-sourced."],
  read_only: true,
};

describe("NeuralView is structurally read-only (U2/U3)", () => {
  // strip comments — we assert about the CODE, not prose that merely mentions what is absent
  const code = src.replace(/\/\*[\s\S]*?\*\//g, "").replace(/\/\/.*$/gm, "");
  it("has no write path in its source — no write command, no sendCommand, no editable control", () => {
    expect(code).not.toMatch(/neural_upsert|neural_delete|matrix_upsert|matrix_delete/);
    expect(code).not.toMatch(/\bsendCommand\b/);
    expect(code).not.toMatch(/<textarea|<input/);
    // the only api it may import is the read getter
    expect(code).toMatch(/import\s*\{\s*getNeural\s*\}\s*from\s*"\.\.\/api"/);
  });
});

describe("NeuralView renders the seed as read-only provenance", () => {
  it("shows the single-source-of-truth banner with the seed version and counts", () => {
    render(<NeuralViewContent view={view} selectedId={null} onSelect={() => {}} />);
    expect(screen.getByText("READ-ONLY")).toBeInTheDocument();
    expect(screen.getByText(/single source of truth/)).toBeInTheDocument();
    expect(screen.getByText(/not this browser/)).toBeInTheDocument();
    expect(screen.getByText("v9")).toBeInTheDocument();
  });

  it("chips a placeholder-assumption weight SCAFFOLD but leaves an anatomy-based one unchipped", () => {
    render(<NeuralViewContent view={view} selectedId="LA" onSelect={() => {}} />);
    const detail = screen.getByRole("region", { name: "circuit detail" });
    // LA has one outgoing (assumption -> SCAFFOLD) and one incoming (anatomy -> not). Exactly one chip.
    expect(within(detail).getAllByText("SCAFFOLD")).toHaveLength(1);
    // sources render verbatim
    expect(within(detail).getByText("LeDoux 2000")).toBeInTheDocument();
  });

  it("offers no write affordance in the rendered output", () => {
    render(<NeuralViewContent view={view} selectedId="LA" onSelect={() => {}} />);
    expect(screen.queryByText(/^(Save|Save changes|Delete|Create|\+ New)/)).toBeNull();
  });
});
