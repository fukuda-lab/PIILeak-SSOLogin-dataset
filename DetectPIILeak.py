from hashlib import sha256
from hashlib import sha512
from hashlib import sha1
from hashlib import md5
import base64
import pandas as pd
import sqlite3
import ast
import urllib.parse
import csv
import tldextract
from adblockparser import AdblockRules

f1 = open("easyprivacylist.txt","r",encoding="utf8")
f2 = open("easylist.txt","r",encoding="utf8")

easyprivacyrule = f1.readlines()
easylistrule = f2.readlines()

easyprivacy = AdblockRules(easyprivacyrule,use_re2=False)
easylist = AdblockRules(easylistrule,use_re2=False)

PII_Entities = {
    "Facebook": {
        "EMAIL":["hattori.mina@proton.me","hattori.mina%40proton.me"],
        "USER_NAME":["Minamoto Hattori","Minamoto%20Hattori","MinamotoHattori","MINAMOTO HATTORI","MINAMOTO%20HATTORI","MINAMOTOHATTORI","minamoto hattori","minamoto%20hattori","minamotohattori","Hattori Minamoto","Hattori%20Minamoto","HattoriMinamoto","HATTORI MINAMOTO","HATTORI%20MINAMOTO","HATTORIMINAMOTO","hattori minamoto","hattori%20minamoto","hattoriminamoto"],
        "USER_ID":["100093318801827"]
    },
    "Google": {
        "EMAIL":["phikhanh340@gmail.com","phikhanh340%40gmail.com"],
        "USER_NAME":["Khanh Phi","Khanh%20Phi","KhanhPhi","KHANH PHI","KHANH%20PHI","KHANHPHI","khanh phi","khanh%20phi","khanhphi","Phi Khanh","Phi%20Khanh","PhiKhanh","PHI KHANH","PHI%KHANH","PHIKHANH","phi khanh","phi%20khanh","phikhanh"],
        "USER_ID":["107385361539956577079"]
    }
}

TYPE_OF_ENCODE = ["PLAINTEXT","BASE64","MD5","SHA1","SHA256"]
TYPE_OF_METHOD = ["URI","PAYLOAD","REFERER","COOKIES"]
TYPE_OF_PII = ["EMAIL","USER_NAME","USER_ID"]
site = []

def Encode(type,input):
    if type == "URL-Encode":
        output = urllib.parse.quote(input)

    if type == "UTF-8":
        output = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in input)
        output = output.lower()
    if type == "ASCII":
        x = input.encode(encoding="ascii")
        output = ""
        for c in x:
            output = output + "&#" + str(c) +";" 
    if type == "SHA256":
        output = sha256(input.encode('utf-8')).hexdigest()
    if type == "SHA512":
        output = sha512(input.encode('utf-8')).hexdigest()
    if type == "SHA1":
        output = sha1(input.encode('utf-8')).hexdigest()
    if type == "MD5":
        output = md5(input.encode('utf-8')).hexdigest()
    if type == "BASE64":
        inp_bytes = input.encode("ascii")
        base64_bytes = base64.b64encode(inp_bytes)
        output = base64_bytes.decode("ascii")
    if type == "SHA256_MD5":
        str_md5= md5(input.encode('utf-8')).hexdigest()
        output = sha256(str_md5.encode('utf-8')).hexdigest()
    if type == "PLAINTEXT":
        output = input
    return output

