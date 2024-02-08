from rdflib import Graph, URIRef, Literal
import json
import csv
import re
import string


charreplacements={"š":"sz","Š":"SZ","Ṣ":"S,","ṣ":"s,","Ḫ":"H,","ḫ":"h,","ĝ":"g","ṭ":"t,","Ṭ":"T,","₂":"2","₃":"3","₄":"4","₅":"5","₆":"6","₇":"7","₈":"8","₉":"9","₁":"1","₀":"0"}

rdfset=set()

def replacechars(repstr):
    for key in charreplacements:
        repstr=repstr.replace(key,charreplacements[key])
    return repstr

def cleanString(strr):
    retstr=toASCII(strr)
    retstr=retstr.lower().replace("sh","sz").replace("š","sz").replace("Š","SZ").replace("[","_").replace("]","_").replace("%","_").replace("{","_").replace("}","_").replace(" ","_").replace("\"","").replace(",","_").replace("|","_").replace("/","_").replace("-","_").replace("+","_").replace("%","_").replace("(","_").replace(")","_").replace(".","_").replace(":","_").replace("₄","4").replace("₂","2").replace("₃","3").replace("₅","5").replace("₆","6").replace("₇","7").replace("₈","8").replace("₉","9").replace("₁","1").replace("₀","0")
    if retstr.endswith("_"):
        retstr=retstr[:-1]
    if retstr.startswith("_"):
        retstr=retstr[1:]
    return retstr


def toASCII(word):
    ascii_replacements = {
        'Á' : 'A2','À' : 'A3',
        'á' : 'a2','à' : 'a3',
        'É' : 'E2','È' : 'E3',
        'é' : 'e2','è' : 'e3',
        'Í' : 'I2','Ì' : 'I3',
        'í' : 'i2','ì' : 'i3',
        'Ú' : 'U2','Ù' : 'U3',
        'ú' : 'u2','ù' : 'u3',
        'Ṭ' : 'T,', 'j' : 'i',
        'ĝ' : 'g', 'ṭ' : 't,',
        'ḫ' : 'h', 'Ḫ' : 'H',
        'š' : 'sz', 'Š' : 'SZ',
        'ṣ' : 's,', 'Ṣ' : 'S,',
        '₀' : '0', '₁' : '1',
        '₂' : '2', '₃' : '3',
        '₄' : '4', '₅' : '5',
        '₆' : '6', '₇' : '7',
        '₈' : '8', '₉' : '9'}
    for rep, initial in ascii_replacements.items():
        word = word.replace(rep.lower(), initial)
    #print(word)
    return word

