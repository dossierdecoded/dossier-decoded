"""Fetch everything a pilot needs: narration + word timings, SFX, document scans, photos.
Writes into pilots/<n>/assets/. Errors go to assets/errors.txt (never raises)."""
import base64, json, os, pathlib, subprocess, sys, traceback, urllib.parse
import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDIR = ROOT / "pilots" / sys.argv[1]
JOB = json.loads((PDIR / "job.json").read_text())
A = PDIR / "assets"; A.mkdir(parents=True, exist_ok=True)
CFG = json.loads((ROOT / "config" / "channel.json").read_text())
EL = "https://api.elevenlabs.io"
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"}
UA = {"User-Agent": "DossierDecodedBot/1.0 (dossierdecoded@gmail.com)"}
errors, meta = [], {}

def step(name):
    def deco(fn):
        try:
            fn()
        except Exception:
            errors.append(f"[{name}]\n" + traceback.format_exc())
    return deco


GAP = 0.8  # seconds of silence between long-form chapters


def narrate_chapters():
    """Long-form: one TTS call per chapter (keeps each under the model's text limit), then join.
    Writes voice.mp3, alignment.json (merged, offset) and chapters.json [{title, start}]."""
    vid = CFG["narrator"]["voice_id"]; model = CFG["narrator"].get("model_id", "eleven_v3")
    chars, st, en, chaps, t0, parts = [], [], [], [], 0.0, []
    for i, ch in enumerate(JOB["chapters"], 1):
        f = A / f"voice-{i:02d}.mp3"
        if not f.exists() or not (A / f"alignment-{i:02d}.json").exists():
            r = requests.post(f"{EL}/v1/text-to-speech/{vid}/with-timestamps", headers=H, timeout=600,
                              json={"text": ch["text"], "model_id": model}, params={"output_format": "mp3_44100_192"})
            r.raise_for_status(); j = r.json()
            f.write_bytes(base64.b64decode(j["audio_base64"]))
            (A / f"alignment-{i:02d}.json").write_text(json.dumps(j.get("normalized_alignment") or j.get("alignment")))
        al = json.loads((A / f"alignment-{i:02d}.json").read_text())
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                   capture_output=True, text=True).stdout.strip())
        chaps.append({"title": ch["title"], "start": round(t0, 2)})
        if chars: chars.append(" "); st.append(t0 - 0.01); en.append(t0)
        chars += al["characters"]; st += [x + t0 for x in al["character_start_times_seconds"]]
        en += [x + t0 for x in al["character_end_times_seconds"]]
        parts.append(f); t0 += dur + GAP
    sil = A / "gap.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=mono", "-t", str(GAP), "-b:a", "192k", str(sil)],
                   check=True, capture_output=True)
    lst = A / "concat.txt"
    lst.write_text("".join(f"file '{p.name}'\n" + (f"file '{sil.name}'\n" if k < len(parts) - 1 else "") for k, p in enumerate(parts)))
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-ar", "44100", "-ac", "1", "-b:a", "192k",
                    str(A / "voice.mp3")], check=True, capture_output=True)
    (A / "alignment.json").write_text(json.dumps({"characters": chars, "character_start_times_seconds": st,
                                                  "character_end_times_seconds": en}))
    (A / "chapters.json").write_text(json.dumps(chaps, indent=1))
    meta["alignment_source"] = "chapters"

@step("narration")
def _():
    if JOB.get("chapters"):
        return narrate_chapters()
    vid = CFG["narrator"]["voice_id"]
    body = {"text": JOB["script"], "model_id": CFG["narrator"].get("model_id", "eleven_v3")}
    r = requests.post(f"{EL}/v1/text-to-speech/{vid}/with-timestamps", headers=H, json=body,
                      params={"output_format": "mp3_44100_192"}, timeout=300)
    if r.ok:
        j = r.json()
        (A / "voice.mp3").write_bytes(base64.b64decode(j["audio_base64"]))
        (A / "alignment.json").write_text(json.dumps(j.get("normalized_alignment") or j.get("alignment"), indent=1))
        meta["alignment_source"] = "with-timestamps"
        return
    errors.append(f"with-timestamps {r.status_code}: {r.text[:300]}")
    r = requests.post(f"{EL}/v1/text-to-speech/{vid}", headers=H, json=body,
                      params={"output_format": "mp3_44100_192"}, timeout=300)
    r.raise_for_status()
    (A / "voice.mp3").write_bytes(r.content)
    # forced alignment on the spoken text (tags removed)
    import re
    plain = re.sub(r"\[[^\]]+\]\s*", "", JOB["script"])
    fa = requests.post(f"{EL}/v1/forced-alignment", headers={"xi-api-key": H["xi-api-key"]},
                       files={"file": ("voice.mp3", r.content, "audio/mpeg")}, data={"text": plain}, timeout=300)
    fa.raise_for_status()
    (A / "alignment.json").write_text(json.dumps(fa.json(), indent=1))
    meta["alignment_source"] = "forced-alignment"

