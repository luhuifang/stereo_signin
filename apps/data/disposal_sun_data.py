import json
import pandas as pd
import numpy as np
from decimal import Decimal

import plotly.express as px
import plotly.graph_objects as go
from pandas.core.frame import DataFrame

from apps.data.load_json import data_json,data_dict

def tran_data(data):
    if 'K' in data:
        return Decimal(float(data.strip('K'))/1000).quantize(Decimal("0.00"))
    elif 'M' in data:
        return Decimal(float(data.strip('M'))).quantize(Decimal("0.00"))
    else:
        return Decimal(float(data)).quantize(Decimal("0.00"))

def get_sun_fig(values):
    Reference_Mapping_reads,Chimeric_Reads,Multi_Mapping_Reads,Unique_Mapped_Reads,Unique_Mapped_Reads_RATE,Multi_Mapping_RATE,Chimeric_RATE,\
    Unmapping_RATE,Input_read_num,Unmapping_Read,UnMapping,Raw_Reads,mapped_reads = 0,0,0,0,0,0,0,0,0,0,0,0,0
    for value in values:
        # Filter and deduplication
        # Pass Filter Data
        DuPlication_Reads = round(Decimal(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['DUPLICATION_RATE'])/100*tran_data(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['PASS_FILTER']),2)
        Unique_Reads = Decimal(tran_data(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['UNIQUE_READS'])).quantize(Decimal("0.00"))
        # Fail Filter Data
        Fail_Filter = round(tran_data(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["TOTAL_READS"])*Decimal(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["FAIL_FILTER_RATE"])/100,2)

        # Clean Reads Data
        # mapping reads
        Unique_Mapped_Reads = tran_data(data_dict["2.Alignment"]["2.2.Uniquely_Mapped_Read"][value]['Mapped_Reads_Number']) 
        Multi_Mapping_Reads = tran_data(data_dict["2.Alignment"]["2.3.Multi_Mapping_Read"][value]['Multiple_Loci'].split('(')[-2]) 
        Chimeric_Reads = tran_data(data_dict["2.Alignment"]["2.5.Chimeric_Read"][value]['Number_Of_Chimeric_Reads'].split('(')[-2]) 
        Reference_Mapping_reads += round(Unique_Mapped_Reads + Multi_Mapping_Reads + Chimeric_Reads,2)
        # print(Unique_Mapped_Reads,Multi_Mapping_Reads,Chimeric_Reads)
        # Unmaping reads
        Unmapping_RATE = round(Decimal(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Too_Many_Mismatches"].split('(')[-1].strip('%)'))/100 + Decimal(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Too_Short"].split('(')[-1].strip('%)'))/100 + Decimal(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Other"].split('(')[-1].strip('%)'))/100,2)
        Input_read_num = tran_data(data_dict["2.Alignment"]["2.1.Input_Read"][value]["Number_Of_Input_Reads"])
        Unmapping_Read += Decimal(Input_read_num*Unmapping_RATE).quantize(Decimal("0.00"))

        # Filiter reads Data
        Raw_Reads += tran_data(data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"][value]["Raw_Reads"])
        Low_Quality_Reads = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Low_Quality_Reads"])+tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Low_Quality_Reads"])
        Too_Many_N_Reads = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Too_Many_N_Reads"])+tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Too_Many_N_Reads"])
        Too_Short_Reads = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Too_Short_Reads"])+tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Too_Short_Reads"])
        Too_Long_Reads = tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][0]["Too_Long_Reads"])+tran_data(data_json["1.Filter_and_Map"]["1.2.Filter_Stat"][1]["Too_Long_Reads"])
        mapped_reads += tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["mapped_reads"].split('(')[-2])
        Umi_Filter_Reads = mapped_reads - Raw_Reads
        
        # UnMapping Data
        UnMapping += tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]) - tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["mapped_reads"].split('(')[-2])
        Clean_reads = Reference_Mapping_reads + Unmapping_Read
        Filter_reads = Umi_Filter_Reads + Too_Long_Reads + Too_Short_Reads + Low_Quality_Reads + Too_Many_N_Reads
        Barcode_Mapping = Filter_reads + Clean_reads
        #Total reads Data
        Total_reads = Barcode_Mapping + UnMapping

    labels_color = {'Total_reads':'#F0FFFF','Barcode_Mapping':'Total_reads','UnMapping':'Total_reads','Filter_reads':'Barcode_Mapping',
    'Clean_reads':'Barcode_Mapping', 'Umi_Filter_Reads':'Filter_reads','Too_Long_Reads':'Filter_reads',
    'Too_Short_Reads':'Filter_reads','Too_Many_N_Reads':'Filter_reads','Low_Quality_Reads':'Filter_reads',
    'Reference_Mapping_reads':'Clean_reads','Unmapping_Read':'Clean_reads','DuPlication_Reads':'Reference_Mapping_reads',
    'Fail_Filter':'Reference_Mapping_reads','Unique_Reads':'Reference_Mapping_reads'
    }

    hovertext_dict = {'Total_reads':'Total number of sequencing reads',
    'Barcode_Mapping':'Number of reads from the second sequencing map back to the first time',
    'UnMapping':'Second sequencing cannot map back the number of reads from the first time',
    'Filter_reads':'Number of filter reads after quality control',
    'Clean_reads':'Number of reads after quality control', 
    'Umi_Filter_Reads':'Number of reads filtered with Umi',
    'Too_Long_Reads':'Number of reads filtered with too long',
    'Too_Short_Reads':'Number of reads filtered which too short',
    'Too_Many_N_Reads':'Number of reads filtered that contain too many N',
    'Low_Quality_Reads':'Number of reads filtered due to low quality',
    'Reference_Mapping_reads':'Uniquely mapped reads number',
    'Unmapping_Read':'Unmapped reads number',
    'DuPlication_Reads':'Number of reads of duplication',
    'Fail_Filter':'Number of reads that failed to pass the q10 filter',
    'Unique_Reads':'Reads number of uniquely'
    }

    parents_dict = {'Total_reads':'','Barcode_Mapping':'Total_reads','UnMapping':'Total_reads','Filter_reads':'Barcode_Mapping',
    'Clean_reads':'Barcode_Mapping', 'Umi_Filter_Reads':'Filter_reads','Too_Long_Reads':'Filter_reads',
    'Too_Short_Reads':'Filter_reads','Too_Many_N_Reads':'Filter_reads','Low_Quality_Reads':'Filter_reads',
    'Reference_Mapping_reads':'Clean_reads','Unmapping_Read':'Clean_reads','DuPlication_Reads':'Reference_Mapping_reads',
    'Fail_Filter':'Reference_Mapping_reads','Unique_Reads':'Reference_Mapping_reads'
    }
    parents_dict_sort = {'Total_reads':'','Barcode_Mapping':'Total_reads','UnMapping':'Total_reads','Filter_reads':'Barcode_Mapping',
    'Clean_reads':'Barcode_Mapping', 'Umi_Filter_Reads':'Filter_reads','Too_Long_Reads':'Filter_reads',
    'Too_Short_Reads':'Filter_reads','Too_Many_N_Reads':'Filter_reads','Low_Quality_Reads':'Filter_reads',
    'Reference_Mapping_reads':'Clean_reads','Unmapping_Read':'Clean_reads'
    }
    name_pro = []
    df = [['labels','parents','value','text']]
    if len(values) == len(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"].keys()):
        for k,v in parents_dict.items():
            df.append([k.replace('_',' '),v.replace('_',' '),str(eval(k)),hovertext_dict[k]])
            name_pro.append(str(round(eval(k),2))+'M')
    else:
        for k,v in parents_dict_sort.items():
            df.append([k.replace('_',' '),v.replace('_',' '),str(eval(k)),hovertext_dict[k]])
            name_pro.append(str(round(eval(k),2))+'M')
    
    df = DataFrame(df)
    df.columns = df.loc[0,:]
    df = df.loc[1:,:]
    fig = go.Figure()

    fig.add_trace(go.Sunburst(
        values=df.value,
        labels=df.labels,
        parents=df.parents,
        # name = 'name_pro',
        hovertext=df.text,
        # text = ['hello','hello'],
        hoverinfo='label+text',
        # hovertemplate = "<extra>{fullData.name}</extra>",
        text = name_pro,
        branchvalues="total",
        marker = {
            # 'colors':['#ff922b','#e64980','#a61e4d','#94d82d','#74b816','#c5f6fa','#99e9f2',
            # '#66d9e8','#3bc9db','#22b8cf','#15aabf','#1098ad','#91a7ff','#4c6ef5','#364fc7'],
            'colors':['#CC99CC','#FF9999','#FFCCCC','#9999CC','#CCCCFF','#CCFFFF','#99CCFF',
            '#66CCFF','#6699CC','#99CCFF','#66CCCC','#CCFFCC','#99CC99','#669933','#336633'],
            'line':{'color':'green','width':2},'colorscale':'YlGnBu'},
        
    ))
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0),height=450)
    return fig