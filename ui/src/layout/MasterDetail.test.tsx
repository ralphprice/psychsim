import { describe, it, expect, vi } from "vitest";
import { useState } from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { MasterDetail } from "./MasterDetail";

interface Row {
  id: string;
  name: string;
}
const mk = (n: number): Row[] => Array.from({ length: n }, (_, i) => ({ id: `r${i}`, name: `Row ${i}` }));

// A stateful harness so keyboard/click selection actually moves (selection is controlled).
function Harness({ items, initial = null }: { items: Row[]; initial?: string | null }) {
  const [sel, setSel] = useState<string | null>(initial);
  return (
    <MasterDetail
      items={items}
      getId={(r) => r.id}
      getText={(r) => r.name}
      renderRow={(r) => <span>{r.name}</span>}
      renderDetail={(r) => <div>detail:{r.name}</div>}
      selectedId={sel}
      onSelect={setSel}
      noun="widget"
    />
  );
}

describe("MasterDetail", () => {
  it("renders a row per item and shows the empty-detail copy until one is selected", () => {
    render(<Harness items={mk(3)} />);
    expect(screen.getAllByRole("option")).toHaveLength(3);
    expect(screen.getByText("Select a widget to see its detail.")).toBeInTheDocument();
  });

  it("clicking a row selects it (onSelect) and renders its detail", () => {
    render(<Harness items={mk(3)} />);
    fireEvent.click(screen.getByText("Row 1"));
    expect(screen.getByRole("option", { selected: true })).toHaveTextContent("Row 1");
    expect(screen.getByText("detail:Row 1")).toBeInTheDocument();
  });

  it("calls onSelect with the clicked id (controlled)", () => {
    const onSelect = vi.fn();
    render(
      <MasterDetail
        items={mk(3)}
        getId={(r) => r.id}
        getText={(r) => r.name}
        renderRow={(r) => <span>{r.name}</span>}
        renderDetail={(r) => <div>{r.name}</div>}
        selectedId={null}
        onSelect={onSelect}
        noun="widget"
      />,
    );
    fireEvent.click(screen.getByText("Row 2"));
    expect(onSelect).toHaveBeenCalledWith("r2");
  });

  it("shows the filter box only when the list exceeds the threshold", () => {
    const { unmount } = render(<Harness items={mk(3)} />);
    expect(screen.queryByLabelText("filter widgets")).toBeNull();
    unmount();
    render(<Harness items={mk(12)} />);
    expect(screen.getByLabelText("filter widgets")).toBeInTheDocument();
  });

  it("typing in the filter narrows the visible rows (case-insensitive)", () => {
    render(<Harness items={mk(12)} />);
    const filter = screen.getByLabelText("filter widgets");
    fireEvent.change(filter, { target: { value: "Row 5" } });
    expect(screen.getAllByRole("option")).toHaveLength(1);
    expect(screen.getByRole("option")).toHaveTextContent("Row 5");
    fireEvent.change(filter, { target: { value: "row" } });
    expect(screen.getAllByRole("option")).toHaveLength(12);
    fireEvent.change(filter, { target: { value: "zzz" } });
    expect(screen.queryAllByRole("option")).toHaveLength(0);
    expect(screen.getByText("No matches.")).toBeInTheDocument();
  });

  it("Arrow keys move the selection, clamped at both ends", () => {
    render(<Harness items={mk(3)} initial="r0" />);
    const list = screen.getByRole("listbox");
    const selected = () => screen.getByRole("option", { selected: true }).textContent;

    fireEvent.keyDown(list, { key: "ArrowDown" });
    expect(selected()).toBe("Row 1");
    fireEvent.keyDown(list, { key: "ArrowDown" });
    expect(selected()).toBe("Row 2");
    fireEvent.keyDown(list, { key: "ArrowDown" }); // clamp at bottom
    expect(selected()).toBe("Row 2");
    fireEvent.keyDown(list, { key: "ArrowUp" });
    expect(selected()).toBe("Row 1");
  });

  it("'/' focuses the filter box", () => {
    render(<Harness items={mk(12)} />);
    fireEvent.keyDown(screen.getByRole("listbox"), { key: "/" });
    expect(document.activeElement).toBe(screen.getByLabelText("filter widgets"));
  });

  it("Enter focuses the detail panel", () => {
    render(<Harness items={mk(3)} initial="r0" />);
    fireEvent.keyDown(screen.getByRole("listbox"), { key: "Enter" });
    expect(document.activeElement).toBe(screen.getByRole("region", { name: "widget detail" }));
  });

  it("empty state: no items shows the empty list and empty detail", () => {
    render(<Harness items={[]} />);
    expect(screen.getByText("No widgets yet.")).toBeInTheDocument();
    expect(screen.getByText("Select a widget to see its detail.")).toBeInTheDocument();
  });

  it("uses the provided label as the listbox accessible name", () => {
    render(
      <MasterDetail
        items={mk(3)}
        getId={(r) => r.id}
        getText={(r) => r.name}
        renderRow={(r) => <span>{r.name}</span>}
        renderDetail={(r) => <div>{r.name}</div>}
        selectedId={null}
        onSelect={() => {}}
        noun="widget"
        label="Social role-pairs"
      />,
    );
    expect(screen.getByRole("listbox", { name: "Social role-pairs" })).toBeInTheDocument();
  });

  it("tracks the selected option via aria-activedescendant as selection moves", () => {
    render(<Harness items={mk(3)} initial="r0" />);
    const list = screen.getByRole("listbox");
    const active = () => document.getElementById(list.getAttribute("aria-activedescendant") ?? "");
    expect(active()).toHaveTextContent("Row 0");
    fireEvent.keyDown(list, { key: "ArrowDown" });
    expect(active()).toHaveTextContent("Row 1");
  });

  it("renders a listFooter at the bottom of the list column", () => {
    render(
      <MasterDetail
        items={mk(3)}
        getId={(r) => r.id}
        getText={(r) => r.name}
        renderRow={(r) => <span>{r.name}</span>}
        renderDetail={(r) => <div>{r.name}</div>}
        selectedId={null}
        onSelect={() => {}}
        noun="widget"
        listFooter={<button>+ New widget</button>}
      />,
    );
    expect(screen.getByRole("button", { name: "+ New widget" })).toBeInTheDocument();
  });

  it("detailOverride replaces the detail panel (selected item and empty state alike)", () => {
    render(
      <MasterDetail
        items={mk(3)}
        getId={(r) => r.id}
        getText={(r) => r.name}
        renderRow={(r) => <span>{r.name}</span>}
        renderDetail={(r) => <div>detail:{r.name}</div>}
        selectedId="r1"
        onSelect={() => {}}
        noun="widget"
        detailOverride={<div>NEW FORM</div>}
      />,
    );
    expect(screen.getByText("NEW FORM")).toBeInTheDocument();
    expect(screen.queryByText("detail:Row 1")).toBeNull(); // override wins over the selected item
  });
});
