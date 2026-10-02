"""Voice audition: renders the same hook in several candidate voices.

Reads jobs/audition.json, writes MP3s and a summary to auditions/<run>/.
Candidates: professional Voice Library narrators (filtered for low overuse,
long notice period, no custom rate) plus custom Voice Design voices.
"""
import base64
import json
import os
import pathlib
import sys
import time

import requests

API = "https://api.elevenlabs.io"
KEY = os.environ["ELEVENLABS_API_KEY"]
H = {"xi-api-key": KEY}
ROOT = pathlib.Path(__file__).resolve().parent.parent
JOB = json.loads((ROOT / "jobs" / "audition.json").read_text())
OUT = ROOT / "auditions" / JOB["run"]
OUT.mkdir(parents=True, exist_ok=True)
summary = {"text": JOB["text"], "candidates": [], "errors": []}


def log(*a):
    print(*a, flush=True)


def tts(voice_id, path):
    r = requests.post(
        f"{API}/v1/text-to-speech/{voice_id}",
        params={"output_format": "mp3_44100_128"},
        headers={**H, "Content-Type": "application/json"},
        json={"text": JOB["text"], "model_id": JOB.get("tts_model", "eleven_v3")},
        timeout=180,
    )
    if r.status_code != 200:
        raise RuntimeError(f"TTS {r.status_code}: {r.text[:300]}")
    path.write_bytes(r.content)


# ---------- 1. Voice Library candidates ----------
def search(params):
    base = {"page_size": 100, "category": "professional", "language": "en"}
    base.update(params)
    r = requests.get(f"{API}/v1/shared-voices", headers=H, params=base, timeout=60)
    if r.status_code != 200:
        summary["errors"].append(f"search {params}: {r.status_code} {r.text[:200]}")
        return []
    return r.json().get("voices", [])


pool = {}
for q in JOB["library_queries"]:
    for v in search(q):
        pool[v.get("voice_id")] = v
log(f"library pool: {len(pool)} voices")
if pool:
    log("voice fields:", sorted(next(iter(pool.values())).keys()))


def ok(v):
    if v.get("rate") not in (None, 0, 1, 1.0):  # no custom credit multiplier
        return False
    np_ = v.get("notice_period")
    if np_ is not None and np_ < JOB.get("min_notice_days", 365):
        return False
    return True


cands = [v for v in pool.values() if ok(v)]
cands.sort(key=lambda v: v.get("cloned_by_count") or 0, reverse=True)
skip = JOB.get("skip_most_popular", 10)  # avoid the voices every channel uses
cands = cands[skip:]
picked, n_by_gender = [], {}
for v in cands:
    g = (v.get("gender") or "unknown").lower()
    if n_by_gender.get(g, 0) >= JOB["library_per_gender"].get(g, 0):
        continue
    picked.append(v)
    n_by_gender[g] = n_by_gender.get(g, 0) + 1
    if len(picked) >= sum(JOB["library_per_gender"].values()):
        break

idx = 1
for v in picked:
    name = v.get("name", "voice")
    meta = {
        "n": idx, "kind": "library", "name": name, "voice_id": v.get("voice_id"),
        "public_owner_id": v.get("public_owner_id"), "gender": v.get("gender"),
        "accent": v.get("accent"), "age": v.get("age"), "descriptive": v.get("descriptive"),
        "use_case": v.get("use_case"), "cloned_by_count": v.get("cloned_by_count"),
        "notice_period": v.get("notice_period"), "description": (v.get("description") or "")[:200],
    }
    path = OUT / f"{idx:02d}-library-{name.split()[0].lower()}.mp3"
    try:
        add = requests.post(
            f"{API}/v1/voices/add/{v['public_owner_id']}/{v['voice_id']}",
            headers={**H, "Content-Type": "application/json"},
            json={"new_name": f"DD audition {idx} - {name}"[:60]}, timeout=60,
        )
        vid = add.json().get("voice_id") if add.status_code == 200 else None
        if not vid:
            raise RuntimeError(f"add {add.status_code}: {add.text[:200]}")
        meta["my_voice_id"] = vid
        tts(vid, path)
        meta["file"] = path.name
    except Exception as e:  # fall back to the owner's preview clip
        summary["errors"].append(f"{name}: {e}")
        if v.get("preview_url"):
            path = path.with_name(path.stem + "-PREVIEW-own-text.mp3")
            path.write_bytes(requests.get(v["preview_url"], timeout=60).content)
            meta["file"] = path.name
            meta["note"] = "owner's preview text, not our script"
    summary["candidates"].append(meta)
    idx += 1
    time.sleep(1)

# ---------- 2. Custom designed voices ----------
for d in JOB["designs"]:
    try:
        r = requests.post(
            f"{API}/v1/text-to-voice/design",
            headers={**H, "Content-Type": "application/json"},
            json={"voice_description": d["description"], "model_id": "eleven_ttv_v3",
                  "text": JOB["design_text"]},
            timeout=180,
        )
        if r.status_code != 200:
            raise RuntimeError(f"design {r.status_code}: {r.text[:300]}")
        prev = r.json()["previews"][0]
        path = OUT / f"{idx:02d}-custom-{d['slug']}.mp3"
        path.write_bytes(base64.b64decode(prev["audio_base_64"] if "audio_base_64" in prev else prev["audio_base64"]))
        summary["candidates"].append({
            "n": idx, "kind": "custom", "name": d["slug"], "description": d["description"],
            "generated_voice_id": prev.get("generated_voice_id"), "file": path.name,
        })
    except Exception as e:
        summary["errors"].append(f"design {d['slug']}: {e}")
    idx += 1

(OUT / "summary.json").write_text(json.dumps(summary, indent=2))
log(json.dumps(summary, indent=2))
if not any("file" in c for c in summary["candidates"]):
    sys.exit("no audio produced")
