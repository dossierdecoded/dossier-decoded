"""Render a Dossier Decoded Short from pilots/<n>/{scenes.json,assets/}.

Pure Python + PIL + ffmpeg. 1080x1920 @ 30 fps.
Usage: python scripts/render_pilot.py 001 [--preview SECONDS...]
"""
import json, math, pathlib, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDIR = ROOT / "pilots" / sys.argv[1]
A = PDIR / "assets"
SPEC = json.loads((PDIR / "scenes.json").read_text())
FONTS = ROOT / "fonts"  # OFL fonts committed to the repo (Big Shoulders Display, IBM Plex Mono)
W, H, FPS = 1080, 1920, 30
INK, MANILA, RED, MUTED = (17, 20, 24), (234, 219, 184), (224, 74, 43), (150, 143, 128)
PAPER_DARK, PAPER_LIGHT = (28, 26, 24), (238, 229, 208)
VOICE_OFFSET, TAIL = 0.35, 2.6
VIEW = (60, 300, 1020, 1400)  # x0,y0,x1,y1 of the media panel


def font(name, size, wght=None):
    f = ImageFont.truetype(str(FONTS / name), size)
    if wght:
        f.set_variation_by_axes([wght])
    return f

F_BIG = font("BigShouldersDisplay[wght].ttf", 104, 800)
F_CARD = font("BigShouldersDisplay[wght].ttf", 168, 800)
F_MONO = font("IBMPlexMono-SemiBold.ttf", 30)
F_MONO_S = font("IBMPlexMono-Medium.ttf", 26)
F_STAMP = font("IBMPlexMono-SemiBold.ttf", 76)

# ---------- words + timings ----------
al = json.loads((A / "alignment.json").read_text())
chars, cst, cen = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
words, cur, depth = [], None, 0
for ch, s, e in zip(chars, cst, cen):
    if ch == "[":
        depth += 1; continue
    if ch == "]":
        depth -= 1; continue
    if depth:
        continue
    if ch.isspace():
        if cur: words.append(cur); cur = None
        continue
    if cur is None:
        cur = {"text": ch, "start": s, "end": e}
    else:
        cur["text"] += ch; cur["end"] = e
if cur: words.append(cur)
for w in words:
    w["start"] += VOICE_OFFSET; w["end"] += VOICE_OFFSET
norm = lambda t: re.sub(r"[^a-z0-9']", "", t.lower().replace("’", "'"))
VOICE_END = words[-1]["end"]
DUR = VOICE_END + TAIL


def find(word, start_idx):
    for i in range(start_idx, len(words)):
        if norm(words[i]["text"]) == norm(word):
            return i
    raise SystemExit(f"word not found: {word!r} after #{start_idx}")

scenes, idx = SPEC["scenes"], 0
for sc in scenes:
    idx = find(sc["at"], idx)
    sc["t0"] = 0.0 if not scenes.index(sc) else words[idx]["start"] - 0.08
    sc["i0"] = idx
    for key in ("reveal", "stamp_at"):
        if key in sc:
            sc[key + "_t"] = words[find(sc[key], idx)]["start"]
    sc["sfx_t"] = [(name, words[find(w, idx)]["start"]) for name, w in sc.get("sfx_at", [])]
for a, b in zip(scenes, scenes[1:]):
    a["t1"] = b["t0"]
scenes[-1]["t1"] = DUR

# caption groups: break on punctuation or every 3 words
groups, g = [], []
for i, w in enumerate(words):
    g.append(i)
    if len(g) >= 3 or re.search(r"[.,?!:;\"…]$", w["text"]) or w["text"].endswith("..."):
        groups.append(g); g = []
if g: groups.append(g)
end_start = next(s for s in scenes if s["type"] == "end")["t0"]

# ---------- asset prep ----------
_cache = {}
def paper(name):
    if name not in _cache:
        im = Image.open(A / name).convert("L")
        im = ImageOps.autocontrast(im, cutoff=1)
        _cache[name] = ImageOps.colorize(im, PAPER_DARK, PAPER_LIGHT).convert("RGB")
    return _cache[name]

def photo(name):
    if name not in _cache:
        im = Image.open(A / name).convert("L")
        im = ImageOps.autocontrast(im, cutoff=1)
        _cache[name] = ImageOps.colorize(im, (12, 12, 14), (232, 224, 205)).convert("RGB")
    return _cache[name]

