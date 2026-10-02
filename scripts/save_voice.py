"""Save a designed voice preview as a permanent voice, then test it with TTS."""
import json, os, pathlib, sys, requests
_ROOT = pathlib.Path(__file__).resolve().parent.parent
def fail(msg):
    (_ROOT / "auditions" / "save_voice_error.txt").write_text(msg)
    sys.exit(msg)
API = "https://api.elevenlabs.io"
H = {"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"}
ROOT = pathlib.Path(__file__).resolve().parent.parent
job = json.loads((ROOT / "jobs" / "save_voice.json").read_text())
body = {"voice_name": job["name"], "voice_description": job["description"],
        "generated_voice_id": job["generated_voice_id"]}
vid, errs = None, []
for path in ("/v1/text-to-voice", "/v1/text-to-voice/create", "/v1/text-to-voice/create-voice-from-preview"):
    r = requests.post(API + path, headers=H, json=body, timeout=120)
    if r.status_code == 200 and r.json().get("voice_id"):
        vid = r.json()["voice_id"]; break
    errs.append(f"{path}: {r.status_code} {r.text[:200]}")
if not vid:
    fail("\n".join(errs))
cfg_path = ROOT / "config" / "channel.json"
cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
cfg["narrator"] = {"name": job["name"], "voice_id": vid, "model_id": "eleven_v3",
                   "description": job["description"]}
cfg_path.write_text(json.dumps(cfg, indent=2))
out = ROOT / "auditions" / "narrator-test.mp3"
r = requests.post(f"{API}/v1/text-to-speech/{vid}", params={"output_format": "mp3_44100_128"},
                  headers=H, json={"text": job["test_text"], "model_id": "eleven_v3"}, timeout=180)
if r.status_code != 200:
    fail(f"saved {vid} but TTS failed: {r.status_code} {r.text[:300]}")
out.write_bytes(r.content)
print("saved voice", vid)
