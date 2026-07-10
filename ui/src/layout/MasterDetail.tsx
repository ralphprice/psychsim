// MasterDetail — the shared list-column + detail-panel primitive that every non-Town tab inherits
// (Social / Environment / Group matrices, the Development cohort). Written once so its keyboard
// model, filter behaviour and empty states are consistent everywhere.
//
//   ┌──────────────┬──────────────────────────────┐
//   │ filter box   │  DETAIL PANEL                 │
//   │ ▸ item       │  (renderDetail of the         │
//   │ ▸ item ◀ sel │   selected item, or the       │
//   │ ▸ item       │   "Select a <noun>…" empty)   │
//   └──────────────┴──────────────────────────────┘
//
// Selection is CONTROLLED (selectedId + onSelect) so a tab can persist it in the shell. The filter
// query is local view state. Keyboard: ↑/↓ move selection (clamped), Enter focuses the detail
// panel, "/" focuses the filter box.

import { useRef, useState } from "react";
import type { KeyboardEvent, ReactNode } from "react";
import { filterItems, moveSelection } from "./masterDetailModel";

export interface MasterDetailProps<T> {
  items: T[];
  getId: (item: T) => string;
  /** searchable text for one item — used for filtering (and typically the row label too) */
  getText: (item: T) => string;
  renderRow: (item: T, selected: boolean) => ReactNode;
  renderDetail: (item: T) => ReactNode;
  selectedId: string | null;
  onSelect: (id: string) => void;
  /** singular noun for the empty-state copy ("Select a role-pair to see its detail.") */
  noun?: string;
  /** show the filter box once the list is longer than this (default 10) */
  filterThreshold?: number;
}

export function MasterDetail<T>({
  items,
  getId,
  getText,
  renderRow,
  renderDetail,
  selectedId,
  onSelect,
  noun = "item",
  filterThreshold = 10,
}: MasterDetailProps<T>) {
  const [query, setQuery] = useState("");
  const filterRef = useRef<HTMLInputElement>(null);
  const detailRef = useRef<HTMLDivElement>(null);

  const filtered = filterItems(items, getText, query);
  const filteredIds = filtered.map(getId);
  const selectedItem = items.find((it) => getId(it) === selectedId) ?? null;
  const showFilter = items.length > filterThreshold;

  const onKeyDown = (e: KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "/" && e.target !== filterRef.current) {
      e.preventDefault();
      filterRef.current?.focus();
    } else if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      e.preventDefault();
      const next = moveSelection(filteredIds, selectedId, e.key === "ArrowDown" ? 1 : -1);
      if (next) onSelect(next);
    } else if (e.key === "Enter" && selectedItem) {
      e.preventDefault();
      detailRef.current?.focus();
    }
  };

  return (
    <div className="master-detail" onKeyDown={onKeyDown}>
      <div className="md-list-col">
        {showFilter && (
          <input
            ref={filterRef}
            className="md-filter"
            type="text"
            placeholder={`filter ${noun}s…  (/)`}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            aria-label={`filter ${noun}s`}
          />
        )}
        <ul className="md-list" role="listbox" tabIndex={0} aria-label={`${noun} list`}>
          {filteredIds.length === 0 ? (
            <li className="md-empty-list">
              {items.length === 0 ? `No ${noun}s yet.` : "No matches."}
            </li>
          ) : (
            filtered.map((it) => {
              const id = getId(it);
              const sel = id === selectedId;
              return (
                <li
                  key={id}
                  role="option"
                  aria-selected={sel}
                  className={"md-row" + (sel ? " selected" : "")}
                  onClick={() => onSelect(id)}
                >
                  {renderRow(it, sel)}
                </li>
              );
            })
          )}
        </ul>
      </div>

      <div className="md-detail" ref={detailRef} tabIndex={-1} role="region" aria-label={`${noun} detail`}>
        {selectedItem ? (
          renderDetail(selectedItem)
        ) : (
          <div className="md-empty">Select a {noun} to see its detail.</div>
        )}
      </div>
    </div>
  );
}