def ease(x):
    x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

VW, VH = VIEW[2] - VIEW[0], VIEW[3] - VIEW[1]
_vig = None
def vignette():
    global _vig
    if _vig is None:
        m = Image.new("L", (VW, VH), 0)
        ImageDraw.Draw(m).rounded_rectangle([40, 40, VW - 40, VH - 40], 60, fill=255)
        _vig = m.filter(ImageFilter.GaussianBlur(70))
    return _vig

def crop_fit(src, cx, cy, cw, ch, zoom, pad_col=PAPER_LIGHT):
    """crop a (cw/zoom x ch/zoom) window centred on cx,cy, sized to the view aspect."""
    asp = VW / VH
    if cw / ch > asp: ch = cw / asp
    else: cw = ch * asp
    cw, ch = cw / zoom, ch / zoom
    x0 = max(0, min(src.width - cw, cx - cw / 2)); y0 = max(0, min(src.height - ch, cy - ch / 2))
    if cw > src.width or ch > src.height:  # pad
        pad = Image.new("RGB", (int(max(cw, src.width)) + 2, int(max(ch, src.height)) + 2), pad_col)
        pad.paste(src, (0, 0)); src = pad
    return src.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((VW, VH), Image.LANCZOS), (x0, y0, cw / VW)


def draw_doc(fr, sc, t):
    pg = paper(sc["page"])
    x0, y0, x1, y1 = sc["window"]
    p = (t - sc["t0"]) / max(0.1, sc["t1"] - sc["t0"])
    z = sc["zoom"][0] + (sc["zoom"][1] - sc["zoom"][0]) * ease(p)
    lines = sc.get("lines", [])
    if lines:
        cx = sum((l[0] + l[2]) / 2 for l in lines) / len(lines); cy = sum((l[1] + l[3]) / 2 for l in lines) / len(lines)
        cx = (cx + (x0 + x1) / 2) / 2; cy = (cy + (y0 + y1) / 2) / 2
    else:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if lines:  # frame tightly around the highlighted lines so text is large on a phone
        lw = max(l[2] for l in lines) - min(l[0] for l in lines) + 90
        cx = (max(l[2] for l in lines) + min(l[0] for l in lines)) / 2
        cw = max(lw * z, 560); view, (ox, oy, sc_) = crop_fit(pg, cx, cy, cw, 10, z)
    else:
        view, (ox, oy, sc_) = crop_fit(pg, cx, cy, x1 - x0, y1 - y0, z)
    d = ImageDraw.Draw(view, "RGBA")
    rt = sc.get("reveal_t", sc["t0"] + 0.4)
    k = 1.0 if sc.get("instant") else ease((t - rt) / 0.45)  # instant: highlight already revealed (hook frame)
    for (lx0, ly0, lx1, ly1) in lines:
        a = ((lx0 - ox) / sc_ - 10, (ly0 - oy) / sc_ - 8, (lx1 - ox) / sc_ + 10, (ly1 - oy) / sc_ + 8)
        if k > 0:  # red marker under revealed text
            d.rectangle(a, fill=(224, 74, 43, int(70 * k)))
            d.rectangle((a[0], a[3] - 6, a[0] + (a[2] - a[0]) * k, a[3]), fill=RED + (255,))
        if k < 1:  # redaction bar wiping off left -> right
            d.rectangle((a[0] + (a[2] - a[0]) * k, a[1], a[2], a[3]), fill=(10, 10, 12, 255))
    fr.paste(Image.composite(view, Image.new("RGB", (VW, VH), INK), vignette()), VIEW[:2])
    if sc.get("label"):
        tag(fr, sc["label"], VIEW[1] + 24)


