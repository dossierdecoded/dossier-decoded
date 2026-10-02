"""Publish a Reel via the Instagram API with Instagram Login.
Reads pilots/<n>/instagram_job.json {video_url, caption}; writes pilots/<n>/instagram.json."""
import json, os, pathlib, sys, time, traceback
import requests

G = "https://graph.instagram.com/v23.0"
ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "pilots" / sys.argv[1]
job = json.loads((P / "instagram_job.json").read_text())
TOKEN = os.environ["IG_ACCESS_TOKEN"]
res = {"ok": False, "steps": []}


def call(method, path, **params):
    params["access_token"] = TOKEN
    r = requests.request(method, G + path, params=params if method == "GET" else None,
                         data=params if method == "POST" else None, timeout=120)
    res["steps"].append({"call": f"{method} {path}", "status": r.status_code, "body": r.text[:500]})
    r.raise_for_status()
    return r.json()

try:
    me = call("GET", "/me", fields="user_id,username")
    uid = me.get("user_id") or me["id"]
    res["username"] = me.get("username")
    c = call("POST", f"/{uid}/media", media_type="REELS", video_url=job["video_url"],
             caption=job["caption"], share_to_feed="true")
    cid = c["id"]
    for _ in range(60):  # wait up to ~10 min for Instagram to process the video
        st = call("GET", f"/{cid}", fields="status_code,status")
        if st.get("status_code") == "FINISHED":
            break
        if st.get("status_code") in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"container {st}")
        time.sleep(10)
    pub = call("POST", f"/{uid}/media_publish", creation_id=cid)
    info = call("GET", f"/{pub['id']}", fields="permalink")
    res.update({"ok": True, "media_id": pub["id"], "permalink": info.get("permalink")})
except Exception:
    res["error"] = traceback.format_exc()[-1500:]
res["steps"] = res["steps"][-8:]
(P / "instagram.json").write_text(json.dumps(res, indent=2))
print(json.dumps(res, indent=2))
