// Palette + geometry shared across the views. Drive colours match the batch
// renderer (sim_viz.compositor.NETWORK_COLOUR) so the live and static views agree.

import type { Drive } from "./types";

export const DRIVE_COLOUR: Record<Drive, string> = {
  SEEKING: "#2E86C1",
  CARE: "#28B463",
  PLAY: "#F1C40F",
  LUST: "#E91E8C",
  FEAR: "#7F8C8D",
  RAGE: "#C0392B",
  PANIC: "#5D6D7E",
};

export function driveColour(d: string): string {
  return (DRIVE_COLOUR as Record<string, string>)[d] ?? "#888";
}

// Grid-view tinting (the fast top-down grid, not the plan view).
export const TERRAIN_COLOUR: Record<string, string> = {
  terrain_grass: "#b7d6a0",
  terrain_pavement: "#9a9a9a",
  terrain_park: "#8fbf7f",
};
export const BUILDING_COLOUR: Record<string, string> = {
  building_home: "#c98a5a",
  building_apartment: "#b0895f",
  building_school: "#5b6fa0",
  building_workplace: "#8a8a9a",
  building_shop: "#b0a060",
  building_market: "#a89a55",
  building_pub: "#a06a6a",
  building_cafe: "#bfa079",
  building_sports: "#7fae7f",
  building_institution: "#8f8fa2",
  building_hospital: "#c96a6a",
  building_clinic: "#cf9a9a",
  building_worship: "#9a86b8",
};

/** Cell size for the grid view (px per tile). The plan view carries its own. */
export const GRID_CELL = 26;

export const ROLE_EMOJI: Record<string, string> = {
  child: "🧒",
  adult: "🧑",
};
