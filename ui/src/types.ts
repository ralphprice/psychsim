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
  /** sim wall-clock (Phase 8): the tick count, the fixed epoch, the current sim time (ISO,
   *  epoch + elapsed), whole elapsed hours, and the speed multiplier. */
  tick?: number;
  epoch?: string;
  sim_time?: string;
  elapsed_hours?: number;
  speed?: number;
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

// ---- Arena (the fine-detail lens: a few agents in a confined micro-env, developed + watched) ----
/** A defined micro-environment = its present Things + the STRUCTURAL escape count (never a tag). */
export interface ArenaEnvironment { id: string; note: string; present: string[]; escape: number }
/** The instrument's design bound (S12.2): the UI enforces min 2 / max 5. */
export interface ArenaRosterBounds { min: number; max: number; why: string }
export interface ArenaEnvironmentsView { environments: ArenaEnvironment[]; roster: ArenaRosterBounds }
/** Slot sources + the temperament GAIN-DIM vocabulary (parameters, never outcome names). */
export interface ArenaSources { kinds: string[]; gain_dims: string[]; default_grow_years: number; banked_ids: string[] }
export interface ArenaRelationships { defined: string[]; substrate: string; note: string }
/** One roster slot the UI composes and posts. Temperament is optional gain dims (default = intact). */
export interface ArenaSlotPayload {
  slot_id: string;
  source: string;            // "newborn" | "grown" | "banked"
  age: number;               // spawn age (years)
  grow_years?: number;       // if grown
  bank_id?: string;          // if banked
  gains?: Record<string, number>;  // temperament parameters (0..1); absent => intact reference
}
/** One episode of the ArenaTrace: emergent acts + saturation/drift per agent, strain per tie-pair. */
export interface ArenaRecord {
  episode: number;
  age: number;
  acts: Record<string, string>;     // agent id -> emergent act
  max_act: Record<string, number>;  // agent id -> max circuit activation (the saturation signal)
  drift: Record<string, number>;    // agent id -> developed-weight drift
  strain: Record<string, number>;   // "a|b" tie-pair -> strain
}
export interface ArenaTraceResult {
  spec: { micro_env: string; seed: number; shared_hours: number; escape: number;
          slots: { slot_id: string; source: string; age: number }[] };
  agent_ids: string[];
  records: ArenaRecord[];
  act_counts: Record<string, number>;
  peak_activation: number;  // highest single-circuit activation any agent reached
  viable: boolean;          // no agent driven into persistent saturation
  settled: boolean;         // tail-settled, not oscillating (Regime-B)
}

/** POST /cmd payloads. */
export type Command =
  | { cmd: "play" }
  | { cmd: "pause" }
  | { cmd: "speed"; interval: number }
  | { cmd: "add_person"; role: string }
  | { cmd: "respawn"; population?: number; seed?: number; experiment?: boolean; study_subjects?: string[]; profile?: string }
  | { cmd: "save"; name: string }
  | { cmd: "load"; slug: string }
  | { cmd: "delete_save"; slug: string }
  | { cmd: "matrix_upsert"; kind: string; item: MatrixItem }
  | { cmd: "matrix_delete"; kind: string; id: string }
  | { cmd: "arena_run"; micro_env: string; seed: number; shared_hours: number; childhood_years: number; slots: ArenaSlotPayload[] };
// neural_upsert / neural_delete are GONE (Phase 6): the seed is the single source of truth and the
// Neural tab is read-only. The server rejects them as unknown commands.