def analyzeSignName(signname,signuri,rdfset):
    res=[]
    spl=re.split('times|\.|over|×|x|/|plus|, |_|-|!', signname.lower())
    for sl in spl:
        signparturi=("https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(sl)).replace("__","_")
        rdfset.add("<"+str(signuri)+"> graphemon:hasPart <"+str(signparturi)+"> .\n")

def convertToRDF(cuneiformsigndict,nuolenna,aasigndict,rdfset,unicodetowikidata):
    unicodeToURI={}
    signnameToURI={}
    tocheckforUnicode={}
    sensescounter=0
    charsensecounter=0
    rdfset.add("<https://situx.github.io/cuneiformontology/signlist/signlist_cuneiform> rdf:type graphemon:GraphemeList .\n ")
    rdfset.add("<https://situx.github.io/cuneiformontology/signlist/signlist_cuneiform> rdfs:label \"Cuneiform Sign List\" .\n ")
    for entry in cuneiformsigndict:
        print(entry)
        if "(" in entry["signname"] and ")" in entry["signname"]:
            signuri=("https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(entry["signname"][0:entry["signname"].find("(")])).replace("__","_")
        else:
            signuri=("https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(entry["signname"])).replace("__","_")
        signnameToURI[toASCII(str(entry["signname"])).replace("\"","")]=str(signuri)
        rdfset.add("<https://situx.github.io/cuneiformontology/signlist/signlist_cuneiform> rdfs:member <"+str(signuri)+"> .\n ")
        if "unicodename" in entry and len(entry["unicodename"])>1:
            rdfset.add("<"+str(signuri)+"> rdf:type graphemon:GraphemeComposition .\n ")
            rdfset.add("<"+str(signuri)+"> rdfs:label \"Character Composition: "+toASCII(str(entry["signname"])).replace("\"","")+"\" .\n ")
        else:
            rdfset.add("<"+str(signuri)+"> rdf:type graphemon:Grapheme .\n ")
            rdfset.add("<"+str(signuri)+"> rdfs:label \"Character: "+toASCII(str(entry["signname"])).replace("\"","")+"\" .\n ")
            if entry["unicodename"] in unicodetowikidata:
                rdfset.add("<"+str(signuri)+"> owl:sameAs <"+str(unicodetowikidata[entry["unicodename"]])+"> .\n ")
                rdfset.add("<"+str(unicodetowikidata[entry["unicodename"]])+"> rdfs:label \"Wikidata: "+str(entry["unicodename"])+" ("+str(entry["unicode"]).replace("\"","")+")\" .\n ")
            tocheckforUnicode[str(signuri)]=str(entry["unicodename"]).replace("\"","")
        if entry["meszl"]!="":
            rdfset.add("<"+str(signuri)+"> graphemon:meszl \""+str(entry["meszl"]).replace("\"","")+"\" .\n ")
        if entry["slha"]!="":
            rdfset.add("<"+str(signuri)+"> graphemon:slha \""+str(entry["slha"]).replace("\"","")+"\" .\n")
        if entry["hethzl"]!="":
            rdfset.add("<"+str(signuri)+"> graphemon:hethzl \""+str(entry["hethzl"]).replace("\"","")+"\" .\n ")
        if entry["abzl"]!="":
            rdfset.add("<"+str(signuri)+"> graphemon:abzl \""+str(entry["abzl"]).replace("\"","")+"\" .\n ")
        rdfset.add("<"+str(signuri)+"> graphemon:signName \""+str(entry["signname"]).replace("\"","")+"\" .\n ")
        analyzeSignName(str(entry["signname"]).replace("\"",""),str(signuri),rdfset)
        rdfset.add("<"+str(signuri)+"> graphemon:unicodeCodepoint \""+str(entry["unicode"]).replace("\"","")+"\" .\n ")
        rdfset.add("<"+str(signuri)+"> graphemon:unicodeRepresentation \""+str(entry["unicodename"]).replace("\"","")+"\" .\n ")
        if "unicodename" in entry and len(entry["unicodename"])>1:
            unicodeToURI[entry["unicodename"]]={"@id":str(signuri),"signname":toASCII(str(entry["signname"])).replace("\"",""),"@type":"Grapheme"}
        else:
            unicodeToURI[entry["unicodename"]]={"@id":str(signuri),"signname":toASCII(str(entry["signname"])).replace("\"",""),"@type":"GrapemeComposition"}
    #print(unicodeToURI)
    nuolennamatchcounter=0
    for item in nuolenna:
        if nuolenna[item] in unicodeToURI:
            cururi=unicodeToURI[nuolenna[item]]["@id"]
            cursignname=unicodeToURI[nuolenna[item]]["signname"]
            readinguri=(str(cururi)+"_reading_"+cleanString(str(item))).replace("__","_").replace("__","_")
            if readinguri[-1]=="_":
                readinguri=readinguri[0:-1]
            rdfset.add("<"+str(cururi)+"> graphemon:hasGraphemeReading <"+readinguri+"> .\n ")
            rdfset.add("<"+readinguri+"> rdf:type graphemon:GraphemeReading .\n ")
            rdfset.add("<"+readinguri+"> rdfs:label \"Grapheme Reading "+str(cursignname)+": "+toASCII(str(item)).replace("\"","")+"\" .\n ")
            rdfset.add("<"+readinguri+"> graphemon:readingValue \""+toASCII(str(item)).replace("\"","")+"\" .\n ")
            nuolennamatchcounter+=1
        else:
            if len(nuolenna[item])>1:
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"> rdf:type graphemon:GraphemeComposition .\n ")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"> rdfs:label \"Character Composition: "+toASCII(str(item)).replace("\"","")+"\" .\n ")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"> graphemon:hasGraphemeReading <https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_reading_"+cleanString(str(item))+"> .\n ")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_reading_"+cleanString(str(item))+"> rdf:type graphemon:GraphemeReading .\n ")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_reading_"+cleanString(str(item))+"> graphemon:readingValue \""+toASCII(str(item)).replace("\"","")+"\" .\n ")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_reading_"+cleanString(str(item))+"> rdfs:label \"Grapheme Reading "+toASCII(str(item)).replace("\"","")+": "+toASCII(str(item)).replace("\"","")+"\" .\n ")
                tocheckforUnicode[str("https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item)))]=nuolenna[item]
                for chara in nuolenna[item]:
                    if chara in unicodeToURI and "uri" in unicodeToURI[chara]:
                        rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"> graphemon:isComposedOf <"+str(unicodeToURI[chara]["@id"])+"> .\n ")
                        rdfset.add("<"+str(unicodeToURI[chara]["@id"])+"> graphemon:partOf <https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"> .\n ")  
            else:
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"> rdf:type graphemon:Grapheme .\n ")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"> rdfs:label \"Character: "+toASCII(str(item)).replace("\"","")+"\" .\n ")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"> graphemon:hasGraphemeReading <https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_reading_"+cleanString(str(item))+"> .\n ")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_reading_"+cleanString(str(item))+"> rdf:type graphemon:GraphemeReading .\n ")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_reading_"+cleanString(str(item))+"> graphemon:readingValue \""+toASCII(str(item)).replace("\"","")+"\" .\n ")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_reading_"+cleanString(str(item))+"> rdfs:label \"Grapheme Reading "+toASCII(str(item)).replace("\"","")+": "+toASCII(str(item)).replace("\"","")+"\" .\n ")
            rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"> graphemon:unicodeRepresentation \""+str(nuolenna[item]).replace("\"","")+"\" .\n ")     
            if toASCII(str(item)).replace("\"","").isdigit() and toASCII(str(item)).replace("\"","") in sensesmap:
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"> lemon:sense <https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_sense_"+str(toASCII(str(item)).replace("\"",""))+"> .\n")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_sense_"+str(toASCII(str(item)).replace("\"",""))+"> rdf:type graphemon:GraphemeSense .\n")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_sense_"+str(toASCII(str(item)).replace("\"",""))+"> rdfs:label \"Grapheme Sense "+str(toASCII(str(item)).replace("\"",""))+": "+str(toASCII(str(item)).replace("\"",""))+"\" .\n")
                rdfset.add("<https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"_sense_"+str(toASCII(str(item)).replace("\"",""))+"> lemon:reference <"+sensesmap[toASCII(str(item)).replace("\"","")]+"> .\n")
                rdfset.add("<"+sensesmap[toASCII(str(item)).replace("\"","")]+"> rdfs:label \"Wikidata: "+str(toASCII(str(item)).replace("\"",""))+"\" .\n")
            if len(nuolenna[item])>1:
                unicodeToURI[item]={"@id":"https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item)),"signname":toASCII(str(item)).replace("\"",""),"@type":"GraphemeComposition"}
            else:
                unicodeToURI[item]={"@id":"https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item)),"signname":toASCII(str(item)).replace("\"",""),"@type":"Grapheme"}
    for uri in tocheckforUnicode:
        for chara in tocheckforUnicode[uri]:
            if len(chara)>1 and chara in unicodeToURI and "@id" in unicodeToURI[chara]:
                rdfset.add("<"+str(uri)+"> graphemon:isComposedOf <"+str(unicodeToURI[chara]["@id"])+"> .\n ")
                rdfset.add("<"+str(unicodeToURI[chara]["@id"])+"> graphemon:partOf <https://situx.github.io/cuneiformontology/signlist/character_"+cleanString(str(item))+"> .\n ")  
    print("Matched "+str(nuolennamatchcounter)+" items in nuolenna!")
    aalistmatchcounter=0
    for entry in aasigndict:
        sname=str(entry["unicodename"]).strip()
        #print(sname)
        if sname in unicodeToURI:
            cururi=unicodeToURI[sname]["@id"]
            if entry["labat"]!="":
                rdfset.add("<"+str(cururi)+"> graphemon:labat \""+str(entry["labat"])+"\" .\n ")
            if entry["obo"]!="":
                rdfset.add("<"+str(cururi)+"> graphemon:obo \""+str(entry["obo"])+"\" .\n ")
            if entry["lak"]!="":
                rdfset.add("<"+str(cururi)+"> graphemon:lak \""+str(entry["lak"])+"\" .\n ")
            if "meaning" in entry and entry["meaning"]!="":
                meanings=entry["meaning"].replace("v.","").replace("n.","")
                if ";" in entry["meaning"]:
                    meanings=entry["meaning"].split(";")
                else:
                    meanings=[entry["meaning"]]
                for mean in meanings:
                    if mean.strip()!="n." and mean.strip()!="v." and mean.strip()!="adj.":
                        rdfset.add("<"+str(cururi)+"> lemon:sense <"+str(cururi)+"_sense_"+cleanString(str(mean)).replace("n.","").replace("v.","").replace("adj.","")+"> .\n ")
                        rdfset.add("<"+str(cururi)+"_sense_"+cleanString(str(mean))+"> rdfs:label \"Grapheme Sense "+str(entry["unicode"])+": "+str(mean).replace("\"","").strip().replace("n.","").replace("v.","").replace("adj.","")+"\" .\n ")
                        rdfset.add("<"+str(cururi)+"_sense_"+cleanString(str(mean)).replace("n.","").replace("v.","").replace("adj.","")+"> rdf:type graphemon:GraphemeSense .\n ")
                        #print(str(mean).replace("\"","").strip())
                        if str(mean).replace("\"","").strip() in sensesmap:
                            sensescounter+=1
                            rdfset.add("<"+str(cururi)+"_sense_"+cleanString(str(mean)).replace("n.","").replace("v.","").replace("adj.","")+"> lemon:reference <"+str(sensesmap[str(mean).replace("\"","").strip()])+"> .\n ")
                            rdfset.add("<"+str(sensesmap[str(mean).replace("\"","").strip()])+"> rdfs:label \"Wikidata: "+str(mean).replace("\"","").strip()+"\" .\n ")
            terms=[{"term":"oldbab","label":"Old Babylonian","uri":"http://www.wikidata.org/entity/Q733897"},{"term":"lagasz2","label":"Lagasz2","uri":""},{"term":"edIII","label":"EdIII","uri":"http://www.wikidata.org/entity/Q110209565"},{"term":"oldass","label":"Old Assyrian","uri":"http://www.wikidata.org/entity/Q22948607"},{"term":"middleass","label":"Middle Assyrian","uri":""},{"term":"middlebab","label":"Middle Babylonian","uri":"http://www.wikidata.org/entity/Q16530848"}]
            for term in terms:
                #print(term["term"])
                if term["term"] in entry and entry[term["term"]]!="":
                    readings=entry[term["term"]]
                    if ";" in entry[term["term"]]:
                        readings=entry[term["term"]].split(";")
                    else:
                        readings=[entry[term["term"]]]
                    #print(readings)
                    for reading in readings:
                        if reading.replace("__","_").replace("__","_").replace(",","").strip()=="":
                            continue
                        readinguri=(str(cururi)+"_reading_"+cleanString(reading)).replace("__","_").replace("__","_").replace(" ","")
                        if readinguri.endswith("_"):
                            readinguri=readinguri[:-1]
                        pattern=re.compile("^.*_[0-9]+$")
                        if pattern.search(readinguri)!=None:
                            readinguri=readinguri.rstrip(string.digits)
                        if readinguri.endswith("_"):
                            readinguri=readinguri[:-1]
                        if reading.replace("__","_").replace("__","_").replace(",","").strip()=="":
                            continue
                        #print(reading)
                        #print(readinguri)
                        if "uri" in term:
                            rdfset.add("<"+readinguri+"> graphemon:epoch <"+str(term["uri"])+"> .\n ")
                            rdfset.add("<"+readinguri+"> rdf:type graphemon:GraphemeReading .\n ")
                            if "(" in reading:
                                rdfset.add("<"+readinguri+"> rdfs:label \"Grapheme Reading "+str(unicodeToURI[sname]["signname"])+": "+toASCII(str(reading)[0:reading.index("(")]).strip()+"\" .\n ")
                            else:
                                rdfset.add("<"+readinguri+"> rdfs:label \"Grapheme Reading "+str(unicodeToURI[sname]["signname"])+": "+toASCII(str(reading)).strip()+"\" .\n ")
                            rdfset.add("<"+readinguri[0:readinguri.index("_reading_")].replace("__","_")+"> graphemon:hasGraphemeReading <"+readinguri+"> .\n ")
                            rdfset.add("<"+str(term["uri"])+"> rdf:type cunei:Epoch .\n ")
                            if "label" in term and term["label"]!="":
                                rdfset.add("<"+str(term["uri"])+"> rdfs:label \"Wikidata: "+str(term["label"])+"\" .\n ")
                            else:
                                rdfset.add("<"+str(term["uri"])+"> rdfs:label \"Wikidata: "+str(term["term"])+"\" .\n ")
                        else:
                            rdfset.add("<"+readinguri+"> graphemon:epochId \""+str(term["term"])+"\" .\n ")
            aalistmatchcounter+=1
    with open('signmapping.json', mode='w', encoding="utf-8") as f:
        json.dump(unicodeToURI,f,indent=2)
    print("Matched "+str(aalistmatchcounter)+" items in aalist")
    print("Matched "+str(sensescounter)+" senses")

