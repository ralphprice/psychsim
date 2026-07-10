// TabBar — the top-level navigation: one full screen per subsystem. No router; a discriminated
// union + a switch is enough for six tabs. Implements the WAI-ARIA tablist keyboard pattern:
// ←/→ (and ↑/↓) move between tabs with automatic activation, Home/End jump to first/last, and a
// roving tabindex means Tab enters the tablist once and Shift-Tab/Tab leaves it — the rest of the
// console is reachable by keyboard alone.

import { useRef } from "react";
import type { KeyboardEvent } from "react";

export const TABS = [
  { id: "town", label: "Town" },
  { id: "cohort", label: "Development Cohort" },
  { id: "social", label: "Social" },
  { id: "environment", label: "Environment" },
  { id: "group", label: "Group" },
  { id: "neural", label: "Neural" },
] as const;

export type TabId = (typeof TABS)[number]["id"];

export function TabBar({ active, onTab }: { active: TabId; onTab: (t: TabId) => void }) {
  const refs = useRef<(HTMLButtonElement | null)[]>([]);
  const activeIdx = TABS.findIndex((t) => t.id === active);

  const go = (idx: number) => {
    const n = TABS.length;
    const i = ((idx % n) + n) % n; // wrap
    onTab(TABS[i].id);
    refs.current[i]?.focus();
  };

  const onKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    switch (e.key) {
      case "ArrowRight":
      case "ArrowDown":
        e.preventDefault();
        go(activeIdx + 1);
        break;
      case "ArrowLeft":
      case "ArrowUp":
        e.preventDefault();
        go(activeIdx - 1);
        break;
      case "Home":
        e.preventDefault();
        go(0);
        break;
      case "End":
        e.preventDefault();
        go(TABS.length - 1);
        break;
    }
  };

  return (
    <div className="tabbar" role="tablist" aria-label="subsystem" onKeyDown={onKeyDown}>
      {TABS.map((t, i) => {
        const selected = active === t.id;
        return (
          <button
            key={t.id}
            ref={(el) => {
              refs.current[i] = el;
            }}
            id={`tab-${t.id}`}
            role="tab"
            aria-selected={selected}
            aria-controls="tabpanel"
            tabIndex={selected ? 0 : -1}
            className={"tab" + (selected ? " active" : "")}
            onClick={() => onTab(t.id)}
          >
            {t.label}
          </button>
        );
      })}
    </div>
  );
}
