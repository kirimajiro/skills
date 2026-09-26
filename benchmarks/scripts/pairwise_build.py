"""Build a single static HTML for pairwise judging from t2i sheets and _local/ images.

Usage:
  python benchmarks/scripts/pairwise_build.py --mode ab --a krea-2-turbo --b flux-2-klein-9b [--variant enhanced|raw] [--baseline show|hide]
  python benchmarks/scripts/pairwise_build.py --mode raw-enh --a krea-2-turbo [--baseline show|hide]
  python benchmarks/scripts/pairwise_build.py --mode vs-baseline --a krea-2-turbo [--variant enhanced|raw]
  common: [--only 05,06,21] [--seed 1] [--out benchmarks/_local/pairwise/<session-id>.html]

Standard library only. Prints ASCII only (safe on cp932 consoles).
"""
import argparse
import datetime as dt
import json
import os
import random
import re
import sys
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
LOCAL = BENCH / "_local"
OUT_DIR = LOCAL / "pairwise"
TEMPLATE = Path(__file__).with_name("pairwise_template.html")
BASELINE_MODEL = "gpt-image-2-5"


# ---------- sheets ----------

def parse_frontmatter(text):
    """Line-based parser for the sheet frontmatter, including the `pairwise:` list."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fm, pairwise, cur = {}, [], None
    for line in m.group(1).splitlines():
        if line.startswith("  - aspect:"):
            cur = {"aspect": line.split(":", 1)[1].strip()}
            pairwise.append(cur)
        elif line.startswith("    q:") and cur is not None:
            cur["q"] = line.split(":", 1)[1].strip()
        elif not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    fm["pairwise"] = pairwise
    return fm, text[m.end():]


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def load_sheets(only):
    sheets = []
    for path in sorted((BENCH / "t2i").glob("[0-9][0-9]-*.md")):
        nn = path.name[:2]
        if only and nn not in only:
            continue
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        title = re.search(r"^# \d\d (.+)$", body, re.M).group(1)
        generic = re.search(r"```text\n(.*?)\n```", body, re.S).group(1)
        styles = None
        if "variants" in fm:
            styles = [v.strip() for v in fm["variants"].strip("[]").split(",")]
        if not fm["pairwise"]:
            raise SystemExit(f"{path.name}: no pairwise: block (ticket 10)")
        sheets.append(dict(nn=nn, slug=path.stem[3:], id=fm["id"], title=title,
                           summary=fm.get("summary", ""), generic=generic,
                           styles=styles, questions=fm["pairwise"]))
    return sheets


def aspect_table():
    """id -> Japanese name, from the README aspect-set table."""
    md = (BENCH / "README.md").read_text(encoding="utf-8")
    sec = md.split("## 観点セット", 1)[1].split("\n## ", 1)[0]
    out = {}
    for row in re.findall(r"^\| ([a-z]+) \| ([^|]+) \|", sec, re.M):
        out[row[0]] = row[1].strip()
    return out


# ---------- images ----------

def image_path(model, sheet, variant, style, seed):
    name = f"{sheet['nn']}-{sheet['slug']}-{variant}"
    if style:
        name += f"-{slugify(style)}"
    return LOCAL / model / "t2i" / f"{name}_{seed:05d}.png"


def rel(path, out_dir):
    return Path(os.path.relpath(path, out_dir)).as_posix()


# ---------- build ----------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["ab", "raw-enh", "vs-baseline"])
    ap.add_argument("--a", help="model slug for side A")
    ap.add_argument("--b", help="model slug for side B (mode ab)")
    ap.add_argument("--variant", default="enhanced", choices=["enhanced", "raw"])
    ap.add_argument("--baseline", default="hide", choices=["show", "hide"])
    ap.add_argument("--baseline-model", default=BASELINE_MODEL)
    ap.add_argument("--only", help="comma-separated sheet numbers, e.g. 05,06,21")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--out")
    ap.add_argument("--rebuild", help="re-apply the template to an existing HTML, keeping its session data")
    args = ap.parse_args()

    if args.rebuild:
        src = Path(args.rebuild)
        m = re.search(r"const DATA = (.*?);\nconst KEY", src.read_text(encoding="utf-8"), re.S)
        src.write_text(TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", m.group(1)), encoding="utf-8")
        print(f"rebuilt {src} (session {json.loads(m.group(1))['session']['id']})")
        return

    if not args.mode or not args.a:
        ap.error("--mode and --a are required (unless --rebuild)")
    if args.mode == "ab":
        if not args.b:
            ap.error("--mode ab needs --b")
        a = {"model": args.a, "variant": args.variant}
        b = {"model": args.b, "variant": args.variant}
    elif args.mode == "raw-enh":
        a = {"model": args.a, "variant": "enhanced"}
        b = {"model": args.a, "variant": "raw"}
    else:
        a = {"model": args.a, "variant": args.variant}
        b = {"model": args.baseline_model, "variant": "raw"}
        args.baseline = "hide"

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M")
    session_id = f"{args.mode}_{args.a}" + (f"_{b['model']}" if b["model"] != args.a else "") + f"_{stamp}"
    rng = random.Random(session_id)
    only = set(args.only.split(",")) if args.only else None
    out = Path(args.out) if args.out else OUT_DIR / f"{session_id}.html"
    out_dir = out.resolve().parent

    items, skipped = [], []
    for sheet in load_sheets(only):
        for style in (sheet["styles"] or [None]):
            pa = image_path(a["model"], sheet, a["variant"], style, args.seed)
            pb = image_path(b["model"], sheet, b["variant"], style, args.seed)
            pbase = image_path(args.baseline_model, sheet, "raw", style, args.seed) if args.baseline == "show" else None
            missing = [p for p in (pa, pb) if not p.exists()]
            if missing:
                skipped.append((sheet["id"], style, [m.name for m in missing]))
                continue
            if pbase is not None and not pbase.exists():
                pbase = None
            swap = rng.random() < 0.5
            left, right = (("b", pb), ("a", pa)) if swap else (("a", pa), ("b", pb))
            items.append({
                "problem": sheet["id"], "style": style,
                "title": sheet["title"], "summary": sheet["summary"],
                "prompt": sheet["generic"].replace("{style}", style) if style else sheet["generic"],
                "left": {"side": left[0], "img": rel(left[1], out_dir)},
                "right": {"side": right[0], "img": rel(right[1], out_dir)},
                "baseline": rel(pbase, out_dir) if pbase else None,
                "questions": sheet["questions"],
            })

    if not items:
        raise SystemExit("no items: check --a/--b and images under _local/")

    data = {
        "session": {"id": session_id, "mode": args.mode, "a": a, "b": b,
                    "baseline_shown": any(i["baseline"] for i in items),
                    "created": dt.datetime.now().isoformat(timespec="seconds")},
        "aspects": aspect_table(),
        "items": items,
    }
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")

    n_q = sum(len(i["questions"]) for i in items)
    print(f"session {session_id}")
    print(f"A = {a['model']} ({a['variant']})  B = {b['model']} ({b['variant']})  baseline shown = {data['session']['baseline_shown']}")
    print(f"items {len(items)}, questions {n_q}")
    for pid, style, names in skipped:
        print(f"skipped {pid}" + (f" [{style}]" if style else "") + ": missing " + ", ".join(names))
    print(f"out {out}")


if __name__ == "__main__":
    main()
