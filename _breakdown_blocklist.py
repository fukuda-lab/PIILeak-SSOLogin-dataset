import pandas as pd
from utils import unique


def Preprocess(dataframe,type):
    #Exclude same company
    temp_df = dataframe[dataframe['st_domain'].str.split(".").str[0] != dataframe['thrd_domain'].str.split(".").str[0]]

    #Exclude authentication
    #Facebook exclude (not meta) or (request contains ....)
    if type=="Facebook":
        Meta = ['facebook.com', 'fbsbx.com', 'facebook.net']
        exclude_df = temp_df[(~temp_df.thrd_domain.isin(Meta))|(temp_df['http_request'].str.contains("https://www.facebook.com/tr"))]
    
    #Google exclude request contains myaccount.....
    if type=="Google":
        temp_df1 = temp_df[~temp_df['http_request'].str.contains("https://accounts.google.com")]
        exclude_df = temp_df1[~temp_df1['http_request'].str.contains("https://myaccount.google.com")]

    return exclude_df


def AnaBlocklist_Request(type):
    print("-------"+type+"------------")
    data = pd.read_csv('input/Adhoc/Japan/'+type+'.csv')
    df = Preprocess(data,type)
    df1 = df[['id_site','id_request','http_request','method','easylist','privacylist']]
    df1 = df1.drop_duplicates()
    
    df_tracking = df1[(df1['easylist']==True)|(df1['privacylist']==True)]
    
    print("Third_party_Request: ",len(df1.index))
    print("Third_party_tracking_Request: ",len(df_tracking.index))

def AnaBlocklist_All_Domain(type):
    print("-------"+type+"------------")
    
    data = pd.read_csv('input/Adhoc/Japan/'+type+'.csv')
    df = Preprocess(data,type)
    df1 = df[['id_site','id_request','http_request','method','easylist','privacylist','st_domain','thrd_domain']]
    df1 = df1.drop_duplicates()
    
    list_rd = unique(df1['thrd_domain'].tolist())
    df_tracking = df1[(df1['easylist']==True)|(df1['privacylist']==True)]
    
    num = 0
    list_rd_track = []
    for rd in list_rd:
        df_tr_fil = df_tracking[(df_tracking['thrd_domain']==rd)]
        df_fil = df1[(df1['thrd_domain']==rd)] 
        num_req_tracking = len(df_tr_fil.index)
        num_req = len(df_fil.index)
        if num_req == num_req_tracking:
            list_rd_track.append(rd)
            num = num+1
    
    print("Total domains all requests be blocked: ",num)


print("============REQUEST=============")
AnaBlocklist_Request("Google")
AnaBlocklist_Request("Facebook")    
    


print("============ALL REQUEST BLOCK IN DOMAIN=============")
AnaBlocklist_All_Domain("Google")
AnaBlocklist_All_Domain("Facebook")
