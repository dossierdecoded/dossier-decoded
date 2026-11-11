import json,re
P=lambda at,ph,label,**k: dict(at=at,type="photo",photo=f"photo-{ph}.jpg",focus=k.pop("focus",[0.5,0.45]),zoom=k.pop("zoom",[1.0,1.1]),label=label,**k)
C=lambda at,text,sub=None,**k: dict(at=at,type="card",text=text,**({"sub":sub} if sub else {}),**k)
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
FC=dict(fit="contain")
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
S=[
 P("In","factory","DIAL PAINTERS AT WORK · 1920s",zoom=[1.25,1.05],sfx=[["tick",0.0]]),
 C("radioactive","RADIOACTIVE PAINT\nIN THEIR MOUTHS",None,red=True),
 C("safe.","“SAFE”",None,sfx=[["stamp",0.0]]),
 C("teeth","TEETH FELL OUT\nJAWS CRUMBLED",None,red=True),
 C("glow","THEY GLOWED\nIN THE DARK","THE RADIUM DUST"),
 C("Doctors","COMPANY DOCTORS:\n“SOMETHING ELSE”",None),
 C("sue","THEY SUED",None,red=True),
 C("report","COMING UP:\nTHE HIDDEN REPORT\nTHE BONES\nTHE COURTROOM",None),
 CH("discovered",2,"The miracle element"),
 P("1898.","curie","PIERRE & MARIE CURIE · THEIR LAB",**FC),
 C("glowed.","IT GLOWED",None),
 P("tonics,","radithor","“CERTIFIED RADIOACTIVE WATER”",**FC),
 C("cancer,","“A LITTLE RADIUM\nIS GOOD FOR YOU”",None),
 C("luminous","LUMINOUS\nPAINT",None),
 P("Undark.","undark","“UNDARK” · 1921 ADVERT",**FC,zoom=[1.0,1.15]),
 C("War,","WORLD WAR I","WATCHES · INSTRUMENT DIALS"),
 C("invented","SABIN VON SOCHOCKY","INVENTED UNDARK"),
 C("1928.","DIED 1928","RADIUM POISONING",red=True),
 C("teenagers,","MANY WERE\nTEENAGERS",None),
 CH("paid",3,"The dial painters"),
 C("glamorous","“A GLAMOROUS JOB”",None),
 C("camel","CAMEL-HAIR\nBRUSHES",None),
 C("Lip,","LIP.\nDIP.\nPAINT.",None,red=True,sfx=[["stamp",0.0]]),
 P("Over","factory","OVER AND OVER, ALL DAY",zoom=[1.4,1.6]),
 C("fifty","~250 DIALS\nA DAY",None),
 C("swallowed","SWALLOWED\nEVERY DAY",None,red=True),
 C("harmless.","“HARMLESS”",None),
 C("nails","NAILS · TEETH\nFOR FUN",None),
 C("Dust","DUST ON\nHAIR AND CLOTHES",None),
 C("chemists","THE CHEMISTS:\nLEAD SCREENS · MASKS · TONGS",None,red=True),
 C("calcium","RADIUM ≈ CALCIUM",None),
 C("bones.","INTO THE\nBONES",None,red=True,sfx=[["geiger",0.0]]),
 CH("Around",4,"Radium jaw"),
 C("Teeth","TEETH FELL OUT",None),
 C("Jawbones","JAWBONES\nCRUMBLED",None,red=True),
 C("Mollie","MOLLIE MAGGIA","DIED 1922 · BLAMED ON SYPHILIS"),
 C("dentist","“RADIUM JAW”","A NEW YORK DENTIST"),
 C("1924,","1924:\nTHE PAINT IS\nLIKELY THE CAUSE","A HARVARD STUDY",red=True,sfx=[["paper",0.0]]),
 C("share","NOT SHARED",None,sfx=[["stamp",0.0]]),
 C("health.","“WORKERS IN\nGOOD HEALTH”","REPORT GIVEN TO STATE OFFICIALS"),
 C("Martland,","HARRISON MARTLAND","NEWARK MEDICAL EXAMINER"),
 C("breath.","RADIOACTIVE\nBREATH",None,sfx=[["geiger",0.0]]),
 C("first","FIRST PROOF:\nRADIUM BUILDS UP\nIN THE BODY",None),
 C("exhumed.","1927","MOLLIE MAGGIA EXHUMED"),
 C("radioactive.","HER BONES:\nRADIOACTIVE",None,red=True,sfx=[["hit",0.0]]),
 C("never","NEVER\nSYPHILIS",None,red=True),
 CH("By",5,"The trial"),
 P("Fryer","fryer","GRACE FRYER",**FC),
 C("afraid","LAWYERS\nWERE AFRAID",None),
 C("Berry","RAYMOND BERRY","LAWYER · 1927"),
 C("clock.","THE CLOCK",None),
 C("long.","“WAITED TOO LONG”",None,red=True),
 C("admit","AN INJURY NO ONE\nWOULD ADMIT",None),
 C("Hussman,","GRACE FRYER · EDNA HUSSMAN\nKATHERINE SCHAUB\nQUINTA McDONALD · ALBINA LARICE",None),
 C("Radium","THE RADIUM GIRLS",None),
 C("Curie","MARIE CURIE",
"“NO KNOWN WAY TO REMOVE IT”"),
 C("cured.","NOT SUING\nTO BE CURED",None),
 C("delay,","DELAY",None),
 C("oath.","TOO SICK TO\nRAISE THEIR ARMS",None,red=True),
 C("thousand","$10,000 EACH\n$600 A YEAR","1928 SETTLEMENT · + MEDICAL AND LEGAL COSTS",sfx=[["gavel",0.0]]),
 C("decade.","MOST DEAD\nWITHIN A DECADE",None,red=True),
 C("Ottawa,","OTTAWA, ILLINOIS","RADIUM DIAL COMPANY"),
 C("Donohue,","CATHERINE DONOHUE","1938 · SHE WON",red=True),
 C("home,","THE HEARING\nAT HER HOME",None),
 C("1939,","1939","THE COMPANY LOST"),
 CH("changed",6,"What the file tells us"),
 C("sue","THE RIGHT TO SUE\nFOR JOB DISEASES",None),
 C("bomb","THE ATOMIC AGE","SAFETY LIMITS FOR RADIATION"),
 C("decades","STUDIED\nFOR DECADES",None),
 C("volunteered,","THEY VOLUNTEERED",None),
 P("chemists","factory","THE CHEMISTS PROTECTED THEMSELVES",zoom=[1.1,1.25]),
 C("named","A REPORT THAT\nNAMED THE CAUSE",None,red=True),
 C("truth,","THE TRUTH",None),
 C("believe","HOW LONG WOULD\nYOU BELIEVE IT?","TELL ME IN THE COMMENTS"),
 {"at":"Dossier","type":"end"},
]
json.dump({"title":"THE RADIUM GIRLS","case":"040","landscape":True,"scenes":S},open("scenes.json","w"),indent=1,ensure_ascii=False)
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
