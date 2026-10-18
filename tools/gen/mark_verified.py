# -*- coding: utf-8 -*-
"""Flip AI-drafted labels to "ai-verified" once the refuter has passed them (orchestrator only).

    PYTHONUTF8=1 py tools/gen/mark_verified.py <CODE> [qnum ...]

The step-author writes `stepsSource` / `rubricSource` as "ai-draft"; the build strips ai-draft parts
(see build_report.md "ai-draft parts stripped"). After the refuter agrees (or the arbiter rules), run
this to flip the label, then re-run tools/build_questions.py. No qnums = every question of the exam;
with qnums = those question numbers only (all parts of a number).

It edits both the data file `tools/raw/<CODE>.json` and the generator `tools/gen/gen_<CODE>.py`
(so re-running the generator does not bring the draft label back). In the generator it looks for
`stepsSource="ai-draft"` / `"rubricSource": "ai-draft"` inside the `Q(<num>, ...)` call of each number.
If a generator has another shape, the script says so and you flip the label there by hand.
Prints ASCII only.
"""
import json
import pathlib
import re
import sys

GEN = pathlib.Path(__file__).resolve().parent
RAW = GEN.parent / "raw"
FIELDS = ("stepsSource", "rubricSource")
LABEL = re.compile(r"""(?P<k>["']?)(?P<f>stepsSource|rubricSource)(?P=k)(?P<sep>\s*[=:]\s*)(?P<q>["'])ai-draft(?P=q)""")
CALL = re.compile(r"(?<![\w.])Q\(\s*(\d+)\s*,")


def flip_raw(fp, nums):
    data = json.loads(fp.read_text(encoding="utf-8"))
    n = 0
    for q in data.get("questions", []):
        if nums and q.get("num") not in nums:
            continue
        for f in FIELDS:
            if q.get(f) == "ai-draft":
                q[f] = "ai-verified"
                n += 1
    if n:
        fp.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return n


def flip_gen(fp, nums):
    """Returns (flipped, note)."""
    text = fp.read_text(encoding="utf-8")
    calls = list(CALL.finditer(text))
    if not calls:
        n = len(LABEL.findall(text))
        if n and nums:
            return 0, "generator has no Q(<num>, ...) calls: flip its labels by hand"
        out, n = LABEL.subn(lambda m: m.group(0).replace("ai-draft", "ai-verified"), text)
        if n:
            fp.write_text(out, encoding="utf-8")
        return n, ""
    pieces, last, n = [], 0, 0
    for i, m in enumerate(calls):
        end = calls[i + 1].start() if i + 1 < len(calls) else len(text)
        pieces.append(text[last:m.start()])
        block = text[m.start():end]
        if not nums or int(m.group(1)) in nums:
            block, k = LABEL.subn(lambda x: x.group(0).replace("ai-draft", "ai-verified"), block)
            n += k
        pieces.append(block)
        last = end
    out = "".join(pieces) + text[last:]
    if n:
        fp.write_text(out, encoding="utf-8")
    return n, ""


def main(argv):
    if not argv or not argv[0] or argv[0].startswith("-") or not all(a.isdigit() for a in argv[1:]):
        print("usage: mark_verified.py <CODE> [qnum ...]")
        return 2
    code, nums = argv[0], {int(a) for a in argv[1:]}
    fp = RAW / f"{code}.json"
    if not fp.is_file():
        print(f"error: {fp.name} not found in tools/raw")
        return 1
    n_raw = flip_raw(fp, nums)
    gen = GEN / f"gen_{code}.py"
    n_gen, note = (flip_gen(gen, nums) if gen.is_file() else (0, "no generator file"))
    scope = ("questions " + ",".join(map(str, sorted(nums)))) if nums else "all questions"
    print(f"{code}: {scope}: {n_raw} label(s) flipped to ai-verified in raw, {n_gen} in generator"
          + (f" ({note})" if note else ""))
    if not n_raw and not n_gen:
        print("nothing to flip (no ai-draft labels there)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
