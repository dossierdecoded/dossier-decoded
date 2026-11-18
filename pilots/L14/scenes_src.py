import json,re
P=lambda at,ph,label,**k: dict(at=at,type="photo",photo=f"photo-{ph}.jpg",focus=k.pop("focus",[0.5,0.45]),zoom=k.pop("zoom",[1.0,1.1]),label=label,**k)
C=lambda at,text,sub=None,**k: dict(at=at,type="card",text=text,**({"sub":sub} if sub else {}),**k)
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 7",sfx=[["paper",0.0]])
FC=dict(fit="contain")
S=[
 P("On","croatoan2","\"CRO\" TREE · MODERN RECREATION, FORT RALEIGH",zoom=[1.2,1.05],sfx=[["hit",0.0]]),
 C("walked","AUGUST 18, 1590",None),
 C("birthday.","HIS GRANDDAUGHTER'S\n3RD BIRTHDAY",None),
 C("nine","LAST SEEN:\n9 DAYS OLD",None),
 C("hundred","115 MEN, WOMEN\nAND CHILDREN",None),
 C("gone.","THE HOUSES\nWERE GONE",None,red=True),
 P("tall","fort","FORT RALEIGH · ROANOKE ISLAND",**FC),
 C("people.","NO PEOPLE · NO BODIES\nNO GRAVES",None,red=True),
 C("Carved","ONE WORD",None,sfx=[["carve",0.0]]),
 P("Croatoan.","croatoan2","\"CRO\" · MODERN RECREATION",zoom=[1.3,1.6],focus=[0.5,0.5]),
 C("four","400+ YEARS LATER",None),
 C("Lost","THE LOST COLONY\nOF ROANOKE",None,red=True),
 CH("To",2,"The first attempt"),
 C("foothold","A FOOTHOLD IN\nNORTH AMERICA",None),
 P("Elizabeth","elizabeth","QUEEN ELIZABETH I",**FC),
 P("favorites,","raleigh","WALTER RALEIGH",**FC),
 P("1584,","outerbanks","THE OUTER BANKS · NORTH CAROLINA",sfx=[["waves",0.0]]),
 C("glowing","GLOWING\nREPORTS",None),
 C("Manteo","MANTEO & WANCHESE",None),
 C("Croatoan,","MANTEO:\nA CROATOAN",None,red=True),
 C("1585,","1585","~100 MEN · ROANOKE ISLAND"),
 C("badly.","IT WENT BADLY",None),
 C("food.","DEPENDENT ON NATIVE\nCOMMUNITIES FOR FOOD",None),
 C("Lane,","RALPH LANE ATTACKS\nWINGINA",None,red=True),
 C("June","JUNE 1586","DRAKE TAKES THEM HOME"),
 C("relief","A RELIEF FLEET\nFINDS IT DESERTED",None),
 C("fifteen","15 MEN\nLEFT BEHIND",None),
 C("never","NEVER SEEN AGAIN",None,red=True,sfx=[["stamp",0.0]]),
 CH("Raleigh",3,"The second colony"),
 C("1587,","1587","~115 COLONISTS"),
 P("governor","secotan","JOHN WHITE · VILLAGE OF SECOTAN (WATERCOLOR)",**FC),
 C("Eleanor,","ELEANOR DARE","PREGNANT"),
 C("plan","THE PLAN:\nNOT ROANOKE",None),
 P("Chesapeake","white","JOHN WHITE'S MAP OF THE COAST",**FC),
 C("Fernandes,","SIMON FERNANDES\nREFUSED",None,red=True),
 C("Howe,","GEORGE HOWE\nKILLED",None),
 C("Eleanor","AUGUST 18, 1587",None),
 P("Virginia","dare","VIRGINIA DARE (19TH-CENTURY ILLUSTRATION)",**FC),
 C("supplies,","JOHN WHITE SAILS\nFOR SUPPLIES",None),
 C("moved,","IF THEY MOVED:\nCARVE WHERE",None),
 C("danger,","IF IN DANGER:\nADD A CROSS",None,red=True),
 CH("White",4,"The war that got in the way"),
 C("crisis.","SPAIN PREPARES\nTO INVADE",None),
 P("Armada","armada","THE SPANISH ARMADA",**FC),
 C("seaworthy","EVERY SHIP\nSTAYS HOME",None),
 C("robbed","ATTACKED AND\nROBBED AT SEA",None,red=True),
 C("summer","SUMMER 1588","THE ARMADA"),
 C("priority.","NOT A PRIORITY",None),
 C("ride","1590","ON PRIVATEER SHIPS"),
 P("weather","storm","STORM AT SEA (17TH-CENTURY PAINTING)",**FC,sfx=[["waves",0.0]]),
 C("seven","7 SAILORS\nDROWNED",None,red=True),
 C("smoke","SMOKE ON\nTHE ISLAND",None),
 C("songs","A TRUMPET\nINTO THE DARK",None,sfx=[["trumpet",0.0]]),
 C("Nobody","NOBODY\nANSWERED",None,red=True),
 CH("On",5,"What White found"),
 C("C,","C · R · O",None,sfx=[["carve",0.0]]),
 P("palisade","fort","A NEW WOODEN WALL",**FC),
 P("full","croatoan2","MODERN RECREATION · FORT RALEIGH",zoom=[1.2,1.5]),
 C("cross.","NO CROSS",None,red=True,sfx=[["stamp",0.0]]),
 P("Croatoan","hatteras","CROATOAN ISLAND (HATTERAS TODAY)",zoom=[1.0,1.1]),
 C("chests","CHESTS DUG UP",None),
 C("books","BOOKS TORN\nMAPS RUINED\nARMOR RUSTING",None),
 C("decided","BURIED BY THE\nCOLONISTS?",None),
 C("ready","READY TO SAIL\nFOR CROATOAN",None),
 C("anchor","AN ANCHOR\nCABLE SNAPS",None,red=True),
 C("fleet","THEY HEAD HOME",None),
 C("never","WHITE NEVER\nMADE IT BACK",None,red=True),
 CH("So",6,"The theories"),
 C("first,","THEORY 1:\nTHEY JOINED THE CROATOAN",None),
 P("2013,","hatteras","HATTERAS ISLAND",zoom=[1.1,1.25]),
 C("sword,","SWORD PIECES · GUN PART\nA WRITING SLATE",None),
 C("mixed","OR JUST\nTRADE GOODS?",None),
 C("second","THEORY 2:\nA HIDDEN MAP",None),
 P("patch","white","JOHN WHITE'S MAP · BRITISH MUSEUM",**FC),
 C("fifty","50 MILES INLAND",None,red=True),
 C("Site","\"SITE X\"",None),
 C("graves","NO GRAVES\nNO BUILDINGS",None),
 C("third","THEORY 3:\nKILLED",None,red=True),
 C("Jamestown","JAMESTOWN · 1607",None),
 C("proven.","NEVER PROVEN",None,sfx=[["stamp",0.0]]),
 C("1998,","1998 · TREE RINGS",None),
 C("droughts","WORST DROUGHT\nIN ~800 YEARS",None,red=True),
 CH("Here's",7,"Our analysis"),
 C("houses","TIME TO TAKE\nTHE HOUSES APART",None),
 C("distress","NO DISTRESS SIGN",None),
 C("guess","THEY SPLIT UP?",None,red=True),
 P("south","hatteras","SOUTH: CROATOAN",zoom=[1.15,1.0]),
 P("inland,","white","INLAND: SITE X",**FC),
 C("drought,","TOO MANY\nTO FEED",None),
 C("married","MARRIED INTO\nNATIVE COMMUNITIES",None),
 C("lost.","NEVER LOST.\nJUST NEVER FOUND.",None,red=True),
 C("think","WHAT HAPPENED\nTO THEM?","TELL ME IN THE COMMENTS"),
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
json.dump({"title":"THE LOST COLONY","case":"027","landscape":True,"scenes":S},open("scenes.json","w"),indent=1,ensure_ascii=False)
