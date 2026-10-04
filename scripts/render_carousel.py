"""Render an Instagram carousel (1080x1350 JPEG slides) from pilots/<case>/carousel.json.

carousel.json:
{"case": "011", "slides": [
  {"type": "hook", "text": "THE FBI MEMO\\nWRITTEN THE NEXT\\nNIGHT", "sub": "ALCATRAZ · 12 JUNE 1962", "photo": "photo-x.jpg" (optional bg)},
  {"type": "doc", "page": "doc-002.png", "lines": [[x0,y0,x1,y1], ...], "label": "FBI MEMO · 12 JUNE 1962", "caption": "One or two short sentences."},
  {"type": "photo", "photo": "photo-x.jpg", "focus": [0.5,0.4], "fit": "contain"?, "label": "...", "caption": "..."},
  {"type": "text", "text": "BIG LINE", "sub": "smaller line", "red": true},
  {"type": "end"}
]}
Writes pilots/<case>/carousel/slide-NN.jpg.  Usage: python scripts/render_carousel.py 011
"""
import io, json, pathlib, sys, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDIR = ROOT / "pilots" / sys.argv[1]
A, OUT = PDIR / "assets", PDIR / "carousel"
SPEC = json.loads((PDIR / "carousel.json").read_text())
FONTS = ROOT / "fonts"
W, H = 1080, 1350
INK, MANILA, RED, MUTED, PAPER = (17, 20, 24), (234, 219, 184), (224, 74, 43), (150, 143, 128), (238, 229, 208)


def font(name, size, wght=None):
    f = ImageFont.truetype(str(FONTS / name), size)
    if wght: f.set_variation_by_axes([wght])
    return f

F_HOOK = font("BigShouldersDisplay[wght].ttf", 128, 800)
F_TEXT = font("BigShouldersDisplay[wght].ttf", 96, 800)
F_CAP = font("IBMPlexMono-Medium.ttf", 34)
F_MONO = font("IBMPlexMono-SemiBold.ttf", 28)
F_SMALL = font("IBMPlexMono-Medium.ttf", 24)


def mark(size):
    import cairosvg
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="222 230 376 368"><path d="M230 278 L230 252 Q230 238 244 238 '
           'L318 238 L344 270 L430 270 A160 160 0 0 1 430 590 L246 590 Q230 590 230 574 Z" fill="#EADBB8"/><rect x="280" y="345" '
           'width="240" height="40" fill="#111418"/><rect x="280" y="415" width="130" height="40" fill="#111418"/><rect x="422" '
           'y="415" width="118" height="40" fill="#E04A2B"/><rect x="280" y="485" width="190" height="40" fill="#111418"/></svg>')
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=size,
                                                  output_height=int(size * 368 / 376)))).convert("RGBA")

M_SMALL, M_BIG = mark(44), mark(260)
N = len(SPEC["slides"])


def centered(d, y, text, f, fill, spacing=1.0):
    for ln in text.split("\n"):
        tw = d.textlength(ln, font=f); d.text(((W - tw) / 2, y), ln, font=f, fill=fill)
        y += int(f.size * spacing)
    return y


def chrome(im, i):
    d = ImageDraw.Draw(im)
    im.paste(M_SMALL, (48, 40), M_SMALL)
    d.text((104, 50), f"DOSSIER DECODED · CASE FILE #{SPEC['case']}", font=F_SMALL, fill=MANILA)
    s = f"{i + 1}/{N}"; d.text((W - 48 - d.textlength(s, font=F_SMALL), 50), s, font=F_SMALL, fill=MUTED)
    if i < N - 1:
        s = "SWIPE →"; d.text((W - 48 - d.textlength(s, font=F_SMALL), H - 70), s, font=F_SMALL, fill=RED)


def caption(im, text, y0):
    """Manila panel with dark mono text; returns nothing. y0 = top of panel."""
    d = ImageDraw.Draw(im)
    lines = textwrap.wrap(text, 46)
    h = 44 + 46 * len(lines)
    d.rectangle([48, y0, W - 48, y0 + h], fill=MANILA)
    y = y0 + 22
    for ln in lines:
        d.text((76, y), ln, font=F_CAP, fill=INK); y += 46


def label(im, text, y):
    d = ImageDraw.Draw(im, "RGBA")
    tw = d.textlength(text, font=F_MONO)
    d.rectangle([(W - tw) / 2 - 16, y - 8, (W + tw) / 2 + 16, y + 40], fill=(10, 10, 12, 220))
    d.text(((W - tw) / 2, y), text, font=F_MONO, fill=MANILA)


