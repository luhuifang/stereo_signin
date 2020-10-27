import json
import plotly.express as px
from pandas.core.frame import DataFrame


def tran_data(data):
    if 'K' in data:
        return float(data.strip('K'))/1000
    elif 'M' in data:
        return float(data.strip('M'))
    else:
        return float(data)

with open('../../data/final_result.json','r') as read_json:
    data_json = json.load(read_json)

DUPLICATION_RATE = float(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['DUPLICATION_RATE'])/100
UNIQUE_RATE = 1 - float(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['DUPLICATION_RATE'])/100
FAIL_FILTER_RATE = float(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['FAIL_FILTER_RATE'])/100

Unique_Mapped_Reads_RATE_1 = float(data_json["2.Alignment"]["2.2.Uniquely_Mapped_Read"][0]['Mapped_Reads(%)'].strip('%'))/100
Unique_Mapped_Reads_RATE_2 = float(data_json["2.Alignment"]["2.2.Uniquely_Mapped_Read"][1]['Mapped_Reads(%)'].strip('%'))/100

Multi_Mapping_RATE_1 = float(data_json["2.Alignment"]["2.3.Multi_Mapping_Read"][0]["Multiple_Loci"].split('(')[-1].strip('%)'))/100+float(data_json["2.Alignment"]["2.3.Multi_Mapping_Read"][0]["Many_Loci"].split('(')[-1].strip('%)'))/100
Multi_Mapping_RATE_2 = float(data_json["2.Alignment"]["2.3.Multi_Mapping_Read"][1]["Multiple_Loci"].split('(')[-1].strip('%)'))/100+float(data_json["2.Alignment"]["2.3.Multi_Mapping_Read"][1]["Many_Loci"].split('(')[-1].strip('%)'))/100

Chimeric_RATE_1 = float(data_json["2.Alignment"]["2.5.Chimeric_Read"][0]["Number_Of_Chimeric_Reads"].split('(')[-1].strip('%)'))/100
Chimeric_RATE_2 = float(data_json["2.Alignment"]["2.5.Chimeric_Read"][1]["Number_Of_Chimeric_Reads"].split('(')[-1].strip('%)'))/100

Input_read_num_1 = tran_data(data_json["2.Alignment"]["2.1.Input_Read"][0]["Number_Of_Input_Reads"])
Input_read_num_2 = tran_data(data_json["2.Alignment"]["2.1.Input_Read"][1]["Number_Of_Input_Reads"])

Unmapping_RATE_1 = float(data_json["2.Alignment"]["2.4.Unmapping_Read"][0]["Too_Many_Mismatches"].split('(')[-1].strip('%)'))/100 + float(data_json["2.Alignment"]["2.4.Unmapping_Read"][0]["Too_Short"].split('(')[-1].strip('%)'))/100 + float(data_json["2.Alignment"]["2.4.Unmapping_Read"][0]["Other"].split('(')[-1].strip('%)'))/100
Unmapping_RATE_2 = float(data_json["2.Alignment"]["2.4.Unmapping_Read"][1]["Too_Many_Mismatches"].split('(')[-1].strip('%)'))/100 + float(data_json["2.Alignment"]["2.4.Unmapping_Read"][1]["Too_Short"].split('(')[-1].strip('%)'))/100 + float(data_json["2.Alignment"]["2.4.Unmapping_Read"][1]["Other"].split('(')[-1].strip('%)'))/100

Unmapping_Read_1 = Input_read_num_1*Unmapping_RATE_1
Unmapping_Read_2 = Input_read_num_2*Unmapping_RATE_2

Unpass_Filter = tran_data(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["TOTAL_READS"])*float(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["FAIL_FILTER_RATE"])/100

EXONIC = tran_data(data_json["2.Alignment"]["2.7.Annotation"][0]["EXONIC"].split('(')[-2])
INTRONIC = tran_data(data_json["2.Alignment"]["2.7.Annotation"][0]["INTRONIC"].split('(')[-2])
INTERGENIC = tran_data(data_json["2.Alignment"]["2.7.Annotation"][0]["INTERGENIC"].split('(')[-2])
TRANSCRIPTOME = tran_data(data_json["2.Alignment"]["2.7.Annotation"][0]["TRANSCRIPTOME"].split('(')[-2])
ANTISENSE = tran_data(data_json["2.Alignment"]["2.7.Annotation"][0]["ANTISENSE"].split('(')[-2])

