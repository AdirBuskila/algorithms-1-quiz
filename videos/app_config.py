# -*- coding: utf-8 -*-
"""App configuration for the video engine (tools/video/vid.py and friends)."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]

APP_NAME = "אלגוריתמים 1"
COURSE_CODE = ""
SITE = "https://adirbuskila.github.io/algorithms-1-quiz/"
BANK = "questions.json"
SIM_PATHS = ["tools/verify/needhelp"]

# same order, names and icons as course.config.json "courses". The guided levels are C01.. in every course, so a
# video id is the course letter + the level number: D03 = dp_ladder/C03.
COURSES = [
    ("dp_ladder", "תכנות דינמי: מנוסחת נסיגה לאלגוריתם", "🧩"),
    ("greedy_proofs", "אלגוריתם חמדן והוכחת נכונות", "🎯"),
    ("kmp_prefix", "KMP ופונקציית רישא", "🔤"),
    ("graph_search", "גרפים: BFS, DFS וטענות על גרפים", "🕸️"),
]
LETTER = {"D": "dp_ladder", "B": "graph_search", "G": "greedy_proofs", "K": "kmp_prefix"}

BONUS_GOAL = {}

SRC = ROOT / "courses"
REF = re.compile(r'bankId:\s*"([^"]+)"')


def level_file(video_id):
    return SRC / LETTER[video_id[0]] / f"C{video_id[1:3]}.js"


def quiz_ids():
    """bank ids used by any guided-course quiz (level quizzes and the boss levels): never solved in a video"""
    return {m.group(1) for f in SRC.glob("*/*.js") for m in REF.finditer(f.read_text(encoding="utf-8"))}


def boss_ids():
    return quiz_ids()


def is_boss(video_id):
    f = level_file(video_id)
    return f.exists() and re.search(r"boss:\s*true", f.read_text(encoding="utf-8")) is not None


def level_goal(course, level_id):
    """level_id is the video id (L03) or the level id (C03)"""
    f = SRC / course / f"C{level_id[1:3]}.js"
    m = re.search(r'goal:\s*"([^"]*)"', f.read_text(encoding="utf-8")) if f.exists() else None
    return m.group(1) if m else ""
