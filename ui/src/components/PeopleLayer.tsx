// PeopleLayer — the live residents, overlaid on whichever background is showing.
//
// The server reports discrete tile positions ~5x/second; a person can jump several
// tiles per tick. To avoid teleport-y "gliding", each dot eases toward its target
// pixel every animation frame (requestAnimationFrame), decoupled from the poll rate.
// React handles who exists; rAF handles where they are. While a person is followed,
// this same loop recentres the camera on their eased position (no React re-render).

import { memo, useEffect, useRef } from "react";
import type * as React from "react";
import type { SimState } from "../types";
import type { ViewModel } from "../view";
import type { StageHandle } from "./Stage";
import { driveColour, ROLE_EMOJI } from "../theme";

interface PeopleLayerProps {
  people: SimState["people"];
  view: ViewModel;
  selectedCid: string | null;
  followCid: string | null;
  showLabels: boolean;
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
  stage,
}: PeopleLayerProps) {
  // eased pixel position + DOM node per resident, kept across renders
  const pos = useRef<Map<string, Pt>>(new Map());
  const nodes = useRef<Map<string, SVGGElement>>(new Map());
  // latest inputs, read by the rAF loop without restarting it
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
      // drop the eased state of anyone who has left
      for (const cid of pos.current.keys()) {
        if (!(cid in ppl)) pos.current.delete(cid);
      }
      // camera-follow rides the eased position for smoothness
      if (fcid) {
        const c = pos.current.get(fcid);
        if (c) stage.current?.centerOn(c.x, c.y);
      }
      raf = requestAnimationFrame(frame);
    };
    raf = requestAnimationFrame(frame);
    return () => cancelAnimationFrame(raf);
  }, [stage]);

  const r = view.mode === "plan" ? 5.5 : 7;

  return (
    <svg className="overlay" width={view.W} height={view.H} viewBox={`0 0 ${view.W} ${view.H}`}>
      {Object.entries(people).map(([cid, p]) => {
        const selected = cid === selectedCid;
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
            {selected && <circle r={r + 4} fill="none" stroke="#111" strokeWidth={2} opacity={0.55} />}
            {/* fixed background residents render faded + dashed; live study subjects solid */}
            <circle
              r={r}
              fill={driveColour(p.drive)}
              fillOpacity={p.subject ? 1 : 0.32}
              stroke={selected ? "#111" : p.subject ? "#222" : "#666"}
              strokeWidth={selected ? 1.6 : p.subject ? 1 : 1.1}
              strokeDasharray={p.subject ? undefined : "2 1.5"}
            />
            {showLabels && (
              <text className="plabel" x={r + 3} y={r - 2} fontSize={r * 1.5}>
                {ROLE_EMOJI[p.role] ?? ""}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}

export const PeopleLayer = memo(PeopleLayerImpl);
