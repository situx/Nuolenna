from rdflib import Graph, URIRef, Literal
import json


charreplacements={"š":"sz","Š":"SZ","Ṣ":"S,","ṣ":"s,","Ḫ":"H,","ḫ":"h,","ĝ":"g","ṭ":"t,","Ṭ":"T,","₂":"2","₃":"3","₄":"4","₅":"5","₆":"6","₇":"7","₈":"8","₉":"9","₁":"1","₀":"0"}

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

file1 = open('sign_list.txt', 'r',encoding="utf-8")
count = 0

jsonresult={}
jsoncatfresult={}
csvresult_ascii = open('sign_list_ascii.csv', 'w',encoding="utf-8")
csvresult = open('sign_list.csv', 'w',encoding="utf-8")
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
        csvresult.write(str(splitted[0].strip())+";"+str(splitted[1].strip())+"\n")
        csvresult_ascii.write(replacechars(str(splitted[0].strip()))+";"+replacechars(str(splitted[1].strip()))+"\n")
    # if line is empty
    # end of file is reached
    if not line:
        break
csvresult.close()
csvresult_ascii.close()
f=open("sign_list.json","w",encoding="utf-8")
f.write(json.dumps(jsonresult,indent=2))
f.close()
f=open("sign_list_ascii.json","w",encoding="utf-8")
f.write(json.dumps(jsoncatfresult,indent=2))
f.close()

g.serialize("sign_list.ttl")