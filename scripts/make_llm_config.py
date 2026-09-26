"""Generate comfyui-llm-session config JSONs whose system_prompt is a lite skill file.

Usage:
  python scripts/make_llm_config.py --base <base-config.json> --out-dir <llm-configs dir> [LITE.md ...]

- LITE files default to every skills/*/SKILL-lite-*.md in the repository.
- Each output is named <plugin>-<mode>.json (from skills/<plugin>/SKILL-lite-<mode>.md) and is the base
  config with only `system_prompt` replaced by the lite file's text. Re-run after editing a lite file.
- A file given as <name>=<path> uses <name>.json instead of the derived name (for prompts kept outside skills/).

Standard library only. Prints ASCII only.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def derive_name(path):
    m = re.match(r"SKILL-lite-(.+)\.md$", path.name)
    if m and path.parent.parent.name == "skills":
        return f"{path.parent.name}-{m.group(1)}"
    raise SystemExit(f"{path}: not a skills/<plugin>/SKILL-lite-<mode>.md file; pass it as <name>=<path>")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True, help="existing config JSON to copy settings from")
    ap.add_argument("--out-dir", required=True, help="directory for the generated JSONs (e.g. ComfyUI/user/llm-configs)")
    ap.add_argument("lite", nargs="*", help="lite files, or <name>=<path>; default: all skills/*/SKILL-lite-*.md")
    args = ap.parse_args()

    base = json.loads(Path(args.base).read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    items = []
    if args.lite:
        for spec in args.lite:
            name, _, path = spec.partition("=")
            if path:
                items.append((name, Path(path)))
            else:
                p = Path(name)
                items.append((derive_name(p), p))
    else:
        for p in sorted(ROOT.glob("skills/*/SKILL-lite-*.md")):
            items.append((derive_name(p), p))

    for name, path in items:
        text = path.read_text(encoding="utf-8").strip("\n")
        if text.startswith("---"):
            raise SystemExit(f"{path}: has frontmatter; lite files must not")
        cfg = dict(base)
        cfg["system_prompt"] = text
        out = out_dir / f"{name}.json"
        out.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out}  ({len(text)} chars from {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path})")


if __name__ == "__main__":
    main()