file1 = open('sign_list.txt', 'r',encoding="utf-8")
count = 0

jsonresult={}
jsoncatfresult={}
jsresult=[]
csvresult_ascii = open('sign_list_ascii.csv', 'w',encoding="utf-8")
csvresult = open('sign_list.csv', 'w',encoding="utf-8")
txtresult=open("sign_list_ascii.txt","w",encoding="utf-8")
csvresult.write("Reading;Unicode\n")
g=Graph()
g.add((URIRef("https://situx.github.io/nuolenna/sign_list"),URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),URIRef("http://purl.org/graphemon/GraphemeList")))
g.add((URIRef("https://situx.github.io/nuolenna/sign_list"),URIRef("http://www.w3.org/2000/01/rdf-schema#label"),Literal("Nuolenna Sign List",lang="en")))
while True:
    count += 1
    # Get next line from file
    line = file1.readline()
    if line.strip()!="":
        splitted=line.split("\t")
        jsonresult[splitted[0].strip()]=splitted[1].strip()
        jsoncatfresult[replacechars(splitted[0].strip())]=replacechars(splitted[1].strip())
        jsresult.append([splitted[0].strip(),splitted[1].strip()])
        csvresult.write(str(splitted[0].strip())+";"+str(splitted[1].strip())+"\n")
        csvresult_ascii.write(replacechars(str(splitted[0].strip()))+";"+replacechars(str(splitted[1].strip()))+"\n")
        txtresult.write(replacechars(str(splitted[0].strip()))+"\t"+replacechars(str(splitted[0].strip()))+"\n")
    # if line is empty
    # end of file is reached
    if not line:
        break
