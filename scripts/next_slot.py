"""Print the next free 5 pm ET publishing slot, the next backlog case, and any drafts awaiting approval.

A slot is taken by a queue.json (approved) or by a draft.json whose slot is still in the future
(produced, waiting for approval). Usage: python scripts/next_slot.py"""
import datetime as dt, json, pathlib
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
ET = ZoneInfo("America/New_York")
SLOT_HOUR = 17
now = dt.datetime.now(ET)

taken, pending, stale = set(), [], []
for d in sorted(ROOT.glob("pilots/*")):
    q, dr = d / "queue.json", d / "draft.json"
    if q.exists():
        taken.add(dt.datetime.fromisoformat(json.loads(q.read_text())["publish_at"]).astimezone(ET).date())
    elif dr.exists():
        slot = dt.datetime.fromisoformat(json.loads(dr.read_text())["slot"]).astimezone(ET)
        if slot > now:
            taken.add(slot.date()); pending.append({"case": d.name, "slot": slot.isoformat()})
        else:
            stale.append({"case": d.name, "missed_slot": slot.isoformat()})

day = now.date()
while True:
    slot = dt.datetime.combine(day, dt.time(SLOT_HOUR), ET)
    if slot > now + dt.timedelta(minutes=45) and day not in taken:
        break
    day += dt.timedelta(days=1)

backlog = json.loads((ROOT / "config" / "backlog.json").read_text())["cases"]
nxt = next((c for c in backlog if not (ROOT / "pilots" / c["case"]).exists()), None)
print(json.dumps({"now_et": now.isoformat(timespec="minutes"), "next_free_slot": slot.isoformat(),
                  "next_case": nxt, "awaiting_approval": pending, "stale_drafts": stale}, indent=2))
