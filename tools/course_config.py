# -*- coding: utf-8 -*-
"""Single reader of ../course.config.json for every Python tool (open engine).

Schema: slug, titleHe, descriptionHe, accent, accent2, sourceFolder,
        topics [[key,label],...], storePrefix,
        briefs [[file.md,chapterId,topicKey,"topic"|"cheat"],...]   (optional, default [])
        needHelp [{id,titleHe,icon,topic,entryLabelHe,introHe?},...]  (optional, default []; guided courses)
        includeDrafts  bool, default false -- when false, questions whose rubricSource or
                       stepsSource is "ai-draft" are left out of the built bank.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "course.config.json"
REQUIRED = ("slug", "titleHe", "descriptionHe", "accent", "accent2", "sourceFolder",
            "topics", "storePrefix")


NEED_HELP_ID = re.compile(r"^[A-Za-z0-9_-]+$")
NEED_HELP_KEYS = ("id", "titleHe", "icon", "topic", "entryLabelHe")


def _need_help(cfg):
    """needHelp: [{id,titleHe,icon,topic,entryLabelHe,introHe?}] -- the guided "need help?" courses
    (levels live in courses/<id>/*.js). Empty/missing list hides the feature."""
    nh = cfg.get("needHelp", [])
    if not isinstance(nh, list) or len(nh) > 8:
        sys.exit("course.config.json: needHelp must be a list of 0-8 courses")
    topics = {t[0] for t in cfg["topics"]}
    seen = set()
    for i, c in enumerate(nh):
        w = f"course.config.json: needHelp[{i}]"
        if not isinstance(c, dict):
            sys.exit(f"{w} must be an object")
        for k in NEED_HELP_KEYS:
            if not isinstance(c.get(k), str) or not c[k].strip():
                sys.exit(f"{w}: missing {k}")
        extra = set(c) - set(NEED_HELP_KEYS) - {"introHe"}
        if extra:
            sys.exit(f"{w}: unknown keys {sorted(extra)}")
        if "introHe" in c and not isinstance(c["introHe"], str):
            sys.exit(f"{w}: introHe must be a string")
        if not NEED_HELP_ID.match(c["id"]):
            sys.exit(f"{w}: id {c['id']!r} must match [A-Za-z0-9_-]+")
        if c["id"] in seen:
            sys.exit(f"{w}: duplicate id {c['id']!r}")
        seen.add(c["id"])
        if c["topic"] not in topics:
            sys.exit(f"{w}: topic {c['topic']!r} is not in the closed topics list")
    return nh


def load():
    try:
        cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        sys.exit(f"course.config.json unreadable: {str(e).encode('ascii', 'backslashreplace').decode()}")
    missing = [k for k in REQUIRED if k not in cfg]
    if missing:
        sys.exit(f"course.config.json missing keys: {missing}")
    keys = [t[0] for t in cfg["topics"]]
    if not keys or len(set(keys)) != len(keys):
        sys.exit("course.config.json: topics must be a non-empty list with unique keys")
    cfg.setdefault("briefs", [])
    cfg["includeDrafts"] = cfg.get("includeDrafts", False)
    if not isinstance(cfg["includeDrafts"], bool):
        sys.exit("course.config.json: includeDrafts must be true/false")
    cfg["needHelp"] = _need_help(cfg)
    return cfg
