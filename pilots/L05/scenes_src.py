import json,re
P=lambda at,ph,label,**k: dict(at=at,type="photo",photo=f"photo-{ph}.jpg",focus=k.pop("focus",[0.5,0.45]),zoom=k.pop("zoom",[1.0,1.1]),label=label,**k)
C=lambda at,text,sub=None,**k: dict(at=at,type="card",text=text,**({"sub":sub} if sub else {}),**k)
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
FC=dict(fit="contain")
S=[
 P("The","eldridge-1","USS ELDRIDGE (DE-173)",stamp="VANISHED?",stamp_at="gone."),
 P("October","yard","PHILADELPHIA NAVY YARD"),
 P("warship,","eldridge-2","THE DESTROYER ESCORT USS ELDRIDGE"),
 P("green","fog","A “GREEN FOG” (ILLUSTRATION)"),
 C("hidden.","NOT HIDDEN.\nGONE.",None,red=True,sfx=[["hit",0.0]]),
 P("reappeared","norfolk","NORFOLK, VIRGINIA (PRESENT DAY)"),
 P("vanished","eldridge-1","…AND BACK AGAIN",zoom=[1.1,1.2]),
 C("crew,","THE CREW",None),
 C("fused","FUSED INTO\nTHE DECK","THE LEGEND SAYS",red=True),
 C("mad.","DRIVEN MAD","FADING IN AND OUT"),
 C("darkest","THE NAVY'S\nDARKEST SECRET?",None),
 C("books,","BOOKS · FILMS\nLATE-NIGHT RADIO",None),
 C("nobody","WHERE DID IT\nCOME FROM?",None,red=True),
 C("paper","FOLLOW THE\nPAPER TRAIL",None,sfx=[["paper",0.0]]),
 C("letters.","IT STARTS WITH\nLETTERS",None,red=True,sfx=[["typewriter",0.0]]),
 C("records","CASE FILE:\nTHE PHILADELPHIA\nEXPERIMENT","WHAT THE RECORDS SAY"),
 CH("In",2,"The letters"),
 C("Case","“THE CASE\nFOR THE UFO”","MORRIS K. JESSUP · 1955"),
 C("January","JANUARY 1956","THE LETTERS BEGIN",sfx=[["typewriter",0.0]]),
 C("signed","CARLOS MIGUEL\nALLENDE",None,red=True),
 P("merchant","convoy","A WARTIME ATLANTIC CONVOY"),
 C("Furuseth.","S.S. ANDREW\nFURUSETH","A MERCHANT SHIP"),
 P("Einstein","einstein2","ALBERT EINSTEIN",**FC),
 C("Reno,","“FRANKLIN RENO”","THE SCIENTIST HE NAMED"),
 C("rambling,","RAMBLING.\nODDLY CAPITALIZED.",None),
 C("specific.","A SHIP.\nA PLACE.\nA DATE.",None),
 C("proof.","PROOF?",None,red=True),
 C("remember","“MEMORY TO\nBE RECOVERED”",None),
 P("newspaper","yard","PHILADELPHIA · “THE BAR STORY”",zoom=[1.15,1.25]),
 C("never","NEVER FOUND",None,red=True),
 C("exist","ALLENDE\nDIDN'T EXIST",None),
 C("Meredith","CARL MEREDITH\nALLEN","HIS REAL NAME",red=True,sfx=[["stamp",0.0]]),
 CH("Before",3,"The book at the Navy"),
 P("Office","onr","OFFICE OF NAVAL RESEARCH",**FC),
 C("Easter.","“HAPPY EASTER”","AN ANONYMOUS PACKAGE · 1955",sfx=[["paper",0.0]]),
 C("margins","NOTES IN\nTHE MARGINS",None),
 C("three","3 SHADES\nOF BLUE INK","3 “WRITERS”"),
 C("Jemi.","“JEMI”",None,red=True),
 C("1957,","1957","JESSUP IS INVITED IN"),
 C("handwriting","SAME\nHANDWRITING",None,red=True,sfx_at=[["hit","Allende."]]),
 C("Sherby","CAPT. SIDNEY SHERBY\nCMDR. GEORGE HOOVER","OFFICE OF NAVAL RESEARCH"),
 P("Varo","dallas","GARLAND, TEXAS",**FC),
 C("dozen","12 → 127\nCOPIES","THE “VARO EDITION”"),
 C("substance","“NOTHING OF\nSUBSTANCE”","CMDR. HOOVER"),
 C("matter.","BUT IT\nDIDN'T MATTER",None,red=True),
 C("officers","NAVAL OFFICERS\nA MILITARY CONTRACTOR",None),
 C("believers,","“PROOF THE NAVY\nWAS WORRIED”",None,red=True),
 C("1959,","1959","JESSUP DIES"),
 C("legend","THE LEGEND\nKEEPS GOING",None),
 CH("For",4,"A legend grows"),
 C("1965,","1965","VINCENT GADDIS · “INVISIBLE HORIZONS”"),
 P("Berlitz,","berlitz","CHARLES BERLITZ",**FC),
 C("Triangle,","THE BERMUDA\nTRIANGLE","HIS EARLIER BESTSELLER"),
 C("Invisibility,","“PROJECT\nINVISIBILITY”","1979 · BERLITZ & MOORE"),
 C("fact.","PRESENTED\nAS FACT",None,red=True),
 C("novel","“THIN AIR”","A 1978 THRILLER NOVEL"),
 C("1984,","1984","THE HOLLYWOOD FILM"),
 C("time-travel","TIME TRAVEL",None,red=True),
 C("Bielek","AL BIELEK","CLAIMED HE WAS ABOARD"),
 C("conference,","1990","A UFO CONFERENCE"),
 C("Notice","NOTICE WHAT\nHAPPENED",None),
 C("fog.","+ GREEN FOG\n+ TELEPORTATION\n+ TIME TRAVEL",None),
 C("trapped","+ SAILORS IN\nTHE DECK",None),
 C("real,","MORE TELLERS =\nMORE “REAL”",None),
 C("books,","BOOKS · A NOVEL\nA MOVIE",None),
 C("documents","SO WHAT DO THE\nDOCUMENTS SAY?",None,red=True),
 CH("Start",5,"What the records show"),
 P("commissioned","eldridge-2","COMMISSIONED · AUGUST 1943",zoom=[1.1,1.2]),
 P("York.","nyard","NEW YORK NAVY YARD · 1945"),
 C("diary,","THE WAR DIARY","USS ELDRIDGE · OCTOBER 1943",sfx=[["paper",0.0]]),
 C("nowhere","NOWHERE NEAR\nPHILADELPHIA",None,red=True,sfx=[["stamp",0.0]]),
 C("Bermuda","BERMUDA","UNTIL 15 OCTOBER"),
 P("convoy","convoy","CONVOY TO NEW YORK · 18 OCTOBER",zoom=[1.1,1.2]),
 C("harbor","NEW YORK HARBOR","UNTIL 1 NOVEMBER"),
 C("Allen's","S.S. ANDREW\nFURUSETH","ALLEN'S SHIP"),
 C("Henry,","OFF CAPE HENRY","4 OCTOBER"),
 C("twenty-fifth,","LEFT NORFOLK\n25 OCTOBER","A WEEK BEFORE THE ELDRIDGE ARRIVED",red=True),
 C("captain","“NOTHING\nUNUSUAL”","THE FURUSETH'S CAPTAIN"),
 C("reunion","1999 REUNION","“NEVER MADE PORT IN PHILADELPHIA”"),
 C("scientific","THE SCIENCE?",None),
 C("conform","“DOES NOT CONFORM\nTO KNOWN\nPHYSICAL LAWS”","THE NAVY",red=True),
 P("unified","einstein2","UNIFIED FIELD THEORY · NEVER COMPLETED",fit="contain",zoom=[1.1,1.2]),
 P("consultant","einstein","EINSTEIN TO THE NAVY'S BUREAU OF ORDNANCE · 1943",**FC),
 C("explosives.","EXPLOSIVES.\nNOT INVISIBILITY.",None,red=True),
 P("Office","onr","OFFICE OF NAVAL RESEARCH",**FC),
 C("1996","“NEVER”","ONR STATEMENT · 1996"),
 C("exist","ONR FOUNDED\n1946",None,red=True),
 CH("So",6,"What really happened"),
 P("mines","mine","A GERMAN AIR-DROPPED MINE · WWII",**FC),
 C("cables","DEGAUSSING","CABLES AROUND THE HULL CANCEL ITS MAGNETISM",red=True,sfx=[["hum",0.0]]),
 C("mine.","“INVISIBLE”\nTO A MINE",None,red=True),
 C("visible","STILL VISIBLE","EYE · RADAR · SONAR"),
 P("Vallée","vallee","JACQUES VALLÉE · LINKED IT TO USS ENGSTROM",**FC),
 C("veteran","“NOBODY\nVANISHED”","A VETERAN OF THE BAR STORY"),
 C("Carl","CARL ALLEN","“TO SCARE HIM”"),
 C("leg-puller.","“A MASTER\nLEG-PULLER”","HIS FAMILY",red=True),
 C("file","HOW A LEGEND\nIS BUILT","WHAT THE FILE TELLS US"),
 C("One","ONE MAN'S LETTERS",None),
 C("government","A GOVERNMENT\nOFFICE",None),
 C("curious,","CURIOUS.\nNOT ALARMED.",None),
 C("decades","DECADES OF\nRETELLING",None),
 P("scariest","eldridge-1","THE PHILADELPHIA EXPERIMENT",zoom=[1.1,1.25]),
 C("history.","A FEW LETTERS\n→ HISTORY",None,red=True,sfx=[["stamp",0.0]]),
 C("Tell","WHAT DO\nYOU THINK?","TELL ME IN THE COMMENTS"),
 {"at":"Dossier","type":"end"},
]
json.dump({"title":"THE PHILADELPHIA EXPERIMENT","case":"022","landscape":True,"scenes":S},open("scenes.json","w"),indent=1,ensure_ascii=False)
# timing check
al=json.load(open("assets/alignment.json"));ws=[];cur=None;d=0
for ch,s in zip(al["characters"],al["character_start_times_seconds"]):
    if ch=="[":d+=1;continue
    if ch=="]":d-=1;continue
    if d:continue
    if ch.isspace():
        if cur:ws.append(cur);cur=None
        continue
    cur=cur or [ "",s];cur[0]+=ch
if cur:ws.append(cur)
n=lambda t:re.sub(r"[^a-z0-9']","",t.lower().replace("’","'"))
i=0;ts=[]
for sc in S:
    while n(ws[i][0])!=n(sc["at"]): i+=1
    ts.append(ws[i][1])
for k,(a,b) in enumerate(zip(ts,ts[1:]+[ws[-1][1]+3])):
    if b-a<2.2 or b-a>13: print(k,S[k]["at"],round(b-a,1))
print(len(S),"scenes")
