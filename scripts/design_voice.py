"""Design unique channel voices with ElevenLabs Voice Design (v3).

Reads jobs/design.json, writes preview MP3s + summary to auditions/<run>/.
A variant may use one of OUR OWN earlier designed clips as reference audio.
"""
import base64
import json
import os
import pathlib
import sys

import requests

API = "https://api.elevenlabs.io"
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"}
ROOT = pathlib.Path(__file__).resolve().parent.parent
JOB = json.loads((ROOT / "jobs" / "design.json").read_text())
OUT = ROOT / "auditions" / JOB["run"]
OUT.mkdir(parents=True, exist_ok=True)
summary = {"text": JOB["text"], "candidates": [], "errors": []}

n = 1
for v in JOB["variants"]:
    body = {
        "voice_description": v["description"],
        "model_id": "eleven_ttv_v3",
        "text": JOB["text"],
        "guidance_scale": v.get("guidance_scale", 5),
    }
    if v.get("reference"):
        body["reference_audio_base64"] = base64.b64encode((ROOT / v["reference"]).read_bytes()).decode()
        body["prompt_strength"] = v.get("prompt_strength", 0.5)
    if "seed" in v:
        body["seed"] = v["seed"]
    r = requests.post(f"{API}/v1/text-to-voice/design", headers=H, json=body, timeout=240)
    if r.status_code != 200:
        summary["errors"].append(f"{v['slug']}: {r.status_code} {r.text[:300]}")
        continue
    for i, p in enumerate(r.json().get("previews", [])[: v.get("keep", 1)]):
        audio = p.get("audio_base_64") or p.get("audio_base64")
        f = OUT / f"{n}-{v['slug']}{'-' + str(i + 1) if v.get('keep', 1) > 1 else ''}.mp3"
        f.write_bytes(base64.b64decode(audio))
        summary["candidates"].append({"n": n, "slug": v["slug"], "file": f.name,
                                      "generated_voice_id": p.get("generated_voice_id"),
                                      "description": v["description"],
                                      "reference": v.get("reference"),
                                      "prompt_strength": v.get("prompt_strength")})
        n += 1

(OUT / "summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))
if not summary["candidates"]:
    sys.exit("no audio produced")
