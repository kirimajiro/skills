# -*- coding: utf-8 -*-
"""Run the t2i benchmark sheets through GPT-Image 2.5 (the reference model) via an external
generate script that calls the OpenAI Images API (the repository owner's private helper; not included).

GPT-Image version of run_t2i.py. Reads benchmarks/t2i/NN-<slug>.md (generic prompt, aspect,
style variants), writes each prompt verbatim to _local/gpt-image-2-5/prompts/<stem>.txt and
calls the generate script once per image, saving <stem>.png into benchmarks/_local/gpt-image-2-5/t2i/.
Only the raw variant is generated: the reference model has no skill, so there is no enhanced prompt.

Usage (from the repo root, where the dotenvx-encrypted .env with OPENAI_API_KEY lives):
  python benchmarks/scripts/run_gptimg.py [--only 01,05,16] [--dry-run]
      [--model gpt-image-2.5-sunburst-2026-09-08] [--quality high] [--generate-py <path>]
  python benchmarks/scripts/run_gptimg.py --i2i [--only 02,04] [--dry-run]
      runs the i2i sheets (benchmarks/i2i/, raw only) through images.edit with the sheet's refs
      passed as --ref, into _local/gpt-image-2-5/i2i/<NN>-<slug>-raw_00001.png.
  python benchmarks/scripts/run_gptimg.py --refs 4 [--only 01,03] [--dry-run]
      generates N candidates per spec in benchmarks/refs/README.md (768x1024, long edge 1024 as the
      spec requires) into _local/gpt-image-2-5/refs/ref-NN-cand_0000K.png; the user picks one per
      spec and copies it to benchmarks/refs/ref-NN.png.

The API has no seed parameter, so every file is numbered _00001 and a run is not reproducible
beyond the pinned model snapshot. Existing files are skipped, so an interrupted run resumes.
Prompts refused by moderation are recorded in run.json and skipped; any other API error aborts.

Stdlib only. Requires uv + dotenvx on PATH and a generate script given by --generate-py or the
GPTIMG_GENERATE_PY environment variable. The script is invoked as
  uv run <generate.py> --via api -f <prompt.txt> --out-dir <dir> --model <id> --size WxH --quality <q> --name <stem> [--ref <png>]...
and must write <dir>/<stem>.png and print "[info] usage: input=<n> output=<n> total=<n>" to stderr;
a moderation refusal must mention one of REFUSAL_MARKERS. Any script with that contract works.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run_t2i import jobs_for, load_sheets  # noqa: E402  (same sheet parsing as the ComfyUI runner)
from run_i2i import load_sheets as load_i2i_sheets  # noqa: E402

BENCH = HERE.parent
REPO = BENCH.parent
MODEL_SLUG = "gpt-image-2-5"
OUT_ROOT = BENCH / "_local" / MODEL_SLUG / "t2i"
PROMPT_DIR = BENCH / "_local" / MODEL_SLUG / "prompts"
REFS_OUT = BENCH / "_local" / MODEL_SLUG / "refs"
I2I_OUT = BENCH / "_local" / MODEL_SLUG / "i2i"
REFS_SIZE = "768x1024"  # 3:4 with the long edge at 1024 px, as refs/README.md requires

# Fixed conditions (tasks/benchmarks/issues/04). Dated snapshot for reproducibility; high for all 26.
DEFAULT_MODEL = "gpt-image-2.5-sunburst-2026-09-08"
DEFAULT_QUALITY = "high"
# Official presets where one exists, else a custom WxH (both edges multiples of 16, >= 655,360 px).
SIZES = {
    "1:1": "1024x1024",
    "3:2": "1536x1024",
    "2:3": "1024x1536",
    "3:4": "864x1152",
    "16:9": "1344x752",
}
# Dry-run cost estimate only. OpenAI publishes token rates but no per-image table for 2.5
# (docs/research/2026-09_gpt-image-2-5-api.md), so the table holds output tokens measured on
# 2026-09-23 (constant per size, not proportional to pixels); unmeasured quality/size pairs fall back
# to the plugin's unofficial 1024x1024 figures scaled by pixel count. Actual usage goes into run.json.
IMAGE_OUTPUT_USD_PER_TOKEN = 30 / 1e6
MEASURED_OUTPUT_TOKENS = {"high": {"1024x1024": 1756, "1536x1024": 1372, "1024x1536": 1372,
                                   "864x1152": 1294, "1344x752": 976}}
COST_1024_USD = {"low": 0.006, "medium": 0.013, "high": 0.053, "xhigh": 0.09, "max": 0.21}

REFUSAL_MARKERS = ("content_policy_violation", "moderation_blocked", "safety system")


def find_generate_py(explicit):
    spec = explicit or os.environ.get("GPTIMG_GENERATE_PY", "")
    if not spec:
        sys.exit("no generate script: pass --generate-py <path> or set GPTIMG_GENERATE_PY (see the module docstring)")
    p = Path(spec)
    if not p.is_file():
        sys.exit(f"generate script not found: {p}")
    return p


def load_ref_specs(only):
    """[(nn, prompt)] from the ### ref-NN sections of benchmarks/refs/README.md."""
    md = (BENCH / "refs" / "README.md").read_text(encoding="utf-8")
    specs = []
    for m in re.finditer(r"\n### ref-(\d\d)\n(.*?)(?=\n### |\Z)", md, re.S):
        nn, body = m.group(1), m.group(2)
        if only and nn not in only:
            continue
        specs.append((nn, re.search(r"```text\n(.*?)\n```", body, re.S).group(1)))
    return specs