def GetQuery(str_hash,type_of_method,list_site=None):
    i = 0
    for str in str_hash:
        if type_of_method == "URI":
            if i == 0:
                query = "SELECT REQUESTS.id_site,REQUESTS.id_request,REQUESTS.http_request,REQUESTS.method,REQUESTS.easylist,REQUESTS.privacylist,REQUESTS.postData,SUMMARY.site,REQUESTS.initiator_url,REQUESTS.initiator_type,REQUESTS.initiator_function,REQUESTS.is_st_party,REQUESTS.headers, REQUESTS_EXTRA.headers AS extra_headers FROM (REQUESTS JOIN SUMMARY ON REQUESTS.id_site = SUMMARY.id_site) JOIN REQUESTS_EXTRA ON REQUESTS.id_request = REQUESTS_EXTRA.id_request WHERE (REQUESTS.is_st_party = 'False') AND (LOWER(REQUESTS.http_request) LIKE LOWER('%"+str+"%')"
            else:
                query = query + " OR LOWER(REQUESTS.http_request) LIKE LOWER('%"+str+"%')"
    
        if type_of_method == "PAYLOAD":
            if i == 0:
                query = "SELECT REQUESTS.id_site,REQUESTS.id_request,REQUESTS.http_request,REQUESTS.method,REQUESTS.easylist,REQUESTS.privacylist,REQUESTS.postData,SUMMARY.site,REQUESTS.initiator_url,REQUESTS.initiator_type,REQUESTS.initiator_function,REQUESTS.is_st_party,REQUESTS.headers, REQUESTS_EXTRA.headers AS extra_headers FROM (REQUESTS JOIN SUMMARY ON REQUESTS.id_site = SUMMARY.id_site) JOIN REQUESTS_EXTRA ON REQUESTS.id_request = REQUESTS_EXTRA.id_request WHERE (REQUESTS.is_st_party = 'False') AND (LOWER(REQUESTS.postData) LIKE LOWER('%"+str+"%')"
            else:
                query = query + " OR LOWER(REQUESTS.postData) LIKE LOWER('%"+str+"%')"
        
        if type_of_method == "REFERER" or type_of_method == "AUTHORIZATION" or type_of_method == "COOKIES":
            if i == 0:
                query = "SELECT REQUESTS.id_site,REQUESTS.id_request,REQUESTS.http_request,REQUESTS.method,REQUESTS.easylist,REQUESTS.privacylist,REQUESTS.postData,SUMMARY.site,REQUESTS.initiator_url,REQUESTS.initiator_type,REQUESTS.initiator_function,REQUESTS.is_st_party,REQUESTS.headers, REQUESTS_EXTRA.headers AS extra_headers FROM (REQUESTS JOIN SUMMARY ON REQUESTS.id_site = SUMMARY.id_site) JOIN REQUESTS_EXTRA ON REQUESTS.id_request = REQUESTS_EXTRA.id_request WHERE (REQUESTS.is_st_party = 'False') AND (LOWER(REQUESTS_EXTRA.headers) LIKE LOWER('%"+str+"%')" + " OR LOWER(REQUESTS.headers) LIKE LOWER('%"+str+"%')"
            else:
                query = query + " OR LOWER(REQUESTS_EXTRA.headers) LIKE LOWER('%"+str+"%')" + " OR LOWER(REQUESTS.headers) LIKE LOWER('%"+str+"%')"
        i = i +1

    if list_site is not None:
        query = query + " AND REQUESTS.id_site in "+list_site
    query = query+")"
    return query

