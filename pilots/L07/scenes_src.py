import json,re
P=lambda at,ph,label,**k: dict(at=at,type="photo",photo=f"photo-{ph}.jpg",focus=k.pop("focus",[0.5,0.45]),zoom=k.pop("zoom",[1.0,1.1]),label=label,**k)
C=lambda at,text,sub=None,**k: dict(at=at,type="card",text=text,**({"sub":sub} if sub else {}),**k)
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
FC=dict(fit="contain")
S=[
 P("On","miller-2","MAJOR GLENN MILLER · US ARMY AIR FORCES",fit="contain",stamp="MISSING",stamp_at="countryside."),
 C("Fog","FOG.\nLOW CLOUD.",None,sfx=[["engine",0.0]]),
 C("three","3 MEN",None),
 C("bandleader","THE MOST FAMOUS\nBANDLEADER\nIN THE WORLD",None,red=True),
 P("Paris,","paris","PARIS · LIBERATED AUGUST 1944"),
 C("arrived.","NEVER ARRIVED.\nNO WRECKAGE.",None,red=True,sfx=[["hit",0.0]]),
 C("eighty","80+ YEARS\nOF ARGUMENT",None),
 C("storm.","A STORM? AN ENGINE?\nBOMBS? A COVER-UP?",None),
 P("records","miller-1","CASE FILE: GLENN MILLER",zoom=[1.1,1.2]),
 CH("To",2,"The sound of a generation"),
 C("Iowa","IOWA · 1904",None),
 P("trombone","trombone","GLENN MILLER",sfx=[["swing",0.0]]),
 C("Schillinger,","“MILLER'S TUNE”\n→ MOONLIGHT\nSERENADE",None),
 C("failed.","FIRST BAND\nFAILED · 1937",None,red=True),
 C("clarinet","THE\nMILLER SOUND","CLARINET ON TOP · SAXOPHONES BELOW"),
 P("America.","miller3","THE GLENN MILLER ORCHESTRA"),
 C("Tuxedo","115,000","TUXEDO JUNCTION · FIRST WEEK"),
 C("Chattanooga","THE FIRST\nGOLD RECORD","CHATTANOOGA CHOO CHOO · 1942",red=True),
 P("jukeboxes","jukebox","A 1940s JUKEBOX",**FC),
 C("Moonlight","MOONLIGHT SERENADE\nIN THE MOOD",None),
 P("Hollywood,","sunvalley","SUN VALLEY SERENADE · 1941"),
 C("twenty","$20,000\nA WEEK",None),
 C("gave","HE GAVE IT\nALL UP",None,red=True),
 CH("In",3,"Captain Miller"),
 C("thirty-eight","AGE 38",None),
 C("Navy","THE NAVY\nSAID NO",None,red=True),
 P("captain.","miller-2","CAPTAIN GLENN MILLER · 1942",fit="contain",zoom=[1.1,1.2]),
 C("swing","SWING FOR\nTHE TROOPS",None),
 P("Air","miller3","THE BAND",zoom=[1.15,1.25]),
 C("broadcast","ON THE RADIO","INCLUDING TO GERMAN SOLDIERS",sfx=[["radio",0.0]]),
 P("Eisenhower","eisenhower","GENERAL EISENHOWER · 1944",**FC),
 P("liberated","paris","PARIS",zoom=[1.1,1.2]),
 C("eighty","~80 HOURS\nRECORDED",None),
 C("twelfth","DONE BY\n12 DEC",None),
 C("weather","THE WEATHER",None),
 C("cancelled.","13 & 14 DEC:\nFLIGHTS CANCELLED",None,red=True),
 CH("On",4,"The last flight"),
 C("Baessell","LT. COL.\nNORMAN BAESSELL",None),
 C("Norseman.","A UC-64\nNORSEMAN","SINGLE ENGINE"),
 C("Morgan.","FLIGHT OFFICER\nJOHN MORGAN","THE PILOT"),
 C("drizzle.","LOW CLOUD.\nDRIZZLE.",None),
 C("blind","NOT BUILT FOR\nFLYING BLIND",None),
 P("Twinwood","twinwood","RAF TWINWOOD FARM (1948 AERIAL)",**FC),
 P("observer","beachy","BEACHY HEAD",zoom=[1.1,1.2]),
 C("diary","A TEENAGE\nPLANE SPOTTER","NEAR READING"),
 C("last","THE LAST\nANYONE KNOWS",None,red=True),
 C("Nobody","NOBODY\nNOTICED",None,red=True),
 P("Ardennes.","bulge","THE BATTLE OF THE BULGE · 16 DEC 1944",**FC),
 C("eighteenth","18 DEC","MISSING NOTICED"),
 C("wife","23 DEC","HIS WIFE IS TOLD"),
 C("Christmas","CHRISTMAS EVE","THE WORLD FINDS OUT",red=True,sfx=[["stamp",0.0]]),
 CH("With",5,"The theories"),
 C("Shaw,","FRED SHAW","RAF NAVIGATOR"),
 P("Lancaster","lancaster","RAF LANCASTER BOMBERS"),
 C("dumped","BOMBS DUMPED\nOVER THE CHANNEL",None,red=True,sfx=[["hit",0.0]]),
 C("problems.","THE PROBLEMS",None),
 C("memory","ONE MAN'S\nMEMORY",None),
 C("record","NO RECORD\nFOR YEARS",None),
 C("wings.","“BARELY SEE\nTHEIR WINGS”","OTHER AIRMEN"),
 C("timing","THE TIMING\nDOESN'T FIT",None),
 C("darker","THE DARKER\nTHEORIES",None,red=True),
 C("embarrassing","DIED IN PARIS?\nA COVER-UP?",None),
 C("Germany.","A SECRET\nMISSION?",None),
 C("evidence","NO REAL\nEVIDENCE",None,red=True),
 C("1997","1997","A STORY THE JOURNALIST DISOWNED"),
 P("loved","miller-1","GLENN MILLER",zoom=[1.05,1.15]),
 CH("So",6,"What the file tells us"),
 C("2017,","2017","DENNIS SPRAGG · GLENN MILLER ARCHIVE"),
 C("unusual,","AN UNUSUAL\nROUTE",None),
 C("instruments","NOT CERTIFIED\nFOR INSTRUMENTS",None,red=True),
 C("weakness.","A KNOWN\nWEAKNESS",None),
 C("carburetor","CARBURETOR\nICE",None,red=True),
 P("Channel,","beachy","THE FREEZING CHANNEL",zoom=[1.2,1.3]),
 C("radio","NO TIME FOR\nA RADIO CALL",None),
 C("satisfying","NOT A\nSATISFYING ANSWER",None),
 C("fits","BUT IT FITS\nTHE EVIDENCE",None,red=True),
 P("missing","memorial","ARLINGTON NATIONAL CEMETERY · “MIA”",**FC),
 P("Bronze","cambridge","CAMBRIDGE AMERICAN CEMETERY · ENGLAND"),
 C("1954,","1954","“THE GLENN MILLER STORY” · JAMES STEWART"),
 C("1946,","1946","A NEW GLENN MILLER ORCHESTRA"),
 P("Mood","miller3","IN THE MOOD",zoom=[1.1,1.2],sfx=[["swing",0.0]]),
 C("Tell","WHAT DO\nYOU THINK?","TELL ME IN THE COMMENTS"),
 {"at":"Dossier","type":"end"},
]
json.dump({"title":"THE GLENN MILLER MYSTERY","case":"029","landscape":True,"scenes":S},open("scenes.json","w"),indent=1,ensure_ascii=False)
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
