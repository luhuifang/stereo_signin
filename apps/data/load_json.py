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
        for index in range(len(v2)):
            if "Sample_id" in v2[index].keys():
                v2[index]["Sample_id"] = v2[index]["Sample_id"] + f'_{index+1}'
                data_dict[k1][k2][v2[index]["Sample_id"]] = v2[index]
                continue
            if "Sample_Name" in v2[index].keys():
                v2[index]["Sample_Name"] = v2[index]["Sample_Name"] + f'_{index+1}'
                data_dict[k1][k2][v2[index]["Sample_Name"]] = v2[index]
                continue
            if "Sample_Id" in v2[index].keys():
                v2[index]["Sample_Id"] = v2[index]["Sample_Id"] + f'_{index+1}'
                data_dict[k1][k2][v2[index]["Sample_Id"]] = v2[index]
                continue
            data_dict[k1][k2][count] = v2[index]
            count += 1