def QueryData(DATABASE,LEAKAGE_METHOD,ENCODING_FORM,PII_TYPE,PII_ENT):
    global site
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    data = []
    str_hash = []
    for plaintext in PII_ENT[PII_TYPE]:
        str_hash.append(Encode(type=ENCODING_FORM,input=plaintext))
    
    query = GetQuery(str_hash=str_hash,type_of_method=LEAKAGE_METHOD)
    data_raw = pd.read_sql_query(query,db)
    data_raw["encoding_form"] = ENCODING_FORM
    data_raw["leakage_method"] = LEAKAGE_METHOD
    data_raw["pii_type"] = PII_TYPE
    data_raw["st_domain"] = ""
    data_raw["thrd_domain"] = ""    
    data_raw["referer"] = ""
    data_raw["authorization"] = ""
    data_raw["cookies"] = ""
    data_raw["referer_extra"] = ""
    data_raw["cookies_extra"] = ""
        

    for index, row in data_raw.iterrows():
        if row["easylist"] is None:
            if row['is_st_party'] == "False":
                try:
                    res_easy = str(easylist.should_block(row['http_request'],{'third-party': True}))
                except Exception as e:
                    #print(e)
                    res_easy = "False"
        
                try:
                    res_privacy = str(easyprivacy.should_block(row['http_request'],{'third-party': True}))
                except Exception as e:
                    #print(e)
                    data_raw.at[index,'privacylist']="False"

                data_raw.at[index,'easylist'] = res_easy
                data_raw.at[index,'privacylist'] = res_privacy
                quer = "UPDATE REQUESTS SET easylist='"+res_easy+"',privacylist='"+res_privacy+"' WHERE id_site = "+str(row["id_site"])+" AND id_request = '"+str(row["id_request"])+"' AND http_request = '"+row["http_request"]+"'"
                print(quer)
                cursor.execute(quer)
                db.commit()
            else:
                data_raw.at[index,'easylist'] = "False"
                data_raw.at[index,'privacylist'] = "False"
                res_privacy = "False"
                res_easy = "False"
                quer = "UPDATE REQUESTS SET easylist='"+res_easy+"',privacylist='"+res_privacy+"' WHERE id_site = "+str(row["id_site"])+" AND id_request = '"+str(row["id_request"])+"' AND http_request = '"+row["http_request"]+"'"
                print(quer)
                cursor.execute(quer)
                db.commit()
        
        site.append(row["site"])
        st_domain = tldextract.extract(row["site"]).registered_domain
        data_raw.at[index,'st_domain'] = st_domain
        if row["is_st_party"] == "False":
            thrd_domain = tldextract.extract(row["http_request"]).registered_domain
            data_raw.at[index,'thrd_domain'] = thrd_domain
            
        try:
            referer = ast.literal_eval(row["headers"])['Referer']
        except:
            try:
                referer = ast.literal_eval(row["headers"])['referer']
            except:
                referer = ""
            
        try:
            cookies = str(ast.literal_eval(row["headers"])['Cookie']).replace('"',"'")
        except:
            try:
                cookies = str(ast.literal_eval(row["headers"])['cookie']).replace('"',"'")
            except:
                cookies = ""
            
        try:
            authorization = str(ast.literal_eval(row["headers"])['Authorization']).replace('"',"'")
        except:
            try:
                authorization = str(ast.literal_eval(row["headers"])['authorization']).replace('"',"'")
            except:
                authorization = ""
            
        try:
            referer_extra = ast.literal_eval(row["extra_headers"])['Referer']
        except:
            try:
                referer_extra = ast.literal_eval(row["extra_headers"])['referer']
            except:
                referer_extra = ""
            
        try:
            cookies_extra = str(ast.literal_eval(row["extra_headers"])['Cookie']).replace('"',"'")
        except:
            try:
                cookies_extra = str(ast.literal_eval(row["extra_headers"])['cookie']).replace('"',"'")
            except:
                cookies_extra = ""

        data_raw.at[index,'referer'] = referer
        data_raw.at[index,'cookies'] = cookies
        data_raw.at[index,'authorization'] = authorization
        data_raw.at[index,'referer_extra'] = referer_extra
        data_raw.at[index,'cookies_extra'] = cookies_extra
        
    if LEAKAGE_METHOD == "REFERER":
        for enc in str_hash:
            data_raw2 = data_raw[data_raw["referer"].str.contains(enc) | data_raw["referer_extra"].str.contains(enc)]
            data.append(data_raw2)
    if LEAKAGE_METHOD == "COOKIES":
        for enc in str_hash:
            data_raw2 = data_raw[data_raw["cookies"].str.contains(enc) | data_raw["cookies_extra"].str.contains(enc)]
            data.append(data_raw2)
    if LEAKAGE_METHOD == "AUTHORIZATION":
        for enc in str_hash:
            data_raw2 = data_raw[data_raw["authorization"].str.contains(enc)]
            data.append(data_raw2)
    
    if len(data)>0:
        data_exp = pd.concat(data,ignore_index=True)
        return data_exp
    else:
        return data_raw

def Export_Data(DATABASE,TYPE):
    global site
    data = []
    for method in TYPE_OF_METHOD:
        print(method)
        for encode in TYPE_OF_ENCODE:
            for pii in TYPE_OF_PII:
                res = QueryData(DATABASE=DATABASE,LEAKAGE_METHOD=method,ENCODING_FORM=encode,PII_TYPE=pii,PII_ENT=PII_Entities[TYPE])
                data.append(res)

    data_exp = pd.concat(data,ignore_index=True)
    data_exp.drop(['site', 'headers','extra_headers'], axis=1, inplace=True)
    return data_exp

types = ["Google"]
for t in types:
    input = "Japan_"+t+".sqlite"
    output = "Adhoc_JP_"+t+".csv.gz"

    data_final = Export_Data(input,t)
    data_final.to_csv(output,compression='gzip',encoding='utf-8',index_label='no',quoting=csv.QUOTE_ALL)