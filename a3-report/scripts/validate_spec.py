#!/usr/bin/env python3
"""Pre-build linter for A3 spec JSON.

Usage:
    python scripts/validate_spec.py spec.json

Checks the *content quality rules* of the a3-report skill before building,
so quality is enforced by the system, not by memory ("fix the system, not
the person"). Prints [WARN]/[INFO] lines to stderr. Exit code:
    0 = OK (possibly with INFO notes)
    1 = warnings found (build anyway is allowed, but fix them first)
    2 = spec unreadable / invalid JSON
Stdlib only; no dependencies.
"""
import json
import re
import sys

WARN, INFO = [], []


def warn(msg):
    WARN.append(msg)


def info(msg):
    INFO.append(msg)


# Keywords that indicate an escalation-type countermeasure (who to ask)
ESCALATION_WORDS = [
    # Japanese
    "上司", "相談", "依頼", "支援", "外部", "専門家", "エスカレ", "巻き込", "協力",
    "ベンダ", "コンサル", "補助金", "承認", "決裁", "紹介",
    # English
    "boss", "manager", "escalat", "consult", "ask ", "vendor", "external",
    "expert", "support", "approval", "refer", "mentor", "agency",
]

# Keywords that indicate a verification / Check milestone in the timeline
VERIFY_WORDS = [
    "測定", "検証", "確認", "効果", "評価", "振り返", "レビュー", "KPI", "通過率",
    "measure", "verify", "check", "review", "evaluat", "kpi", "metric",
    "assess", "audit",
]

# 判定 symbols expected in an iteration sheet's previous-results table
JUDGE_MARKS = ["◎", "○", "△", "×", "－"]
# Result words that mean a countermeasure was dropped / deferred
DROPPED_WORDS = ["未実施", "保留", "必要なし", "中止", "見送り", "not done",
                 "skipped", "deferred", "dropped"]
# Words that show a re-trigger condition exists for dropped items
RETRIGGER_WORDS = ["条件", "再発動", "再開", "トリガー", "発動", "re-trigger",
                   "reactivat", "if ", "たら", "れば"]


def _disp_width(s):
    """Approximate display width: full-width (CJK) chars count 2, others 1."""
    import unicodedata
    return sum(2 if unicodedata.east_asian_width(c) in ("F", "W") else 1 for c in s)


def _step_fields(step):
    if isinstance(step, dict):
        return str(step.get("text", "")), step.get("mark"), bool(step.get("dashed"))
    return str(step), None, False


def _flat_text(obj):
    """All human-visible text in a section, joined lowercase."""
    out = []

    def rec(x):
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, dict):
            for v in x.values():
                rec(v)
        elif isinstance(x, list):
            for v in x:
                rec(v)

    rec(obj)
    return " ".join(out).lower()


def check_five_whys(spec):
    fw = spec.get("five_whys")
    if not fw:
        warn("five_whys: section missing — an A3 without the Five-Whys is not finished.")
        return 0, 0
    trees = fw.get("trees", [])
    if not (1 <= len(trees) <= 3):
        warn(f"five_whys: {len(trees)} trees — use 1-3 (more gets cramped).")
    stars = triangles = diamonds = 0
    for ti, tree in enumerate(trees, 1):
        steps = tree.get("steps", [])
        if len(steps) > 5:
            warn(f"five_whys tree {ti}: {len(steps)} steps — max 5 (Why-1..Why-5) fits the layout.")
        if len(steps) < 3:
            info(f"five_whys tree {ti}: only {len(steps)} steps — is the chain deep enough to reach a root?")
        for step in steps:
            txt, mark, _ = _step_fields(step)
            w = _disp_width(txt)
            if w > 40:
                warn(f"five_whys tree {ti}: step text too long (width {w} > 40, fixed 12pt will overflow): '{txt[:20]}…'")
            if mark == "star":
                stars += 1
            elif mark == "triangle":
                triangles += 1
            elif mark == "diamond":
                diamonds += 1
    if stars == 0:
        warn("five_whys: no ★ bottleneck marked — an A3 with no ★ hasn't finished its analysis.")
    if triangles == 0:
        warn("five_whys: no ▲ escalation node — at least 1 root cause (ideally 2) must be "
             "escalated to a boss / external help. Apply the 5 escalation tests "
             "(authority / resources / expertise / scope / deadline).")
    elif triangles == 1:
        info("five_whys: 1 ▲ escalation node found — 2 is the recommended target.")
    if diamonds == 0:
        info("five_whys: no ◆ unknown-unknowns marked — are there really none?")
    return stars, triangles


