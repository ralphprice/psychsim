// Development — the study read-out: the cohort's emergent-dominant distribution and,
// for a selected subject, its development trajectory. Descriptive only (system names,
// never a psychopath/sophropath verdict); chaotic crude-stage output is expected.

import { useEffect, useState } from "react";
import { getCohortReport, getSubjectReport } from "../api";
import type { CohortReport, SubjectReport } from "../types";
import { driveColour } from "../theme";

const POLL_MS = 3000;

export function Development({ selectedCid }: { selectedCid: string | null }) {
  const [cohort, setCohort] = useState<CohortReport | null>(null);
  const [subject, setSubject] = useState<SubjectReport | null>(null);

  useEffect(() => {
    const tick = () => getCohortReport().then(setCohort).catch(() => {});
    tick();
    const id = setInterval(tick, POLL_MS);
    return () => clearInterval(id);
  }, []);

  useEffect(() => {
    if (!selectedCid) {
      setSubject(null);
      return;
    }
    const tick = () => getSubjectReport(selectedCid).then(setSubject).catch(() => {});
    tick();
    const id = setInterval(tick, POLL_MS);
    return () => clearInterval(id);
  }, [selectedCid]);

  const total = cohort
    ? Object.values(cohort.distribution).reduce((a, b) => a + b, 0) || 1
    : 1;
  const path = subject ? [...new Set(subject.trajectory.map((s) => s.dominant))] : [];

  return (
    <div className="dev">
      <h3>development · cohort ({cohort?.n ?? 0} subjects)</h3>
      {cohort ? (
        <>
          {Object.entries(cohort.distribution)
            .sort((a, b) => b[1] - a[1])
            .map(([sys, c]) => (
              <div className="net" key={sys}>
                <span className="n">{sys}</span>
                <span className="bar">
                  <span className="f" style={{ width: `${(c / total) * 100}%`, background: driveColour(sys) }} />
                </span>
                <span className="v">{c}</span>
              </div>
            ))}
          <div className="axis">
            emergent axis {cohort.axis_mean >= 0 ? "+" : ""}
            {cohort.axis_mean.toFixed(3)} (sd {cohort.axis_stdev.toFixed(3)})
          </div>
        </>
      ) : (
        <div className="muted">no report yet</div>
      )}
      {subject && (
        <div className="subjtraj">
          <b>{subject.cid}</b> · {subject.trajectory.length} samples
          {path.length > 0 && <> · {path.join(" → ")}</>}
        </div>
      )}
      {cohort && <div className="caveat">{cohort.caveat}</div>}
    </div>
  );
}
