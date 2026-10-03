"""Publish queued pilots whose time has come. Reads pilots/<n>/queue.json:
{"publish_at": ISO8601, "youtube": {...publish.json youtube block...}, "file": "...", "instagram": {"video_url","caption"}}
Writes publish.json / instagram_job.json at publish time, then runs the uploaders."""
import datetime as dt, json, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
now = dt.datetime.now(dt.timezone.utc)
for q in sorted(ROOT.glob("pilots/*/queue.json")):
    P, n = q.parent, q.parent.name
    job = json.loads(q.read_text())
    if dt.datetime.fromisoformat(job["publish_at"]) > now:
        continue
    def done(f):
        try: return json.loads((P / f).read_text()).get("ok") is True
        except Exception: return False
    if not done("youtube.json"):
        (P / "publish.json").write_text(json.dumps({"file": job["file"], "youtube": job["youtube"]}, indent=2, ensure_ascii=False))
        subprocess.run([sys.executable, str(ROOT / "scripts" / "upload_youtube.py"), n])
    if not done("instagram.json") and job.get("instagram"):
        (P / "instagram_job.json").write_text(json.dumps(job["instagram"], indent=2, ensure_ascii=False))
        subprocess.run([sys.executable, str(ROOT / "scripts" / "publish_instagram.py"), n])
    print(n, "youtube", done("youtube.json"), "instagram", done("instagram.json"))
