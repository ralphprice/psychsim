/// <reference types="vitest/config" />
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

// In dev (`npm run dev` on :5173) the UI uses same-origin relative URLs and Vite
// proxies the sim API to the Python server on :8765 — no CORS, no hard-coded host.
// In production the built app is served BY that same Python server, so the same
// relative URLs resolve on their own. One set of fetch paths, both modes.
const API = "http://127.0.0.1:8765";
const routes = ["/town", "/plan", "/state", "/person", "/saves", "/cmd", "/health"];

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1", // bind IPv4 loopback explicitly (predictable on WSL2)
    port: 5173,
    proxy: Object.fromEntries(routes.map((r) => [r, { target: API, changeOrigin: true }])),
  },
  build: {
    outDir: "dist",
    // keep asset names predictable; the Python static server serves whatever is here
    emptyOutDir: true,
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    include: ["src/**/*.test.{ts,tsx}"],
    css: false,
  },
});
