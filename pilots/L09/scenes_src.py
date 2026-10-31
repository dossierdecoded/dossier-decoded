import json,re
P=lambda at,ph,label,**k: dict(at=at,type="photo",photo=f"photo-{ph}.jpg",focus=k.pop("focus",[0.5,0.45]),zoom=k.pop("zoom",[1.0,1.1]),label=label,**k)
C=lambda at,text,sub=None,**k: dict(at=at,type="card",text=text,**({"sub":sub} if sub else {}),**k)
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
FC=dict(fit="contain")
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
S=[
 P("At","californian","SS CALIFORNIAN",zoom=[1.3,1.1],sfx=[["morse",0.0]]),
 C("stopped","“WE ARE STOPPED AND\nSURROUNDED BY ICE.”","CALIFORNIAN · ~11 PM, 14 APRIL 1912",red=True),
 P("Phillips,","phillips","MARCONI OPERATORS · JACK PHILLIPS",**FC),
 C("telegrams","PASSENGERS' TELEGRAMS","→ CAPE RACE, NEWFOUNDLAND"),
 P("loud,","radioroom","TITANIC'S MARCONI ROOM",**FC),
 C("Shut","“SHUT UP, SHUT UP.\nI AM BUSY.”","JACK PHILLIPS",red=True,sfx=[["stamp",0.0]]),
 C("Evans,","CYRIL EVANS","CALIFORNIAN'S OPERATOR"),
 C("headphones,","~11:30 PM\nRADIO OFF",None),
 C("Ten","10 MINUTES\nLATER",None,red=True,sfx=[["hit",0.0]]),
 C("first","AT LEAST\nTHE SIXTH WARNING",None),
 P("story","titanic-2","RMS TITANIC",zoom=[1.0,1.15]),
 CH("left",2,"Unsinkable"),
 P("largest","southampton","LEAVING SOUTHAMPTON · 10 APRIL 1912",**FC),
 C("gym,","GYM · POOL\nSQUASH COURT",None),
 C("twentytwo","~2,200\nABOARD",None),
 P("safe","titanic-1","“AS SAFE AS A SHIP COULD BE”",zoom=[1.05,1.2]),
 C("compartments","WATERTIGHT\nCOMPARTMENTS",None),
 C("four.","COULD FLOAT WITH\nTHE FIRST FOUR FLOODED",None),
 P("Marconi","radioroom","THE MARCONI ROOM",**FC,zoom=[1.1,1.25]),
 C("Star","THEY WORKED\nFOR MARCONI","NOT WHITE STAR"),
 C("word.","PASSENGERS PAID\nBY THE WORD",None),
 C("bridge.","NAVIGATION MESSAGES\n→ THE BRIDGE",None),
 C("broken","SET BROKE DOWN\nTHE NIGHT BEFORE",None,red=True),
 P("mountain","phillips","A BACKLOG OF MESSAGES",**FC,zoom=[1.1,1.2]),
 CH("started",3,"Six warnings"),
 C("Caronia","9:00 AM · CARONIA","BERGS, GROWLERS, FIELD ICE",sfx=[["morse",0.0]]),
 C("Edward","CAPTAIN SMITH\nACKNOWLEDGED",None),
 C("Baltic","1:42 PM · BALTIC","ICEBERGS AND FIELD ICE",sfx=[["morse",0.0]]),
 P("Ismay,","ismay","J. BRUCE ISMAY · WHITE STAR CHAIRMAN",**FC),
 C("pocket.","IN HIS\nPOCKET","THEN SHOWN TO TWO PASSENGERS",red=True,sfx=[["stamp",0.0]]),
 C("seven","7:15 PM","FINALLY POSTED IN THE CHART ROOM"),
 C("Amerika,","1:45 PM · AMERIKA","TWO LARGE ICEBERGS",sfx=[["morse",0.0]]),
 C("never","NEVER REACHED\nTHE BRIDGE",None,red=True),
 C("three","~7:30 PM · CALIFORNIAN","THREE LARGE BERGS"),
 P("took","bride","HAROLD BRIDE · JUNIOR OPERATOR",**FC),
 C("Mesaba","9:40 PM · MESABA",None,sfx=[["morse",0.0]]),
 C("pack","“HEAVY PACK ICE …\nGREAT NUMBER\nLARGE ICEBERGS”",None,red=True),
 C("inquiry","NEVER REACHED THE\nCAPTAIN OR ANY OFFICER","BRITISH INQUIRY"),
 C("eleven,","11:00 PM\nCALIFORNIAN",None,red=True),
 CH("night",4,"Iceberg, right ahead"),
 C("moon,","NO MOON\nFLAT CALM",None),
 C("twentytwo","~22 KNOTS","CLOSE TO TOP SPEED"),
 C("Fleet","LOOKOUT\nFREDERICK FLEET","~11:40 PM",sfx=[["bell",0.0]]),
 C("Iceberg,","“ICEBERG,\nRIGHT AHEAD.”",None,red=True,sfx=[["hit",0.0]]),
 P("scraped","iceberg","AN ICEBERG PHOTOGRAPHED NEAR THE SITE, 1912",sfx=[["creak",0.0]]),
 C("Andrews,","THOMAS ANDREWS","SHIP'S DESIGNER"),
 C("Five","5–6 COMPARTMENTS\nFLOODING",None,red=True),
 P("sink,","titanic-1","AN HOUR OR TWO",zoom=[1.2,1.05]),
 P("lifeboats,","lifeboat","A TITANIC LIFEBOAT",**FC),
 C("seventyeight","20 LIFEBOATS\n~1,178 SEATS",None),
 C("law","MORE THAN\nTHE LAW REQUIRED",None),
 C("half","BARELY HALF\nOF THOSE ABOARD",None,red=True),
 CH("Shortly",5,"The ship that watched"),
 P("Carpathia,","carpathia","RMS CARPATHIA · 58 MILES AWAY"),
 P("Rostron,","rostron","CAPTAIN ARTHUR ROSTRON",**FC),
 P("Californian,","californian","THE CALIFORNIAN",zoom=[1.1,1.25]),
 C("off.","HER RADIO\nWAS OFF",None,red=True),
 C("rockets","8 WHITE\nROCKETS",None),
 P("Lord,","lord","CAPTAIN STANLEY LORD · “KEEP TRYING THE MORSE LAMP”",**FC),
 C("Nobody","NOBODY WOKE\nTHE RADIO OPERATOR",None,red=True),
 C("two","2:20 AM","15 APRIL 1912",red=True,sfx=[["hit",0.0]]),
 C("fifteen","1,500+\nDEAD",None),
 P("lifeboats","lifeboat","LOWERED HALF EMPTY",**FC,zoom=[1.1,1.2]),
 P("four","carpathia","~700 SURVIVORS",zoom=[1.1,1.0]),
 C("five","~5:30 AM","THE CALIFORNIAN'S RADIO GOES BACK ON"),
 CH("Two",6,"What the file tells us"),
 P("Britain.","inquiry","US SENATE INQUIRY · 1912",**FC),
 C("many,","“MIGHT HAVE SAVED MANY,\nIF NOT ALL”","BRITISH INQUIRY ON THE CALIFORNIAN",red=True),
 P("insisting","lord","STANLEY LORD",**FC,zoom=[1.1,1.2]),
 C("argue","HOW FAR APART?\nSTILL DEBATED",None),
 P("American","inquiry","THE AMERICAN INQUIRY",**FC,zoom=[1.1,1.2]),
 P("rules","newspaper","THE NEW YORK TIMES · 16 APRIL 1912",**FC),
 C("Lifeboat","LIFEBOATS\nFOR EVERYONE",None),
 C("drills","DRILLS ON\nEVERY VOYAGE",None),
 C("twentyfour","24-HOUR\nRADIO WATCH",None),
 P("International","icepatrol","INTERNATIONAL ICE PATROL · TODAY"),
 C("lack","NOT A LACK OF\nINFORMATION",None,red=True),
 C("Caronia,","CARONIA · BALTIC · AMERIKA\nCALIFORNIAN · MESABA\nCALIFORNIAN",None),
 C("chairman's","1 IN A POCKET\n2 NEVER REACHED THE BRIDGE\n1 TOLD TO SHUT UP",None,red=True),
 P("system","titanic-2","RMS TITANIC · 1912",zoom=[1.0,1.2]),
 C("Which","WHICH WARNING\nCOULD HAVE SAVED HER?","TELL ME IN THE COMMENTS"),
 {"at":"Dossier","type":"end"},
]
json.dump({"title":"THE TITANIC WARNINGS","case":"036","landscape":True,"scenes":S},open("scenes.json","w"),indent=1,ensure_ascii=False)
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
