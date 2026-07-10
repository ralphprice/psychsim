// DevelopmentCohortTab — master-detail over the cohort. A cohort summary strip (counts +
// distributions only, verbatim from /report/cohort — no derived "health" score, no aggregate
// classification) above a resident list; selecting a resident shows three stacked cards: Subject
// (/person), Development (the existing component, for the trajectory), and the Observer read-out
// (/report/subject, rendered VERBATIM per U4, with the "never fed back" footer under THAT card).
//
// Data reality (flagged): the sim exposes no numeric age and no distinct names (name === cid), so the
// list shows cid + life-stage (role_name) + role and sorts by cid; a true age column/sort would need
// a server field. Not added here — Phase 5 stays client-only.

import { useEffect, useState } from "react";
import { getCohortReport, getPerson, getSubjectReport } from "../api";
import type { CohortReport, PersonDetail, SubjectReport, SimState } from "../types";
import { MasterDetail } from "../layout/MasterDetail";
import { Development } from "../components/Development";
import { ObserverReadout } from "../components/ObserverReadout";

const COHORT_POLL_MS = 4000;

export function DevelopmentCohortTab({
  people,
  selectedId,
  onSelect,
  monitoredIndex,
  onToggleMonitor,
}: {
  people: SimState["people"];
  selectedId: string | null;
  onSelect: (id: string | null) => void;
  /** cid -> 1-based badge index; this tab IS the lookup for the map badges */
  monitoredIndex: Record<string, number>;
  onToggleMonitor: (cid: string) => void;
}) {
  const [cohort, setCohort] = useState<CohortReport | null>(null);
  useEffect(() => {
    const tick = () => getCohortReport().then(setCohort).catch(() => {});
    tick();
    const id = setInterval(tick, COHORT_POLL_MS);
    return () => clearInterval(id);
  }, []);

  const residents = Object.entries(people)
    .map(([cid, p]) => ({ cid, role: p.role, role_name: p.role_name ?? null, subject: p.subject }))
    .sort((a, b) => a.cid.localeCompare(b.cid, undefined, { numeric: true }));

  return (
    <div className="cohort-tab">
      <CohortStrip cohort={cohort} />
      <MasterDetail
        items={residents}
        getId={(r) => r.cid}
        getText={(r) => `${r.cid} ${r.role} ${r.role_name ?? ""}`}
        renderRow={(r) => (
          <span className="co-row">
            {monitoredIndex[r.cid] != null && (
              <span className="co-badge" title="monitored — badge index on the map">
                {monitoredIndex[r.cid]}
              </span>
            )}
            <b>{r.cid}</b>
            <span className="co-stage">{r.role_name ?? r.role}</span>
            {r.subject && (
              <span className="co-live" title="study subject (live)">
                ●
              </span>
            )}
          </span>
        )}
        renderDetail={(r) => (
          <SubjectDetail
            cid={r.cid}
            monitorIndex={monitoredIndex[r.cid]}
            onToggleMonitor={onToggleMonitor}
          />
        )}
        selectedId={selectedId}
        onSelect={(id) => onSelect(id)}
        noun="resident"
        label="Residents"
      />
    </div>
  );
}

// counts + distributions only — everything shown is emitted by /report/cohort, verbatim; the UI adds
// no summary or classification of its own
function CohortStrip({ cohort }: { cohort: CohortReport | null }) {
  if (!cohort) return <div className="cohort-strip muted">cohort report loading…</div>;
  return (
    <div className="cohort-strip">
      <div className="cohort-n">
        <b>{cohort.n}</b> residents
      </div>
      <div className="cohort-block">
        <span className="cohort-label">dominant distribution</span>
        {Object.entries(cohort.distribution).map(([k, c]) => (
          <span className="cohort-chip" key={k}>
            {k} <b>{c}</b>
          </span>
        ))}
      </div>
      <div className="cohort-block">
        <span className="cohort-label">mean profile</span>
        {Object.entries(cohort.mean_profile).map(([k, v]) => (
          <span className="cohort-chip" key={k}>
            {k} <b>{v.toFixed(3)}</b>
          </span>
        ))}
      </div>
      <div className="cohort-block">
        <span className="cohort-label">axis</span>
        <span className="cohort-chip">
          mean <b>{cohort.axis_mean.toFixed(3)}</b>
        </span>
        <span className="cohort-chip">
          sd <b>{cohort.axis_stdev.toFixed(3)}</b>
        </span>
      </div>
      {cohort.caveat && <div className="cohort-caveat">{cohort.caveat}</div>}
    </div>
  );
}

function SubjectDetail({
  cid,
  monitorIndex,
  onToggleMonitor,
}: {
  cid: string;
  monitorIndex: number | undefined;
  onToggleMonitor: (cid: string) => void;
}) {
  const [person, setPerson] = useState<PersonDetail | null>(null);
  const [report, setReport] = useState<SubjectReport | null>(null);

  useEffect(() => {
    let live = true;
    setPerson(null);
    setReport(null);
    getPerson(cid)
      .then((d) => live && setPerson(d))
      .catch(() => {});
    getSubjectReport(cid)
      .then((d) => live && setReport(d))
      .catch(() => {});
    return () => {
      live = false;
    };
  }, [cid]);

  return (
    <div className="subject-detail">
      <section className="subject-card">
        <div className="subject-head">
          <h3>Subject</h3>
          <button
            className={"co-monitor" + (monitorIndex != null ? " on" : "")}
            onClick={() => onToggleMonitor(cid)}
            title="show a numeric badge on this resident on the map (a plain index, not a label)"
          >
            {monitorIndex != null ? `● monitored · ${monitorIndex}` : "○ monitor on map"}
          </button>
        </div>
        {person ? (
          <>
            <dl className="subject-facts">
              <dt>id</dt>
              <dd>{person.cid}</dd>
              <dt>role</dt>
              <dd>
                {person.role_name ?? person.role} · {person.role}
              </dd>
              <dt>home</dt>
              <dd>{person.home ?? "—"}</dd>
              {person.work && (
                <>
                  <dt>works</dt>
                  <dd>{person.work}</dd>
                </>
              )}
              <dt>state</dt>
              <dd>{person.mind_state}</dd>
              {person.temperament && (
                <>
                  <dt>temperament (given)</dt>
                  <dd>{person.temperament}</dd>
                </>
              )}
            </dl>
            {person.groups.length > 0 && (
              <div className="subject-standing">
                <span className="subject-sub">standing</span>
                {person.groups.map((g, i) => (
                  <div className="standing-row" key={i}>
                    {g.group}: standing {g.standing}, belonging {g.belonging} <i>({g.route})</i>
                  </div>
                ))}
              </div>
            )}
          </>
        ) : (
          <div className="muted">loading…</div>
        )}
      </section>

      <section className="subject-card">
        <h3>Development</h3>
        <Development selectedCid={cid} />
      </section>

      <section className="subject-card">
        <h3>Observer read-out</h3>
        {report ? (
          <>
            <ObserverReadout data={report.observer} />
            {report.caveat && <div className="ro-caveat">{report.caveat}</div>}
          </>
        ) : (
          <div className="muted">loading…</div>
        )}
        <div className="ro-footer">Measured over emergent behaviour. Never fed back.</div>
      </section>
    </div>
  );
}
