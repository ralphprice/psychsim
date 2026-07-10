// TabBar — the top-level navigation: one full screen per subsystem. No router; a discriminated
// union + a switch is enough for six tabs.

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
  return (
    <div className="tabbar" role="tablist" aria-label="subsystem">
      {TABS.map((t) => (
        <button
          key={t.id}
          role="tab"
          aria-selected={active === t.id}
          className={"tab" + (active === t.id ? " active" : "")}
          onClick={() => onTab(t.id)}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}
