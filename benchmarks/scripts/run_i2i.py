# -*- coding: utf-8 -*-
"""Run the i2i benchmark sheets through a local ComfyUI server.

Reads benchmarks/i2i/NN-<slug>.md (generic instruction, refs, aspect, samples) and
benchmarks/results/<model>/i2i.md (enhanced prompts), uploads the reference images from
benchmarks/refs/ to ComfyUI, submits each instruction x variant x seed, and downloads the images
into benchmarks/_local/<model>/i2i/. Companion of run_t2i.py (same naming and seed rules).

Usage:
  python benchmarks/scripts/run_i2i.py --model qwen-image-2-1 --api-json <exported API json>
      [--server http://127.0.0.1:8188] [--only 01,02] [--variants raw,enhanced]
      [--seeds 1|4|sheet] [--dry-run]

Aspect "follow ref-01" keeps the size of the base image (the workflow's image-derived latent);
any other aspect switches to an empty latent of the SIZES entry from run_t2i.py.
Sheets with one ref get the second image input removed from the workflow.

Stdlib only.
"""
import argparse
import json
import mimetypes
import re
import sys
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from run_t2i import BENCH, SIZES, Comfy, parse_frontmatter, text_blocks  # noqa: E402

# Node ids inside each model's exported image-edit API json.
NODE_MAPS = {
    "qwen-image-2-1": {
        "prompt": ("459:474", "prompt"),              # TextEncodeQwenImage21
        "negative": ("459:474", "negative_prompt"),
        "images": ("459:474", ["images.image_1", "images.image_2"]),  # links to LoadImage nodes
        "loaders": ["470", "475"],                     # LoadImage nodes for image1 / image2
        "latent_switch": ("459:468", "switch"),        # False = latent from image1, True = empty latent
        "width": ("459:456", "width"),                 # EmptyLatentImage (linked to ResolutionSelector in the export)
        "height": ("459:456", "height"),
        "seed": ("459:458", "seed"),                   # KSampler
        "prefix": ("461", "filename_prefix"),          # SaveImageAdvanced
        "sampler": "459:458",
    },
}
REF_UPLOAD_NAME = "kirimajiro-{ref}.png"  # name inside ComfyUI's input folder


def load_sheets(only):
    sheets = []
    for path in sorted((BENCH / "i2i").glob("[0-9][0-9]-*.md")):
        fm, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        nn = path.name[:2]
        if only and nn not in only:
            continue
        refs = [r.strip() for r in fm["refs"].strip("[]").split(",")]
        sheets.append(dict(nn=nn, slug=path.stem[3:], id=fm["id"], aspect=fm["aspect"], refs=refs,
                           samples=int(re.match(r"\d+", fm["samples"]).group(0)), generic=text_blocks(body)[0]))
    return sheets


def load_enhanced(model):
    path = BENCH / "results" / model / "i2i.md"
    if not path.exists():
        return {}
    out = {}
    for sec in re.split(r"\n### ", path.read_text(encoding="utf-8"))[1:]:
        blocks = text_blocks(sec)
        if blocks:
            out[sec.split()[0]] = blocks[0]
    return out


