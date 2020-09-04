import json
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from pandas.core.frame import DataFrame

from apps.data.load_json import data_json

def tran_data(data):
    if 'K' in data:
        return round(float(data.strip('K'))/1000,2)
    elif 'M' in data:
        return round(float(data.strip('M')),2)
    else:
        return round(float(data),2)

def get_sun_fig():
    DUPLICATION_RATE = float(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['DUPLICATION_RATE'])/100
    UNIQUE_RATE = 1 - float(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['DUPLICATION_RATE'])/100
    FAIL_FILTER_RATE = float(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['FAIL_FILTER_RATE'])/100

    Unique_Mapped_Reads_RATE_1 = float(data_json["2.Alignment"]["2.2.Uniquely_Mapped_Read"][0]['Mapped_Reads(%)'].strip('%'))/100
    Unique_Mapped_Reads_RATE_2 = float(data_json["2.Alignment"]["2.2.Uniquely_Mapped_Read"][1]['Mapped_Reads(%)'].strip('%'))/100

    Multi_Mapping_RATE_1 = float(data_json["2.Alignment"]["2.3.Multi_Mapping_Read"][0]["Multiple_Loci"].split('(')[-1].strip('%)'))/100+float(data_json["2.Alignment"]["2.3.Multi_Mapping_Read"][0]["Many_Loci"].split('(')[-1].strip('%)'))/100
    Multi_Mapping_RATE_2 = float(data_json["2.Alignment"]["2.3.Multi_Mapping_Read"][1]["Multiple_Loci"].split('(')[-1].strip('%)'))/100+float(data_json["2.Alignment"]["2.3.Multi_Mapping_Read"][1]["Many_Loci"].split('(')[-1].strip('%)'))/100

    Chimeric_RATE_1 = float(data_json["2.Alignment"]["2.5.Chimeric_Read"][0]["Number_Of_Chimeric_Reads"].split('(')[-1].strip('%)'))/100
    Chimeric_RATE_2 = float(data_json["2.Alignment"]["2.5.Chimeric_Read"][1]["Number_Of_Chimeric_Reads"].split('(')[-1].strip('%)'))/100


    # Filter and deduplication
    # Pass Filter Data
    DuPlication_Reads = round(float(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['DUPLICATION_RATE'])/100*tran_data(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['PASS_FILTER']),2)
    Unique_Reads = tran_data(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['UNIQUE_READS'])

    # Fail Filter Data
    Fail_Filter = round(tran_data(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["TOTAL_READS"])*float(data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["FAIL_FILTER_RATE"])/100,2)

    # Annotation Data
    EXONIC = tran_data(data_json["2.Alignment"]["2.7.Annotation"][0]["EXONIC"].split('(')[-2])
    INTRONIC = tran_data(data_json["2.Alignment"]["2.7.Annotation"][0]["INTRONIC"].split('(')[-2])
    INTERGENIC = tran_data(data_json["2.Alignment"]["2.7.Annotation"][0]["INTERGENIC"].split('(')[-2])
    TRANSCRIPTOME = tran_data(data_json["2.Alignment"]["2.7.Annotation"][0]["TRANSCRIPTOME"].split('(')[-2])
    ANTISENSE = tran_data(data_json["2.Alignment"]["2.7.Annotation"][0]["ANTISENSE"].split('(')[-2])

    # Clean Reads Data
    # mapping reads
    Unique_Mapped_Reads = tran_data(data_json["2.Alignment"]["2.2.Uniquely_Mapped_Read"][0]['Mapped_Reads_Number']) + tran_data(data_json["2.Alignment"]["2.2.Uniquely_Mapped_Read"][1]['Mapped_Reads_Number'])
    Multi_Mapping_Reads = tran_data(data_json["2.Alignment"]["2.3.Multi_Mapping_Read"][0]['Multiple_Loci'].split('(')[-2]) + tran_data(data_json["2.Alignment"]["2.3.Multi_Mapping_Read"][1]['Multiple_Loci'].split('(')[-2])
    Chimeric_Reads = tran_data(data_json["2.Alignment"]["2.5.Chimeric_Read"][0]['Number_Of_Chimeric_Reads'].split('(')[-2]) + tran_data(data_json["2.Alignment"]["2.5.Chimeric_Read"][1]['Number_Of_Chimeric_Reads'].split('(')[-2])
    Mapping_reads = round(Unique_Mapped_Reads + Multi_Mapping_Reads + Chimeric_Reads,2)
    # Unmaping reads
    Unmapping_RATE_1 = round(float(data_json["2.Alignment"]["2.4.Unmapping_Read"][0]["Too_Many_Mismatches"].split('(')[-1].strip('%)'))/100 + float(data_json["2.Alignment"]["2.4.Unmapping_Read"][0]["Too_Short"].split('(')[-1].strip('%)'))/100 + float(data_json["2.Alignment"]["2.4.Unmapping_Read"][0]["Other"].split('(')[-1].strip('%)'))/100,2)
    Unmapping_RATE_2 = round(float(data_json["2.Alignment"]["2.4.Unmapping_Read"][1]["Too_Many_Mismatches"].split('(')[-1].strip('%)'))/100 + float(data_json["2.Alignment"]["2.4.Unmapping_Read"][1]["Too_Short"].split('(')[-1].strip('%)'))/100 + float(data_json["2.Alignment"]["2.4.Unmapping_Read"][1]["Other"].split('(')[-1].strip('%)'))/100,2)
    Input_read_num_1 = tran_data(data_json["2.Alignment"]["2.1.Input_Read"][0]["Number_Of_Input_Reads"])
    Input_read_num_2 = tran_data(data_json["2.Alignment"]["2.1.Input_Read"][1]["Number_Of_Input_Reads"])
    Unmapping_Read_1 = Input_read_num_1*Unmapping_RATE_1
    Unmapping_Read_2 = Input_read_num_2*Unmapping_RATE_2
    Unmapping_Read = round(Unmapping_Read_1 + Unmapping_Read_2,2)

    # Filiter reads Data
    Raw_Reads = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Raw_Reads"])+tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Raw_Reads"])
    Low_Quality_Reads = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Low_Quality_Reads"])+tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Low_Quality_Reads"])
    Too_Many_N_Reads = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Too_Many_N_Reads"])+tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Too_Many_N_Reads"])
    Too_Short_Reads = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Too_Short_Reads"])+tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Too_Short_Reads"])
    Too_Long_Reads = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Too_Long_Reads"])+tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Too_Long_Reads"])
    Umi_Filter_Reads = tran_data(data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"][0]["mapped_reads"].split('(')[-2])+tran_data(data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"][1]["mapped_reads"].split('(')[-2]) - Raw_Reads

    # UnMapping Data
    UnMapping_1 = tran_data(data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"][0]["total_reads"]) - tran_data(data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"][0]["mapped_reads"].split('(')[-2])
    UnMapping_2 = tran_data(data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"][1]["total_reads"]) - tran_data(data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"][1]["mapped_reads"].split('(')[-2])
    UnMapping = UnMapping_1 + UnMapping_2



    Clean_reads = Mapping_reads + Unmapping_Read

    Filter_reads = Umi_Filter_Reads + Too_Long_Reads + Too_Short_Reads + Low_Quality_Reads + Too_Many_N_Reads

    Mapping = Filter_reads + Clean_reads

    #Total reads Data
    Total_reads = Mapping + UnMapping
    labels_color = {'Total_reads':'#F0FFFF','Mapping':'Total_reads','UnMapping':'Total_reads','Filter_reads':'Mapping',
    'Clean_reads':'Mapping', 'Umi_Filter_Reads':'Filter_reads','Too_Long_Reads':'Filter_reads',
    'Too_Short_Reads':'Filter_reads','Too_Many_N_Reads':'Filter_reads','Low_Quality_Reads':'Filter_reads',
    'Mapping_reads':'Clean_reads','Unmapping_Read':'Clean_reads','DuPlication_Reads':'Mapping_reads',
    'Fail_Filter':'Mapping_reads','Unique_Reads':'Mapping_reads'
    }

    hovertext_dice = {'Total_reads':'#F0FFFF','Mapping':'Total_reads','UnMapping':'Total_reads','Filter_reads':'Mapping',
    'Clean_reads':'Mapping', 'Umi_Filter_Reads':'Filter_reads','Too_Long_Reads':'Filter_reads',
    'Too_Short_Reads':'Filter_reads','Too_Many_N_Reads':'Filter_reads','Low_Quality_Reads':'Filter_reads',
    'Mapping_reads':'Clean_reads','Unmapping_Read':'Clean_reads','DuPlication_Reads':'Mapping_reads',
    'Fail_Filter':'Mapping_reads','Unique_Reads':'Mapping_reads'
    }

    parents_dict = {'Total_reads':'','Mapping':'Total_reads','UnMapping':'Total_reads','Filter_reads':'Mapping',
    'Clean_reads':'Mapping', 'Umi_Filter_Reads':'Filter_reads','Too_Long_Reads':'Filter_reads',
    'Too_Short_Reads':'Filter_reads','Too_Many_N_Reads':'Filter_reads','Low_Quality_Reads':'Filter_reads',
    'Mapping_reads':'Clean_reads','Unmapping_Read':'Clean_reads','DuPlication_Reads':'Mapping_reads',
    'Fail_Filter':'Mapping_reads','Unique_Reads':'Mapping_reads'
    }

    df = [['labels','parents','value']]
    for k,v in parents_dict.items():
        df.append([k.replace('_',' '),v.replace('_',' '),eval(k)])
    df = DataFrame(df)
    df.columns = df.loc[0,:]
    df = df.loc[1:,:]

    fig = go.Figure()

    fig.add_trace(go.Sunburst(
        values=df.value,
        labels=df.labels,
        parents=df.parents,
        hovertext='hello',
    #     text = ['hello'],
        hoverinfo='label+value+text',
        branchvalues="total",
        marker = {
    #         'colors':['red'],
            'line':{'color':'green','width':2},'colorscale':'YlGnBu'},
        
    ))
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
  
    return fig