def check_traceability(spec, triangles):
    """Every ▲ needs a countermeasure that names who/what/when."""
    cm_text = _flat_text(spec.get("countermeasures", {}))
    if not cm_text:
        warn("countermeasures: section missing.")
        return
    if triangles > 0 and not any(w in cm_text for w in ESCALATION_WORDS):
        warn("traceability: ▲ escalation node(s) exist but no countermeasure mentions "
             "asking anyone (上司/相談/依頼/consult/vendor/…). Each ▲ needs a "
             "countermeasure naming WHO to ask, WHAT to ask for, and BY WHEN.")
    da_text = _flat_text(spec.get("deep_analysis", {}))
    if triangles > 0 and da_text and not any(w in da_text for w in ESCALATION_WORDS):
        info("deep_analysis: consider a researched 'escalation / external help' block "
             "(what the boss or external parties can concretely provide).")


def check_goals(spec):
    goals_text = _flat_text(spec.get("goals", []))
    if not goals_text:
        warn("goals: section missing.")
        return
    if not re.search(r"\d", goals_text):
        warn("goals: no numbers found — goals must be measurable (KPI, %, count, deadline).")


def check_timeline_verification(spec):
    tl_text = _flat_text(spec.get("timeline", {}))
    if not tl_text:
        warn("timeline: section missing.")
        return
    if not any(w.lower() in tl_text for w in VERIFY_WORDS):
        warn("timeline: no verification/Check milestone found — include at least one "
             "point where the Goal KPI is measured (効果測定/検証/KPI確認/review), "
             "or the PDCA loop never closes.")


def check_cost(spec):
    cost = spec.get("cost_analysis", {})
    table = cost.get("table") or {}
    rows = table.get("rows") or []
    if len(rows) > 6:
        warn(f"cost_analysis: table has {len(rows)} rows — keep ≤6 or it will be clipped.")
    bullets = cost.get("bullets") or []
    if len(bullets) > 5:
        warn(f"cost_analysis: {len(bullets)} bullets — keep to ~4 one-liners.")


def check_iteration(spec):
    """Iteration sheets (No.2, No.3 …) must open with a previous-results
    Check table, judge each measure, and never silently drop an item."""
    import re as _re
    title = str(spec.get("meta", {}).get("title", ""))
    m = _re.search(r"[Nn]o\.?\s*(\d+)", title)
    cycle = int(m.group(1)) if m else 1
    cp = spec.get("current_problems", {})
    table = cp.get("table") if isinstance(cp, dict) else None
    bg = spec.get("background", {})
    bg_table = bg.get("table") if isinstance(bg, dict) else None
    results = table or bg_table

    if cycle >= 2 and not results:
        warn("iteration: title says No.%d but no previous-results (Check) table "
             "found in section 1 or 2 — an iteration sheet must OPEN with "
             "last round's countermeasures and their results." % cycle)
        return
    if not results:
        return  # round 1: nothing to check

    rows = results.get("rows", [])
    flat_rows = [" ".join(str(c) for c in r) for r in rows]
    unjudged = [r[:18] for r in flat_rows
                if not any(s in r for s in JUDGE_MARKS)]
    if unjudged:
        warn("iteration: %d result row(s) lack a 判定 mark (◎○△×－): e.g. '%s…' "
             "— judge EFFECT, not just implementation (実施≠効果)."
             % (len(unjudged), unjudged[0]))
    dropped = [r for r in flat_rows if any(w in r for w in DROPPED_WORDS)]
    if dropped:
        whole = _flat_text(spec)
        if not any(w in whole for w in RETRIGGER_WORDS):
            warn("iteration: a previous countermeasure is 未実施/保留/中止 but no "
                 "re-trigger condition found anywhere in the spec — dropped "
                 "items (especially ▲) need a documented 'if X happens, "
                 "reactivate' condition, not silent deletion.")


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            spec = json.load(f)
    except Exception as e:  # noqa: BLE001
        print(f"[ERROR] cannot read spec: {e}", file=sys.stderr)
        return 2

    _, triangles = check_five_whys(spec)
    check_traceability(spec, triangles)
    check_goals(spec)
    check_timeline_verification(spec)
    check_cost(spec)
    check_iteration(spec)

    for m in WARN:
        print(f"[WARN] {m}", file=sys.stderr)
    for m in INFO:
        print(f"[INFO] {m}", file=sys.stderr)
    if not WARN and not INFO:
        print("[OK] spec passes all content-quality checks.", file=sys.stderr)
    elif not WARN:
        print("[OK] no warnings (see INFO notes).", file=sys.stderr)
    return 1 if WARN else 0


if __name__ == "__main__":
    sys.exit(main())