@step("sfx")
def _():
    for s in JOB["sfx"]:
        r = requests.post(f"{EL}/v1/sound-generation", headers=H, timeout=180,
                          json={"text": s["text"], "duration_seconds": s["seconds"], "prompt_influence": 0.5})
        if r.ok:
            (A / f"sfx-{s['slug']}.mp3").write_bytes(r.content)
        else:
            errors.append(f"sfx {s['slug']}: {r.status_code} {r.text[:200]}")

@step("pdf")
def _():
    if not JOB.get("pdf"): return
    r = requests.get(JOB["pdf"], headers=UA, timeout=120); r.raise_for_status()
    pdf = A / "source.pdf"; pdf.write_bytes(r.content)
    rng = JOB.get("pages")  # optional [first, last] to avoid rasterising huge files
    extra = ["-f", str(rng[0]), "-l", str(rng[1])] if rng else []
    subprocess.run(["pdftoppm", "-r", "150", *extra, "-png", str(pdf), str(A / "doc")], check=True)
    texts, boxes = {}, {}
    for png in sorted(A.glob("doc-*.png")):
        out = subprocess.run(["tesseract", str(png), "-", "--psm", "3"], capture_output=True, text=True)
        texts[png.name] = out.stdout
        tsv = subprocess.run(["tesseract", str(png), "-", "--psm", "3", "tsv"], capture_output=True, text=True).stdout
        lines = {}
        for row in tsv.splitlines()[1:]:
            c = row.split("\t")
            if len(c) < 12 or not c[11].strip() or float(c[10]) < 30: continue
            k = (c[2], c[3], c[4]); x, y, w, h = map(int, c[6:10])
            L = lines.setdefault(k, {"text": [], "box": [x, y, x + w, y + h]})
            L["text"].append(c[11]); b = L["box"]
            L["box"] = [min(b[0], x), min(b[1], y), max(b[2], x + w), max(b[3], y + h)]
        boxes[png.name] = [{"text": " ".join(v["text"]), "box": v["box"]} for v in lines.values()]
    (A / "ocr.json").write_text(json.dumps(texts, indent=1))
    (A / "ocr_lines.json").write_text(json.dumps(boxes, indent=1))  # line boxes in page pixels, for scenes.json "lines"
    pdf.unlink()  # keep repo small; pages are kept as PNG

@step("commons")
def _():
    lic, seen = [], set()
    for c in JOB.get("commons", []):
      for k in range(c.get("n", 1)):
        q = requests.get("https://commons.wikimedia.org/w/api.php", headers=UA, timeout=60, params={
            "action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
            "gsrsearch": c["query"], "gsrlimit": 15, "prop": "imageinfo",
            "iiprop": "url|extmetadata|size", "iiurlwidth": 1600}).json()
        pages = sorted(q.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
        for p in pages:
            if p["title"] in seen: continue
            ii = p["imageinfo"][0]; em = ii.get("extmetadata", {})
            lname = (em.get("LicenseShortName", {}).get("value") or "")
            if not ii.get("thumburl") or not any(kw in lname.lower() for kw in ("public domain", "pd", "cc0", "cc by")):
                continue
            img = requests.get(ii["thumburl"], headers=UA, timeout=120); img.raise_for_status()
            ext = ".png" if ii["thumburl"].lower().endswith(".png") else ".jpg"
            seen.add(p["title"]); slug = c["slug"] + (f"-{k+1}" if c.get("n", 1) > 1 else "")
            (A / f"photo-{slug}{ext}").write_bytes(img.content)
            lic.append({"slug": slug, "title": p["title"], "license": lname,
                        "artist": em.get("Artist", {}).get("value", "")[:200],
                        "page": ii.get("descriptionurl")})
            break
        else:
            errors.append(f"commons: nothing usable for {c['query']} #{k+1}")
    (A / "photo_licenses.json").write_text(json.dumps(lic, indent=1))

(A / "meta.json").write_text(json.dumps(meta, indent=1))
(A / "errors.txt").write_text("\n\n".join(errors) or "none")
print("\n".join(errors) or "all ok")
