import pandas as pd
from utils import unique

def GetListBelongsEcosysem(type):
    df = pd.read_csv('input/Ghostery/3rd_'+type+'.csv',sep='|')
    df_exclue = df[(df['name of organization']=='Meta') | (df['name of organization']=='Google')]
    return unique(df_exclue['input'].to_list())


def ExcludeEcosystem(type):
    list_exclude = GetListBelongsEcosysem(type)
    data_adhoc = pd.read_csv('input/Adhoc/Japan/'+type+'.csv.gz',compression='gzip')
    exclude_data = data_adhoc[~data_adhoc.thrd_domain.isin(list_exclude)]
    exclude_data = exclude_data[exclude_data['st_domain'].str.split(".").str[0] != exclude_data['thrd_domain'].str.split(".").str[0]]
    exclude_data.to_csv("input/Japan/"+type+"_PIILeak_ThirdParty.csv",index=False)

types = ["Google","Facebook"]
for t in types:
    ExcludeEcosystem(t)