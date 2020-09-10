import json
import pandas as pd

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()    # retain local pointer to value
        return value                        # faster to return than dict lookup

with open('./data/final_result.json','r') as read_json:
    data_json = json.load(read_json)

df_table = pd.DataFrame(
        [list(i.values()) for i in data_json["4.TissueCut"]["4.2.TissueCut_Bin_stat"]]  
    )
df_table.columns = ['binSize', 'MeanReads', 'MedianReads', 'MeanGeneType', 'MedianGeneType', 'MeanUmi', 'MedianUmi']
# print(list(data_json["4.TissueCut"]["4.2.TissueCut_Bin_stat"][0].keys()))

data_dict = Vividict()
for k1,v1 in data_json.items():
    for k2,v2 in v1.items():
        count = 0
        for i in v2:
            if "Sample_id" in i.keys():
                data_dict[k1][k2][i["Sample_id"]] = i
                continue
            if "Sample_Name" in i.keys():
                data_dict[k1][k2][i["Sample_Name"]] = i
                continue
            if "Sample_Id" in i.keys():
                data_dict[k1][k2][i["Sample_Id"]] = i
                continue
            data_dict[k1][k2][count] = i
            count += 1