def est_cost(quality, size):
    tokens = MEASURED_OUTPUT_TOKENS.get(quality, {}).get(size)
    if tokens:
        return tokens * IMAGE_OUTPUT_USD_PER_TOKEN
    w, h = (int(x) for x in size.split("x"))
    return COST_1024_USD[quality] * (w * h) / (1024 * 1024)


def run_one(cmd, timeout):
    """Run generate.py; return (returncode, stderr_text)."""
    t0 = time.time()
    proc = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout)
    return proc.returncode, proc.stderr, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="comma-separated sheet numbers, e.g. 01,05")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--quality", default=DEFAULT_QUALITY, choices=list(COST_1024_USD))
    ap.add_argument("--generate-py", default="", help="generate script (default: $GPTIMG_GENERATE_PY)")
    ap.add_argument("--timeout", type=int, default=600, help="seconds per image")
    ap.add_argument("--i2i", action="store_true", help="run the i2i sheets (raw only, images.edit with the sheet's refs)")
    ap.add_argument("--refs", type=int, default=0, metavar="N",
                    help="generate N candidates per spec in refs/README.md instead of the t2i sheets")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    gen = find_generate_py(a.generate_py)
    dotenvx, uv = shutil.which("dotenvx"), shutil.which("uv")
    if not a.dry_run and not (dotenvx and uv):
        sys.exit("dotenvx and uv must be on PATH")
    if not (REPO / ".env").is_file():
        print(f"WARNING: {REPO / '.env'} not found; dotenvx will not inject OPENAI_API_KEY", file=sys.stderr)

    only = {s.strip().zfill(2) for s in a.only.split(",") if s.strip()}
    if a.refs:
        out_root, sizes = REFS_OUT, {"3:4": REFS_SIZE}
        jobs = [(f"ref-{nn}", f"ref-{nn}-cand_{k:05d}", prompt, REFS_SIZE, [])
                for nn, prompt in load_ref_specs(only) for k in range(1, a.refs + 1)]
    elif a.i2i:
        # "follow ref-01" keeps the reference's 768x1024; other aspects use the t2i size table
        out_root, sizes = I2I_OUT, {"follow ref-01": REFS_SIZE, **SIZES}
        jobs = []
        for sheet in load_i2i_sheets(only):
            size = REFS_SIZE if sheet["aspect"].startswith("follow") else SIZES[sheet["aspect"]]
            refs = [str((BENCH / "refs" / f"{r}.png").resolve()) for r in sheet["refs"]]
            jobs.append((sheet["id"], f"{sheet['nn']}-{sheet['slug']}-raw_00001", sheet["generic"], size, refs))
    else:
        out_root, sizes = OUT_ROOT, SIZES
        jobs = []
        for sheet in load_sheets(only):
            if sheet["aspect"] not in SIZES:
                sys.exit(f"no size for aspect {sheet['aspect']} ({sheet['id']}); add it to SIZES")
            for label, prompt, _n in jobs_for(sheet, {}, ["raw"], "1"):
                jobs.append((sheet["id"], f"{sheet['nn']}-{sheet['slug']}-{label}_00001", prompt, SIZES[sheet["aspect"]], []))
    print(f"model={a.model} quality={a.quality} sizes={sizes} generate.py={gen}")

    run_log = {}
    if (out_root / "run.json").is_file():
        run_log = json.loads((out_root / "run.json").read_text(encoding="utf-8"))
    results = run_log.get("images", {})
    refused = {r["file"]: r for r in run_log.get("refused", [])}

    planned = done = skipped = 0
    est_total = 0.0
    for sid, stem, prompt, size, refs in jobs:
        dest = out_root / f"{stem}.png"
        if dest.exists():
            skipped += 1
            continue
        planned += 1
        est_total += est_cost(a.quality, size)
        print(f"{dest.name}  {size}  ~${est_cost(a.quality, size):.3f}" + (f"  refs={[Path(r).name for r in refs]}" if refs else ""))
        if a.dry_run:
            continue
        PROMPT_DIR.mkdir(parents=True, exist_ok=True)
        out_root.mkdir(parents=True, exist_ok=True)
        pfile = PROMPT_DIR / f"{stem}.txt"
        pfile.write_text(prompt, encoding="utf-8")
        cmd = [dotenvx, "run", "--", uv, "run", str(gen), "--via", "api", "-f", str(pfile),
               "--out-dir", str(out_root), "--model", a.model, "--size", size,
               "--quality", a.quality, "--name", stem]
        for r in refs:
            cmd += ["--ref", r]
        rc, err, secs = run_one(cmd, a.timeout)
        tail = [ln for ln in err.splitlines() if ln.startswith(("[saved]", "[done]", "ERROR", "[info] usage"))]
        print("\n".join("  " + ln for ln in tail))
        if rc == 0 and dest.exists():
            m = re.search(r"usage: input=(\S+) output=(\S+) total=(\S+)", err)
            results[dest.name] = dict(model=a.model, quality=a.quality, size=size, seconds=round(secs, 1),
                                      usage=dict(zip(("input", "output", "total"), m.groups())) if m else None)
            refused.pop(dest.name, None)
            done += 1
        elif any(k in err for k in REFUSAL_MARKERS):
            reason = next((ln for ln in err.splitlines() if ln.startswith("ERROR")), err[-300:])
            print(f"  REFUSED {dest.name}: {reason}", file=sys.stderr)
            refused[dest.name] = dict(file=dest.name, id=sid, reason=reason.strip())
        else:
            print(err, file=sys.stderr)
            sys.exit(f"generate.py failed (rc={rc}) on {dest.name}; fix and re-run to resume")
        # write the log after every image so an interrupted run keeps what it did
        out_root.mkdir(parents=True, exist_ok=True)
        (out_root / "run.json").write_text(json.dumps(dict(
            model_slug=MODEL_SLUG, model=a.model, quality=a.quality, seed="none (API has no seed parameter)",
            sizes=sizes, route="generate.py --via api (OpenAI Images API)", generate_py=str(gen),
            last_run=date.today().isoformat(), images=results, refused=list(refused.values()),
        ), indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"planned {planned}, generated {done}, already present {skipped}, refused {len(refused)}, "
          f"est. ~${est_total:.2f} for the planned images, output {out_root}")


if __name__ == "__main__":
    main()
