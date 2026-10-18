# Stage-2 support for blind verification (open engine).
#   strip:   py tools/gen/verify_strip.py strip <CODE>    -> tools/raw/_blind_<CODE>.json
#            Keeps ONLY num, part, kind, topic, points, question, contextId, image and the mcq
#            options (no ids' keys). Everything that carries an answer -- solution, steps,
#            rubric, pitfalls, correctId, acceptedIds, verdict, explanation -- is dropped.
#   compare: py tools/gen/verify_strip.py compare <CODE>  -> compares tools/raw/<CODE>.json with the
#            verifier's tools/raw/_verify_<CODE>.json:
#              {"answers": {"<num>[part]": {"answer": "b", "confident": true,
#                                           "agrees": true, "transcriptionIssues": ""}}}
#            keyed by the question's num plus ASCII part suffix ("3", "3b").
#            mcq     : verifier "answer" must be among correctId/acceptedIds.
#            truefalse: verifier "answer" must equal the verdict (true/false).
#            others  : verifier states "agrees": true|false against the solution and steps.
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from richtext import part_suffix  # noqa: E402

RAW = pathlib.Path(__file__).resolve().parents[1] / "raw"
KEEP_Q = ("num", "part", "kind", "topic", "points", "question", "contextId", "image", "options")


def key(q):
    return f"{q['num']}{part_suffix(q.get('part')) or ''}"


cmd, code = sys.argv[1], sys.argv[2]
src = json.loads((RAW / f"{code}.json").read_text(encoding="utf-8"))
if cmd == "strip":
    out = {"examCode": code, "sourceFile": src.get("sourceFile"), "contexts": src.get("contexts", {}),
           "questions": [{k: q[k] for k in KEEP_Q if k in q} for q in src["questions"]]}
    (RAW / f"_blind_{code}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote _blind_{code}.json ({len(out['questions'])} questions)")
elif cmd == "compare":
    ver = json.loads((RAW / f"_verify_{code}.json").read_text(encoding="utf-8"))["answers"]
    agree = dis = 0
    for q in src["questions"]:
        k = key(q)
        v = ver.get(k)
        if v is None:
            print(f"Q{k}: MISSING in verifier"); dis += 1; continue
        issues = v.get("transcriptionIssues") or ""
        if q.get("hold"):
            ok = False
        elif q["kind"] == "mcq":
            ok = v.get("answer") in set(q.get("acceptedIds") or [q["correctId"]])
        elif q["kind"] == "truefalse":
            ok = v.get("answer") == q["verdict"]
        else:
            ok = v.get("agrees") is True
        if ok and v.get("confident", True) and not issues:
            agree += 1
        else:
            dis += 1
            print(f"Q{k}: kind={q['kind']} hold={str(q.get('hold') or '')[:40]!r} verifier={v.get('answer')!r} "
                  f"agrees={v.get('agrees')} confident={v.get('confident')} issues={issues[:120]!r}")
    print(f"{code}: agree {agree}, not-agreed {dis}")
