import pandas as pd
from utils import unique

def Result(data,filename):
    thrd_domains = unique(data["thrd_domain"].tolist())
    list_receiver = []
    list_num = []
    for domain in thrd_domains:
        filtered = data[(data['thrd_domain']==domain)]
        count_domain = len(unique(filtered['st_domain'].tolist()))
        list_receiver.append(domain)
        list_num.append(count_domain)

    _result = {'receiver': list_receiver, 'num_of_st': list_num}
    df_result = pd.DataFrame(_result)
    sorted_df_result = df_result.sort_values(by=['num_of_st'], ascending=False)
    print(sorted_df_result)
    sorted_df_result.to_csv(filename,header=False,index=False)

print("Breakdown of Top third-party domains involved in PII leakage")
print("Login with Google")
data_gg = pd.read_csv('input/Japan/Google_PIILeak_ThirdParty.csv')
Result(data_gg,"output/3rd_domains_breakdown/google.csv")

print("Login with Facebook")
data_fb = pd.read_csv('input/Japan/Facebook_PIILeak_ThirdParty.csv')
Result(data_fb,"output/3rd_domains_breakdown/facebook.csv")

print("Detail CSV file stored at /output/3rd_domains_breakdown/")