#!/usr/bin/env python3
"""
psychsim_server.py -- run the PsychSim step loop CONTINUOUSLY and stream it to a page.

Starts a running SimEngine, steps it on a background thread while "playing", and serves
its live state over plain HTTP (no extra dependencies). A frontend (psychsim_ui.html)
polls /state and posts control commands. This is the Park-style live loop, modernised.

    python psychsim_server.py            # then open psychsim_ui.html in a browser
    python psychsim_server.py --port 8000 --population 100

Endpoints:
    GET  /town            static town geometry, grid form (draw once)
    GET  /plan[?cell=64]  designed plan-view "glass-roof" SVG + grid->pixel mapping
    GET  /state           live per-person positions + drives + clock (poll this)
    GET  /person?cid=ID   full inspectable state for one person
    GET  /saves           metadata for every saved simulation on disk
    GET  /library         the grown-adult library available as fixed background
    GET  /modules         the plug-in research modules discovered under extensions/
    GET  /report/cohort   descriptive cohort development report (study subjects)
    GET  /report/subject?cid=ID   one subject's development trajectory
    POST /cmd             {"cmd": "play"|"pause"|"speed"|"add_person"|"respawn"
                                  |"save"|"load"|"delete_save", ...}
                          respawn accepts {experiment, study_subjects, fearless_frac|module_params}
"""
import argparse
import json
import mimetypes
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

# put core/ and extensions/ on the path as ROOTS, so any core package and any
# researcher-dropped extension module resolves without reinstalling (the plug-in
# system relies on this -- see core/modular/registry.discover_modules).
_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in ("core", "extensions"):
    _pp = os.path.join(_HERE, _p)
    if _pp not in sys.path:
        sys.path.insert(0, _pp)

from sophropathy.engine import SimEngine
from sophropathy.townlife import available_roles
from project import available_modules, available_profiles
from config.matrixstore import kinds as matrix_kinds, list_items, upsert_item, delete_item
from neuraldesigner.store import (library_view as neural_view, upsert as neural_upsert_item,
                                  remove as neural_remove_item)
from affective_engine.exec_store import (executive_view, upsert_monitor, delete_monitor)

# ---- the running simulation + its loop -----------------------------------
ENGINE: SimEngine = None
LOCK = threading.Lock()
PLAYING = False
STEP_INTERVAL = 0.25          # seconds between steps while playing (speed control)
UI_DIR = None                 # if set, serve the built React UI (ui/dist) at /


def _loop():
    """Background thread: step the engine while playing."""
    global PLAYING
    while True:
        if PLAYING and ENGINE is not None:
            with LOCK:
                ENGINE.step()
            time.sleep(STEP_INTERVAL)
        else:
            time.sleep(0.05)


