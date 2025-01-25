import pandas as pd
from utils import unique

data_fb = pd.read_csv('input/Japan/Facebook_PIILeak_ThirdParty.csv')
data_gg = pd.read_csv('input/Japan/Google_PIILeak_ThirdParty.csv')

def Result(type,type_value,df_gg,df_fb):        
    sender_gg_total = len(unique(df_gg["st_domain"].tolist()))
    receiver_gg_total = len(unique(df_gg["thrd_domain"].tolist()))
    
    sender_fb_total = len(unique(df_fb["st_domain"].tolist()))
    receiver_fb_total = len(unique(df_fb["thrd_domain"].tolist()))

    column_names = pd.DataFrame([
        ["TYPE",""],
        ["GOOGLE SSO", "Sender_#"],
        ["GOOGLE SSO", "Sender_%"], 
        ["GOOGLE SSO", "Receiver_#"],
        ["GOOGLE SSO", "Receiver_%"], 
        ["FACEBOOK SSO", "Sender_#"],
        ["FACEBOOK SSO", "Sender_%"],
        ["FACEBOOK SSO", "Receiver_#"],
        ["FACEBOOK SSO", "Receiver_%"]],
        columns=["NO", ""])
    
    result = []
    
    for val in type_value:
        fil_gg = df_gg[(df_gg[type]==val)]
        fil_fb = df_fb[(df_fb[type]==val)]
        filenamegg = "output/leakage_breakdown/gg_"+val+".csv"
        filenamefb = "output/leakage_breakdown/fb_"+val+".csv"
        fil_gg.to_csv(filenamegg,index=False)
        fil_fb.to_csv(filenamefb,index=False)
    
        sender_gg = len(unique(fil_gg["st_domain"].tolist()))
        receiver_gg = len(unique(fil_gg["thrd_domain"].tolist()))
    
        sender_fb = len(unique(fil_fb["st_domain"].tolist()))
        receiver_fb = len(unique(fil_fb["thrd_domain"].tolist()))
    
        percent_sender_gg = round((sender_gg/sender_gg_total)*100,2)
        percent_receiver_gg = round((receiver_gg/receiver_gg_total)*100,2)
    
        percent_sender_fb = round((sender_fb/sender_fb_total)*100,2)
        percent_receiver_fb = round((receiver_fb/receiver_fb_total)*100,2)
        result.append([val.capitalize(),sender_gg,percent_sender_gg,receiver_gg,percent_receiver_gg,sender_fb,percent_sender_fb,receiver_fb,percent_receiver_fb])

    result.append(["Total",sender_gg_total,100,receiver_gg_total,100,sender_fb_total,100,receiver_fb_total,100])
    columns = pd.MultiIndex.from_frame(column_names)
    df = pd.DataFrame(result,columns=columns)
    print(df)

#METHOD
leak_method = ['URI', 'REFERER', 'PAYLOAD', 'COOKIES']
encoding_form = ['PLAINTEXT', 'BASE64', 'MD5', 'SHA1', 'SHA256']
pii_type = ['EMAIL', 'USER_NAME', 'USER_ID']
categories = ['leakage_method','encoding_form','pii_type']

print("====================BREAKDOWN of PII LEAKAGE TO THIRD-PARTY DOMAINS====================")
print("")
for category in categories:
    match(category):
        case 'leakage_method':
            print("# By LEAKAGE CHANNEL")
            Result(category,leak_method,data_gg,data_fb)
        case 'encoding_form':
            print("# By ENCODING/HASHING")
            Result(category,encoding_form,data_gg,data_fb)
        case 'pii_type':
            print("# By LEAKAGE CHANNEL")
            Result(category,pii_type,data_gg,data_fb)
    print("--"*50)
print("Detail CSV file stored at /output/leakage_breakdown/")