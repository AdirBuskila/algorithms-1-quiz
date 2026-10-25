# -*- coding: utf-8 -*-
"""Runs every learn-brief check. PYTHONUTF8=1 py tools/verify/learn/run_all.py   (exit 1 if any script fails)"""
import pathlib, subprocess, sys

here = pathlib.Path(__file__).resolve().parent
bad = 0
for f in sorted(here.glob("v*.py")):
    r = subprocess.run([sys.executable, str(f)], capture_output=True, text=True, encoding="utf-8")
    fails = [l for l in r.stdout.splitlines() if l.startswith("FAIL")]
    print("%-28s rc=%d  checks=%d  fails=%d" % (f.name, r.returncode, r.stdout.count("\nOK") + r.stdout.count("OK   ") // 1 if False else sum(1 for l in r.stdout.splitlines() if l.startswith(("OK", "FAIL"))), len(fails)))
    bad += r.returncode != 0
sys.exit(1 if bad else 0)