def draw_photo(fr, sc, t):
    im = photo(sc["photo"])
    p = (t - sc["t0"]) / max(0.1, sc["t1"] - sc["t0"])
    z = sc["zoom"][0] + (sc["zoom"][1] - sc["zoom"][0]) * ease(p)
    fx, fy = sc["focus"]
    if im.width / im.height > VW / VH and sc.get('fit') != 'contain':   # landscape: fill height, pan across
        cw, ch = im.height * VW / VH, im.height
    else:
        cw, ch = im.width, im.width * VH / VW
    view, _ = crop_fit(im, im.width * fx, im.height * fy, cw, ch, z, INK)
    fr.paste(Image.composite(view, Image.new("RGB", (VW, VH), INK), vignette()), VIEW[:2])
    if sc.get("label"):
        tag(fr, sc["label"], VIEW[3] - 70)
    if sc.get("stamp"):
        stamp(fr, sc["stamp"], t - sc.get("stamp_at_t", 1e9), (W // 2, VIEW[1] + int(VH * 0.74)))


def draw_card(fr, sc, t):
    d = ImageDraw.Draw(fr)
    k = ease((t - sc["t0"]) / 0.25)
    lines = sc["text"].split("\n")
    lh = 160; y = VIEW[1] + VH // 2 - lh * len(lines) // 2 - 40
    for ln in lines:
        tw = d.textlength(ln, font=F_CARD)
        col = RED if sc.get("red") and ln == lines[-1] else MANILA
        d.text(((W - tw) / 2, y + (1 - k) * 30), ln, font=F_CARD, fill=col)
        y += lh
    if sc.get("sub"):
        tw = d.textlength(sc["sub"], font=F_MONO)
        d.text(((W - tw) / 2, y + 30), sc["sub"], font=F_MONO, fill=MUTED)
    if sc.get("stamp"):
        stamp(fr, sc["stamp"], t - sc.get("stamp_at_t", 1e9), (W // 2, y + 190))


def stamp(fr, text, dt, center):
    if dt < 0: return
    k = ease(dt / 0.12); sc = 1.6 - 0.6 * k
    bw = int(F_STAMP.getlength(text)) + 70; bh = 120
    lay = Image.new("RGBA", (bw + 20, bh + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle([10, 10, bw + 10, bh + 10], outline=RED + (235,), width=8)
    d.text((45, 24), text, font=F_STAMP, fill=RED + (235,))
    lay = lay.resize((int(lay.width * sc), int(lay.height * sc))).rotate(-8, expand=True, resample=Image.BICUBIC)
    lay.putalpha(lay.getchannel("A").point(lambda a: int(a * min(1, k * 1.5))))
    fr.paste(lay, (center[0] - lay.width // 2, center[1] - lay.height // 2), lay)


def tag(fr, text, y):
    d = ImageDraw.Draw(fr, "RGBA")
    tw = d.textlength(text, font=F_MONO_S)
    d.rectangle([(W - tw) / 2 - 18, y - 10, (W + tw) / 2 + 18, y + 40], fill=(10, 10, 12, 210))
    d.text(((W - tw) / 2, y), text, font=F_MONO_S, fill=MANILA)


MARK = None
def mark(size):
    import cairosvg, io
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="222 230 376 368"><path d="M230 278 L230 252 Q230 238 244 238 '
           'L318 238 L344 270 L430 270 A160 160 0 0 1 430 590 L246 590 Q230 590 230 574 Z" fill="#EADBB8"/><rect x="280" y="345" '
           'width="240" height="40" fill="#111418"/><rect x="280" y="415" width="130" height="40" fill="#111418"/><rect x="422" '
           'y="415" width="118" height="40" fill="#E04A2B"/><rect x="280" y="485" width="190" height="40" fill="#111418"/></svg>')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=size, output_height=int(size * 368 / 376)))).convert("RGBA")

M_SMALL, M_BIG = mark(54), mark(300)


def draw_end(fr, sc, t):
    d = ImageDraw.Draw(fr)
    k = ease((t - sc["t0"]) / 0.4)
    fr.paste(M_BIG, ((W - M_BIG.width) // 2, 520 + int((1 - k) * 40)), M_BIG)
    for txt, f, col, y in [("DOSSIER", F_CARD, MANILA, 880), ("D E C O D E D", F_MONO, RED, 1060),
                           (f"CASE FILE #{SPEC['case']} · CLOSED", F_MONO_S, MUTED, 1140)]:
        tw = d.textlength(txt, font=f); d.text(((W - tw) / 2, y), txt, font=f, fill=col)
    if t > sc["t0"] + 1.2:
        q = "WHICH FILE NEXT? COMMENT ↓"
        tw = d.textlength(q, font=F_MONO); d.text(((W - tw) / 2, 1290), q, font=F_MONO, fill=MANILA)


def header(fr):
    d = ImageDraw.Draw(fr)
    fr.paste(M_SMALL, (60, 120), M_SMALL)
    d.text((132, 122), f"DOSSIER #{SPEC['case']}", font=F_MONO, fill=MANILA)
    d.text((132, 160), SPEC["title"], font=F_MONO_S, fill=MUTED)


def captions(fr, t):
    if t >= end_start: return
    gi = next((g for g in groups if words[g[0]]["start"] - 0.05 <= t <= words[g[-1]]["end"] + 0.25), None)
    if gi is None: return
    d = ImageDraw.Draw(fr)
    toks = [re.sub(r"[\"“”]", "", words[i]["text"]).upper().rstrip(",") for i in gi]
    sp = 24; widths = [d.textlength(x, font=F_BIG) for x in toks]
    total = sum(widths) + sp * (len(toks) - 1)
    lines = [list(range(len(toks)))] if total < W - 120 else [list(range(len(toks) - 1)), [len(toks) - 1]]
    y = 1480
    for ln in lines:
        lw = sum(widths[j] for j in ln) + sp * (len(ln) - 1); x = (W - lw) / 2
        for j in ln:
            i = gi[j]; active = words[i]["start"] <= t <= words[i]["end"] + 0.05
            for dx, dy in ((0, 5),):
                d.text((x + dx, y + dy), toks[j], font=F_BIG, fill=(0, 0, 0))
            d.text((x, y), toks[j], font=F_BIG, fill=RED if active else MANILA)
            x += widths[j] + sp
        y += 112


def frame(t):
    fr = Image.new("RGB", (W, H), INK)
    sc = next(s for s in scenes if s["t0"] <= t < s["t1"]) if t < DUR else scenes[-1]
    {"doc": draw_doc, "photo": draw_photo, "card": draw_card, "end": draw_end}[sc["type"]](fr, sc, t)
    if sc["type"] != "end":
        header(fr)
    captions(fr, t)
    return fr


def sfx_events():
    ev = []
    for sc in scenes:
        for name, at in sc.get("sfx", []):
            ev.append((name, sc["t0"] + at))
        ev += sc["sfx_t"]
        if sc["type"] == "doc" and "reveal_t" in sc:
            ev.append(("stamp", sc["reveal_t"]))
        if "stamp_at_t" in sc:
            ev.append(("stamp", sc["stamp_at_t"]))
        if sc["type"] == "doc" and scenes.index(sc) > 0:
            ev.append(("paper", sc["t0"]))
    return ev


if __name__ == "__main__":
    if "--preview" in sys.argv:
        out = []
        for ts in sys.argv[sys.argv.index("--preview") + 1:]:
            fr = frame(float(ts)); p = PDIR / f"preview-{ts}.jpg"; fr.save(p, quality=85); out.append(str(p))
        print("\n".join(out)); sys.exit()
    silent = PDIR / "video_noaudio.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                           "-pix_fmt", "yuv420p", str(silent)], stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        ff.stdin.write(frame(i / FPS).tobytes())
        if i % 150 == 0: print(f"frame {i}/{n}", flush=True)
    ff.stdin.close(); ff.wait()
    # ---- audio mix ----
    inputs = ["-i", str(silent), "-i", str(A / "voice.mp3"), "-stream_loop", "-1", "-i", str(A / "sfx-drone.mp3")]
    filt = [f"[1:a]adelay={int(VOICE_OFFSET*1000)}|{int(VOICE_OFFSET*1000)},volume=1.0[v]",
            f"[2:a]volume=0.16,atrim=0:{DUR:.2f},afade=t=in:d=1.2,afade=t=out:st={DUR-2:.2f}:d=2[dr]"]
    mixes = ["[v]", "[dr]"]
    vol = {"stamp": 0.55, "paper": 0.35, "typewriter": 0.45, "hit": 0.7}
    for k, (name, at) in enumerate(sfx_events()):
        f = A / f"sfx-{name}.mp3"
        if not f.exists(): continue
        inputs += ["-i", str(f)]; j = 3 + k
        ms = max(0, int(at * 1000))
        filt.append(f"[{j}:a]volume={vol.get(name, 0.5)},adelay={ms}|{ms}[s{k}]"); mixes.append(f"[s{k}]")
    filt.append("".join(mixes) + f"amix=inputs={len(mixes)}:normalize=0,alimiter=limit=0.95[a]")
    out = PDIR / f"{SPEC['case']}-final.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt), "-map", "0:v",
                    "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR:.2f}", str(out)], check=True)
    silent.unlink()
    (PDIR / "meta.json").write_text(json.dumps({"duration": round(DUR, 2)}))
    print("wrote", out)
