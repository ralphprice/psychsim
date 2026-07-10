// vitest setup: jest-dom matchers (toBeInTheDocument, toHaveTextContent, …) + DOM cleanup between
// tests. Imported via vite.config test.setupFiles.
import "@testing-library/jest-dom/vitest";
import { afterEach } from "vitest";
import { cleanup } from "@testing-library/react";

afterEach(() => cleanup());
