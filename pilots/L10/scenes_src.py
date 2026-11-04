import json,re
P=lambda at,ph,label,**k: dict(at=at,type="photo",photo=f"photo-{ph}.jpg",focus=k.pop("focus",[0.5,0.45]),zoom=k.pop("zoom",[1.0,1.1]),label=label,**k)
C=lambda at,text,sub=None,**k: dict(at=at,type="card",text=text,**({"sub":sub} if sub else {}),**k)
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
FC=dict(fit="contain")
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
S=[
 P("At","launch-1","CHALLENGER · 28 JANUARY 1986",zoom=[1.25,1.05],sfx=[["rumble",0.0]]),
 P("schoolteacher,","mcauliffe","CHRISTA McAULIFFE",**FC),
 C("Millions","MILLIONS\nWATCHING","MANY IN CLASSROOMS"),
 C("Seventythree","73 SECONDS",None,red=True,sfx=[["hit",0.0]]),
 P("killed.","breakup","ALL SEVEN KILLED"),
 C("conference","THE NIGHT BEFORE","A CONFERENCE CALL · UTAH · ALABAMA · FLORIDA",sfx=[["phone",0.0]]),
 C("knew","THEY KNEW\nWHAT WOULD FAIL",None),
 C("overruled.","OVERRULED",None,red=True,sfx=[["stamp",0.0]]),
 C("memo","COMING UP:\nTHE MEMO\nTHE HAT",None),
 CH("understand",2,"The joint"),
 P("boosters,","srb","SOLID ROCKET BOOSTER SEGMENTS (LATER MISSION)"),
 C("Thiokol.","MORTON THIOKOL","UTAH"),
 P("Orings,","oring","THE FIELD JOINT · O-RINGS ~37 FT AROUND",**FC),
 C("five","5,000°F+\nGAS",None,red=True),
 C("signs","FOR YEARS:\nWARNING SIGNS",None),
 C("scorched,","SCORCHED\nPARTLY BURNED AWAY",None),
 C("acceptable","“AN ACCEPTABLE\nRISK”",None),
 C("1985,","JANUARY 1985","A COLD LAUNCH · THE WORST DAMAGE YET",red=True),
 C("stiff.","COLD = STIFF\nRUBBER",None),
 C("Erosion,","EROSION",
"HOT GAS EATING INTO THE RUBBER"),
 C("blowby,","BLOW-BY","GAS GETTING PAST IT"),
 CH("examined",3,"The memo"),
 C("Boisjoly,","ROGER BOISJOLY","THIOKOL SEAL ENGINEER"),
 C("31st,","31 JULY 1985","HIS MEMO TO MANAGEMENT",sfx=[["paper",0.0]]),
 C("catastrophe","“A CATASTROPHE OF\nTHE HIGHEST ORDER”","ROGER BOISJOLY",red=True),
 C("Loss","“LOSS OF\nHUMAN LIFE”",None,red=True,sfx=[["stamp",0.0]]),
 C("August,","AUGUST 1985","BRIEFING AT NASA HEADQUARTERS"),
 C("team","A SEAL\nTASK FORCE",None),
 C("understaffed","UNDERSTAFFED.\nSLOW.",None),
 P("schedule","launch-2","MORE LAUNCHES THAN EVER"),
 P("Teacher","mcauliffe","TEACHER IN SPACE",**FC,zoom=[1.1,1.2]),
 C("fiftyone","MISSION 51-L",None),
 C("delayed","DELAYED\nSEVERAL TIMES",None),
 C("cold","A COLD FRONT",None,red=True),
 CH("27th,",4,"The call"),
 C("freezing.","FORECAST:\nBELOW FREEZING",None),
 C("fiftythree","PREVIOUS COLDEST:\nO-RINGS ~53°F",None),
 C("teleconference","THE TELECONFERENCE","27 JANUARY · EVENING",sfx=[["phone",0.0]]),
 C("recommendation.","DO NOT LAUNCH\nBELOW 53°F","THIOKOL ENGINEERS",red=True),
 C("April?","“WHEN DO YOU WANT ME\nTO LAUNCH, NEXT APRIL?”","LAWRENCE MULLOY · NASA"),
 C("appalled","“APPALLED”","ANOTHER NASA MANAGER"),
 C("offline.","THIOKOL\nGOES OFFLINE",None),
 C("photographs","PHOTOS OF THE\nDAMAGED O-RINGS",None),
 C("Mason,","JERRY MASON","SENIOR VICE PRESIDENT"),
 C("engineering","“TAKE OFF YOUR\nENGINEERING HAT”",None,red=True),
 C("management","“PUT ON YOUR\nMANAGEMENT HAT”",None,red=True,sfx=[["stamp",0.0]]),
 C("changed","LUND CHANGES\nHIS VOTE",None),
 C("resumed,","RECOMMEND\nLAUNCH",None,red=True),
 C("four","ONLY 4 MANAGERS\nVOTED",None),
 C("blow","“IT'S GOING TO\nBLOW UP.”","BOB EBELING, THIOKOL ENGINEER, TO HIS WIFE",red=True),
 CH("next",5,"January 28th"),
 C("thirtysix","36°F","AT THE PAD"),
 P("Icicles","icicles","ICICLES ON THE LAUNCH TOWER · 28 JAN 1986"),
 P("eleven","launch-1","LIFTOFF · 11:38 AM",zoom=[1.0,1.15],sfx=[["rumble",0.0]]),
 P("puffs","smoke","BLACK SMOKE · RIGHT BOOSTER",zoom=[1.2,1.4]),
 C("seal.","THE O-RING\nFAILED TO SEAL",None,red=True),
 C("plugged","TEMPORARILY\nPLUGGED",None),
 C("fiftyeight","T+58 SECONDS","A FLAME",red=True),
 C("seventythree","T+73 SECONDS",None,red=True,sfx=[["hit",0.0]]),
 P("broke","breakup","~9 MILES ABOVE THE ATLANTIC"),
 C("crowd","THE CROWD DIDN'T\nUNDERSTAND",None),
 C("obviously","“OBVIOUSLY A MAJOR\nMALFUNCTION.”","NASA MISSION COMMENTARY"),
 C("cabin","THE CREW CABIN\nSURVIVED",None),
 C("ocean","2+ MINUTES\nLATER",None),
 P("Scobee.","crew","SCOBEE · SMITH · RESNIK · ONIZUKA · McNAIR · JARVIS · McAULIFFE",zoom=[1.0,1.12]),
 CH("President",6,"What the file tells us"),
 P("members","feynman","THE ROGERS COMMISSION ARRIVES AT KENNEDY"),
 C("Feynman.","RICHARD FEYNMAN","PHYSICIST · COMMISSION MEMBER"),
 C("ice","O-RING RUBBER\n+ ICE WATER",None),
 C("squashed.","IT DIDN'T\nSPRING BACK",None,red=True),
 C("cause","CAUSE:\nTHE O-RING SEAL","MADE WORSE BY THE COLD"),
 P("flawed,","rogers","SENATE HEARINGS ON THE ROGERS REPORT",**FC),
 C("third","A THIRD O-RING\nJOINT HEATERS",None),
 P("fly","return","RETURN TO FLIGHT · SEPTEMBER 1988"),
 C("shunned","BOISJOLY:\nSHUNNED AT WORK",None),
 C("knew","THE PEOPLE WHO KNEW\nWERE OVERRULED",None,red=True),
 C("reality","“REALITY MUST TAKE\nPRECEDENCE OVER\nPUBLIC RELATIONS”","RICHARD FEYNMAN"),
 C("nature","“NATURE CANNOT\nBE FOOLED.”",None,red=True),
 C("spoken","WOULD YOU HAVE\nSPOKEN UP?","TELL ME IN THE COMMENTS"),
 {"at":"Dossier","type":"end"},
]
json.dump({"title":"CHALLENGER","case":"038","landscape":True,"scenes":S},open("scenes.json","w"),indent=1,ensure_ascii=False)
al=json.load(open("assets/alignment.json"));ws=[];cur=None;d=0
for ch,s in zip(al["characters"],al["character_start_times_seconds"]):
    if ch=="[":d+=1;continue
    if ch=="]":d-=1;continue
    if d:continue
    if ch.isspace():
        if cur:ws.append(cur);cur=None
        continue
    cur=cur or ["",s];cur[0]+=ch
if cur:ws.append(cur)
n=lambda t:re.sub(r"[^a-z0-9']","",t.lower().replace("’","'"))
i=0;ts=[]
for sc in S:
    st=i
    while i<len(ws) and n(ws[i][0])!=n(sc["at"]): i+=1
    if i>=len(ws): raise SystemExit(f"not found {sc['at']} after {ws[st][0]}@{st}")
    ts.append(ws[i][1])
for k,(a,b) in enumerate(zip(ts,ts[1:]+[ws[-1][1]+3])):
    if b-a<2.0 or b-a>13: print(k,S[k]["at"],round(b-a,1))
print(len(S),"scenes")
