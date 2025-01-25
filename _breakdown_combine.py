import pandas as pd
from utils import unique
from utils import intersection
import itertools

def mix(methods):
    lo = ["gg","fb"]
    lo_num = []
    for la in lo:
        lists = []
        for method in methods:
            _filename = "output/leakage_breakdown/"+la+"_"+method+".csv"
            _df = pd.read_csv(_filename)
            lists.append(unique(_df['st_domain'].tolist()))
        
        re = lists[0]
        for list in lists:
            re = intersection(re,list)
        lo_num.append(len(re))
    
    
    combined = ""
    for method in methods:
        combined = combined + method + " x "
    combined = combined[:-3]
    return [combined,lo_num]



def run(comb):
    data = []
    columns=["Combine","Google","Facebook"]
    for r in range(2, len(comb) + 1):
        combinations = itertools.combinations(comb, r)
        for combo in combinations:
            row = mix(combo)
            if(all([val == 0 for val in row[1]]) == False):
                data.append([row[0],row[1][0],row[1][1]])
    df = pd.DataFrame(data,columns=columns)
    print(df)
    print()

print("====Breakdown of the number of first-party domains that share PII to third-party domain by combining.===")
print()


print("By LEAKED CHANNEL")
channels = ["PAYLOAD", "COOKIES", "REFERER", "URI"]
run(channels)

print("By ENCODING/HASHING")
forms = ["Plaintext", "BASE64", "MD5", "SHA1", "SHA256"]
run(forms)

print("By PII TYPE")
types = ["EMAIL", "USER_NAME", "USER_ID"]
run(types)


