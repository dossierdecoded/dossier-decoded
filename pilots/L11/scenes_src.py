import json,re
P=lambda at,ph,label,**k: dict(at=at,type="photo",photo=f"photo-{ph}.jpg",focus=k.pop("focus",[0.5,0.45]),zoom=k.pop("zoom",[1.0,1.1]),label=label,**k)
C=lambda at,text,sub=None,**k: dict(at=at,type="card",text=text,**({"sub":sub} if sub else {}),**k)
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
FC=dict(fit="contain")
CH=lambda at,n,title: dict(at=at,type="card",text=title.upper(),sub=f"CHAPTER {n} OF 6",sfx=[["paper",0.0]])
S=[
 P("On","atlantis","1 FEBRUARY 2003 · WAITING FOR COLUMBIA",zoom=[1.2,1.05]),
 C("Sixteen","16 MINUTES\nBEFORE LANDING",None,red=True,sfx=[["hit",0.0]]),
 P("seven","crew","ALL 7 KILLED · 17 YEARS AFTER CHALLENGER",zoom=[1.0,1.1]),
 C("spotted","SPOTTED WITHIN\nA DAY OF LAUNCH",None,red=True),
 C("asked,","THEY ASKED\nTO LOOK",None),
 C("no.","TOLD\nNO",None,red=True,sfx=[["stamp",0.0]]),
 C("cancelled,","COMING UP:\nTHE CANCELLED REQUEST\nTHE UNSENT EMAIL\nTHE TEST",None),
 CH("launched",2,"Eighty-two seconds"),
 P("sixteenday","launch","STS-107 · 16 JAN 2003 · A 16-DAY MISSION",zoom=[1.0,1.15],sfx=[["rumble",0.0]]),
 P("Husband,","husband","CMDR. RICK HUSBAND",**FC),
 P("Ramon,","ramon","ILAN RAMON · FIRST ISRAELI ASTRONAUT",**FC),
 C("eightytwo","T+82 SECONDS",None,red=True),
 C("foam","INSULATING\nFOAM",None),
 C("bipod","FROM THE\n“BIPOD RAMP”",None),
 C("briefcase,","~BRIEFCASE SIZED\nUNDER 2 POUNDS",None),
 P("leading","launch","THE LEFT WING",focus=[0.62,0.55],zoom=[1.6,1.8],sfx=[["hit",0.0]]),
 C("five","500+ MPH",None,red=True),
 C("films.","FOUND THE NEXT DAY\nIN LAUNCH FILMS",None),
 P("carbon.","rcc","REINFORCED CARBON PANELS (TEST PIECES)",**FC),
 C("three","~3,000°F\nON REENTRY",None),
 C("broken,","IF ONE BROKE…",None,red=True),
 C("years.","FOAM STRIKES:\nFOR YEARS",None),
 C("months","OCTOBER 2002:\nFOAM LOST AGAIN",None),
 C("maintenance","“A MAINTENANCE\nPROBLEM”",None,red=True),
 CH("team",3,"Asking to look"),
 C("Rocha,","RODNEY ROCHA","NASA STRUCTURAL ENGINEER"),
 C("model","THE DAMAGE MODEL",
"BUILT FOR TINY DEBRIS"),
 C("hundreds","HUNDREDS OF TIMES\nLARGER",None,red=True),
 C("know","THEY DIDN'T\nKNOW",None),
 C("requests","3+ REQUESTS\nFOR IMAGES",None),
 P("military","orbit","COULD MILITARY TELESCOPES SEE THE WING?",zoom=[1.0,1.15]),
 C("22nd,","22 JANUARY",None),
 C("cancelled.","REQUEST\nCANCELLED","LINDA HAM · MISSION MANAGEMENT TEAM CHAIR",red=True,sfx=[["stamp",0.0]]),
 C("requirement","“NO REQUIREMENT”",None),
 C("backwards.","BACKWARDS",None),
 C("pictures.","NO PROOF\nWITHOUT PICTURES",None),
 C("email","ROCHA'S EMAIL",None,sfx=[["paper",0.0]]),
 C("irresponsible.","“THE WRONG (AND\nBORDERING ON\nIRRESPONSIBLE) ANSWER”","RODNEY ROCHA",red=True),
 C("never","NEVER\nSENT",None,red=True,sfx=[["stamp",0.0]]),
 CH("eight",4,"No concern"),
 P("Husband","cockpit","THE STS-107 CREW IN ORBIT",zoom=[1.0,1.1]),
 C("absolutely","“ABSOLUTELY NO\nCONCERN FOR ENTRY”","FLIGHT DIRECTOR EMAIL · 23 JAN"),
 C("worth","“NOT EVEN WORTH\nMENTIONING”",None,red=True),
 C("probably","“PROBABLY\nSURVIVE”",None),
 C("24th,","24 JANUARY","MISSION MANAGEMENT TEAM"),
 C("presented","A SHORT\nBRIEFING",None),
 C("accepted","ACCEPTED WITH\nLITTLE DISCUSSION",None),
 C("unchallenged.","ESSENTIALLY\nUNCHALLENGED",None,red=True),
 P("science","crew","AROUND THE CLOCK · 2+ WEEKS",zoom=[1.1,1.2]),
 C("idea","A HOLE IN\nTHEIR WING",None,red=True),
 CH("fired",5,"February 1st"),
 C("superheated","SUPERHEATED AIR\nINTO THE LEFT WING",None,red=True),
 C("sensor","STRANGE SENSOR\nREADINGS",None),
 C("offline,","SENSORS\nGO OFFLINE",None),
 C("tire","LEFT TIRE\nPRESSURES: LOST",None,sfx=[["radio",0.0]]),
 C("Cain,","LEROY CAIN","FLIGHT DIRECTOR"),
 C("lost.","“ROGER, UH—”\nSIGNAL LOST","CMDR. RICK HUSBAND · LAST WORDS",red=True,sfx=[["hit",0.0]]),
 C("Texas,","~9:00 AM ET","200,000 FT · MACH 18 · OVER TEXAS",sfx=[["boom",0.0]]),
 C("streaks","STREAKS OF LIGHT",None),
 P("Debris","hangar","THE RECONSTRUCTION TEAM · 80,000+ PIECES"),
 P("Rick","crew","HUSBAND · McCOOL · ANDERSON · CHAWLA · BROWN · CLARK · RAMON",zoom=[1.0,1.12]),
 CH("independent",6,"What the file tells us"),
 C("Investigation","COLUMBIA ACCIDENT\nINVESTIGATION BOARD",None),
 C("July","JULY 2003","THE FOAM TEST"),
 P("panel.","foamtest","THE TESTED PANEL",zoom=[1.0,1.15],sfx=[["hit",0.0]]),
 P("sixteen","foamtest","~16-INCH HOLE",focus=[0.45,0.4],zoom=[1.6,1.8]),
 C("gasped.","“GASPS”","REPORTEDLY"),
 P("Atlantis,","atlantis","ATLANTIS · A POSSIBLE RESCUE"),
 C("difficult","DIFFICULT.\nRISKY.\nPOSSIBLE.",None),
 C("culture","NASA'S CULTURE\n= AS LARGE A ROLE\nAS THE FOAM",None,red=True),
 C("Challenger","THE SAME PATTERN\nAS CHALLENGER",None),
 C("normal.","WARNING SIGNS\nBECAME NORMAL",None,red=True),
 P("2005,","return","RETURN TO FLIGHT · 2005"),
 C("retired.","2011:\nSHUTTLE RETIRED",None),
 C("noticed.","IT WASN'T\nTHAT NOBODY NOTICED",None),
 C("prove","ASKED TO PROVE IT\nWITHOUT LOOKING",None,red=True),
 C("sent","WOULD YOU HAVE\nSENT THAT EMAIL?","TELL ME IN THE COMMENTS"),
 {"at":"Dossier","type":"end"},
]
json.dump({"title":"COLUMBIA","case":"041","landscape":True,"scenes":S},open("scenes.json","w"),indent=1,ensure_ascii=False)
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
