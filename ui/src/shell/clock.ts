// Pure formatting for the sim wall-clock (Phase 8). The tick<->time mapping lives on the server; the
// UI only FORMATS what /state already computed (epoch, sim_time, elapsed_hours). Parsing is by regex
// on the naive ISO string on purpose — `new Date("...T..")` would reinterpret it in the viewer's
// timezone and shift the hour. No relative-time prose.

/** "2003-04-17T14:00:00" -> "2003-04-17 14:00" (date + HH:MM, no seconds, no TZ). */
export function formatSimDate(iso: string | undefined): string {
  if (!iso) return "—";
  const m = iso.match(/^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})/);
  return m ? `${m[1]} ${m[2]}` : iso;
}

/** whole elapsed hours -> "+3y 107d 14h" (365-day years; a duration, the number that maps to age). */
export function formatElapsed(hours: number | undefined): string {
  if (hours == null || hours < 0) return "—";
  const h = Math.floor(hours);
  const y = Math.floor(h / (365 * 24));
  const d = Math.floor((h % (365 * 24)) / 24);
  const hh = h % 24;
  return `+${y}y ${d}d ${hh}h`;
}

/** the sim hour (0–23) from an ISO sim_time, or null if unparseable. */
export function simHour(iso: string | undefined): number | null {
  if (!iso) return null;
  const m = iso.match(/T(\d{2}):/);
  return m ? parseInt(m[1], 10) : null;
}

/** day = 06:00–17:59 by the SIM CLOCK. This is a clock read-out only — the substrate has no diurnal
 *  coupling, so it never implies agents behave differently at night. */
export function isDaytime(iso: string | undefined): boolean {
  const h = simHour(iso);
  return h == null ? true : h >= 6 && h < 18;
}
