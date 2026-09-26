# -*- coding: utf-8 -*-
"""Run the t2i benchmark sheets through a local ComfyUI server.

Reads benchmarks/t2i/NN-<slug>.md (generic prompt, samples, aspect, variants) and
benchmarks/results/<model>/t2i.md (enhanced prompts), submits each prompt x variant x seed
to ComfyUI via its HTTP API, and downloads the images into benchmarks/_local/<model>/t2i/.

Usage:
  python benchmarks/scripts/run_t2i.py --model qwen-image-2-1 --api-json <exported API json>
      [--server http://127.0.0.1:8188] [--only 01,05,16] [--variants raw,enhanced]
      [--seeds 1|4|sheet] [--dry-run]

Seeds start at 1 and the ComfyUI filename counter equals the seed
(Bench/<model>/t2i/<NN>-<slug>-<variant>_00003_.png is seed 3), so keep ComfyUI's
output folder for this model free of other files with the same prefixes.

Stdlib only. Requires the ComfyUI API-format export of the workflow (Dev mode -> Export (API)).
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BENCH = HERE.parent

# Node ids inside each model's exported API json. Add an entry per model-slug when a new
# workflow is exported; keys other than "sampler" may be omitted when the workflow has no such input.
NODE_MAPS = {
    "qwen-image-2-1": {
        "prompt": ("459:452", "prompt"),          # TextEncodeQwenImage21.prompt
        "negative": ("459:452", "negative_prompt"),
        "width": ("459:456", "width"),            # EmptyLatentImage
        "height": ("459:456", "height"),
        "seed": ("470", "seed"),                  # Seed node feeding KSampler
        "prefix": ("461", "filename_prefix"),     # SaveImageAdvanced
        "sampler": "459:458",                     # KSampler, read for the run log
    },
    "krea-2-turbo": {
        "prompt": ("30:19", "value"),             # PrimitiveStringMultiline (user prompt; enhancer switch 30:24 stays False)
        "width": ("30:5", "width"),               # EmptyLatentImage
        "height": ("30:5", "height"),
        "seed": ("30:3", "seed"),                 # KSampler.seed directly
        "prefix": ("29", "filename_prefix"),      # SaveImage
        "sampler": "30:3",
    },
    "flux-2-klein-9b": {
        "prompt": ("75:74", "text"),              # CLIPTextEncode (positive)
        "negative": ("75:67", "text"),            # CLIPTextEncode (negative), kept empty
        "width": ("75:68", "value"),              # PrimitiveInt feeding Flux2Scheduler and EmptyFlux2LatentImage
        "height": ("75:69", "value"),
        "seed": ("75:73", "noise_seed"),          # RandomNoise
        "prefix": ("9", "filename_prefix"),       # SaveImage
        # settings are spread over several nodes instead of one KSampler
        "settings": {"steps": ("75:62", "steps"), "cfg": ("75:63", "cfg"),
                     "sampler_name": ("75:61", "sampler_name"), "scheduler": ("75:62", None)},
    },
}
NODE = {}

# ~1 MP, multiples of 16, matching Qwen-Image-2.1's supported ratios.
SIZES = {
    "1:1": (1024, 1024),
    "3:2": (1216, 816),
    "2:3": (816, 1216),
    "4:3": (1152, 864),
    "3:4": (864, 1152),
    "16:9": (1344, 752),
    "9:16": (752, 1344),
}


def parse_frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    fm = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def text_blocks(md):
    return re.findall(r"```text\n(.*?)\n```", md, re.S)


def load_sheets(only):
    sheets = []
    for path in sorted((BENCH / "t2i").glob("[0-9][0-9]-*.md")):
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        nn = path.name[:2]
        if only and nn not in only:
            continue
        samples = int(re.match(r"\d+", fm["samples"]).group(0))
        variants = None
        if "variants" in fm:
            variants = [v.strip() for v in fm["variants"].strip("[]").split(",")]
        sheets.append(dict(nn=nn, slug=path.stem[3:], id=fm["id"], aspect=fm["aspect"],
                           samples=samples, style_variants=variants, generic=text_blocks(body)[0]))
    return sheets


def load_enhanced(model):
    """Map id -> prompt (str) or {style: prompt} for style-variant sheets."""
    path = BENCH / "results" / model / "t2i.md"
    if not path.exists():
        return {}
    md = path.read_text(encoding="utf-8")
    out = {}
    for sec in re.split(r"\n### ", md)[1:]:
        pid = sec.split()[0]
        if "Enhanced prompts" in sec:
            pairs = re.findall(r"\n- (.+?)\n\n```text\n(.*?)\n```", sec, re.S)
            out[pid] = {k.strip(): v for k, v in pairs}
        else:
            blocks = text_blocks(sec)
            if blocks:
                out[pid] = blocks[0]
    return out


def jobs_for(sheet, enhanced, variants, seeds):
    """Yield (variant_label, prompt, n_seeds) for one sheet."""
    n = sheet["samples"] if seeds == "sheet" else int(seeds)
    styles = sheet["style_variants"]
    for variant in variants:
        if styles:
            for style in styles:
                label = f"{variant}-{slugify(style)}"
                if variant == "raw":
                    prompt = sheet["generic"].replace("{style}", style)
                else:
                    prompt = (enhanced.get(sheet["id"]) or {}).get(style)
                if prompt:
                    yield label, prompt, n
                else:
                    print(f"  skip {sheet['id']} {label}: no enhanced prompt", file=sys.stderr)
        else:
            prompt = sheet["generic"] if variant == "raw" else enhanced.get(sheet["id"])
            if prompt:
                yield variant, prompt, n
            else:
                print(f"  skip {sheet['id']} {variant}: no enhanced prompt", file=sys.stderr)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


class Comfy:
    def __init__(self, server):
        self.server = server.rstrip("/")
        self.client_id = "kirimajiro-bench"

    def _get(self, path):
        with urllib.request.urlopen(self.server + path, timeout=60) as r:
            return json.loads(r.read())

    def submit(self, workflow):
        data = json.dumps({"prompt": workflow, "client_id": self.client_id}).encode()
        req = urllib.request.Request(self.server + "/prompt", data=data,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            res = json.loads(r.read())
        if "prompt_id" not in res:
            raise RuntimeError(f"submit failed: {res}")
        return res["prompt_id"]

    def wait(self, prompt_id, timeout=1800):
        t0 = time.time()
        while time.time() - t0 < timeout:
            hist = self._get(f"/history/{prompt_id}")
            if prompt_id in hist:
                entry = hist[prompt_id]
                status = entry.get("status", {})
                if status.get("status_str") == "error":
                    raise RuntimeError(f"ComfyUI error: {json.dumps(status)[:500]}")
                images = []
                for node_out in entry.get("outputs", {}).values():
                    images += node_out.get("images", [])
                if images:
                    return images
            time.sleep(2)
        raise TimeoutError(prompt_id)

    def download(self, image, dest):
        q = urllib.parse.urlencode({"filename": image["filename"], "subfolder": image.get("subfolder", ""),
                                    "type": image.get("type", "output")})
        with urllib.request.urlopen(f"{self.server}/view?{q}", timeout=120) as r:
            dest.write_bytes(r.read())


def set_input(wf, key, value):
    if key not in NODE:
        return
    node, field = NODE[key]
    wf[node]["inputs"][field] = value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--api-json", required=True)
    ap.add_argument("--server", default="http://127.0.0.1:8188")
    ap.add_argument("--only", default="", help="comma-separated sheet numbers, e.g. 01,05")
    ap.add_argument("--variants", default="raw,enhanced")
    ap.add_argument("--seeds", default="1", help="seeds per prompt: a number (default 1) or 'sheet' to use each sheet's samples")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.model not in NODE_MAPS:
        sys.exit(f"no node map for {a.model}; add it to NODE_MAPS in {__file__}")
    NODE.update(NODE_MAPS[a.model])
    base = json.loads(Path(a.api_json).read_text(encoding="utf-8"))
    for key, spec in NODE.items():
        if key in ("sampler", "settings"):
            continue
        node, field = spec
        if node not in base or field not in base[node]["inputs"]:
            sys.exit(f"node map mismatch: {key} -> {node}.{field} not in {a.api_json}")
    only = {s.strip().zfill(2) for s in a.only.split(",") if s.strip()}
    variants = [v.strip() for v in a.variants.split(",") if v.strip()]
    sheets = load_sheets(only)
    enhanced = load_enhanced(a.model)
    out_root = BENCH / "_local" / a.model / "t2i"
    comfy = Comfy(a.server)

    if "settings" in NODE:
        settings = {}
        for k, (node, field) in NODE["settings"].items():
            settings[k] = base[node]["inputs"].get(field) if field else base[node]["class_type"]
    else:
        ks = base[NODE["sampler"]]["inputs"]
        settings = {k: ks[k] for k in ("steps", "cfg", "sampler_name", "scheduler")}
    settings["megapixels"] = "~1.0 (see SIZES)"
    print("settings:", settings)

    total = done = 0
    for sheet in sheets:
        w, h = SIZES[sheet["aspect"]]
        for label, prompt, n in jobs_for(sheet, enhanced, variants, a.seeds):
            stem = f"{sheet['nn']}-{sheet['slug']}-{label}"
            for seed in range(1, n + 1):
                total += 1
                dest = out_root / f"{stem}_{seed:05d}.png"
                if dest.exists():
                    continue
                print(f"{dest.name}  {w}x{h}")
                if a.dry_run:
                    continue
                wf = json.loads(json.dumps(base))
                set_input(wf, "prompt", prompt)
                set_input(wf, "negative", "")
                set_input(wf, "width", w)
                set_input(wf, "height", h)
                set_input(wf, "seed", seed)
                # Flat layout in ComfyUI's own output folder; its counter becomes the seed number.
                set_input(wf, "prefix", f"Bench/{a.model}/t2i/{stem}")
                pid = comfy.submit(wf)
                images = comfy.wait(pid)
                m = re.search(r"_(\d+)_?\.png$", images[0]["filename"])
                if not m or int(m.group(1)) != seed:
                    print(f"  WARNING: ComfyUI wrote {images[0]['filename']} but seed is {seed}; "
                          f"clear stale files under Bench/{a.model}/t2i/ in ComfyUI's output folder", file=sys.stderr)
                out_root.mkdir(parents=True, exist_ok=True)
                comfy.download(images[0], dest)
                done += 1
    if not a.dry_run:
        (out_root / "run.json").write_text(json.dumps(dict(model=a.model, settings=settings, sizes=SIZES,
                                                            api_json=str(a.api_json)), indent=2, ensure_ascii=False),
                                          encoding="utf-8")
    print(f"planned {total}, generated {done}, output {out_root}")


if __name__ == "__main__":
    main()
