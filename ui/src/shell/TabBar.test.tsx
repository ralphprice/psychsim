import { describe, it, expect, vi } from "vitest";
import { useState } from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { TabBar, TABS, type TabId } from "./TabBar";

// stateful harness so activation actually moves
function Harness({ onTab }: { onTab?: (t: TabId) => void }) {
  const [active, setActive] = useState<TabId>("town");
  return (
    <TabBar
      active={active}
      onTab={(t) => {
        setActive(t);
        onTab?.(t);
      }}
    />
  );
}

describe("TabBar — WAI-ARIA tablist keyboard pattern", () => {
  it("exposes a tablist of tabs with one selected + roving tabindex", () => {
    render(<Harness />);
    const tabs = screen.getAllByRole("tab");
    expect(tabs).toHaveLength(TABS.length);
    const selected = screen.getByRole("tab", { selected: true });
    expect(selected).toHaveTextContent("Town");
    expect(selected).toHaveAttribute("tabindex", "0");
    // the non-selected tabs are removed from the tab order (roving tabindex)
    expect(screen.getByRole("tab", { name: "Neural" })).toHaveAttribute("tabindex", "-1");
  });

  it("links each tab to the tabpanel (aria-controls)", () => {
    render(<Harness />);
    expect(screen.getByRole("tab", { name: "Town" })).toHaveAttribute("aria-controls", "tabpanel");
    expect(screen.getByRole("tab", { name: "Town" })).toHaveAttribute("id", "tab-town");
  });

  it("ArrowRight / ArrowLeft move selection with automatic activation, wrapping", () => {
    const onTab = vi.fn();
    render(<Harness onTab={onTab} />);
    const list = screen.getByRole("tablist");
    fireEvent.keyDown(list, { key: "ArrowRight" });
    expect(onTab).toHaveBeenLastCalledWith("arena");                 // Arena is the 2nd tab
    expect(screen.getByRole("tab", { selected: true })).toHaveTextContent("Arena");
    fireEvent.keyDown(list, { key: "ArrowLeft" });                   // arena -> town
    fireEvent.keyDown(list, { key: "ArrowLeft" }); // wrap past town -> neural
    expect(screen.getByRole("tab", { selected: true })).toHaveTextContent("Neural");
  });

  it("Home / End jump to first / last", () => {
    render(<Harness />);
    const list = screen.getByRole("tablist");
    fireEvent.keyDown(list, { key: "End" });
    expect(screen.getByRole("tab", { selected: true })).toHaveTextContent("Neural");
    fireEvent.keyDown(list, { key: "Home" });
    expect(screen.getByRole("tab", { selected: true })).toHaveTextContent("Town");
  });
});
