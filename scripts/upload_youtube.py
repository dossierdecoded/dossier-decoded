"""Upload a rendered pilot to YouTube via the Data API (resumable upload).
Reads pilots/<n>/publish.json; writes pilots/<n>/youtube.json with the result."""
import json, os, pathlib, sys, traceback
import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "pilots" / sys.argv[1]
pub = json.loads((P / "publish.json").read_text())
out = P / "youtube.json"
try:
    tok = requests.post("https://oauth2.googleapis.com/token", timeout=60, data={
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"})
    tok.raise_for_status()
    auth = {"Authorization": "Bearer " + tok.json()["access_token"]}
    video = P / pub["file"]
    body = {
        "snippet": {"title": pub["youtube"]["title"], "description": pub["youtube"]["description"],
                    "tags": pub["youtube"].get("tags", []), "categoryId": pub["youtube"].get("categoryId", "27")},
        "status": {"privacyStatus": pub["youtube"].get("privacy", "public"), "selfDeclaredMadeForKids": False,
                   "containsSyntheticMedia": pub["youtube"].get("containsSyntheticMedia", False)},
    }
    init = requests.post("https://www.googleapis.com/upload/youtube/v3/videos", timeout=60,
                         params={"uploadType": "resumable", "part": "snippet,status"},
                         headers={**auth, "Content-Type": "application/json; charset=UTF-8",
                                  "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(video.stat().st_size)},
                         data=json.dumps(body))
    init.raise_for_status()
    up = requests.put(init.headers["Location"], data=video.read_bytes(), timeout=600,
                      headers={**auth, "Content-Type": "video/mp4"})
    up.raise_for_status()
    v = up.json()
    res = {"ok": True, "id": v["id"], "url": f"https://youtube.com/shorts/{v['id']}",
           "privacyStatus": v.get("status", {}).get("privacyStatus"), "uploadStatus": v.get("status", {}).get("uploadStatus")}
except Exception:
    res = {"ok": False, "error": traceback.format_exc()[-2000:]}
    try:
        res["response"] = (up if "up" in dir() else init).text[:1500]
    except Exception:
        pass
out.write_text(json.dumps(res, indent=2))
print(json.dumps(res, indent=2))
