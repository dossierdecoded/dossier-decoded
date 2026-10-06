# Dossier Decoded — daily production runbook

You are producing one Short a day for **Dossier Decoded**, a faceless channel on real mysteries and
declassified history (YouTube @dossierdecoded, Instagram @dossierdecoded, TikTok @dossierdecoded).
The owner (Tanmay) approves every video before it goes out. **Never publish anything without his
explicit approval in this conversation.**

Strategy doc (why these rules exist): https://claude.ai/code/artifact/672d372c-89ca-4057-9702-0476ae44fa3f
Live dashboard: https://dossierdecoded.github.io/dashboard/

Two stages:
- **Stage A (scheduled, ~9:47 am ET):** research → script → assets → render → send the draft and nudge Tanmay. Stop and wait.
- **Stage B (when Tanmay replies "post" / approves):** queue it for its 5 pm ET slot; GitHub Actions posts to YouTube and Instagram; hand him the TikTok file + caption.

---

## 0. Setup (every fresh session)

1. Attach the repo with push access: `add_repo(owner="dossierdecoded", repo="dossier-decoded", access="push")`, then clone it to `/home/claude/dossier-decoded` with the command it gives you.
2. `git config user.name "Dossier Decoded"; git config user.email dossierdecoded@gmail.com`
3. Fonts are committed in `fonts/` (OFL licence); nothing to install.
4. `pip install --break-system-packages pillow requests cairosvg` and check `which ffmpeg` (install with apt if missing).
5. Load `SendUserMessage` and `SendUserFile` (ToolSearch) so you can reach Tanmay mid-task.

Secrets (ElevenLabs, YouTube, Instagram, site token) live only in GitHub Actions secrets. You never see
or need them: all API calls run in Actions, triggered by pushing files.

## 1. Pick the slot and the case

Run `python scripts/next_slot.py`.
- `next_free_slot` = the 5 pm ET slot this video is for (a slot is taken by an approved `queue.json` or a draft still awaiting approval).
- `next_case` = first backlog entry in `config/backlog.json` without a `pilots/<case>/` folder.
- If `awaiting_approval` already has **2 or more** drafts, do not produce another. Re-nudge Tanmay about the oldest one and stop.
- If there are `stale_drafts` (approval never came before their slot), mention them in the nudge; they can be re-slotted if he approves later.
- Read `config/learnings.md` before writing: it records what the data has taught us (winning length, hooks, topics).
- If recent comments asked for a specific case (see the dashboard / YouTube), you may swap it in as format `you-asked`.

## 2. Research (accuracy is non-negotiable)

- Use WebSearch/WebFetch. Confirm every fact in at least two reliable sources (official archives, major outlets, Wikipedia + its citations). Never state a theory as fact; say "the FBI believed…", "one theory is…".
- Find a **primary document** if one exists: FBI Vault (vault.fbi.gov), CIA reading room (cia.gov/readingroom), NARA, National Security Archive (nsarchive.gwu.edu), congressional reports. You need a direct PDF URL that a plain `requests.get` can download from GitHub Actions. US federal government works are public domain (17 U.S.C. §105).
- Photos come from Wikimedia Commons via search queries (the fetcher only keeps free licences and records credits).
- No graphic violence, no victim/crime-scene photos, nothing that sensationalises real victims.

## 3. Write the script (the part that decides whether anyone watches)

