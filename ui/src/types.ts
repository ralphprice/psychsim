// Typed mirrors of the psychsim_server.py JSON payloads.
// Keep these in sync with SimEngine.town()/plan()/snapshot()/person_detail().

/** The 7 Pankseppian primary systems, in canonical order. */
export const DRIVES = [
  "SEEKING",
  "CARE",
  "PLAY",
  "LUST",
  "FEAR",
  "RAGE",
  "PANIC",
] as const;
export type Drive = (typeof DRIVES)[number];

/** GET /town — static grid geometry, drawn once. */
export interface TownGeometry {
  cols: number;
  rows: number;
  terrain: string[][];
  roads: [number, number][];
  buildings: TownBuilding[];
  props: TownProp[];
}
export interface TownBuilding {
  place: string;
  kind: string; // e.g. "building_home"
  x: number;
  y: number;
  w: number;
  h: number;
}
export interface TownProp {
  kind: string;
  x: number;
  y: number;
}

/** GET /plan — the designed "glass-roof" plan view as an SVG string + mapping. */
export interface PlanView {
  svg: string;
  cell: number;
  pad: number;
  cols: number;
  rows: number;
  width: number;
  height: number;
}

/** GET /state — live per-person positions + drive, plus the clock. */
export interface SimState {
  clock: string;
  minutes: number;
  step: number;
  /** controlled-experiment mode: fixed grown-adult background + live study subjects */
  experiment: boolean;
  subjects: number;
  background: number;
  people: Record<string, PersonLive>;
  playing: boolean;
  interval: number;
  /** telemetry (for the console strip): the sim seed and the substrate seed version. */
  seed?: number;
  version?: string;
}
export interface PersonLive {
  x: number;
  y: number;
  drive: string; // a Drive, or "" before it settles
  role: "child" | "adult";
  role_name?: string | null; // fine role (child/teenager/retired/...)
  /** true = evolves live (study subject); false = fixed grown background */
  subject: boolean;
}

/** GET /person?cid= — full inspectable state for one resident. */
export interface PersonDetail {
  cid: string;
  name: string;
  role: "child" | "adult";
  role_name?: string | null;
  home: string | null;
  work: string | null;
  subject: boolean;
  mind_state: string; // "study subject (live)" | "background (fixed)"
  temperament: string | null; // set for authored subjects (given inherited reactivity)
  /** substrate domain -> normalised activity share under a neutral probe (values sum to ~1) */
  systems: Record<string, number>;
  memories: MemoryEvent[];
  groups: GroupStanding[];
}

/** GET /library — the grown-adult library available as fixed background. */
export interface LibraryInfo {
  count: number;
  adults: { name: string; temperament: string; rearing: string; dominant: string }[];
}

/** GET /modules — the plug-in research modules discovered under extensions/. */
export interface ModuleInfo {
  name: string;
  title: string;
  description: string;
  params: Record<string, unknown>;
  hooks: string[];
}

/** GET /report/cohort — a descriptive cohort development report. */
export interface CohortReport {
  n: number;
  distribution: Record<string, number>; // emergent dominant system -> count
  mean_profile: Record<string, number>;
  axis_mean: number;
  axis_stdev: number;
  caveat: string;
}

/** GET /report/subject — one subject's development trajectory (descriptive). */
export interface SubjectReport {
  cid: string;
  temperament: string | null;
  home: string | null;
  trajectory: { step: number; clock: string; dominant: string; axis: number }[];
  /** The observer's per-subject read-out, exactly as it names it. Deliberately loose (an opaque
   *  key→value tree): the UI must render it VERBATIM (U4), never hard-code the observer's schema. */
  observer?: Record<string, unknown>;
  caveat: string;
}
export interface MemoryEvent {
  label: string;
  valence: number;
}
export interface GroupStanding {
  group: string;
  standing: number;
  belonging: number;
  route: string;
}

/** GET /saves — metadata for saved simulations on disk. */
export interface SaveMeta {
  name: string;
  slug: string;
  clock: string;
  minutes: number;
  step: number;
  residents: number;
  population: number;
  seed: number;
  saved_at: number;
  saved_label: string;
}

/** GET /matrix — the editable matrix definition kinds. */
export interface MatrixKindInfo {
  label: string;
  fields: string[];
  id_field: string;
}
export type MatrixItem = Record<string, unknown>;

/** GET /neural — a READ-ONLY view of the LIVE v9 substrate seed (the single source of truth, read
 *  through the same loader the engine uses). Provenance (sources/confidence/basis) comes from the
 *  seed; nothing here is editable. */
export interface NeuralCircuit {
  id: string;
  name: string;
  domain: string;
  function: string;
  baseline: number;
  tau_ms: number;
  online_age: number;
  sign: number; // +1 excitatory / -1 inhibitory
  confidence: string | null; // E | Em | H, verbatim from the seed
  evidence_base: string | null;
  sources: string | null; // citations, verbatim from the seed
}
export interface NeuralConnection {
  source: string;
  target: string;
  weight0: number;
  default_weight: string | null; // qualitative seed value (low/moderate/strong)
  basis: string | null; // assumption | anatomy | innate_reinforcer | literature
  scaffold: boolean; // true when the weight is a placeholder assumption, not measured
  gating_neuromodulator: string;
  confidence: string | null;
  citation: string | null; // the seed's `source` note (renamed to avoid colliding with the edge source)
  is_innate_reinforcer_link: boolean;
}
export interface NeuralView {
  meta: {
    version: string | null;
    title: string | null;
    n_circuits: number;
    n_connections: number;
    source_of_truth: string; // the seed file path
  };
  circuits: NeuralCircuit[];
  connections: NeuralConnection[];
  domains: string[];
  gaps: string[]; // the seed's gaps_register — why default weights are scaffold, not measured
  read_only: boolean;
}

/** POST /cmd payloads. */
export type Command =
  | { cmd: "play" }
  | { cmd: "pause" }
  | { cmd: "speed"; interval: number }
  | { cmd: "add_person"; role: string; temperament?: string }
  | { cmd: "respawn"; population?: number; seed?: number; experiment?: boolean; study_subjects?: string[]; profile?: string }
  | { cmd: "save"; name: string }
  | { cmd: "load"; slug: string }
  | { cmd: "delete_save"; slug: string }
  | { cmd: "matrix_upsert"; kind: string; item: MatrixItem }
  | { cmd: "matrix_delete"; kind: string; id: string };
// neural_upsert / neural_delete are GONE (Phase 6): the seed is the single source of truth and the
// Neural tab is read-only. The server rejects them as unknown commands.
