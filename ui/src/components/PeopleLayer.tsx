// PeopleLayer — the live residents, overlaid on whichever background is showing.
//
// The server reports discrete tile positions ~5x/second; a person can jump several tiles per tick.
// To avoid teleport-y "gliding", each marker eases toward its target pixel every animation frame
// (requestAnimationFrame), decoupled from the poll rate. React handles who exists; rAF handles where.
//
// Phase 8: the FACE (role emoji) IS the marker — no spot behind it. A selection ring (--trace) is
// drawn on the selected person only; a numeric badge (--warn) on monitored agents only (a plain
// index, keyed to the cohort lookup — never a condition label). Below a zoom threshold the face is
// illegible, so we render a single dot instead (never both — that keeps one node per person).

import { memo, useEffect, useRef } from "react";
import type * as React from "react";
import type { SimState } from "../types";
import type { ViewModel } from "../view";
import type { StageHandle } from "./Stage";
import { ROLE_EMOJI } from "../theme";

interface PeopleLayerProps {
  people: SimState["people"];
  view: ViewModel;
  selectedCid: string | null;
  followCid: string | null;
  showLabels: boolean;
  /** cid -> 1-based monitor index; a badge is drawn only for cids present here */
  monitoredIndex: Record<string, number>;
  /** true when the stage is zoomed out far enough that faces are illegible -> render dots */
  zoomedOut: boolean;
  stage: React.RefObject<StageHandle>;
}

interface Pt {
  x: number;
  y: number;
}

const EASE = 0.22; // fraction of the remaining distance closed per frame

function PeopleLayerImpl({
  people,
  view,
  selectedCid,
  followCid,
  showLabels,
  monitoredIndex,
  zoomedOut,
  stage,
}: PeopleLayerProps) {
  const pos = useRef<Map<string, Pt>>(new Map());
  const nodes = useRef<Map<string, SVGGElement>>(new Map());
  const latest = useRef({ people, view, followCid });
  latest.current = { people, view, followCid };

  useEffect(() => {
    let raf = 0;
    const frame = () => {
      const { people: ppl, view: vm, followCid: fcid } = latest.current;
      for (const [cid, p] of Object.entries(ppl)) {
        const [tx, ty] = vm.tileToPx(p.x, p.y);
        let cur = pos.current.get(cid);
        if (!cur) {
          cur = { x: tx, y: ty }; // spawn in place, no fly-in from the origin
          pos.current.set(cid, cur);
        } else {
          cur.x += (tx - cur.x) * EASE;
          cur.y += (ty - cur.y) * EASE;
        }
        const node = nodes.current.get(cid);
        if (node) node.setAttribute("transform", `translate(${cur.x.toFixed(2)},${cur.y.toFixed(2)})`);
      }
      for (const cid of pos.current.keys()) {
        if (!(cid in ppl)) pos.current.delete(cid);
      }
      if (fcid) {
        const c = pos.current.get(fcid);
        if (c) stage.current?.centerOn(c.x, c.y);
      }
      raf = requestAnimationFrame(frame);
    };
    raf = requestAnimationFrame(frame);
    return () => cancelAnimationFrame(raf);
  }, [stage]);

  const face = view.mode === "plan" ? 13 : 15; // emoji size in world px
  const dotR = view.mode === "plan" ? 4 : 5;
  const ringR = face * 0.62;

  return (
    <svg className="overlay" width={view.W} height={view.H} viewBox={`0 0 ${view.W} ${view.H}`}>
      {Object.entries(people).map(([cid, p]) => {
        const selected = cid === selectedCid;
        const idx = monitoredIndex[cid]; // number | undefined
        const faded = !p.subject; // fixed background residents render dimmer
        return (
          <g
            className="person"
            key={cid}
            data-cid={cid}
            ref={(el) => {
              if (el) nodes.current.set(cid, el);
              else nodes.current.delete(cid);
            }}
          >
            {selected && <circle className="sel-ring" r={ringR} fill="none" strokeWidth={2} />}
            {zoomedOut ? (
              <circle className="pdot" r={dotR} opacity={faded ? 0.45 : 1} />
            ) : (
              <text
                className="pface"
                textAnchor="middle"
                dominantBaseline="central"
                fontSize={face}
                opacity={faded ? 0.5 : 1}
              >
                {ROLE_EMOJI[p.role] ?? "•"}
              </text>
            )}
            {idx != null && (
              <text className="pbadge" x={face * 0.5} y={-face * 0.42} fontSize={10}>
                {idx}
              </text>
            )}
            {showLabels && (
              <text className="plabel" x={face * 0.55} y={face * 0.62} fontSize={9}>
                {cid}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}

export const PeopleLayer = memo(PeopleLayerImpl);