def fit_cover(src, box_w, box_h, focus=(0.5, 0.5)):
    s = max(box_w / src.width, box_h / src.height)
    r = src.resize((int(src.width * s) + 1, int(src.height * s) + 1), Image.LANCZOS)
    x = int((r.width - box_w) * focus[0]); y = int((r.height - box_h) * focus[1])
    return r.crop((x, y, x + box_w, y + box_h))


def fit_contain(src, box_w, box_h, bg=INK):
    s = min(box_w / src.width, box_h / src.height)
    r = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    c = Image.new("RGB", (box_w, box_h), bg); c.paste(r, ((box_w - r.width) // 2, (box_h - r.height) // 2)); return c


BOX = (48, 120, W - 48, 1000)  # media area
BW, BH = BOX[2] - BOX[0], BOX[3] - BOX[1]


def slide(sc, i):
    im = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(im)
    t = sc["type"]
    if t == "hook":
        if sc.get("photo"):
            bg = fit_cover(Image.open(A / sc["photo"]).convert("RGB"), W, H, sc.get("focus", (0.5, 0.4)))
            bg = ImageOps.grayscale(bg).convert("RGB").filter(ImageFilter.GaussianBlur(2))
            im = Image.blend(bg, Image.new("RGB", (W, H), INK), 0.62); d = ImageDraw.Draw(im)
        n = sc["text"].count("\n") + 1
        y = centered(d, (H - n * 124) // 2 - 60, sc["text"], F_HOOK, MANILA, 0.97)
        if sc.get("sub"): centered(d, y + 30, sc["sub"], F_MONO, RED)
    elif t == "text":
        n = sc["text"].count("\n") + 1
        y = centered(d, (H - n * 100) // 2 - 80, sc["text"], F_TEXT, RED if sc.get("red") else MANILA, 1.0)
        if sc.get("sub"):
            for ln in textwrap.wrap(sc["sub"], 40):
                y = centered(d, y + 14, ln, F_CAP, MANILA)
    elif t in ("doc", "photo"):
        if t == "doc":
            pg = Image.open(A / sc["page"]).convert("RGB")
            L = sc["lines"]
            x0 = min(l[0] for l in L); x1 = max(l[2] for l in L); y0 = min(l[1] for l in L); y1 = max(l[3] for l in L)
            cw = max(x1 - x0 + 70, 560); ch = int(cw * BH / BW)
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            left = max(0, min(pg.width - cw, cx - cw / 2)); topy = max(0, min(pg.height - ch, cy - ch / 2))
            pad = Image.new("RGB", (max(pg.width, int(left + cw)), max(pg.height, int(topy + ch))), PAPER); pad.paste(pg)
            crop = pad.crop((int(left), int(topy), int(left + cw), int(topy + ch)))
            sc_ = BW / cw; media = crop.resize((BW, BH), Image.LANCZOS)
            md = ImageDraw.Draw(media, "RGBA")
            for (a, b, c, e) in L:
                r = ((a - left) * sc_ - 10, (b - topy) * sc_ - 8, (c - left) * sc_ + 10, (e - topy) * sc_ + 8)
                md.rectangle(r, fill=(224, 74, 43, 70)); md.rectangle((r[0], r[3] - 6, r[2], r[3]), fill=RED + (255,))
        else:
            src = Image.open(A / sc["photo"]).convert("RGB")
            media = fit_contain(src, BW, BH) if sc.get("fit") == "contain" else fit_cover(src, BW, BH, sc.get("focus", (0.5, 0.45)))
        im.paste(media, BOX[:2])
        if sc.get("label"): label(im, sc["label"], BOX[1] + 24)
        if sc.get("caption"): caption(im, sc["caption"], BOX[3] + 30)
    elif t == "end":
        im.paste(M_BIG, ((W - M_BIG.width) // 2, 230), M_BIG)
        y = centered(d, 540, "DOSSIER", F_HOOK, MANILA)
        y = centered(d, y + 4, "D E C O D E D", F_MONO, RED)
        y = centered(d, y + 90, sc.get("text", "THE FULL STORY IS IN OUR REEL"), F_CAP, MANILA)
        centered(d, y + 40, "FOLLOW · NEW FILE DAILY", F_MONO, RED)
    chrome(im, i)
    return im


OUT.mkdir(exist_ok=True)
for f in OUT.glob("slide-*.jpg"): f.unlink()
for i, sc in enumerate(SPEC["slides"]):
    p = OUT / f"slide-{i + 1:02d}.jpg"; slide(sc, i).save(p, quality=90); print(p)
