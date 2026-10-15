"""Collect YouTube + Instagram metrics for every published pilot.
Writes metrics/latest.json and appends to metrics/history.json (per-video views over time)."""
import datetime as dt, json, os, pathlib, traceback
import requests
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "metrics"; OUT.mkdir(exist_ok=True)
now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
PILLAR = {"001": "Turned out true", "002": "Strange but true", "003": "Exposed", "004": "Unsolved",
          "005": "Turned out true", "006": "Strange but true", "007": "Unsolved", "008": "Exposed",
          "009": "Turned out true", "010": "Unsolved"}
errors, videos = [], {}
for p in sorted(ROOT.glob("pilots/*")):
    n = p.name
    try: pil = json.loads((p / "job.json").read_text()).get("pillar")
    except Exception: pil = None
    v = {"case": n, "pillar": pil or PILLAR.get(n, "Other")}
    for f, k in (("youtube.json", "yt"), ("instagram.json", "ig")):
        try:
            j = json.loads((p / f).read_text())
            if j.get("ok"): v[k] = {"id": j.get("id") or j.get("media_id"), "url": j.get("url") or j.get("permalink")}
        except Exception: pass
    for f in ("queue.json", "publish.json"):
        try:
            v["title"] = json.loads((p / f).read_text())["youtube"]["title"]; break
        except Exception: pass
    try: v["duration"] = round(json.loads((p / "meta.json").read_text())["duration"], 1)
    except Exception: pass
    if "yt" in v or "ig" in v: videos[n] = v