class Handler(BaseHTTPRequestHandler):
    def _send(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")            # CORS for local file UI
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, fp):
        ctype = mimetypes.guess_type(fp)[0] or "application/octet-stream"
        with open(fp, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_ui(self, path):
        """Serve the built React SPA from UI_DIR (with SPA fallback to index.html).
        When no build exists, keep the old behaviour: '/' is a health probe."""
        if UI_DIR is None:
            if path in ("/", "/index.html"):
                return self._send({"ok": True, "ui": "not built -- run `npm run build` in ui/",
                                   "clock": ENGINE.clock_label() if ENGINE else None})
            return self._send({"error": "not found"}, 404)
        rel = path.lstrip("/") or "index.html"
        fp = os.path.normpath(os.path.join(UI_DIR, rel))
        if not fp.startswith(UI_DIR):                                   # path-traversal guard
            return self._send({"error": "forbidden"}, 403)
        if not os.path.isfile(fp):
            fp = os.path.join(UI_DIR, "index.html")                    # SPA client-side routes
        if not os.path.isfile(fp):
            return self._send({"error": "not found"}, 404)
        self._send_file(fp)

    def do_OPTIONS(self):
        self._send({}, 204)

    def log_message(self, *a):
        pass                                                            # quiet

    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/town":
            with LOCK:
                self._send(ENGINE.town())
        elif u.path == "/plan":
            cell = int(parse_qs(u.query).get("cell", ["64"])[0])
            with LOCK:
                self._send(ENGINE.plan(cell=cell))
        elif u.path == "/state":
            with LOCK:
                self._send({**ENGINE.snapshot(), "playing": PLAYING,
                            "interval": STEP_INTERVAL})
        elif u.path == "/person":
            cid = parse_qs(u.query).get("cid", [""])[0]
            with LOCK:
                self._send(ENGINE.person_detail(cid))
        elif u.path == "/saves":
            self._send({"saves": SimEngine.list_saves()})
        elif u.path == "/library":
            with LOCK:
                self._send(ENGINE.library_info())
        elif u.path == "/modules":
            self._send({"modules": available_modules()})
        elif u.path == "/profiles":
            self._send({"profiles": available_profiles()})
        elif u.path == "/roles":
            self._send({"roles": available_roles()})
        elif u.path == "/matrix":
            self._send({"kinds": matrix_kinds()})
        elif u.path == "/matrix/items":
            kind = parse_qs(u.query).get("kind", ["group"])[0]
            try:
                self._send({"kind": kind, "items": list_items(kind)})
            except KeyError:
                self._send({"error": f"unknown matrix kind {kind}"}, 404)
        elif u.path == "/neural":
            self._send(neural_view())
        elif u.path == "/executive":
            self._send(executive_view())
        elif u.path == "/report/cohort":
            with LOCK:
                self._send(ENGINE.cohort_report().to_dict())
        elif u.path == "/report/subject":
            cid = parse_qs(u.query).get("cid", [""])[0]
            with LOCK:
                self._send(ENGINE.subject_report(cid).to_dict())
        elif u.path == "/health":
            self._send({"ok": True, "clock": ENGINE.clock_label() if ENGINE else None})
        else:
            self._serve_ui(u.path)                                      # built React SPA (or 404)

    def do_POST(self):
        global PLAYING, STEP_INTERVAL, ENGINE
        if urlparse(self.path).path != "/cmd":
            return self._send({"error": "not found"}, 404)
        n = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            data = {}
        cmd = data.get("cmd")
        result = {"ok": True}
        if cmd == "play":
            PLAYING = True
        elif cmd == "pause":
            PLAYING = False
        elif cmd == "speed":
            # interval in seconds; smaller = faster. Clamp to sane bounds.
            STEP_INTERVAL = max(0.02, min(2.0, float(data.get("interval", 0.25))))
        elif cmd == "add_person":
            with LOCK:
                result["cid"] = ENGINE.add_person(data.get("role", "child"),
                                                  temperament=data.get("temperament", "typical"))
        elif cmd == "respawn":
            # the sophropath module's one live knob is fearless_frac; accept it directly
            # or via module_params={"sophropathy": {"fearless_frac": ...}}
            mp = data.get("module_params") or {}
            frac = data.get("fearless_frac", mp.get("sophropathy", {}).get("fearless_frac"))
            with LOCK:
                ENGINE.respawn(population=data.get("population"), seed=data.get("seed"),
                               experiment=data.get("experiment"),
                               study_subjects=data.get("study_subjects", "__keep__"),
                               fearless_frac=frac, profile=data.get("profile"))
            PLAYING = False
        elif cmd == "save":
            with LOCK:
                result["saved"] = ENGINE.save(data.get("name", "sim"))
        elif cmd == "load":
            key = data.get("slug") or data.get("name") or ""
            try:
                loaded = SimEngine.load(key)                            # read from disk (no lock)
            except Exception as ex:
                result = {"error": f"load failed: {ex}"}
            else:
                with LOCK:
                    ENGINE = loaded                                    # swap the running world
                PLAYING = False
                result["loaded"] = {"clock": loaded.clock_label(),
                                    "residents": len(loaded.state)}
        elif cmd == "delete_save":
            result["deleted"] = SimEngine.delete_save(data.get("slug") or data.get("name") or "")
        elif cmd == "matrix_upsert":
            try:
                result["item"] = upsert_item(data.get("kind"), data.get("item") or {})
            except (KeyError, ValueError) as ex:
                result = {"error": str(ex)}
        elif cmd == "matrix_delete":
            try:
                result["deleted"] = delete_item(data.get("kind"), data.get("id"))
            except KeyError as ex:
                result = {"error": str(ex)}
        elif cmd == "neural_upsert":
            try:
                result["item"] = neural_upsert_item(data.get("kind"), data.get("item") or {})
            except (KeyError, ValueError, TypeError) as ex:
                result = {"error": str(ex)}
        elif cmd == "neural_delete":
            try:
                result["deleted"] = neural_remove_item(data.get("kind"), data.get("id"))
            except KeyError as ex:
                result = {"error": str(ex)}
        elif cmd == "executive_upsert":
            try:
                result["item"] = upsert_monitor(data.get("item") or {})
            except (KeyError, ValueError) as ex:
                result = {"error": str(ex)}
        elif cmd == "executive_delete":
            result["deleted"] = delete_monitor(data.get("id"))
        else:
            result = {"error": f"unknown cmd {cmd}"}
        self._send(result)


def main(argv=None):
    global ENGINE, STEP_INTERVAL, UI_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--population", type=int, default=80)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--tick-minutes", type=int, default=15, dest="tick")
    ap.add_argument("--ui-dir", default=None,
                    help="serve a built React UI from this dir (default: ui/dist if present)")
    args = ap.parse_args(argv)

    # serve the built SPA if it exists, so `python psychsim_server.py` is one command
    here = os.path.dirname(os.path.abspath(__file__))
    ui = args.ui_dir or os.path.join(here, "ui", "dist")
    if os.path.isdir(ui) and os.path.isfile(os.path.join(ui, "index.html")):
        UI_DIR = os.path.normpath(ui)

    ENGINE = SimEngine(population=args.population, seed=args.seed, tick_minutes=args.tick)
    threading.Thread(target=_loop, daemon=True).start()

    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"PsychSim server running on http://127.0.0.1:{args.port}")
    print(f"  town spawned: {len(ENGINE.snapshot()['people'])} residents")
    if UI_DIR:
        print(f"  UI: open http://127.0.0.1:{args.port}/  (serving {os.path.relpath(UI_DIR, here)})")
    else:
        print(f"  UI: build it (cd ui && npm install && npm run build), or `npm run dev` for hot reload")
    print("  Ctrl-C to stop")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
