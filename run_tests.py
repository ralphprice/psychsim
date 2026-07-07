#!/usr/bin/env python3
"""Run the entire platform + extension test suite:  python run_tests.py"""
import sys, os, unittest
_R = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_R, "core"))
sys.path.insert(0, os.path.join(_R, "extensions"))
suite = unittest.defaultTestLoader.discover(os.path.join(_R, "tests"), top_level_dir=_R)
result = unittest.TextTestRunner(verbosity=1).run(suite)
print(f"\nTOTAL: ran {result.testsRun} tests (core platform + sophropathy extension).")
sys.exit(0 if result.wasSuccessful() else 1)
