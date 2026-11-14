import json,re
P=lambda at,ph,label,**k: dict(at=at,type="photo",photo=f"photo-{ph}.jpg",focus=k.pop("focus",[0.5,0.45]),zoom=k.pop("zoom",[1.0,1.1]),label=label,**k)
C=lambda at,text,sub=None,**k: dict(at=at,type="card",text=text,**({"sub":sub} if sub else {}),**k)
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
FC=dict(fit="contain")
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
S=[
 P("At","arizona","USS ARIZONA · 7 DECEMBER 1941",zoom=[1.25,1.05],sfx=[["hit",0.0]]),
 C("two","LESS THAN\nTWO HOURS","2,400+ AMERICANS KILLED",red=True),
 C("Fiftythree","53 MINUTES EARLIER","A RADAR SCREEN",sfx=[["radar",0.0]]),
 C("submarine","AN HOUR BEFORE THAT","A DESTROYER · A SUBMARINE"),
 C("Neither","NEITHER\nSOUNDED THE ALARM",None,red=True,sfx=[["stamp",0.0]]),
 C("blamed","COMING UP:\nWHERE EACH WARNING WENT\nTHE MAN THEY BLAMED",None),
 CH("radar",2,"A new machine"),
 C("mobile","MOBILE RADAR\nSTATIONS · OAHU",None),
 C("Opana.","OPANA","NORTHERN OAHU"),
 C("truck,","A TRUCK · A TRAILER\nA GENERATOR · AN ANTENNA",None),
 C("hundred","100+ MILES\nRANGE",None),
 C("whose.","FRIEND OR FOE?\nIT COULDN'T TELL",None,red=True),
 C("Shafter,","INFORMATION CENTER","FORT SHAFTER",sfx=[["phone",0.0]]),
 C("set","STILL BEING\nSET UP",None),
 C("four","RADAR HOURS:\n4 AM – 7 AM",None),
 CH("sea.",3,"The submarine"),
 C("periscope","~3:45 AM","A MINESWEEPER REPORTS A PERISCOPE"),
 P("Ward,","ward","USS WARD"),
 C("fire","FIRE\nDEPTH CHARGES",None,red=True,sfx=[["depth",0.0]]),
 C("first","THE FIRST AMERICAN SHOT\nOF THE PACIFIC WAR",None),
 C("Outerbridge,","LT. WILLIAM OUTERBRIDGE","CAPTAIN, USS WARD"),
 C("defensive","“ATTACKED, FIRED UPON\nAND DROPPED DEPTH CHARGES”",None,sfx=[["paper",0.0]]),
 C("busy","BUSY LINES\n“PLEASE CONFIRM”",None),
 C("false","FALSE SIGHTINGS\nBEFORE",None),
 C("slowly","IT MOVED\nSLOWLY",None),
 P("acted","attack","TOO LATE",zoom=[1.0,1.15]),
 CH("crew",4,"The blip"),
 C("Lockard","PVT. JOSEPH LOCKARD\nPVT. GEORGE ELLIOTT",None),
 C("practice.","KEPT IT RUNNING\nFOR PRACTICE",None),
 C("blip","7:02 AM\nA BLIP",None,red=True,sfx=[["radar",0.0]]),
 C("broken.","“IS IT BROKEN?”",None),
 C("thirty","~130 MILES NORTH","AND CLOSER"),
 C("called","ELLIOTT CALLS\nFORT SHAFTER",None,sfx=[["phone",0.0]]),
 C("largest","“THE LARGEST GROUP\nHE'D EVER SEEN”",None),
 C("Tyler,","LT. KERMIT TYLER","FIGHTER PILOT · SECOND DAY ON DUTY"),
 P("B17","b17","A B-17 AT HICKAM · THAT MORNING"),
 C("worry","“DON'T WORRY\nABOUT IT”","IN EFFECT",red=True,sfx=[["stamp",0.0]]),
 C("tracking","THEY KEPT\nTRACKING",None),
 C("lost","~7:39 AM\nLOST IN THE HILLS",None),
 C("Sixteen","16 MINUTES\nLATER",None,red=True,sfx=[["siren",0.0]]),
 CH("came",5,"December 7th"),
 P("battleships","battleship-2","BATTLESHIP ROW · FORD ISLAND",zoom=[1.0,1.15]),
 P("airfields","hickam","HICKAM FIELD",zoom=[1.0,1.12]),
 C("sabotage.","PARKED WINGTIP\nTO WINGTIP",
"TO GUARD AGAINST SABOTAGE"),
 P("Arizona","arizona","USS ARIZONA",zoom=[1.0,1.15],sfx=[["hit",0.0]]),
 C("seventyseven","1,177 KILLED\nON THE ARIZONA",None,red=True),
 P("Oklahoma","oklahoma","USS OKLAHOMA · CAPSIZED"),
 C("Nevada,","USS NEVADA","RUN AGROUND"),
 P("carriers","japanplanes","THE CARRIERS WERE AWAY AT SEA",zoom=[1.0,1.1]),
 C("twentynine","JAPAN LOST\n29 PLANES",None),
 P("twentyfour","battleship-1","2,400+ DEAD · ~1,200 WOUNDED",zoom=[1.0,1.15]),
 P("twelve","b17","12 B-17s · UNARMED · INTO THE BATTLE",zoom=[1.2,1.3]),
 C("fuel,","UNARMED\nLOW ON FUEL",None),
 C("next","8 DECEMBER 1941",None),
 C("infamy,","“A DATE WHICH WILL\nLIVE IN INFAMY”","PRESIDENT ROOSEVELT · 8 DEC 1941",red=True),
 CH("weeks",6,"What the file tells us"),
 C("Kimmel","ADM. HUSBAND KIMMEL\nGEN. WALTER SHORT","RELIEVED OF COMMAND"),
 C("earlier,","A WARNING FROM\nWASHINGTON","10 DAYS EARLIER"),
 C("argued","STILL\nARGUED",None),
 C("withheld","“INTELLIGENCE\nWITHHELD”",None),
 C("1999,","1999","SENATE: “UNFAIRLY BLAMED”"),
 C("investigated","KERMIT TYLER:\nINVESTIGATED",None),
 C("cleared","CLEARED",None,red=True,sfx=[["stamp",0.0]]),
 C("training,","NO TRAINING\nNO REAL STAFF",None),
 C("friend","FRIEND OR FOE?",None),
 C("bombers","AMERICAN BOMBERS\nREALLY WERE COMING",None),
 C("failure","A FAILURE\nOF WARNING",None,red=True),
 C("connect","NOT A LACK OF INFORMATION.\nA FAILURE TO CONNECT IT.",None),
 P("destroyer","ward","A DESTROYER SAW IT",zoom=[1.1,1.2]),
 C("privates","TWO PRIVATES\nWATCHED IT",None),
 C("ready","A SYSTEM NOT READY\nTO BELIEVE IT",None,red=True),
 C("phone,","WHAT WOULD\nYOU HAVE DONE?","TELL ME IN THE COMMENTS"),
 {"at":"Dossier","type":"end"},
]
json.dump({"title":"PEARL HARBOR","case":"044","landscape":True,"scenes":S},open("scenes.json","w"),indent=1,ensure_ascii=False)
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