def upload_image(server, path, name):
    """POST /upload/image (multipart, overwrite) so LoadImage can reference `name`."""
    boundary = uuid.uuid4().hex
    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    body = b"".join([
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
        f"Content-Type: {ctype}\r\n\r\n".encode(), path.read_bytes(), b"\r\n",
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n".encode(),
        f"--{boundary}--\r\n".encode(),
    ])
    req = urllib.request.Request(server.rstrip("/") + "/upload/image", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["name"]


def build(base, node, sheet, prompt, seed, prefix, uploaded):
    wf = json.loads(json.dumps(base))
    enc, image_fields = node["images"]
    for i, ref in enumerate(sheet["refs"]):
        wf[node["loaders"][i]]["inputs"]["image"] = uploaded[ref]
    for i in range(len(sheet["refs"]), len(image_fields)):  # drop unused image inputs and their loaders
        wf[enc]["inputs"].pop(image_fields[i], None)
        wf.pop(node["loaders"][i], None)
    for k in list(wf):  # drop nodes that referenced a removed loader (e.g. a preview/compare node)
        deps = [v[0] for v in wf[k]["inputs"].values() if isinstance(v, list) and len(v) == 2 and isinstance(v[0], str)]
        if any(d not in wf for d in deps):
            wf.pop(k)
    n, f = node["prompt"]; wf[n]["inputs"][f] = prompt
    if "negative" in node:
        n, f = node["negative"]; wf[n]["inputs"][f] = ""
    n, f = node["latent_switch"]
    if sheet["aspect"].startswith("follow"):
        wf[n]["inputs"][f] = False
    else:
        wf[n]["inputs"][f] = True
        w, h = SIZES[sheet["aspect"]]
        wf[node["width"][0]]["inputs"][node["width"][1]] = w
        wf[node["height"][0]]["inputs"][node["height"][1]] = h
    n, f = node["seed"]; wf[n]["inputs"][f] = seed
    n, f = node["prefix"]; wf[n]["inputs"][f] = prefix
    return wf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--api-json", required=True)
    ap.add_argument("--server", default="http://127.0.0.1:8188")
    ap.add_argument("--only", default="")
    ap.add_argument("--variants", default="raw,enhanced")
    ap.add_argument("--seeds", default="1", help="a number (default 1) or 'sheet' for each sheet's samples")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.model not in NODE_MAPS:
        sys.exit(f"no node map for {a.model}; add it to NODE_MAPS in {__file__}")
    node = NODE_MAPS[a.model]
    base = json.loads(Path(a.api_json).read_text(encoding="utf-8"))
    checks = [node["prompt"], node["negative"], node["latent_switch"], node["width"], node["height"], node["seed"], node["prefix"]]
    checks += [(node["images"][0], f) for f in node["images"][1]]
    for n, f in checks:
        if n not in base or f not in base[n]["inputs"]:
            sys.exit(f"node map mismatch: {n}.{f} not in {a.api_json}")
    for n in node["loaders"]:
        if base.get(n, {}).get("class_type") != "LoadImage":
            sys.exit(f"node map mismatch: {n} is not a LoadImage node")

    only = {s.strip().zfill(2) for s in a.only.split(",") if s.strip()}
    variants = [v.strip() for v in a.variants.split(",") if v.strip()]
    sheets = load_sheets(only)
    enhanced = load_enhanced(a.model)
    out_root = BENCH / "_local" / a.model / "i2i"
    comfy = Comfy(a.server)
    ks = base[node["sampler"]]["inputs"]
    settings = {k: ks[k] for k in ("steps", "cfg", "sampler_name", "scheduler", "denoise")}
    settings["size"] = "follow ref-01 -> base image size; other aspects -> SIZES (~1 MP)"
    print("settings:", settings)

    uploaded = {}
    if not a.dry_run:
        for ref in sorted({r for s in sheets for r in s["refs"]}):
            uploaded[ref] = upload_image(a.server, BENCH / "refs" / f"{ref}.png", REF_UPLOAD_NAME.format(ref=ref))
        print("uploaded refs:", uploaded)

    total = done = 0
    for sheet in sheets:
        n_seeds = sheet["samples"] if a.seeds == "sheet" else int(a.seeds)
        for variant in variants:
            prompt = sheet["generic"] if variant == "raw" else enhanced.get(sheet["id"])
            if not prompt:
                print(f"  skip {sheet['id']} {variant}: no enhanced prompt", file=sys.stderr)
                continue
            stem = f"{sheet['nn']}-{sheet['slug']}-{variant}"
            for seed in range(1, n_seeds + 1):
                total += 1
                dest = out_root / f"{stem}_{seed:05d}.png"
                if dest.exists():
                    continue
                size = "base image size" if sheet["aspect"].startswith("follow") else "x".join(map(str, SIZES[sheet["aspect"]]))
                print(f"{dest.name}  refs={sheet['refs']}  {size}")
                if a.dry_run:
                    continue
                wf = build(base, node, sheet, prompt, seed, f"Bench/{a.model}/i2i/{stem}", uploaded)
                images = comfy.wait(comfy.submit(wf))
                m = re.search(r"_(\d+)_?\.png$", images[0]["filename"])
                if not m or int(m.group(1)) != seed:
                    print(f"  WARNING: ComfyUI wrote {images[0]['filename']} but seed is {seed}; "
                          f"clear stale files under Bench/{a.model}/i2i/ in ComfyUI's output folder", file=sys.stderr)
                out_root.mkdir(parents=True, exist_ok=True)
                comfy.download(images[0], dest)
                done += 1
    if not a.dry_run:
        (out_root / "run.json").write_text(json.dumps(dict(model=a.model, settings=settings, sizes=SIZES,
                                                            refs=uploaded, api_json=str(a.api_json)),
                                                       indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"planned {total}, generated {done}, output {out_root}")


if __name__ == "__main__":
    main()
