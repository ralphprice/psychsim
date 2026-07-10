"""Regression for the 'pause is inert' report (Phase 8 §5).

Diagnosis: the pause path is correct at every layer -- the client toggle sends the right command
(covered by ui TransportSection.test.tsx, full poll->button->command flow) and the SERVER stops the
tick when PLAYING is cleared. This test locks the server-side acceptance criterion directly: with the
real HTTP server running, pause makes the /state tick stop across two consecutive polls, and play
resumes it.
"""
import sys as _S, os as _O
_ROOT = _O.path.dirname(_O.path.dirname(_O.path.abspath(__file__)))
_S.path.insert(0, _O.path.join(_ROOT, "core"))
_S.path.insert(0, _O.path.join(_ROOT, "extensions"))
_S.path.insert(0, _ROOT)

import json
import threading
import time
import unittest
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer

import psychsim_server as srv
from sophropathy.engine import SimEngine


def _post(base, cmd):
    urllib.request.urlopen(
        base + "/cmd", data=json.dumps(cmd).encode(), timeout=5
    ).read()


def _step(base):
    return json.loads(urllib.request.urlopen(base + "/state", timeout=5).read())["step"]


class TestPauseStopsTheTick(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        srv.ENGINE = SimEngine(population=4, seed=1)
        srv.STEP_INTERVAL = 0.02
        srv.PLAYING = False
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), srv.Handler)
        cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}"
        cls.t_loop = threading.Thread(target=srv._loop, daemon=True)
        cls.t_serve = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.t_loop.start()
        cls.t_serve.start()

    @classmethod
    def tearDownClass(cls):
        srv.PLAYING = False
        cls.httpd.shutdown()

    def test_pause_stops_tick_play_resumes(self):
        base = self.base
        # play -> the tick advances across two polls
        _post(base, {"cmd": "play"})
        time.sleep(0.15)
        a = _step(base)
        time.sleep(0.15)
        b = _step(base)
        self.assertGreater(b, a, "playing advances the tick")

        # pause -> the tick is STABLE across two consecutive polls (the acceptance criterion)
        _post(base, {"cmd": "pause"})
        time.sleep(0.1)
        c = _step(base)
        time.sleep(0.2)
        d = _step(base)
        self.assertEqual(d, c, "pause stops the tick across two polls")

        # play again -> it resumes
        _post(base, {"cmd": "play"})
        time.sleep(0.15)
        e = _step(base)
        self.assertGreater(e, d, "play resumes the tick")

    def test_unknown_command_is_rejected_400(self):
        # while we hold the server, confirm the Phase-6 contract too (unknown cmd -> 400)
        req = urllib.request.Request(
            self.base + "/cmd", data=json.dumps({"cmd": "neural_upsert"}).encode()
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req, timeout=5)
        self.assertEqual(ctx.exception.code, 400)


if __name__ == "__main__":
    unittest.main()
