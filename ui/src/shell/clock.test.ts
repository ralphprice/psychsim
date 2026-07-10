import { describe, it, expect } from "vitest";
import { formatSimDate, formatElapsed, simHour, isDaytime } from "./clock";

describe("formatSimDate", () => {
  it("renders date + HH:MM, dropping seconds and TZ", () => {
    expect(formatSimDate("2003-04-17T14:00:00")).toBe("2003-04-17 14:00");
    expect(formatSimDate("2000-01-01T00:00:00")).toBe("2000-01-01 00:00");
  });
  it("degrades gracefully", () => {
    expect(formatSimDate(undefined)).toBe("—");
  });
});

describe("formatElapsed", () => {
  it("splits whole hours into +{y}y {d}d {h}h (365-day years)", () => {
    expect(formatElapsed(0)).toBe("+0y 0d 0h");
    expect(formatElapsed(25)).toBe("+0y 1d 1h"); // 25h = 1 day 1 hour
    expect(formatElapsed(365 * 24 * 3 + 24 * 107 + 14)).toBe("+3y 107d 14h");
  });
  it("degrades gracefully", () => {
    expect(formatElapsed(undefined)).toBe("—");
    expect(formatElapsed(-5)).toBe("—");
  });
});

describe("simHour / isDaytime", () => {
  it("reads the sim hour", () => {
    expect(simHour("2003-04-17T14:00:00")).toBe(14);
    expect(simHour("2003-04-17T03:30:00")).toBe(3);
    expect(simHour(undefined)).toBeNull();
  });
  it("day is 06:00–17:59 by the sim clock", () => {
    expect(isDaytime("2003-04-17T06:00:00")).toBe(true);
    expect(isDaytime("2003-04-17T14:00:00")).toBe(true);
    expect(isDaytime("2003-04-17T17:59:00")).toBe(true);
    expect(isDaytime("2003-04-17T18:00:00")).toBe(false);
    expect(isDaytime("2003-04-17T03:00:00")).toBe(false);
    expect(isDaytime("2003-04-17T23:00:00")).toBe(false);
  });
});
