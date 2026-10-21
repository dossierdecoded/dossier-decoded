import json,re
P=lambda at,ph,label,**k: dict(at=at,type="photo",photo=f"photo-{ph}.jpg",focus=k.pop("focus",[0.5,0.45]),zoom=k.pop("zoom",[1.0,1.1]),label=label,**k)
C=lambda at,text,sub=None,**k: dict(at=at,type="card",text=text,**({"sub":sub} if sub else {}),**k)
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
FC=dict(fit="contain")
S=[
 P("In","cyclops2","USS CYCLOPS · US NAVY",stamp="LOST",stamp_at="arrived."),
 C("five","542 FEET\n~10,000 TONS OF ORE",None),
 C("hundreds","306 ABOARD","THE NAVY'S USUAL COUNT",red=True),
 C("Baltimore","DUE IN\nBALTIMORE","13 MARCH 1918"),
 C("arrived.","NEVER\nARRIVED",None,red=True,sfx=[["hit",0.0]]),
 C("distress","NO DISTRESS CALL\nNO LIFEBOAT",None),
 C("wreckage.","NO WRECKAGE.\nNO BODIES.",None,red=True),
 C("century","ONE OF THE NAVY'S\nLARGEST NON-COMBAT\nLOSSES OF LIFE",None),
 C("nobody","NOBODY KNOWS\nWHAT HAPPENED",None,red=True),
 C("cargo","THE CARGO · THE ENGINE\nTHE CAPTAIN · THE THEORIES",None),
 P("disappear.","cyclops-1","CASE FILE: THE USS CYCLOPS",zoom=[1.1,1.2]),
 CH("The",2,"The collier"),
 C("collier,","A COLLIER","A FLOATING COAL DEPOT"),
 C("Philadelphia","LAUNCHED 1910","WILLIAM CRAMP & SONS · PHILADELPHIA"),
 C("fuel","FUEL FOR\nTHE FLEET",None),
 P("towers","cyclops-1","HER COAL-HANDLING TOWERS",focus=[0.55,0.4],zoom=[1.3,1.45]),
 C("eight","8,000 TONS NORMAL\n10,800 TONS MAX",None),
 C("Baltic","THE BALTIC →\nTHE CARIBBEAN",None),
 C("Veracruz","VERACRUZ · 1914","FUEL · REFUGEES"),
 C("thanks","THANKED BY THE\nSTATE DEPARTMENT",None),
 C("workhorse.","A WORKHORSE",None),
 C("entered","1917","THE US ENTERS WORLD WAR I"),
 C("formally","COMMISSIONED\n1 MAY 1917","A NAVY CREW"),
 P("Saint-Nazaire","stnazaire","SAINT-NAZAIRE, FRANCE (MONUMENT TO THE 1917 LANDING)",**FC),
 C("Transportation","NAVAL OVERSEAS\nTRANSPORTATION\nSERVICE",None),
 C("January","JANUARY 1918","COAL FOR BRITISH SHIPS · SOUTH AMERICA"),
 CH("The",3,"The last voyage"),
 P("manganese","manganese","MANGANESE ORE",**FC),
 C("steel","FOR STEEL\nFOR THE WAR",None),
 C("Rio","RIO DE JANEIRO","~10,800 TONS LOADED"),
 C("dense.","DENSE.\nHEAVY.\nLOW IN THE WATER.",None),
 C("problem.","ANOTHER\nPROBLEM",None,red=True),
 C("cracked","CRACKED\nCYLINDER","STARBOARD ENGINE",red=True,sfx=[["creak",0.0]]),
 C("thousands","ONE ENGINE",None),
 C("survey","“RETURN TO THE US\nFOR REPAIRS”","SURVEY BOARD"),
 C("Salvador","RIO → SALVADOR\n→ BALTIMORE",None),
 C("ten","~10 KNOTS",None),
 P("submarines","uboat","A GERMAN U-BOAT · WWI (PAINTING)",**FC),
 C("third","3 MARCH 1918","AN UNSCHEDULED STOP",red=True),
 P("Barbados.","barbados","BARBADOS (TODAY)"),
 P("load","plimsoll","A SHIP'S LOAD LINE (EXAMPLE)",**FC),
 C("fourth","4 MARCH 1918","SAILS FOR BALTIMORE"),
 P("last","cyclops2","LAST SEEN",zoom=[1.15,1.25],sfx=[["telegraph",0.0]]),
 CH("Her",4,"The captain"),
 P("Worley.","worley","CAPT. GEORGE WORLEY",**FC),
 C("Germany,","BORN IN GERMANY","AS JOHAN FREDERICK WICHMANN"),
 C("jumping","JUMPED SHIP","SAN FRANCISCO"),
 C("saloon","A SALOON","THE BARBARY COAST"),
 C("reserve.","NAVAL RESERVE\n1917",None),
 C("abusive","“ABUSIVE”\n“VIOLENT”","FORMER CREW",red=True),
 C("pistol.","A PISTOL",None),
 C("underwear","LONG UNDERWEAR\nAND A DERBY HAT",None),
 C("pro-German.","“PRO-GERMAN”?",None,red=True),
 C("consul","THE CONSUL'S\nTELEGRAM","BARBADOS",sfx=[["telegraph",0.0]]),
 C("engines","“ENGINES VERY\nPOOR CONDITION”",None),
 C("Germanic","“MANY GERMANIC\nNAMES”",None),
 C("fear","“I FEAR FATE\nWORSE THAN\nSINKING”","CONSUL LIVINGSTON",red=True),
 C("proven.","NEVER PROVEN",None),
 P("betrayed","worley","BETRAYED BY HER CAPTAIN?",fit="contain",zoom=[1.1,1.2]),
 CH("The",5,"Overdue"),
 C("thirteenth","DUE 13 MARCH",None),
 C("slow.","ONE ENGINE\n= SLOW?",None),
 C("Nothing.","NOTHING.",None,red=True),
 C("tanker","A SIGHTING?","9 MARCH · OFF VIRGINIA"),
 C("denied","DENIED",None,red=True,sfx=[["stamp",0.0]]),
 C("April","APRIL 1918","FRONT-PAGE NEWS"),
 C("vanish.","IT COULD NOT\nJUST VANISH",None),
 P("June","fdr","FRANKLIN D. ROOSEVELT (CENTRE), 1918 · ASSISTANT NAVY SECRETARY",**FC),
 C("lost","“LOST WITH\nALL HANDS”","1 JUNE 1918",red=True),
 C("investigation","“NONE THAT\nSATISFACTORILY\nACCOUNTS FOR HER\nDISAPPEARANCE”","THE NAVY'S INVESTIGATION"),
 C("Gottschalk,","ALFRED GOTTSCHALK","US CONSUL GENERAL · RIO"),
 C("settled.","306? 293? 231?","THE RECORDS DISAGREE"),
 C("families","THE FAMILIES NEVER\nGOT AN ANSWER",None),
 C("funerals","NO COFFINS.\nNO GRAVES.",None),
 CH("So",6,"What happened"),
 P("enemy.","uboat","1 · A GERMAN U-BOAT?",**FC),
 C("records","NO GERMAN CLAIM",None,red=True),
 C("Worley.","2 · SABOTAGE?\nMUTINY?","NO EVIDENCE"),
 C("Bermuda","3 · THE BERMUDA\nTRIANGLE?","A LATER IDEA"),
 P("tenth","virginia","CAPE HENRY, VIRGINIA (TODAY)",**FC),
 C("historians","“PROBABLY SANK IN\nAN UNEXPECTED\nSTORM”","NAVY HISTORIANS"),
 P("Picture","wave","HEAVY SEAS (ILLUSTRATION)",sfx=[["waves",0.0]]),
 C("Loaded","1 ENGINE\nFULL LOAD\nA STORM",None,red=True),
 C("Lloyd's","THE ORE\nCOULD SHIFT","LLOYD'S OF LONDON EXPERT · 2009"),
 C("broke","THE HULL\nBROKE?",None,red=True,sfx=[["creak",0.0]]),
 C("admiral","ERODED\nSTEEL BEAMS?","A RETIRED ADMIRAL'S THEORY"),
 C("message.","NO TIME FOR\nA MESSAGE",None),
 C("sister","HER SISTER SHIPS",None),
 P("Proteus","nereus","SISTER SHIP USS NEREUS · LOST 1941",**FC),
 C("vanished","1941 · BOTH\nVANISHED",None,red=True,sfx=[["hit",0.0]]),
 C("Same","SAME DESIGN.\nSAME CARGO.\nSAME SILENCE.",None),
 C("storm,","STORM? DESIGN FLAW?\nSOMETHING ELSE?",None),
 C("Tell","WHAT DO\nYOU THINK?","TELL ME IN THE COMMENTS"),
 {"at":"Dossier","type":"end"},
]
json.dump({"title":"THE USS CYCLOPS","case":"025","landscape":True,"scenes":S},open("scenes.json","w"),indent=1,ensure_ascii=False)
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
