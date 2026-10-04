"""Builds pilots/L01/job.json for the D. B. Cooper long-form. Facts: Wikipedia 'D. B. Cooper' (and its FBI citations)."""
import json, pathlib

CH = [
 ("The man in 18E", """[serious] On the night before Thanksgiving, 1971, a man jumped out of a passenger jet with two hundred thousand dollars strapped to his body. He jumped into rain, into darkness, into a forest, at ten thousand feet. And then he disappeared. Not into prison. Not into a grave. Into history. Fifty-five years later, the FBI still does not know his name. This is the complete case file on the only unsolved hijacking in the history of American commercial aviation. Let's open it.

November 24th, 1971. Portland International Airport, Oregon. A quiet man in a dark suit, a white shirt and a thin black clip-on tie walks up to the Northwest Orient counter and buys a one-way ticket to Seattle. Twenty dollars, cash. The name he gives is Dan Cooper. Flight 305 is a Boeing 727, a short thirty-minute hop with thirty-six passengers on board. Cooper takes seat 18E, in the very last row. He orders a bourbon and soda. He lights a cigarette. At two fifty in the afternoon, the plane takes off. And a few minutes later, he hands a note to the flight attendant sitting behind him, Florence Schaffner. She assumes it is a phone number. Passengers did that. She drops it in her pocket. He leans over and quietly tells her she had better look at it. The note says: Miss, I have a bomb in my briefcase, and want you to sit by me."""),
 ("The demands", """She sits down beside him. He opens the briefcase just enough for her to see red cylinders, wires, and a battery. Then he dictates his demands, and she writes them down. Two hundred thousand dollars, in twenty dollar bills. Four parachutes: two main, two reserve. A fuel truck waiting in Seattle when they land. Everything by five p.m. No funny stuff.

Notice what he asked for. Not a flight to Cuba, which is what hijackers of that era usually wanted. Money, and parachutes. And not one parachute. Four. Here is the most widely accepted reading of that detail: if he asked for a single parachute, the FBI could hand him a sabotaged one. Ask for four, and they have to assume he might force a member of the crew to jump with him. Nobody would risk giving him a dead parachute. It is a small detail, and it is the first sign that this man had thought very carefully about every step.

In the cockpit, Captain William Scott radios Seattle. Northwest's president agrees to pay. And for almost two hours, Flight 305 circles Puget Sound while the money and the parachutes are gathered. The passengers are told there is a minor mechanical problem. Most of them never know they are being held hostage. Meanwhile the FBI races to assemble ten thousand twenty-dollar bills, and it does one very clever thing. Before the money leaves the bank, agents photograph every single bill. Ten thousand serial numbers, on microfilm. If Cooper ever spends one of them, they will know."""),
 ("Seattle", """At five forty-six p.m., the plane lands at Seattle-Tacoma and taxis to a remote, brightly lit corner of the airfield. A Northwest employee walks up the rear stairs with a knapsack holding the cash, roughly twenty pounds of it, and the parachutes. Cooper releases all thirty-six passengers and two of the flight attendants. He keeps the pilots, the flight engineer, and one flight attendant, Tina Mucklow.

Then he gives his flight plan, and this is where investigators start to believe he knew airplanes. He wants to fly to Mexico City. But he wants to fly at the lowest possible speed without stalling, around one hundred knots. Landing gear down. Wing flaps lowered to fifteen degrees. The cabin unpressurized. And a maximum altitude of ten thousand feet. Every one of those numbers makes a jump survivable. And he knew one more thing. The Boeing 727 has a staircase built into its tail, and it can be lowered in flight. When the crew tells him the plane cannot make Mexico City on one tank, he agrees to a refuelling stop in Reno. At seven forty p.m., Flight 305 takes off again into the dark, followed at a distance by two fighter jets."""),
 ("The jump", """A few minutes into the flight, Cooper tells Tina Mucklow to go to the cockpit and stay there. The last thing she sees through the closing door is a man tying something around his waist. Then, the cockpit warning light shows the rear staircase is open. The crew asks over the intercom whether he needs anything. He answers: no.

At about eight thirteen p.m., somewhere over southwest Washington, the crew feels the tail of the plane suddenly pitch upward. Then the cabin pressure changes. Investigators believe that was the moment Dan Cooper stepped off the bottom of the stairs.

Think about where he went. It is night. It is raining. The wind chill at that altitude is around fifteen degrees Fahrenheit, and he is wearing a business suit and loafers. Below him there is no city, only dense forest, rivers, and the cold, deep waters of Lake Merwin. And when the FBI later examined what he left behind, they found one more problem. Of the two reserve parachutes delivered to him, one was a dummy, a training chute sewn shut for classroom demonstrations. And one reserve left behind on the plane had been cut open, with some of its cords removed. Investigators think he may have used them to tie the money bag to his body.

The plane landed in Reno at ten fifteen p.m. The stairs were still down. Cooper was gone. Left behind were eight cigarette butts, his black tie with its tie clip, and two of the four parachutes."""),
 ("The search", """What followed was one of the largest manhunts in American history. FBI agents and sheriff's deputies combed Clark and Cowlitz counties on foot and by helicopter. They knocked on farmhouse doors. Boats patrolled the lakes. FBI Director J. Edgar Hoover approved flights by the SR-71 Blackbird spy plane, to photograph the flight path from high altitude. Bad weather ruined the pictures.

In the spring of 1972, about two hundred soldiers from Fort Lewis spent weeks walking the most likely landing zone. A submarine searched the bottom of Lake Merwin. They found nothing. No parachute. No body. No money. Meanwhile, the ten thousand serial numbers were sent to banks and businesses all over the world. Not a single bill turned up.

And here is a detail that shows how fast the story escaped everyone's control. The hijacker never called himself D. B. Cooper. Early on, the FBI briefly questioned a Portland man with that name, who had nothing to do with it. A reporter rushing to meet a deadline attached it to the hijacker, a wire service repeated it, and it stuck. The most famous name in the case is a name the hijacker never used."""),
 ("The money on the riverbank", """For eight years, the trail was cold. Then, on February 10th, 1980, an eight-year-old boy named Brian Ingram was on a family picnic on the Columbia River, at a sandy stretch called Tena Bar. He was smoothing out the sand to build a campfire, when he uncovered three packets of rotting twenty-dollar bills, still held together by rubber bands. Five thousand eight hundred dollars. The FBI checked the serial numbers. It was Cooper's money.

It should have been the breakthrough. Instead, it made the case stranger. Tena Bar is on the Columbia River, miles away from the forests the FBI had searched. How did the money get there? Did Cooper drown, and the river carry it? Did he bury it and leave? And why were the bills still bundled together, in the same order the FBI had given them out? In 2020, researchers studied the microscopic diatoms on the bills and concluded the money probably went into the water in the spring, months after the hijacking. Another theory points to a 1974 dredging project on the river that may have dumped buried sand, and the money, onto the beach. No explanation fits every fact. And to this day, it is the only Cooper money ever found. The other one hundred and ninety-four thousand dollars has never surfaced."""),
 ("Who was he?", """Over the years, the FBI considered more than eight hundred suspects. Most were eliminated quickly. A few never quite went away.

Richard McCoy, a former Army paratrooper, hijacked a United Airlines 727 just five months later, in April 1972, and jumped from the rear stairs with half a million dollars. He was caught within days. But the FBI ultimately ruled him out as Cooper. Kenneth Christiansen was a former Army paratrooper who worked for Northwest Orient as a purser, based in Seattle. Florence Schaffner said his photos looked closer to her memory than any other suspect. But he was shorter and lighter than the man she described. Robert Rackstraw, a Vietnam veteran and pilot, was the subject of a television documentary in 2016. The FBI had already ruled him out years earlier.

Even the alias may be a clue. Dan Cooper was the hero of a French-language comic book from Belgium, a fictional test pilot who appeared on one cover parachuting. It was never translated into English. Some investigators wondered whether the hijacker had grown up reading it.

In 2016, the FBI officially suspended its active investigation. And in recent years, independent researchers studying particles on Cooper's tie found traces of titanium and other rare metals, the kind of material used in the aerospace industry of the early 1970s. Perhaps the man in seat 18E worked on airplanes. That would explain a great deal."""),
 ("What the file tells us", """So, did he make it? The case against survival is strong. A night jump, into rain, over forest, in loafers, with no way to see the ground and no one to meet him. Some of the agents who worked the case believed he died that night, and that his body lies somewhere in the trees or under the water. One FBI case agent compared the jump to suicide.

But look at what he did before the jump. He chose the one airliner with stairs in its tail. He asked for four parachutes so none would be sabotaged. He set a speed, an altitude and a flap setting that made a jump possible. He gave the flight attendants his note, and then asked for it back, so no handwriting would be left behind. He was calm, polite, and in control for more than five hours. That is not a man who left his survival to chance. And yet, almost all of the money disappeared, and none of it was ever spent. A man that careful either died with it, or was careful enough never to touch it again.

The FBI's file on Dan Cooper fills sixty-six volumes. It still has no name in it. Somewhere, there is a family that never knew. Send this to someone who loves a mystery they can actually think about. And tell me in the comments: did he survive the jump? This is Dossier Decoded. Case file: D. B. Cooper. Closed by the FBI. Never solved."""),
]