csvresult.close()
csvresult_ascii.close()
txtresult.close()
f=open("sign_list.json","w",encoding="utf-8")
f.write(json.dumps(jsonresult,indent=2))
f.close()
f=open("sign_list.js","w",encoding="utf-8")
f.write("var nuolenna="+json.dumps(jsresult,indent=2))
f.close()
f=open("sign_list_ascii.json","w",encoding="utf-8")
f.write(json.dumps(jsoncatfresult,indent=2))
f.close()


with open('sign_list.json', encoding="utf-8") as f:
   nuolenna = json.load(f)
   
with open('conf/oraccsenses.json', encoding="utf-8") as f:
   sensesmap = json.load(f)
   
with open('conf/unicodeToWikidata.json', encoding="utf-8") as f:
   unicodetowikidata = json.load(f)

print(nuolenna)

cuneiformsigndict = []

with open('conf/listofcuneiformsigns_wikipedia.csv', mode='r', encoding="utf-8") as inp:
    reader = csv.reader(inp)
    counter=0
    for rows in reader:
        try:
            cuneiformsigndict.append({"meszl":rows[0],"slha":rows[1],"abzl":rows[2],"hethzl":rows[3],"signname":rows[5],"unicode":rows[6],"unicodename":rows[7]})
        except:
            print("error")

