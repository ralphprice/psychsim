// Thin, typed wrappers over the psychsim_server.py HTTP API.
//
// All paths are relative: in dev Vite proxies them to the Python server; in
// production the Python server serves this app and answers them directly.

import type {
  TownGeometry, PlanView, SimState, PersonDetail, SaveMeta, LibraryInfo,
  ModuleInfo, CohortReport, SubjectReport, MatrixKindInfo, MatrixItem, NeuralView,
  ExecutiveView, Command,
} from "./types";

async function getJSON<T>(path: string): Promise<T> {
  const r = await fetch(path);
  if (!r.ok) throw new Error(`${path} -> ${r.status}`);
  return (await r.json()) as T;
}

export const getTown = () => getJSON<TownGeometry>("/town");
export const getPlan = (cell = 64) => getJSON<PlanView>(`/plan?cell=${cell}`);
export const getState = () => getJSON<SimState>("/state");
export const getPerson = (cid: string) =>
  getJSON<PersonDetail>(`/person?cid=${encodeURIComponent(cid)}`);
export const getSaves = () => getJSON<{ saves: SaveMeta[] }>("/saves").then((r) => r.saves);
export const getLibrary = () => getJSON<LibraryInfo>("/library");
export const getModules = () => getJSON<{ modules: ModuleInfo[] }>("/modules").then((r) => r.modules);
export const getProfiles = () => getJSON<{ profiles: string[] }>("/profiles").then((r) => r.profiles);
export const getRoles = () => getJSON<{ roles: string[] }>("/roles").then((r) => r.roles);
export const getMatrixKinds = () =>
  getJSON<{ kinds: Record<string, MatrixKindInfo> }>("/matrix").then((r) => r.kinds);
export const getMatrixItems = (kind: string) =>
  getJSON<{ kind: string; items: MatrixItem[] }>(
    `/matrix/items?kind=${encodeURIComponent(kind)}`,
  ).then((r) => r.items);
export const getNeural = () => getJSON<NeuralView>("/neural");
export const getExecutive = () => getJSON<ExecutiveView>("/executive");
export const getCohortReport = () => getJSON<CohortReport>("/report/cohort");
export const getSubjectReport = (cid: string) =>
  getJSON<SubjectReport>(`/report/subject?cid=${encodeURIComponent(cid)}`);

export interface CommandResult {
  ok?: boolean;
  cid?: string;
  error?: string;
  saved?: SaveMeta;
  loaded?: { clock: string; residents: number };
  deleted?: boolean;
}

export async function sendCommand(cmd: Command): Promise<CommandResult> {
  const r = await fetch("/cmd", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cmd),
  });
  return r.json();
}
