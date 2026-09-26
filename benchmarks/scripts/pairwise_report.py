"""Aggregate pairwise session JSONs into a Markdown profile of one model.

Usage:
  python benchmarks/scripts/pairwise_report.py benchmarks/_local/pairwise/*.json [--model krea-2-turbo] [--out -]

- Sessions where the model is side B are flipped so every number is "the model's win rate".
- Win rate = (wins + 0.5 * ties) / n. Cells with n < 3 are marked with *.
- Standard library only. Use --out <file> on a cp932 console (stdout falls back to '?' for unencodable characters).
"""
import argparse
import collections
import glob
import json
import sys
from pathlib import Path

from pairwise_build import aspect_table

SYM = {1: "o", 0.5: "=", 0: "x"}  # model won / tie / model lost


def load(paths):
    sessions = []
    for pat in paths:
        for p in sorted(glob.glob(pat)) or [pat]:
            with open(p, encoding="utf-8") as f:
                s = json.load(f)
            s["_file"] = Path(p).name
            sessions.append(s)
    if not sessions:
        raise SystemExit("no session json")
    return sessions


def pick_model(sessions, model):
    if model:
        return model
    c = collections.Counter(s["session"]["a"]["model"] for s in sessions)
    return c.most_common(1)[0][0]


def opponent_label(sess, model):
    a, b, mode = sess["a"], sess["b"], sess["mode"]
    if mode == "raw-enh":
        return "raw vs enhanced"
    other = b if a["model"] == model else a
    if mode == "vs-baseline":
        return f"vs baseline ({other['model']})"
    return f"vs {other['model']}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("json", nargs="+", help="session JSON files or globs")
    ap.add_argument("--model", help="model slug to profile (default: most frequent side A)")
    ap.add_argument("--out", default="-", help="output file, or - for stdout")
    args = ap.parse_args()

    sessions = load(args.json)
    model = pick_model(sessions, args.model)
    aspects = aspect_table()

    # score[opponent][aspect] -> [wins, ties, losses]; per_problem[opponent][problem] -> [(aspect, value)]
    score = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 0]))
    per_problem = collections.defaultdict(lambda: collections.defaultdict(list))
    used, notes = [], []
    for s in sessions:
        sess = s["session"]
        if model not in (sess["a"]["model"], sess["b"]["model"]):
            continue
        # raw-enh: "the model" means its enhanced side, which build puts on A
        model_side = "a" if sess["mode"] == "raw-enh" or sess["a"]["model"] == model else "b"
        opp = opponent_label(sess, model)
        used.append((sess, opp, len(s["answers"]), s["_file"]))
        for ans in s["answers"]:
            if ans["choice"] == "tie":
                v = 0.5
            else:
                v = 1 if ans[ans["choice"]] == model_side else 0
            sc = score[opp][ans["aspect"]]
            sc[0 if v == 1 else 2 if v == 0 else 1] += 1
            key = ans["problem"] + (f" [{ans['style']}]" if ans.get("style") else "")
            per_problem[opp][key].append((ans["aspect"], v))
        n = s.get("notes") or {}
        if n.get("overall") or n.get("by_aspect"):
            notes.append((sess["id"], opp, n))

    if not used:
        raise SystemExit(f"model {model} appears in no session")

    opps = list(dict.fromkeys(o for _, o, _, _ in used))
    aspect_order = [a for a in aspects if any(a in score[o] for o in opps)]
    aspect_order += sorted({a for o in opps for a in score[o]} - set(aspect_order))

    def cell(sc):
        n = sum(sc)
        if n == 0:
            return "-"
        r = (sc[0] + 0.5 * sc[1]) / n
        return f"{r:.2f} ({sc[0]}/{sc[1]}/{sc[2]}, n={n}{' *' if n < 3 else ''})"

    out = [f"# {model} — pairwise profile", ""]
    out += ["## Sessions", "", "| session | opponent | answers | finished |", "|---|---|---|---|"]
    for sess, opp, n, fname in used:
        out.append(f"| {sess['id']} | {opp} | {n} | {sess.get('finished', sess.get('created', ''))[:16]} |")
    out += ["", "## Aspect profile", "",
            f"Cell = win rate of {model} (win / tie / loss, n). Tie counts 0.5. * = n < 3.", "",
            "| aspect | " + " | ".join(opps) + " |", "|---|" + "---|" * len(opps)]
    for a in aspect_order:
        out.append(f"| {a} {aspects.get(a, '')} | " + " | ".join(cell(score[o][a]) for o in opps) + " |")

    re_key = "raw vs enhanced"
    if re_key in score:
        rows = []
        for a in aspect_order:
            sc = score[re_key][a]
            n = sum(sc)
            if n:
                rows.append(((sc[0] + 0.5 * sc[1]) / n - 0.5, a, n))
        up = [r for r in sorted(rows, reverse=True) if r[0] > 0]
        down = [r for r in sorted(rows) if r[0] < 0]
        flat = [r for r in rows if r[0] == 0]
        out += ["", "## Enhance effect (enhanced vs raw)", ""]
        out.append("- raised: " + (", ".join(f"{a} ({d:+.2f}, n={n})" for d, a, n in up) or "none"))
        out.append("- lowered: " + (", ".join(f"{a} ({d:+.2f}, n={n})" for d, a, n in down) or "none"))
        if flat:
            out.append("- unchanged: " + ", ".join(f"{a} (n={n})" for _, a, n in flat))

    out += ["", "## By problem", "", "o = model won, = tie, x = model lost.", "",
            "| problem | " + " | ".join(opps) + " |", "|---|" + "---|" * len(opps)]
    problems = list(dict.fromkeys(p for o in opps for p in per_problem[o]))
    problems.sort()
    weak = collections.defaultdict(list)
    for p in problems:
        cells = []
        for o in opps:
            vals = per_problem[o].get(p, [])
            cells.append(" ".join(f"{SYM[v]}{a}" for a, v in vals) or "-")
            losses, wins = [v for _, v in vals].count(0), [v for _, v in vals].count(1)
            if losses >= 2 and losses > wins:
                weak[o].append(f"{p} ({losses}/{len(vals)})")
        out.append(f"| {p} | " + " | ".join(cells) + " |")
    out += ["", "Problems where losses concentrate (losses >= 2 and > wins):"]
    for o in opps:
        out.append(f"- {o}: " + (", ".join(weak[o]) or "none"))

    if notes:
        out += ["", "## Notes (verbatim from sessions)", ""]
        for sid, opp, n in notes:
            out.append(f"### {sid} ({opp})")
            out.append("")
            if n.get("overall"):
                out.append(f"- overall: {n['overall']}")
            for a, v in (n.get("by_aspect") or {}).items():
                out.append(f"- {a}: {v}")
            out.append("")

    text = "\n".join(out).rstrip() + "\n"
    if args.out == "-":
        try:
            sys.stdout.reconfigure(errors="replace")
        except AttributeError:
            pass
        sys.stdout.write(text)
    else:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
