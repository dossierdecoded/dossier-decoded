import json,re
P=lambda at,ph,label,**k: dict(at=at,type="photo",photo=f"photo-{ph}.jpg",focus=k.pop("focus",[0.5,0.45]),zoom=k.pop("zoom",[1.0,1.1]),label=label,**k)
C=lambda at,text,sub=None,**k: dict(at=at,type="card",text=text,**({"sub":sub} if sub else {}),**k)
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
FC=dict(fit="contain")
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
S=[
 P("On","howland","HOWLAND ISLAND · CENTRAL PACIFIC",sfx=[["radio",0.0]]),
 C("crackled.","A WOMAN'S\nVOICE",None),
 C("must","“WE MUST BE ON YOU,\nBUT CANNOT SEE YOU.\nGAS IS RUNNING LOW.”","2 JULY 1937",red=True),
 P("belonged","earhart3","AMELIA EARHART",**FC),
 C("twenty","~20 HOURS\nIN THE AIR",None,sfx=[["engine",0.0]]),
 P("strip","howland","HOWLAND ISLAND · ~1.5 MILES LONG",zoom=[1.15,1.3]),
 C("deck","HE SAW\nNOTHING",None),
 C("8:43","8:43 AM","HER LAST CONFIRMED MESSAGE",red=True,sfx=[["stamp",0.0]]),
 C("Noonan,","EARHART & NOONAN","NEVER SEEN AGAIN"),
 P("ninety","oakland","CASE FILE: AMELIA EARHART",zoom=[1.05,1.15]),
 CH("By",2,"The most famous pilot in the world"),
 P("legend.","earhart-1","AMELIA EARHART",**FC),
 C("ten-minute","A 10-MINUTE FLIGHT","WITH A WWI PILOT"),
 P("Atlantic","dfc","HER LOCKHEED VEGA",sfx=[["engine",0.0]]),
 C("first","FIRST WOMAN\nSOLO ACROSS\nTHE ATLANTIC","MAY 1932",red=True),
 C("nonstop","SOLO NONSTOP\nACROSS THE US","1932"),
 C("Distinguished","DISTINGUISHED\nFLYING CROSS","THE FIRST WOMAN"),
 P("books,","earhart-2","WITH HER HUSBAND, PUBLISHER GEORGE PUTNAM",**FC),
 C("record.","ONE MORE\nRECORD",None,red=True),
 P("Equator","map","HER PLANNED ROUTE · ~29,000 MILES",**FC),
 P("Lockheed","oakland","HER LOCKHEED ELECTRA 10E"),
 C("K","KHAQQ","HER CALL SIGN"),
 CH("The",3,"Around the world"),
 C("Hawaii,","MARCH 1937","DAMAGED IN HAWAII",red=True),
 C("reversed.","ROUTE\nREVERSED","EASTBOUND"),
 C("May","21 MAY 1937","OAKLAND, CALIFORNIA"),
 C("Noonan","FRED NOONAN","NAVIGATOR"),
 P("forty","map","40 DAYS · 20+ STOPS",fit="contain",zoom=[1.1,1.2]),
 C("Africa,","SOUTH AMERICA · AFRICA\nINDIA · SOUTHEAST ASIA",None),
 C("twenty-two","~22,000 MILES","DONE"),
 C("Lae,","LAE, NEW GUINEA",None),
 C("seven","~7,000 MILES\nLEFT",None),
 C("twenty-five","2,500+ MILES\nOF OPEN OCEAN",None,red=True),
 P("Howland","howland","A DOT OF LAND",zoom=[1.2,1.35]),
 C("missed","NOWHERE ELSE\nTO LAND",None,red=True),
 CH("On",4,"The last leg"),
 P("loaded","electra","A LOCKHEED ELECTRA (SIMILAR TYPE)",sfx=[["engine",0.0]]),
 C("Itasca,","USCGC ITASCA","WAITING AT HOWLAND"),
 C("conversation","THE RADIO LINK\nNEVER WORKED",None,sfx=[["radio",0.0]]),
 C("haunted","“WE MUST BE ON YOU,\nBUT CANNOT SEE YOU”",None,red=True),
 C("line","“WE ARE ON THE\nLINE 157 337”",None),
 C("navigation","A LINE THROUGH\nTHE ISLAND",None),
 C("which","WHICH WAY?\nHOW FAR?",None,red=True),
 C("nothing.","SILENCE.",None,sfx=[["hit",0.0]]),
 C("Navy","THE NAVY\nJOINS THE SEARCH",None),
 C("wreckage","NO WRECKAGE",None,red=True),
 C("presumed","“LOST AT SEA”","SEARCH CALLED OFF"),
 CH("So",5,"Three theories"),
 C("official","1 · CRASHED\nAT SEA","THE OFFICIAL ANSWER"),
 C("deep","THOUSANDS OF\nFEET DEEP",None),
 C("second","2 · CASTAWAYS",None,red=True),
 P("atoll","niku","NIKUMARORO (GARDNER ISLAND)",**FC,sfx=[["waves",0.0]]),
 C("habitation,","“SIGNS OF RECENT\nHABITATION”","NAVY OVERFLIGHT · ONE WEEK LATER"),
 C("distress","DISTRESS CALLS?","HEARD IN FLORIDA AND CANADA"),
 C("1940,","1940","BONES FOUND ON THE ISLAND",red=True),
 C("male,","“MALE”\nTHEN LOST",None),
 C("2018,","2018","A MATCH FOR EARHART'S BUILD?",red=True),
 C("third","3 · CAPTURED\nBY JAPAN?",None),
 P("Saipan.","saipan","SAIPAN · 1944",**FC),
 P("photo","noonan","THE DISPUTED PHOTO · LATER DATED TO 1935",**FC,stamp="1935",stamp_at="disappeared."),
 CH("The",6,"What the file tells us"),
 C("TIGHAR,","TIGHAR","12+ EXPEDITIONS · A POSSIBLE FRECKLE-CREAM JAR"),
 C("2017,","2017","FORENSIC DOGS"),
 P("crabs,","crab","A COCONUT CRAB",**FC),
 C("sonar,","SONAR SEARCHES","AROUND HOWLAND"),
 C("eighteen","DECLARED DEAD","~18 MONTHS LATER"),
 C("Twenty","20 HOURS.\nNIGHT.\nOPEN OCEAN.",None),
 C("degrees,","A FEW DEGREES\nIS ENOUGH",None,red=True),
 C("simplest","MOST LIKELY:\nTHE SEA",None),
 C("Nikumaroro","BUT NIKUMARORO\nCAN'T BE DISMISSED",None,red=True),
 P("finished.","earhart3","AMELIA EARHART · 1897–1937?",**FC,zoom=[1.05,1.15]),
 C("Tell","WHAT DO\nYOU THINK?","TELL ME IN THE COMMENTS"),
 {"at":"Dossier","type":"end"},
]
json.dump({"title":"AMELIA EARHART","case":"014","landscape":True,"scenes":S},open("scenes.json","w"),indent=1,ensure_ascii=False)
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
