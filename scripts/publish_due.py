"""Publish queued pilots whose time has come. Reads pilots/<n>/queue.json:
{"publish_at": ISO8601, "youtube": {...publish.json youtube block...}, "file": "...", "instagram": {"video_url","caption"}}
Writes publish.json / instagram_job.json at publish time, then runs the uploaders.

Instagram needs a public video URL. When video_url points at https://dossierdecoded.github.io/media/,
this script hosts the file on the site repo (SITE_TOKEN), waits for GitHub Pages to serve it,
publishes, then removes it again."""
import datetime as dt, json, os, pathlib, shutil, subprocess, sys, time
import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE_URL = "https://dossierdecoded.github.io/media/"
SITE_DIR = pathlib.Path("/tmp/site")
now = dt.datetime.now(dt.timezone.utc)
GRACE = dt.timedelta(minutes=15)  # GitHub cron start times drift; a run up to 15 min before the slot still posts


def sh(*a, **kw):
    return subprocess.run(a, cwd=SITE_DIR, check=True, capture_output=True, text=True, **kw)


def site():
    if not SITE_DIR.exists():
        tok = os.environ["SITE_TOKEN"]
        subprocess.run(["git", "clone", "--depth", "1",
                        f"https://x-access-token:{tok}@github.com/dossierdecoded/dossierdecoded.github.io.git",
                        str(SITE_DIR)], check=True, capture_output=True)
        sh("git", "config", "user.name", "dossier-bot")
        sh("git", "config", "user.email", "dossierdecoded@gmail.com")
    return SITE_DIR


def push(msg):
    sh("git", "add", "-A")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=SITE_DIR).returncode == 0:
        return
    sh("git", "commit", "-m", msg)
    for _ in range(4):
        try:
            sh("git", "pull", "--rebase", "origin", "main"); sh("git", "push", "origin", "HEAD:main"); return
        except subprocess.CalledProcessError:
            time.sleep(10)
    raise RuntimeError("could not push site repo")


def host(n, src, url):
    dst = site() / "media" / url.rsplit("/", 1)[1]
    dst.parent.mkdir(exist_ok=True)
    if not dst.exists():
        shutil.copy(src, dst); push(f"Host {n} for Instagram")
    size = src.stat().st_size
    for _ in range(90):  # Pages deploys usually take 1-3 min
        try:
            r = requests.head(url, timeout=30, allow_redirects=True)
            if r.status_code == 200 and int(r.headers.get("content-length", size)) == size:
                return True
        except requests.RequestException:
            pass
        time.sleep(10)
    return False


def unhost(url):
    f = site() / "media" / url.rsplit("/", 1)[1]
    if f.exists():
        f.unlink(); push("Remove hosted video after publishing")



def git(*a):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True)


def claim(P, n, kind):
    """Atomically claim a publish via a pushed lock file, so two overlapping runs can never both post.
    Returns True if this run owns the publish."""
    lock = P / f"{kind}.lock"
    git("config", "user.name", "dossier-bot"); git("config", "user.email", "dossierdecoded@gmail.com")
    git("pull", "--rebase", "-q", "origin", "main")
    if lock.exists():
        age = time.time() - float(lock.read_text().strip() or 0)
        if age < 3600:
            return False  # another run is publishing (or did) this
    lock.write_text(str(time.time()))
    git("add", str(lock)); git("commit", "-q", "-m", f"Claim {kind} publish {n}")
    if git("push", "-q", "origin", "HEAD:main").returncode != 0:  # someone pushed first: re-check
        git("reset", "-q", "--hard", "origin/main"); git("pull", "-q", "--rebase", "origin", "main")
        return False
    return True

for q in sorted(ROOT.glob("pilots/*/queue.json")):
    P, n = q.parent, q.parent.name
    job = json.loads(q.read_text())
    if dt.datetime.fromisoformat(job["publish_at"]) > now + GRACE:
        continue

    def done(f):
        try: return json.loads((P / f).read_text()).get("ok") is True
        except Exception: return False

    if (not done("youtube.json") or (job.get("instagram") and not done("instagram.json"))) and not claim(P, n, "publish"):
        print(n, "skipped: another run holds the publish claim"); continue
    if not done("youtube.json"):
        (P / "publish.json").write_text(json.dumps({"file": job["file"], "youtube": job["youtube"]}, indent=2, ensure_ascii=False))
        subprocess.run([sys.executable, str(ROOT / "scripts" / "upload_youtube.py"), n])
    ig = job.get("instagram")
    if ig:
        url = ig["video_url"]; ours = url.startswith(SITE_URL)
        if not done("instagram.json"):
            if ours and not host(n, P / ig.get("file", job["file"]), url):
                (P / "instagram.json").write_text(json.dumps({"ok": False, "error": "hosted file not served in time"}))
            else:
                (P / "instagram_job.json").write_text(json.dumps(ig, indent=2, ensure_ascii=False))
                subprocess.run([sys.executable, str(ROOT / "scripts" / "publish_instagram.py"), n])
        recent = now - dt.datetime.fromisoformat(job["publish_at"]) < dt.timedelta(days=2)
        if done("instagram.json") and ours and recent:
            try: unhost(url)
            except Exception as e: print(n, "unhost failed:", e)
    print(n, "youtube", done("youtube.json"), "instagram", done("instagram.json"))

# ---------- Instagram carousels: pilots/<n>/carousel_queue.json {publish_at, caption, slides: ["carousel/slide-01.jpg", ...]} ----------
for q in sorted(ROOT.glob("pilots/*/carousel_queue.json")):
    P, n = q.parent, q.parent.name
    job = json.loads(q.read_text())
    if dt.datetime.fromisoformat(job["publish_at"]) > now + GRACE:
        continue
    try: ok = json.loads((P / "carousel_result.json").read_text()).get("ok") is True
    except Exception: ok = False
    names = [f"c{n}-{i + 1:02d}.jpg" for i in range(len(job["slides"]))]
    urls = [SITE_URL + x for x in names]
    if not ok and not claim(P, n, "carousel"):
        print(n, "carousel skipped: claimed by another run"); continue
    if not ok:
        try:
            media = site() / "media"; media.mkdir(exist_ok=True)
            for src, name in zip(job["slides"], names):
                if not (media / name).exists(): shutil.copy(P / src, media / name)
            push(f"Host carousel {n}")
            served = False
            for _ in range(90):
                try: served = all(requests.head(u, timeout=20).status_code == 200 for u in urls)
                except requests.RequestException: served = False
                if served: break
                time.sleep(10)
            if served:
                (P / "carousel_job.json").write_text(json.dumps({"image_urls": urls, "caption": job["caption"]}, indent=2, ensure_ascii=False))
                subprocess.run([sys.executable, str(ROOT / "scripts" / "publish_carousel.py"), n])
                ok = json.loads((P / "carousel_result.json").read_text()).get("ok") is True
            else:
                (P / "carousel_result.json").write_text(json.dumps({"ok": False, "error": "slides not served in time"}))
        except Exception as e:
            print(n, "carousel failed:", e)
    recent = now - dt.datetime.fromisoformat(job["publish_at"]) < dt.timedelta(days=2)
    if ok and recent:
        try:
            media = site() / "media"; gone = False
            for name in names:
                if (media / name).exists(): (media / name).unlink(); gone = True
            if gone: push(f"Remove hosted carousel {n}")
        except Exception as e:
            print(n, "carousel unhost failed:", e)
    print(n, "carousel", ok)
