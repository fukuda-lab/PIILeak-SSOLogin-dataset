import pandas as pd
from utils import unique

def GetListBelongsEcosysem():
    types = ["Google","Facebook"]
    ls_eco = []
    for t in types:
        df = pd.read_csv('input/Ghostery/3rd_'+t+'.csv',sep='|')
        df_exclue = df[(df['name of organization']=='Meta') | (df['name of organization']=='Google')]
        ls_eco = ls_eco + unique(df_exclue['input'].tolist())
    ls_eco = unique(ls_eco)
    return ls_eco

def GetData(type,eco):
    df = pd.read_csv('input/Adhoc/Japan/'+type+'.csv.gz',compression='gzip')
    df_fil = df[(df['thrd_domain']==eco)]
    if type=="Google":
        df_fil = df_fil[~df_fil['http_request'].str.contains("https://accounts.google.com|https://myaccount.google.com")]
    if type=="Facebook":
        if eco == "facebook.com":
            df_fil = df_fil[df_fil['http_request'].str.contains("https://www.facebook.com/tr")]
        
    return df_fil

list_eco = GetListBelongsEcosysem()
result = []
print("=== Breakdown the number of first-party that send PII to third-party domains belonging to Google and Meta. ===")
for e in list_eco:
    types = ["Google","Facebook"]
    number = []
    for t in types:
        data = GetData(t,e)
        number.append(len(unique(data['st_domain'].tolist())))
        data.to_csv("output/3rd_domains_ecosystem/"+t+"/"+e+".csv")
    result.append([e,number[0],number[1]])

df = pd.DataFrame(result,columns=["Third-party domain","Google","Facebook"])
print(df)
print("Detail data stored at /output/3rd_domains_ecosystem/")