# ---------- YouTube ----------
channel = {}
try:
    tok = requests.post("https://oauth2.googleapis.com/token", timeout=60, data={
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).json()["access_token"]
    H = {"Authorization": "Bearer " + tok}
    ids = [v["yt"]["id"] for v in videos.values() if "yt" in v]
    r = requests.get("https://www.googleapis.com/youtube/v3/videos", headers=H, timeout=60,
                     params={"part": "statistics,status,snippet", "id": ",".join(ids)}).json()
    by = {it["id"]: it for it in r.get("items", [])}
    for v in videos.values():
        it = by.get(v.get("yt", {}).get("id"))
        if it:
            s = it.get("statistics", {})
            v["yt"].update({"views": int(s.get("viewCount", 0)), "likes": int(s.get("likeCount", 0)),
                            "comments": int(s.get("commentCount", 0)), "privacy": it["status"]["privacyStatus"],
                            "published": it["snippet"]["publishedAt"]})
    for v in videos.values():  # comment text (top-level), for videos that have any
        y = v.get("yt", {})
        if y.get("comments"):
            ct = requests.get("https://www.googleapis.com/youtube/v3/commentThreads", headers=H, timeout=60,
                              params={"part": "snippet", "videoId": y["id"], "maxResults": 20, "textFormat": "plainText"}).json()
            y["comment_text"] = [{"author": i["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"],
                                  "text": i["snippet"]["topLevelComment"]["snippet"]["textDisplay"][:500],
                                  "at": i["snippet"]["topLevelComment"]["snippet"]["publishedAt"]}
                                 for i in ct.get("items", [])]
    c = requests.get("https://www.googleapis.com/youtube/v3/channels", headers=H, timeout=60,
                     params={"part": "statistics", "mine": "true"}).json()
    if c.get("items"):
        s = c["items"][0]["statistics"]
        channel = {"subscribers": int(s.get("subscriberCount", 0)), "views": int(s.get("viewCount", 0))}
    a = requests.get("https://youtubeanalytics.googleapis.com/v2/reports", headers=H, timeout=60, params={
        "ids": "channel==MINE", "startDate": "2026-09-01", "endDate": now.date().isoformat(),
        "metrics": "views,averageViewDuration,averageViewPercentage,shares,subscribersGained",
        "dimensions": "video", "filters": "video==" + ",".join(ids), "maxResults": 200, "sort": "-views"}).json()
    if "rows" in a:
        cols = [h["name"] for h in a["columnHeaders"]]
        for row in a["rows"]:
            d = dict(zip(cols, row))
            for v in videos.values():
                if v.get("yt", {}).get("id") == d["video"]:
                    v["yt"].update({"avg_view_pct": d.get("averageViewPercentage"), "avg_view_sec": d.get("averageViewDuration"),
                                    "shares": d.get("shares"), "subs_gained": d.get("subscribersGained")})
    elif "error" in a:
        errors.append("yt analytics: " + json.dumps(a["error"])[:300])
except Exception:
    errors.append("youtube: " + traceback.format_exc()[-600:])

# ---------- Instagram ----------
account = {}
try:
    T = os.environ["IG_ACCESS_TOKEN"]; G = "https://graph.instagram.com/v23.0"
    me = requests.get(G + "/me", params={"fields": "followers_count,media_count,username", "access_token": T}, timeout=60).json()
    account = {k: me.get(k) for k in ("followers_count", "media_count", "username")}
    METRICS = ["views", "reach", "likes", "comments", "shares", "saved", "total_interactions", "ig_reels_avg_watch_time"]
    for v in videos.values():
        mid = v.get("ig", {}).get("id")
        if not mid: continue
        got = {}
        r = requests.get(f"{G}/{mid}/insights", params={"metric": ",".join(METRICS), "access_token": T}, timeout=60).json()
        rows = r.get("data")
        if rows is None:  # fall back to one metric at a time
            rows = []
            for m in METRICS:
                rr = requests.get(f"{G}/{mid}/insights", params={"metric": m, "access_token": T}, timeout=60).json()
                rows += rr.get("data", [])
            if not rows: errors.append(f"ig {mid}: " + json.dumps(r)[:200])
        for d in rows:
            val = d.get("values", [{}])[0].get("value") if d.get("values") else d.get("total_value", {}).get("value")
            got[d["name"]] = val
        if "ig_reels_avg_watch_time" in got and got["ig_reels_avg_watch_time"] is not None:
            got["avg_watch_sec"] = round(got.pop("ig_reels_avg_watch_time") / 1000, 1)
        v["ig"].update(got)
except Exception:
    errors.append("instagram: " + traceback.format_exc()[-600:])

# ---------- Instagram carousels ----------
carousels = []
try:
    T = os.environ["IG_ACCESS_TOKEN"]; G = "https://graph.instagram.com/v23.0"
    for f in sorted(ROOT.glob("pilots/*/carousel_result.json")):
        j = json.loads(f.read_text())
        if not j.get("ok"): continue
        c = {"case": f.parent.name, "id": j["media_id"], "url": j.get("permalink")}
        try: c["published"] = json.loads((f.parent / "carousel_queue.json").read_text())["publish_at"]
        except Exception: pass
        for m in ["views", "reach", "likes", "comments", "shares", "saved", "total_interactions"]:
            rr = requests.get(f"{G}/{c['id']}/insights", params={"metric": m, "access_token": T}, timeout=60).json()
            for d in rr.get("data", []):
                c[d["name"]] = d.get("values", [{}])[0].get("value") if d.get("values") else d.get("total_value", {}).get("value")
        carousels.append(c)
except Exception:
    errors.append("carousels: " + traceback.format_exc()[-600:])

latest = {"updated": now.isoformat(), "youtube_channel": channel, "instagram_account": account,
          "videos": list(videos.values()), "carousels": carousels, "errors": errors}
(OUT / "latest.json").write_text(json.dumps(latest, indent=1))
hp = OUT / "history.json"
hist = json.loads(hp.read_text()) if hp.exists() else []
hist.append({"t": now.isoformat(), "yt_subs": channel.get("subscribers"), "ig_followers": account.get("followers_count"),
             "v": {v["case"]: [v.get("yt", {}).get("views"), v.get("ig", {}).get("views")] for v in videos.values()}})
hp.write_text(json.dumps(hist[-1500:], separators=(",", ":")))
print(json.dumps(latest, indent=1)[:3000])
