// Stage — the pannable / zoomable viewport. Holds a "world" layer (background +
// people overlay, both sized W x H) and applies a translate+scale transform to it
// imperatively, so dragging (and camera-follow) never re-render React. Exposes a
// centerOn(x,y) handle the people layer calls each animation frame while following.

import { forwardRef, useCallback, useEffect, useImperativeHandle, useRef } from "react";
import type * as React from "react";
import type { ReactNode } from "react";

export interface StageHandle {
  /** recentre the viewport on a world-pixel point at the current zoom */
  centerOn: (px: number, py: number) => void;
  /** fit the whole world into view */
  fit: () => void;
}

interface StageProps {
  W: number;
  H: number;
  onPick: (cid: string) => void;
  onEmptyClick?: () => void;
  children: ReactNode;
}

interface ViewState {
  s: number;
  x: number;
  y: number;
  drag: boolean;
  lx: number;
  ly: number;
  moved: number;
}

export const Stage = forwardRef<StageHandle, StageProps>(function Stage(
  { W, H, onPick, onEmptyClick, children },
  ref,
) {
  const stageRef = useRef<HTMLDivElement>(null);
  const worldRef = useRef<HTMLDivElement>(null);
  const view = useRef<ViewState>({ s: 1, x: 0, y: 0, drag: false, lx: 0, ly: 0, moved: 0 });

  const apply = useCallback(() => {
    const v = view.current;
    if (worldRef.current) {
      worldRef.current.style.transform = `translate(${v.x}px,${v.y}px) scale(${v.s})`;
    }
  }, []);

  const centerOn = useCallback(
    (px: number, py: number) => {
      const stage = stageRef.current;
      if (!stage) return;
      const v = view.current;
      v.x = stage.clientWidth / 2 - px * v.s;
      v.y = stage.clientHeight / 2 - py * v.s;
      apply();
    },
    [apply],
  );

  const fit = useCallback(() => {
    const stage = stageRef.current;
    if (!stage || !W || !H) return;
    const v = view.current;
    const margin = 0.9;
    v.s = Math.min((stage.clientWidth / W) * margin, (stage.clientHeight / H) * margin, 4);
    v.x = (stage.clientWidth - W * v.s) / 2;
    v.y = (stage.clientHeight - H * v.s) / 2;
    apply();
  }, [W, H, apply]);

  useImperativeHandle(ref, () => ({ centerOn, fit }), [centerOn, fit]);

  // fit whenever the world size (i.e. the town or the view mode) changes
  useEffect(() => {
    fit();
  }, [fit]);

  const onWheel = useCallback(
    (e: React.WheelEvent) => {
      e.preventDefault();
      const stage = stageRef.current;
      if (!stage) return;
      const v = view.current;
      const f = e.deltaY < 0 ? 1.1 : 0.9;
      const r = stage.getBoundingClientRect();
      const mx = e.clientX - r.left;
      const my = e.clientY - r.top;
      v.x = mx - (mx - v.x) * f;
      v.y = my - (my - v.y) * f;
      v.s *= f;
      apply();
    },
    [apply],
  );

  const onDown = (e: React.MouseEvent) => {
    const v = view.current;
    v.drag = true;
    v.lx = e.clientX;
    v.ly = e.clientY;
    v.moved = 0;
  };
  const onMove = (e: React.MouseEvent) => {
    const v = view.current;
    if (!v.drag) return;
    v.x += e.clientX - v.lx;
    v.y += e.clientY - v.ly;
    v.moved += Math.abs(e.clientX - v.lx) + Math.abs(e.clientY - v.ly);
    v.lx = e.clientX;
    v.ly = e.clientY;
    apply();
  };
  const onUp = () => {
    view.current.drag = false;
  };
  const onClick = (e: React.MouseEvent) => {
    if (view.current.moved > 4) return; // a drag, not a click
    const el = (e.target as Element).closest<HTMLElement>(".person");
    if (el?.dataset.cid) onPick(el.dataset.cid);
    else onEmptyClick?.();
  };

  return (
    <div
      className="stage"
      ref={stageRef}
      onWheel={onWheel}
      onMouseDown={onDown}
      onMouseMove={onMove}
      onMouseUp={onUp}
      onMouseLeave={onUp}
      onClick={onClick}
    >
      <div className="world" ref={worldRef} style={{ width: W, height: H }}>
        {children}
      </div>
    </div>
  );
});
