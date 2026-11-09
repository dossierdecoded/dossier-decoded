# What the data has taught us

Append dated lines; newest at the bottom. Production reads this before writing each script.

- 2026-10-03: Day-one result: D. B. Cooper (Unsolved, human stakes, ~61 s) got 276 YouTube views; most other cases under 20. Unsolved cases with a named person lead.
- 2026-10-03: Instagram average watch time was 1–2 s on several Reels: viewers leave before the first sentence ends. Every video now opens on its most striking frame and a stakes-first sentence.
- 2026-10-03: Length A/B test running cases 011–024 (38 s vs 65 s alternating). Pick the winner by YouTube viewed% and average % viewed after case 024.
- 2026-10-06: Unsolved cases with a FAMOUS NAME (D. B. Cooper, Hoffa, Alcatraz) = ~82% of all YouTube views from 3 of 13 Shorts. Obscure unsolved cases (Mary Celeste, Somerton) got <10 views. Put the famous name in the title and in the first spoken line.
- 2026-10-07: Earhart opened on a static photo + a time/date ("At 8:43 in the morning…") and averaged 1.6 s watch on Instagram. Open on the most haunting line or object itself (the quote, the cipher, the note), never on a date.
- 2026-10-08: PAID TEST started: YouTube Studio promotion of L01 (D. B. Cooper long-form), goal Audience growth / Find more subscribers, $20 total, Oct 8-12, US/UK/AU(+CA), English, interest Documentary & Nonfiction TV Fans. Baseline before ad: L01 5 views, channel 5 subs. Review Tue 13 Oct: cost/view, avg % viewed of paid views (>=35% good), subs gained, lift on 004 Short and L02.
- 2026-10-08: Tanmay likes the Cold War 'they actually did this' Shorts (Project A119 = our best Instagram reach, 144 views; first real comment). Alternate famous unsolved cases with secret-experiment stories. Starfish Prime moved up to 017 (teased in a comment reply).
- 2026-10-10: Instagram: ~1,000 views but 2 followers. Added follow line to IG captions and IG link to YouTube descriptions (runbook §13). Tanmay to pin Starfish/Ghost Army/Hoffa and update bio.
- 2026-10-13: Paid test result: $19.87 → 5,716 impressions, 126 views, 34 subscribers (~$0.58/sub). Paid viewers watch ~10%. Verdict: scale (next: Alcatraz, $20). Obscure topics (Acoustic Kitty: 2 views) die; famous events win (Tylenol 151, Flight 19 86 in 16h).
- 2026-10-13: Second paid test started: Alcatraz long-form (L02), ~$20, same settings. Baseline: L02 2 views; channel subs at start (see metrics).
- 2026-10-17: Gulf of Tonkin (024, war/politics, 'government lied') got 4 YouTube views in 16 h — YouTube never tested it. War/politics topics are risky for reach; prefer famous mysteries/disasters.
- 2026-10-17: USS Cyclops (025, Bermuda-Triangle-adjacent disappearance, 65 s, you-decide) = 735 YouTube views + 127 IG in 4 h — best start ever; +3 subs. Naval/sea disappearances with a big number (306 aboard) are a winning lane.
- 2026-10-19: TikTok dropped — YouTube + Instagram only (Tanmay).
- 2026-10-21: Glenn Miller (029, famous name + disappearance + real archive photos, 80 s) = 987 YouTube views in 6 h, +9 subs (71→80). Famous name + vanished + real photos is the formula; length 80 s did not hurt.
- 2026-10-22: Paid promotion running on L05 (Philadelphia documentary) until Sun 25 Oct (Tanmay). Judge L05 view growth with that in mind.
- 2026-10-23: Harold Holt (030) = 68 YouTube views in 9 h despite famous-name formula — name must be famous to AMERICANS (our audience). IG fine (69).
- 2026-10-25: Philadelphia doc promotion (ad-safe thumbnail) = $6.47 → 2,698 impressions, 35 views, 22 subs (~$0.29/sub) — best paid result. Standard: promote each new doc with ad-safe thumbnail.
- 2026-10-27: Glenn Miller doc (L07) grew 2→163 views organically on 26 Oct (no link, no promo); a paid promotion started morning of 27 Oct, so growth after that is mixed — first documentary YouTube recommended on its own. Famous searchable name + documentary = organic reach. Check Studio traffic source.
- 2026-10-31: Queue.json MUST include instagram.video_url (https://dossierdecoded.github.io/media/<case>.mp4) — 037 omitted it and Instagram silently failed (posted 2 h late after fix). Copy the whole instagram block from draft.json.
- 2026-10-31: L09 switched from Somerton (obscure) to the Titanic warnings (036 Short ~930 views); Somerton moved to L10.
- 2026-11-01: Challenger (038, 'engineers warned NASA', famous US disaster, 85 s, posted 9:15 pm) = 1,035 YouTube views + 115 IG overnight; subs 128→138. 'They were warned' + very famous American event is the strongest lane; 85 s did not hurt.
- 2026-11-02: Paid promotion started on L09 (Titanic warnings doc) by Tanmay, afternoon 2 Nov. Baseline before ad: L09 0 views (22 h after posting), channel 148 subs. Judge L09 growth after this as paid.
- 2026-11-03: Radium Girls (040, 'told it was safe', real 1921 ad + real photos, 75 s) = 1,036 YouTube views overnight, 69 likes; subs 148→172. Challenger avg view 97%. 'They were warned / told it was safe' is now 3-for-3 when the subject is famous (Titanic, Challenger, Radium Girls); North Sentinel (no famous-warning angle) 128.
- 2026-11-04: Columbia (041, Challenger follow-up, 'engineers begged, managers said no') = 1,327 YouTube views overnight (new record), 78 likes, IG 153 / 11.8 s; subs 184→244 in 18 h. Titanic doc L09 257 with promo. Space-shuttle 'warned' pair is our best lane.
- 2026-11-05: collect_metrics videos.list failed silently once the channel passed 50 videos (API max 50 ids/call); now batched.
- 2026-11-06: Momentum cooled. Apollo 1 (042) 355 after ~38 h; Johnstown (043, posted 6:43 pm late) 20 YT overnight. Subs 350→365 overnight (vs +50/night earlier in week). Big winners were Challenger/Columbia/Radium Girls (household names); Apollo 1 & Johnstown are less known. Lesson: 'warned' angle needs a HOUSEHOLD-name event; don't stack 3 space Shorts in a row. L10 Challenger doc: 1 view after 19 h (needs Related-video link from 038).
- 2026-11-08: Cron unreliable (publish-scheduled hourly cron actually ran every 3-5 h). Fix: send_later at slot time dispatches publish. See RUNBOOK §15.
- 2026-11-09: Dyatlov (046, unsolved mystery, mostly cards + 1 real photo) = IG avg watch 17.2 s (best ever) and 161 IG views; YT 234 in 8.5 h. Mystery angle holds IG viewers. Subs 471.