print(cuneiformsigndict)

#CTRL,Bauer et al (pg.),Schneider; Ur III,Rosengarten,LAK,REC,OBO,Labat,Borger (MesZL),unicode,OB Signs,Sign var. (?),OGSL,SIGN NAME,ED III Sumerian (Oracc),ED III Sumerian (Oracc)_att,Lagaš II Sumerian (Oracc),Lagaš II Sumerian (Oracc)_att,Ur III,OB Sumerian,Basic Meaning,Other,Akkadian word equivalent,Uruk,Pre-Sargonic,Ebla,Ebla Meaning,OAkk,OB,OA,OA Meaning,Amarna,MA (Oracc),MA (Oracc)_att,MB (Oracc),MB (Oracc)_att,Nuzi,NA,NA (Oracc),NA (Oracc)_att,NB (Oracc),NB (Oracc)_att,LB (Oracc),LB (Oracc)_att
aasigndict = []

with open('conf/aa_signlist.csv', mode='r', encoding="utf-8") as inp:
    reader = csv.reader(inp)
    counter=0
    for rows in reader:
        aasigndict.append({"meszl":rows[8],"labat":rows[7],"obo":rows[6],"rec":rows[5],"lak":rows[4],"unicode":rows[13],"unicodename":rows[11],"edIII":rows[14]+";"+rows[15],"lagasz2":rows[16]+";"+rows[17],"oldbab":rows[19]+","+rows[28],"meaning":rows[20],"akkword":rows[22],"oldass":rows[29],"middleass":rows[32]+","+rows[33],"middlebab":rows[34]+","+rows[35]})