Rules from the strategy doc:
1. **Hook in the first sentence = the stakes**, not the date. Bad: "In 1962…". Good: "Three men vanished from the most escape-proof prison in America — and left their own heads behind."
2. **One open loop** early ("…but the FBI found something in the water"), paid off near the end.
3. **Original analysis** in every script: why this matters, what the document reveals, what's still hidden. Never just describe what's on screen or read a document aloud (YouTube's inauthentic/reused content rules).
4. **Length:** `target_seconds` from the backlog. Narration pace ≈ 2.85 words/second, plus ~3 s of tail. 38 s ≈ 95–100 words; 65 s ≈ 175–180 words.
5. **Ending (platform-neutral, because one narration serves all platforms):** a line worth sending to a friend ("Send this to someone who still trusts the official story."), then "This is Dossier Decoded. Case file number <N>. A new file every day." For `you-decide`, put the question just before "This is Dossier Decoded". Never say "subscribe" or "follow" in the narration: the end card does that per platform.
6. ElevenLabs v3 tags allowed at the start or for one beat: `[serious]`, `[whispers]`. Spell numbers the way they should be spoken.
7. Formats (rotate as the backlog says):
   - `case-file` — the story told chronologically through evidence.
   - `one-document` — one page, line by line, with our reading of it.
   - `then-vs-now` — the official story at the time vs what declassification revealed.
   - `you-decide` — two explanations, the evidence for each, end on the question.
   - `you-asked` — a viewer's comment on screen first, then the case.

## 4. Fetch assets (GitHub Actions)

Create `pilots/<case>/job.json`:
```json
{
  "slug": "011-alcatraz",
  "pillar": "Unsolved",
  "format": "case-file",
  "script": "…",
  "pdf": "https://…/file.pdf or null",
  "pages": [1, 12],
  "commons": [{"slug": "poster", "query": "Frank Morris FBI wanted poster", "n": 1}],
  "sfx": [
    {"slug": "drone", "text": "dark low ambient drone, tense documentary underscore, slow pulsing sub bass, no melody, seamless", "seconds": 22},
    {"slug": "stamp", "text": "a heavy rubber stamp slamming down on paper on a wooden desk, single hit, close up", "seconds": 1.2},
    {"slug": "paper", "text": "a single sheet of paper being slid across a desk and flipped, close up", "seconds": 1.2},
    {"slug": "hit", "text": "deep cinematic impact hit, single boom, short tail", "seconds": 1.5}
  ]
}
```
`drone`, `stamp` and `paper` are required by the renderer; add 1–2 scene-specific effects if useful (e.g. "typewriter", "waves").
`pages` is optional (limits a large PDF to the pages you need).

Commit and push (`git add pilots/<case>/job.json && git commit -m "Case <case> job" && git pull --rebase && git push`).
The push triggers the **Fetch pilot assets** workflow. Do NOT trigger it a second time manually.
Poll with `git pull` every ~60 s until `pilots/<case>/assets/voice.mp3` exists (usually 3–8 min, give up after 25 min and tell Tanmay).
Then read `assets/errors.txt` (empty = fine) and `photo_licenses.json`.

Outputs in `assets/`: `voice.mp3`, `alignment.json`, `sfx-*.mp3`, `photo-<slug>[-k].jpg`, and for a PDF `doc-NN.png` pages plus
`ocr.json` (page text) and `ocr_lines.json` (each text line with its pixel box `[x0, y0, x1, y1]`).
If photos are missing or wrong, adjust the queries in job.json and push again (that re-runs the fetch).

## 5. Build scenes.json and render

Look at every page and photo with the Read tool before using it. Copy the structure of `pilots/004/scenes.json` (photos/cards) and `pilots/001/scenes.json` (documents).

```json
{"title": "THE ALCATRAZ ESCAPE", "case": "011", "scenes": [
  {"at": "<first word of script>", "type": "doc", "page": "doc-03.png", "window": [x0,y0,x1,y1], "zoom": [1.0, 1.1],
   "lines": [[x0,y0,x1,y1]], "instant": true, "label": "FBI FILE · JUNE 1962"},
  {"at": "<trigger word>", "type": "photo", "photo": "photo-poster.jpg", "focus": [0.5, 0.35], "zoom": [1.0, 1.1], "label": "FBI WANTED POSTER", "stamp": "ESCAPED", "stamp_at": "<word>"},
  {"at": "<trigger word>", "type": "card", "text": "3 MEN\n0 BODIES", "sub": "JUNE 1962", "red": true, "sfx_at": [["hit", "<word>"]]},
  {"at": "This", "type": "end"}
]}
```
- `at` = the word where the scene starts. Words are matched **in order**, lowercase, punctuation stripped, searching forward from the previous scene's word — so pick distinctive words (not "the", "a", "and", "it", "his").
- Doc scenes: take `lines` boxes from `ocr_lines.json`; `reveal` = word at which the redaction bar wipes off; `"instant": true` shows the highlight already revealed.
- **Hook frame:** scene 1 must show the most striking image or document line immediately — use a photo, or a doc with `"instant": true`. No title cards first.
- Photos: `focus` = crop centre (0–1), `"fit": "contain"` for small scraps/documents that must not be cropped.
- Change visual every 2–4 seconds. Stamps (`stamp` + `stamp_at`) on the 2–3 biggest beats only.
- The last scene is always `{"at": "This", "type": "end"}` (matches "This is Dossier Decoded").

Preview stills, look at them, fix framing, then render:
```
python scripts/render_pilot.py <case> --preview 0.5 4 9 15 22    # writes pilots/<case>/preview-*.jpg
python scripts/render_pilot.py <case>                            # YouTube cut: <case>-final.mp4 (end card: SUBSCRIBE / SHARE)
python scripts/render_pilot.py <case> --platform ig              # Instagram + TikTok cut: <case>-ig.mp4 (end card: FOLLOW / SEND)
```
Check: the first frame is strong, text is readable on a phone, captions don't cover key text, no scene is
blank, duration is within ±5 s of target. Delete `preview-*.jpg` afterwards.

## 6. Draft metadata

Write `pilots/<case>/draft.json`:
```json
{
  "slot": "<next_free_slot from step 1>",
  "file": "<case>-final.mp4",
  "youtube": {
    "title": "<hook phrase> | <Case name>   (max 70 chars, no clickbait that the video doesn't pay off)",
    "description": "<2–3 sentence factual summary>\n\n📂 Case File #<case>: <Case name>\n\nSources: <primary document + 1–2 references with URLs>\nImages: <credits from photo_licenses.json>.\nNarration voice: AI.\n\nWhich file should we open next? Comment below.\n\n#shorts #history #mystery",
    "tags": ["<6–8 specific tags>"],
    "categoryId": "27",
    "privacy": "public",
    "containsSyntheticMedia": false
  },
  "instagram": {
    "file": "<case>-ig.mp4",
    "video_url": "https://dossierdecoded.github.io/media/<case>.mp4",
    "caption": "<one-line hook> 📂 Case File #<case>: <Case name>\n\n<1 shareable line, e.g. 'Send this to someone who thinks this could never happen.'>\n\nImages: <short credit>.\n\n<exactly 5 specific hashtags>"
  },
  "tiktok_caption": "<hook line> 📂 Case File #<case> <4–5 hashtags>"
}
```
`containsSyntheticMedia` stays false unless a *realistic* AI image/video of a real person or event is used (never do that).

Commit everything (`pilots/<case>/` including the mp4) and push.

## 7. Nudge Tanmay (end of Stage A)

1. Make a phone-friendly preview if the file is over 28 MB:
   `ffmpeg -y -i <case>-final.mp4 -c:v libx264 -crf 27 -preset veryfast -c:a aac -b:a 128k /tmp/<case>-preview.mp4`
2. `SendUserFile` the preview (status `proactive`).
3. `SendUserMessage` with: case + title, the slot ("today 5:00 pm ET" / "tomorrow 5:00 pm ET"), the hook line, length, pillar/format, the main sources, and anything uncertain. End with:
   **"Reply 'post' to queue it for <slot>, or tell me what to change."**
4. Stop and wait. Do not queue or publish.

## 8. Stage B — after approval

When Tanmay says "post" / "approved" / "go":
1. `git pull`. If the draft's slot has already passed, ask: post now, or the next free slot (`scripts/next_slot.py`)? "Now" = a `publish_at` a few minutes in the past.
2. Write `pilots/<case>/queue.json` = `{"publish_at": <slot>, "file", "youtube", "instagram"}` copied from draft.json. Commit + push.
3. The hourly **Publish scheduled** workflow (runs at :07 past each hour) uploads to YouTube, hosts the file on the site, publishes the Reel, and removes the hosted copy. Nothing else to trigger.
4. Send Tanmay the TikTok file (`<case>-ig.mp4`) (full quality if ≤ 30 MB, otherwise re-encode at crf 22) and the `tiktok_caption`, with the reminder: post at 5 pm ET, turn on **"AI-generated content"** in TikTok's settings for the post, don't add TikTok music.
5. If you are still in the session after 17:15 ET, `git pull` and read `youtube.json` / `instagram.json` in the case folder; tell him the links or any error.

If he asks for changes: edit the script/scenes, push job.json again only if the narration changed (that re-runs voice), re-render, update draft.json, re-nudge.

## 9. Hard rules

- Never publish, queue or upload without approval in the current conversation.
- Never delete published videos; never delete-and-reupload a Short.
- Never run `upload_youtube.py` / `publish_instagram.py` yourself; Actions does it from `queue.json`.
- Never manually dispatch a workflow that a push already triggered (it creates duplicates).
- Never post more than one Short per day (one slot per date).
- Never invent facts, quotes, or documents. If unsure, leave it out or say it's disputed.
- Never use copyrighted music, film/TV footage, or non-free images.
- Keep secrets out of files and chat.

## 10. Weekly (Sundays)

In the Sunday run, after the nudge: read `metrics/latest.json`, compare viewed%/watch time by length, pillar and format,
and append 3–5 concrete lines to `config/learnings.md` (e.g. "38 s cuts beat 65 s on YouTube viewed%: 41% vs 29%").
Include a 3-line summary in the nudge message.

## 11. Instagram carousels (Mon / Wed / Fri at 12:00 pm ET)

> **PAUSED since 6 Oct 2026 (Tanmay's decision):** the first carousel reached ~1 person at 0 followers. Do not make carousels until he asks to resume (suggested trigger: ~100 Instagram followers).

Carousels are separate Instagram feed posts (not Reels), 3 a week, built from the documents of a case we
already published as a Short — ideally the most recent one with a good primary document.

**When:** in the **Sunday, Tuesday and Thursday** runs, after the daily Short is ready, also make a carousel for
**the next day at 12:00 ET**. Send it in the same nudge; Tanmay's "post" approves both unless he says otherwise.

1. Pick the case (recent, has `doc-*.png` pages or strong photos, no carousel yet: no `carousel.json`).
2. Write `pilots/<case>/carousel.json` (schema at the top of `scripts/render_carousel.py`), 6–8 slides:
   - `hook` — the document angle in ≤ 4 short lines ("THE FBI'S FIRST MEMO ON ALCATRAZ"), optional darkened photo behind.
   - 3–5 `doc` / `photo` slides — real pages with `lines` boxes from `ocr_lines.json` highlighted; each `caption` 1–2 plain sentences (≤ 140 chars) saying what the line shows. Quote only what the page actually says.
   - one `text` slide — the twist or open question.
   - `end`.
3. `python scripts/render_carousel.py <case>` → `carousel/slide-NN.jpg`. Look at every slide; the highlighted text must be readable on a phone.
4. Write `pilots/<case>/carousel_draft.json`: `{"slot": "<next day>T12:00:00-04:00 (or -05:00 after 1 Nov)", "caption": "<hook line> 📂 Case File #<case>\n\n<one sentence of context>\n\nSwipe through the real pages. Full story in our Reels.\n\nSource: <document> (public domain).\n\n<5 specific hashtags>"}`. Commit + push.
5. Nudge: also send a contact sheet of the slides (combine them into one image) and the caption.
6. On approval: write `pilots/<case>/carousel_queue.json` = `{"publish_at": slot, "caption": ..., "slides": ["carousel/slide-01.jpg", ...]}` and push. `publish_due.py` hosts the images, posts the carousel, writes `carousel_result.json`, and removes the hosted images.
7. ~20 min after noon: `git pull`, read `carousel_result.json`, send Tanmay the permalink (dispatch "Publish scheduled" if GitHub's cron hasn't run).

## 12. Long-form documentaries (2 a week: produced Wed + Sat, posted Thu + Sun at 12:00 ET)

Template: `pilots/L01/` (D. B. Cooper) — copy its `script.py` and `scenes_src.py` patterns exactly.

1. Take the next item in `config/longform_backlog.json` whose `pilots/<id>/` folder doesn't exist. Copy reusable assets from the Short's folder named in `reuse` into `pilots/<id>/assets/` (doc pages, ocr_lines.json, photos + photo_licenses.json).
2. **Research + fact-check:** read at least two solid sources with WebFetch (official archive page + Wikipedia and its citations). Every claim in the script must be supported; drop anything you can't confirm (L01 needed 10 corrections on its second check — do that check BEFORE voicing).
3. **Script:** 7–8 minutes = **1,250–1,350 words** (ElevenLabs budget: Creator plan ~100k chars/month shared with daily Shorts). 5–6 chapters, each under ~2,500 characters, written in `pilots/<id>/script.py` producing `job.json` with `"chapters": [{title, text}]`, `"pillar"`, `"format": "long-form"`, `pdf` if a new document is needed, extra `commons` queries only for missing images. Open with the most dramatic moment, end with our own analysis + "tell me in the comments" + "This is Dossier Decoded."
4. Push `job.json` → Fetch workflow voices each chapter and writes `voice.mp3`, `alignment.json`, `chapters.json`. (On re-runs it keeps existing photos; delete a chapter's `voice-NN.mp3` + `alignment-NN.json` to re-voice just that chapter.) Extra photos only: push `commons_extra.json`.
5. **Scenes:** `scenes_src.py` → `scenes.json` with `"landscape": true` and `"case"` = the Short's case number. A scene every 4–8 s; chapter title cards; the end scene triggers on "Dossier". Validate timings (see the snippet used for L01: print scenes shorter than 2.2 s or longer than 13 s and fix triggers). Preview stills, look at them.
6. Render (`python scripts/render_pilot.py <id>`, ~45 min, run with nohup), then re-encode under GitHub's 100 MB limit:
   `ffmpeg -i <case>-final.mp4 -c:v libx264 -preset slow -crf 25 -tune stillimage -c:a aac -b:a 160k -movflags +faststart out.mp4`
7. Thumbnail 1280×720 `thumbnail.jpg` (pattern of L01: face/key image left, 2-line hook right in Big Shoulders, "STILL UNSOLVED"-style stamp; check nothing is cut off).
8. `draft.json`: `{"slot": <post time from backlog>, "file", "youtube": {"long": true, "thumbnail": "thumbnail.jpg", title, description with chapter timestamps from chapters.json + sources + photo credits + "Narration voice: AI.", tags, categoryId "27", privacy "public", containsSyntheticMedia false}}`. Commit + push.
9. Nudge (with that day's Short): 720p preview (`-vf scale=1280:720 -crf 30`), thumbnail, chapter list, fact-check notes. On approval write `queue.json` (no instagram block) and push; check-in 20 min after the slot, dispatch "Publish scheduled" if needed, send the link, and remind Tanmay to add it to the "Unsolved Case Files" playlist / set it as Related video on its Short.