Low_Quality_Reads_1 = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Low_Quality_Reads"])
Low_Quality_Reads_2 = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Low_Quality_Reads"])
Too_Many_N_Reads_1 = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Too_Many_N_Reads"])
Too_Many_N_Reads_2 = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Too_Many_N_Reads"])
Too_Short_Reads_1 = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Too_Short_Reads"])
Too_Short_Reads_2 = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Too_Short_Reads"])
Too_Long_Reads_1 = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Too_Long_Reads"])
Too_Long_Reads_2 = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Too_Long_Reads"])

UnMapping_1 = tran_data(data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"][0]["total_reads"]) - tran_data(data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"][0]["mapped_reads"].split('(')[-2])
UnMapping_2 = tran_data(data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"][1]["total_reads"]) - tran_data(data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"][1]["mapped_reads"].split('(')[-2])

# print(DUPLICATION_RATE,UNIQUE_RATE,FAIL_FILTER_RATE,Mapped_Reads_RATE_1,Mapped_Reads_RATE_2,Multi_Mapping_RATE_1,\
    # Multi_Mapping_RATE_2,Chimeric_RATE_1,Chimeric_RATE_2,Unmapping_RATE_1,Unmapping_RATE_2)
# print(EXONIC,INTRONIC,INTERGENIC,TRANSCRIPTOME,ANTISENSE)
df = [['Rate','Annotation','Filter and deduplication','Alignment reference reads','Filiter stat','Adapter Filter','total read']]
for i in ['Unique_Mapped_Reads_RATE_1','Unique_Mapped_Reads_RATE_2','Multi_Mapping_RATE_1','Multi_Mapping_RATE_2','Chimeric_RATE_1','Chimeric_RATE_2','Unmapping_Read_1','Unmapping_Read_2']:
    if i == 'Unmapping_Read_1':
        df.append([eval(i),'','','Unmapping_Read_1','Clean reads_1','Mapping_1','Total reads_1'])
        continue
    elif i == 'Unmapping_Read_2':
        df.append([eval(i),'','','Unmapping_Read_2','Clean reads_2','Mapping_2','Total reads_2'])
        continue   
    else:
        if i.split('_')[-1] == '1':
            df.append([Unpass_Filter*eval(i),'','Unpass filiter',''.join(i.split('_RATE')).replace('_',' '),'Clean reads_1','Mapping_1','Total reads_1']) 
        else:
            df.append([Unpass_Filter*eval(i),'','Unpass filiter',''.join(i.split('_RATE')).replace('_',' '),'Clean reads_2','Mapping_2','Total reads_2']) 
        for j in ['DUPLICATION_RATE','UNIQUE_RATE']:
            for m in ['EXONIC','INTRONIC','INTERGENIC','TRANSCRIPTOME','ANTISENSE']:
                if i.split('_')[-1] == '1':
                    df.append([eval(m)*eval(i)*eval(j),m,j.split('_RATE')[0]+ ' reads',''.join(i.split('_RATE')).replace('_',' '),'Clean reads_1','Mapping_1','Total reads_1'])
                else:
                    df.append([eval(m)*eval(i)*eval(j),m,j.split('_RATE')[0]+' reads',''.join(i.split('_RATE')).replace('_',' '),'Clean reads_2','Mapping_2','Total reads_2'])

for ii in ['Low_Quality_Reads_1','Low_Quality_Reads_2','Too_Many_N_Reads_1','Too_Many_N_Reads_2',\
'Too_Short_Reads_1','Too_Short_Reads_2','Too_Long_Reads_1','Too_Long_Reads_2']:
    if ii.split('_')[-1] == '1':
        df.append([eval(ii),'','',ii.replace('_',' '),'Filiter reads_1','Mapping_1','Total reads_1'])
    else:
        df.append([eval(ii),'','',ii.replace('_',' '),'Filiter reads_2','Mapping_2','Total reads_2'])

for iii in ['UnMapping_1','UnMapping_2']:
    if iii.split('_')[-1] == '1':
        df.append([eval(iii),'','','','','UnMapping_1','Total reads_1'])
    else:
        df.append([eval(iii),'','','','','UnMapping_2','Total reads_2'])

df = DataFrame(df)
df.columns = df.loc[0,:]
df = df.loc[1:,:]
fig = px.sunburst(df, path=['total read', 'Adapter Filter', 'Filiter stat','Alignment reference reads','Filter and deduplication','Annotation'], values='Rate')
fig.show()