print(aasigndict)

convertToRDF(cuneiformsigndict,nuolenna,aasigndict,rdfset,unicodetowikidata)

with open('signlist.ttl', mode='w', encoding="utf-8") as f:
    f.write("@prefix graphemon: <http://purl.org/graphemon/> .\n ")
    f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n ")
    f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n ")
    f.write("@prefix lemon: <http://lemon-model.net/lemon#> .\n ")
    f.write("@prefix cuneisignlist: <https://situx.github.io/cuneiformontology/signlist/> .\n ")
    f.write("@prefix cunei: <http://purl.org/cuneiform/> .\n ")
    f.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n ")
    f.write("graphemon:SignlistOntology rdf:type owl:Ontology .\n ")
    f.write("graphemon:GraphemeReading rdf:type owl:Class .\n ")
    f.write("graphemon:GraphemeList rdf:type owl:Class .\n ")
    f.write("graphemon:Grapheme rdf:type owl:Class .\n ")
    f.write("cunei:Epoch rdf:type owl:Class .\n ")
    f.write("rdfs:member rdfs:label \"member\" .\n ")
    f.write("rdfs:label rdfs:label \"label\" .\n ")
    f.write("graphemon:GraphemeComposition rdf:type owl:Class .\n ")
    f.write("graphemon:hasGraphemeReading rdf:type owl:ObjectProperty .\n ")
    f.write("graphemon:isComposedOf rdf:type owl:ObjectProperty .\n ")
    f.write("graphemon:partOf rdf:type owl:ObjectProperty .\n ")
    f.write("graphemon:hethzl rdf:type owl:DatatypeProperty .\n ")
    f.write("lemon:writtenRep rdf:type owl:DatatypeProperty .\n ")
    f.write("lemon:sense rdf:type owl:ObjectProperty .\n ")    
    f.write("lemon:reference rdf:type owl:ObjectProperty .\n ")
    f.write("graphemon:abzl rdf:type owl:DatatypeProperty .\n ")
    f.write("graphemon:epoch rdf:type owl:ObjectProperty .\n ")
    f.write("graphemon:lak rdf:type owl:DatatypeProperty .\n ")
    f.write("graphemon:obo rdf:type owl:DatatypeProperty .\n ")
    f.write("graphemon:labat rdf:type owl:DatatypeProperty .\n ")
    f.write("graphemon:readingValue rdf:type owl:DatatypeProperty .\n ")
    f.write("graphemon:meszl rdf:type owl:DatatypeProperty .\n ")
    f.write("graphemon:slha rdf:type owl:DatatypeProperty .\n ")
    f.write("graphemon:unicodeCodepoint rdf:type owl:DatatypeProperty .\n ")
    f.write("graphemon:unicodeRepresentation rdf:type owl:DatatypeProperty .\n ")
    for item in sorted(list(dict.fromkeys(rdfset))):
        f.write(item)

g = Graph()
g.parse("signlist.ttl")
g.serialize(destination="signlist.ttl")


g.serialize("signlist.ttl")