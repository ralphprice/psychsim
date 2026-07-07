// Headless render smoke test: bundle an SSR entry with esbuild and render every
// component through react-dom/server with mock data. No browser needed — it proves
// the component tree, imports, and render paths execute without throwing (the thing
// typecheck + bundle can't catch). It does NOT exercise effects (fetch, rAF), which
// only run in a real browser.

import { build } from "esbuild";
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const uiRoot = join(here, "..");

const ENTRY = `
import { renderToStaticMarkup } from "react-dom/server";
import { GridBackground } from "./src/components/GridBackground";
import { PlanBackground } from "./src/components/PlanBackground";
import { PeopleLayer } from "./src/components/PeopleLayer";
import { Inspector } from "./src/components/Inspector";
import { Controls } from "./src/components/Controls";
import { Legend } from "./src/components/Legend";
import { Development } from "./src/components/Development";
import { MatrixEditor } from "./src/components/MatrixEditor";
import { NeuralEditor } from "./src/components/NeuralEditor";
import { ExecutiveEditor } from "./src/components/ExecutiveEditor";
import { Stage } from "./src/components/Stage";
import App from "./src/App";
import { gridViewModel, planViewModel } from "./src/view";
import React from "react";

const town = {
  cols: 4, rows: 4,
  terrain: Array.from({ length: 4 }, () => Array(4).fill("terrain_grass")),
  roads: [[0, 0]],
  buildings: [{ place: "home_1", kind: "building_home", x: 1, y: 1, w: 1, h: 1 }],
  props: [{ kind: "prop_tree", x: 2, y: 2 }],
};
const plan = {
  svg: "<svg width='296' height='296'><rect width='296' height='296' fill='#eee'/></svg>",
  cell: 64, pad: 20, cols: 4, rows: 4, width: 296, height: 296,
};
const people = {
  p1: { x: 1, y: 1, drive: "SEEKING", role: "child", role_name: "teenager", subject: true },
  p2: { x: 2, y: 2, drive: "CARE", role: "adult", role_name: "retired", subject: false },
};
const state = {
  clock: "Mon 08:00", minutes: 480, step: 32, experiment: true, subjects: 1,
  background: 1, people, playing: true, interval: 0.25,
};
const detail = {
  cid: "p1", name: "p1", role: "child", home: "home_1", work: null,
  subject: true, mind_state: "study subject (live)", temperament: "fearless",
  systems: { SEEKING: [0.4, 0.5], CARE: [0.2, 0.3], PLAY: [0.1, 0.4], LUST: [0, 0.2],
             FEAR: [0.3, 0.6], RAGE: [0.1, 0.2], PANIC: [0.05, 0.3] },
  memories: [{ label: "with 2 others at Yard", valence: 0.2 }, { label: "class", valence: -0.1 }],
  groups: [{ group: "Yard", standing: 0.3, belonging: 0.5, route: "prestige" }],
};
const stageRef = { current: null };
const noop = () => {};
const acmd = async () => ({ ok: true });

const cases = {
  App: React.createElement(App),
  Legend: React.createElement(Legend),
  Development: React.createElement(Development, { selectedCid: null }),
  MatrixEditor: React.createElement(MatrixEditor),
  NeuralEditor: React.createElement(NeuralEditor),
  ExecutiveEditor: React.createElement(ExecutiveEditor),
  GridBackground: React.createElement(GridBackground, { town }),
  PlanBackground: React.createElement(PlanBackground, { plan }),
  PeopleLayerGrid: React.createElement(PeopleLayer, {
    people, view: gridViewModel(town), selectedCid: "p1", followCid: "p1",
    showLabels: true, stage: stageRef,
  }),
  PeopleLayerPlan: React.createElement(PeopleLayer, {
    people, view: planViewModel(plan), selectedCid: null, followCid: null,
    showLabels: false, stage: stageRef,
  }),
  StageWithChildren: React.createElement(Stage, { W: 296, H: 296, onPick: noop }, null),
  Inspector: React.createElement(Inspector, { p: detail }),
  Controls: React.createElement(Controls, {
    state,
    saves: [
      { name: "run A", slug: "run_a", clock: "Wed 09:00", minutes: 3060, step: 204,
        residents: 22, population: 30, seed: 7, saved_at: 1, saved_label: "2026-07-06 12:00" },
    ],
    error: null, mode: "plan", onMode: noop, labels: true, onLabels: noop,
    follow: false, onFollow: noop, hasSelection: true, command: acmd,
  }),
};

let total = 0;
for (const [name, el] of Object.entries(cases)) {
  const html = renderToStaticMarkup(el);
  if (typeof html !== "string" || html.length === 0) throw new Error(name + " rendered empty");
  total += html.length;
  console.log("  ok  " + name + "  (" + html.length + " chars)");
}
console.log("SMOKE OK — " + Object.keys(cases).length + " render cases, " + total + " chars total");
`;

// output inside the ui dir so Node resolves react/react-dom from ./node_modules
const out = join(uiRoot, ".smoke-bundle.mjs");

await build({
  stdin: { contents: ENTRY, resolveDir: uiRoot, loader: "tsx", sourcefile: "smoke-entry.tsx" },
  bundle: true,
  format: "esm",
  platform: "node",
  jsx: "automatic",
  outfile: out,
  external: ["react", "react/*", "react-dom", "react-dom/*"],
  logLevel: "warning",
});

await import(pathToFileURL(out).href);
