# -*- coding: utf-8 -*-
"""Learn-brief checks: every ```graph fence in docs/briefs/*.md.
For each embedded graph:
  1. its trace (event sequence + final outputs) from graph.js (via graph_js.js) must equal the one from the independent
     Python reference tools/graph_ref.py (and that script's networkx cross-checks must be empty);
  2. node tools/graph_check.js must accept it (shape, preconditions, and every `expect` key against graph.js).
Run: PYTHONUTF8=1 py tools/verify/learn/v04_graph_embeds.py      (ASCII output, exits 1 on a failure)"""
import json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BRIEFS = ROOT / "docs" / "briefs"
FENCE = re.compile(r"^```graph[ \t]*\n(.*?)\n```[ \t]*$", re.S | re.M)

ok = True


def check(name, cond, extra=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + (" " + str(extra) if extra else ""))
    ok &= bool(cond)


def canon(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=True)


specs, where = [], []
for f in sorted(BRIEFS.glob("*.md")):
    text = f.read_text(encoding="utf-8").replace("\r\n", "\n")
    for k, m in enumerate(FENCE.finditer(text), 1):
        try:
            spec = json.loads(m.group(1))
        except ValueError as e:
            check("%s fence %d is valid JSON" % (f.name.encode("ascii", "replace").decode(), k), False, e)
            continue
        specs.append(spec)
        where.append("%s#%d" % (f.name.encode("ascii", "replace").decode(), k))

print("graph fences found:", len(specs))
check("at least one embedded graph", len(specs) > 0)

env = {"PYTHONUTF8": "1", **__import__("os").environ}

# 1. graph.js vs python reference (only specs with an algo have a trace)
algo_idx = [i for i, s in enumerate(specs) if s.get("algo")]
bare = []
for i in algo_idx:
    s = dict(specs[i])
    s.pop("expect", None)
    bare.append(s)
py = subprocess.run([sys.executable, str(ROOT / "tools" / "graph_ref.py")], input=json.dumps(bare), capture_output=True, text=True, env=env)
check("graph_ref.py ran", py.returncode == 0, py.stderr[:300])
js = subprocess.run(["node", str(HERE / "graph_js.js")], input=json.dumps(bare), capture_output=True, text=True, env=env, encoding="utf-8")
check("graph.js ran", js.returncode == 0, js.stderr[:300])
if py.returncode == 0 and js.returncode == 0:
    ref, got = json.loads(py.stdout), json.loads(js.stdout)
    for n, i in enumerate(algo_idx):
        w = where[i] + " " + specs[i]["algo"]
        check(w + ": event sequence graph.js == python", canon(got[n]["events"]) == canon(ref[n]["events"]))
        res_ok = all(canon(got[n]["result"].get(k)) == canon(v) for k, v in ref[n]["result"].items())
        check(w + ": final outputs graph.js == python", res_ok)
        check(w + ": networkx agrees", not ref[n]["nx"], ref[n]["nx"])
        check(w + ": graph.js check() has no problem", not got[n]["problems"], got[n]["problems"])

# 2. graph_check.js (preconditions + expect), for all fences including plain drawings
jobs = [{"where": w, "spec": s} for w, s in zip(where, specs)]
gc = subprocess.run(["node", str(ROOT / "tools" / "graph_check.js")], input=json.dumps(jobs), capture_output=True, text=True, env=env, encoding="utf-8")
try:
    res = json.loads(gc.stdout)
except ValueError:
    res = []
    check("graph_check.js output is JSON", False, gc.stderr[:300])
for r in res:
    check(r["where"] + ": graph_check.js accepts", r["ok"], r["problems"])
check("graph_check.js judged every fence", len(res) == len(specs))

# 3. every spec states what it shows: algo specs must carry an expect block (so the quoted numbers are machine-checked)
for w, s in zip(where, specs):
    if s.get("algo"):
        check(w + ": has an expect block", bool(s.get("expect")))

sys.exit(0 if ok else 1)
