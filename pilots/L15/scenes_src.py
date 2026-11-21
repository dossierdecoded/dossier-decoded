import json,re
P=lambda at,ph,label,**k: dict(at=at,type="photo",photo=f"photo-{ph}.jpg",focus=k.pop("focus",[0.5,0.45]),zoom=k.pop("zoom",[1.0,1.1]),label=label,**k)
C=lambda at,text,sub=None,**k: dict(at=at,type="card",text=text,**({"sub":sub} if sub else {}),**k)
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 7",sfx=[["paper",0.0]])
FC=dict(fit="contain")
S=[
 P("On","detroit","SITE OF THE MACHUS RED FOX · BLOOMFIELD TOWNSHIP, MI",zoom=[1.2,1.05],sfx=[["hit",0.0]]),
 C("thirtieth,","JULY 30, 1975",None),
 C("waiting","WAITING FOR\nA MEETING",None),
 C("pay","2:15 PM · PAY PHONE",None,sfx=[["phone",0.0]]),
 C("stood","\"STOOD UP\"",None,red=True),
 C("gone.","GONE",None,red=True),
 C("unlocked,","HIS CAR: UNLOCKED\nSAME PARKING LOT",None),
 C("note.","NO NOTE · NO STRUGGLE\nNO BODY",None,red=True),
 P("Jimmy","hoffa-1","JAMES R. \"JIMMY\" HOFFA",**FC),
 C("fifty","50+ YEARS",None),
 C("rose,","THE RISE · THE FALL\nTHE EVIDENCE",None),
 CH("James",2,"The rise"),
 C("Indiana,","BRAZIL, INDIANA · 1913",None),
 C("fourteen","LEFT SCHOOL\nAT 14",None),
 C("strike.","HIS FIRST STRIKE",None,sfx=[["stamp",0.0]]),
 C("1932,","1932","INTERNATIONAL BROTHERHOOD OF TEAMSTERS"),
 C("arrested","ARRESTED\nMANY TIMES",None),
 P("national","teamsters","TEAMSTERS HEADQUARTERS · WASHINGTON, D.C.",**FC),
 C("1957,","1957 · PRESIDENT",None,red=True),
 C("two","~2 MILLION\nMEMBERS",None),
 C("contract","FIRST NATIONAL\nTRUCKING CONTRACT",None),
 C("hero","A HERO\nTO MEMBERS",None),
 C("organized","TIES TO\nORGANIZED CRIME",None,red=True),
 CH("By",3,"The feud"),
 C("Senate","SENATE INVESTIGATION\nINTO UNION CORRUPTION",None),
 C("Kennedy.","CHIEF COUNSEL:\nROBERT KENNEDY",None),
 C("blood","\"A BLOOD FEUD\"",None,red=True),
 C("AFL-CIO","TEAMSTERS EXPELLED\nFROM THE AFL-CIO",None),
 C("1961,","1961 · KENNEDY:\nATTORNEY GENERAL",None),
 C("1964,","1964 · CONVICTED\nTWICE",None,red=True,sfx=[["stamp",0.0]]),
 C("tampering,","JURY TAMPERING",None),
 C("fraud,","PENSION FUND FRAUD",None),
 C("hundreds","HUNDREDS OF MILLIONS",None),
 C("casinos","LOANS TO\nLAS VEGAS CASINOS",None,red=True),
 C("Whoever","CONTROL THE UNION =\nCONTROL THE MONEY",None),
 P("1967,","lewisburg","U.S. PENITENTIARY LEWISBURG",**FC),
 CH("Even",4,"The deal"),
 C("Fitzsimmons,","FRANK FITZSIMMONS",None),
 C("resigned","1971 · HOFFA RESIGNS",None),
 P("Nixon","nixon","PRESIDENT RICHARD NIXON",**FC),
 C("catch.","THE CATCH",None,red=True),
 C("barred","BANNED FROM UNION\nMANAGEMENT UNTIL 1980",None,red=True),
 C("lost.","HE LOST",None),
 C("back.","HE WANTED HIS\nUNION BACK",None),
 C("pension","EASY ACCESS TO\nTHE PENSION FUND",None),
 C("exposing","TALKING ABOUT EXPOSING\nMOB INFLUENCE",None),
 C("dangerous","DANGEROUS",None,red=True,sfx=[["hit",0.0]]),
 CH("Which",5,"The last afternoon"),
 C("calendar","2:00 PM",None),
 P("Machus","detroit","SITE OF THE MACHUS RED FOX",zoom=[1.0,1.15]),
 C("Giacalone,","ANTHONY GIACALONE",None),
 C("Provenzano,","ANTHONY PROVENZANO",None),
 C("Neither","NEITHER CAME",None,red=True),
 C("alibi","ALIBIS",None),
 C("quarter","LAST SEEN\n~2:45 PM",None,red=True),
 C("struggle,","NO STRUGGLE",None),
 P("maroon","car","A 1970s MERCURY (SIMILAR MODEL)",**FC,sfx=[["car",0.0]]),
 C("O'Brien,","CHARLES \"CHUCKIE\" O'BRIEN",None),
 C("dogs","POLICE DOGS:\nHOFFA'S SCENT",None),
 C("DNA","2001 · DNA",None),
 C("denied","NEVER CHARGED",None,red=True),
 CH("The",6,"The search"),
 P("Hundreds","fbi","FEDERAL BUREAU OF INVESTIGATION",**FC),
 C("Hoffex","THE \"HOFFEX\" MEMO · 1976",None,sfx=[["paper",0.0]]),
 C("killed","KILLED BY\nORGANIZED CRIME?",None,red=True),
 C("Nobody","NOBODY CHARGED\nWITH MURDER",None),
 C("1982,","1982 · DECLARED\nLEGALLY DEAD",None),
 P("Giants","giants","GIANTS STADIUM · EAST RUTHERFORD, NJ",zoom=[1.0,1.1]),
 C("torn","2010 · DEMOLISHED\nNOTHING FOUND",None),
 C("2004,","2004 · DETROIT\nFLOORBOARDS",None,sfx=[["dig",0.0]]),
 C("Irishman.","\"THE IRISHMAN\"",None),
 C("2006,","2006 · HORSE FARM",None,sfx=[["dig",0.0]]),
 C("2013,","2013 · A FIELD",None),
 P("2021,","skyway","PULASKI SKYWAY · JERSEY CITY",zoom=[1.0,1.15]),
 C("drum.","\"A STEEL DRUM\"",None),
 C("evidentiary","\"NOTHING OF\nEVIDENTIARY VALUE\"",None,red=True,sfx=[["stamp",0.0]]),
 CH("Here's",7,"Our analysis"),
 C("memo.","THE FBI'S\nOWN THEORY",None),
 C("setup.","A SETUP?",None,red=True),
 C("willingly.","HE GOT IN\nWILLINGLY?",None),
 C("runs","THE EVIDENCE\nRUNS OUT",None),
 C("dead.","MOST SUSPECTS:\nDEAD",None),
 C("open.","CASE STILL OPEN",None,red=True),
 C("Where","WHERE IS\nJIMMY HOFFA?","TELL ME IN THE COMMENTS"),
 {"at":"Dossier","type":"end"},
]
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

json.dump({"title":"JIMMY HOFFA","case":"013","landscape":True,"scenes":S},open("scenes.json","w"),indent=1,ensure_ascii=False)