job = {
 "slug": "L01-db-cooper",
 "pillar": "Unsolved",
 "format": "long-form",
 "script": " ".join(t for _, t in CH),
 "chapters": [{"title": t, "text": x} for t, x in CH],
 "pdf": None,
 "commons": [
  {"slug": "sketch", "query": "D. B. Cooper FBI composite sketch", "n": 2},
  {"slug": "poster", "query": "D. B. Cooper wanted poster FBI", "n": 1},
  {"slug": "plane", "query": "Northwest Orient Boeing 727", "n": 2},
  {"slug": "stairs", "query": "Boeing 727 aft airstair ventral stairs", "n": 2},
  {"slug": "money", "query": "D. B. Cooper ransom money found 1980", "n": 2},
  {"slug": "tie", "query": "D. B. Cooper tie FBI evidence", "n": 1},
  {"slug": "sr71", "query": "SR-71 Blackbird in flight", "n": 1},
  {"slug": "merwin", "query": "Lake Merwin Washington", "n": 1},
  {"slug": "columbia", "query": "Columbia River Vancouver Washington", "n": 1},
  {"slug": "seatac", "query": "Seattle-Tacoma International Airport 1970s", "n": 1},
  {"slug": "portland", "query": "Portland International Airport 1970s", "n": 1},
  {"slug": "parachute", "query": "NB-6 parachute Navy backpack", "n": 1},
  {"slug": "mccoy", "query": "Richard Floyd McCoy Jr.", "n": 1},
  {"slug": "forest", "query": "Cascade foothills forest Clark County Washington", "n": 1},
  {"slug": "hoover", "query": "J. Edgar Hoover portrait", "n": 1}
 ],
 "sfx": [
  {"slug": "drone", "text": "dark low ambient drone, tense documentary underscore, slow pulsing sub bass, no melody, seamless", "seconds": 22},
  {"slug": "stamp", "text": "a heavy rubber stamp slamming down on paper on a wooden desk, single hit, close up", "seconds": 1.2},
  {"slug": "paper", "text": "a single sheet of paper being slid across a desk and flipped, close up", "seconds": 1.2},
  {"slug": "hit", "text": "deep cinematic impact hit, single boom, short tail", "seconds": 1.5},
  {"slug": "cabin", "text": "jet airliner cabin interior ambience, engine hum, 1970s airliner", "seconds": 8},
  {"slug": "wind", "text": "violent roaring wind rushing through an open aircraft door at night, rain", "seconds": 6},
  {"slug": "rain", "text": "heavy rain falling on a dark forest at night", "seconds": 8},
  {"slug": "river", "text": "gentle river water lapping on a sandy riverbank", "seconds": 6}
 ]
}
p = pathlib.Path(__file__).parent
(p / "job.json").write_text(json.dumps(job, indent=1, ensure_ascii=False))
import re
w = len(re.sub(r"\[.*?\]", "", job["script"]).split())
print("words", w, "est min", round(w / 2.85 / 60, 1), [len(x) for _, x in CH])
