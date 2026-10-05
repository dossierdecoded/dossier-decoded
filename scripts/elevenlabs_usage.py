"""Write ElevenLabs subscription usage to metrics/elevenlabs.json (no secrets in output)."""
import json, os, pathlib, datetime as dt
import requests
ROOT = pathlib.Path(__file__).resolve().parent.parent
r = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"]}, timeout=60)
j = r.json() if r.ok else {"error": r.status_code, "body": r.text[:300]}
keep = {k: j.get(k) for k in ("tier", "character_count", "character_limit", "next_character_count_reset_unix", "status", "can_extend_character_limit", "voice_limit", "max_voice_add_edits") if k in j}
if "next_character_count_reset_unix" in keep and keep["next_character_count_reset_unix"]:
    keep["resets_at"] = dt.datetime.fromtimestamp(keep["next_character_count_reset_unix"], dt.timezone.utc).isoformat()
if "error" in j: keep = j
(ROOT / "metrics").mkdir(exist_ok=True)
(ROOT / "metrics" / "elevenlabs.json").write_text(json.dumps(keep, indent=1))
print(keep)
