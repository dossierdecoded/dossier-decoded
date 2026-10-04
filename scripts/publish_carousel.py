"""Publish an Instagram carousel. Reads pilots/<n>/carousel_job.json {image_urls: [...], caption};
writes pilots/<n>/carousel_result.json {ok, media_id, permalink}."""
import json, os, pathlib, sys, time, traceback
import requests

G = "https://graph.instagram.com/v23.0"
ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "pilots" / sys.argv[1]
job = json.loads((P / "carousel_job.json").read_text())
TOKEN = os.environ["IG_ACCESS_TOKEN"]
res = {"ok": False, "steps": []}


def call(method, path, **params):
    params["access_token"] = TOKEN
    r = requests.request(method, G + path, params=params if method == "GET" else None,
                         data=params if method == "POST" else None, timeout=120)
    res["steps"].append({"call": f"{method} {path}", "status": r.status_code, "body": r.text[:400]})
    r.raise_for_status()
    return r.json()


def wait(cid):
    for _ in range(60):
        st = call("GET", f"/{cid}", fields="status_code")
        if st.get("status_code") == "FINISHED": return
        if st.get("status_code") in ("ERROR", "EXPIRED"): raise RuntimeError(f"container {cid}: {st}")
        time.sleep(5)

try:
    me = call("GET", "/me", fields="user_id,username"); uid = me.get("user_id") or me["id"]
    kids = []
    for url in job["image_urls"]:
        c = call("POST", f"/{uid}/media", image_url=url, is_carousel_item="true"); wait(c["id"]); kids.append(c["id"])
    car = call("POST", f"/{uid}/media", media_type="CAROUSEL", children=",".join(kids), caption=job["caption"])
    wait(car["id"])
    pub = call("POST", f"/{uid}/media_publish", creation_id=car["id"])
    info = call("GET", f"/{pub['id']}", fields="permalink")
    res.update({"ok": True, "media_id": pub["id"], "permalink": info.get("permalink")})
except Exception:
    res["error"] = traceback.format_exc()[-1500:]
res["steps"] = res["steps"][-6:]
(P / "carousel_result.json").write_text(json.dumps(res, indent=2))
print(json.dumps({k: v for k, v in res.items() if k != "steps"}, indent=2))
