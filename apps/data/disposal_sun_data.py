import json
import pandas as pd
import numpy as np
from decimal import Decimal

import plotly.express as px
import plotly.graph_objects as go
from pandas.core.frame import DataFrame

from apps.data.data_config import Data_Info
from apps.data.get_data import GetData as GD

GD = GD(Data_Info['data_path'])

def get_sun_fig(values):
    
    Total_reads,Barcode_Mapping,UnMapping,Filter_reads,Fail_Filter,Clean_reads,Umi_Filter_Reads,Too_Long_Reads,Too_Short_Reads,\
    Too_Many_N_Reads,Low_Quality_Reads,Unique_Mapped_Reads,Chimeric_Reads,Multi_Mapping_Reads,Reference_Mapping_reads,Unmapping_Read,DuPlication_Reads,Unique_Reads,Contour_area,\
    Number_of_DNB_under_tissue,Ratio,Total_Gene_type,Raw_Reads,Reads_under_tissue,Fraction_Reads_in_Spots_Under_Tissue,\
    Q20_Barcode,Q30_Barcode,Q10_Barcode,Q10_UMI,Q20_UMI,Q30_UMI = GD.get_data(values)

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
    'Unique_Mapped_Reads':'Uniquely mapped reads number',
    'Chimeric_Reads':'A read aligns to two distinct portions of the genome with little or no overlap',
    'Multi_Mapping_Reads':'More than one matching record on the reference',
    'Unmapping_Read':'Unmapped reads number',
    'DuPlication_Reads':'Number of reads of duplication',
    'Unique_Reads':'Reads number of uniquely'
    }

    parents_dict = {'Total_reads':'','Barcode_Mapping':'Total_reads','UnMapping':'Total_reads',
    'Filter_reads':'Barcode_Mapping','Clean_reads':'Barcode_Mapping', 'Umi_Filter_Reads':'Filter_reads',
    'Too_Long_Reads':'Filter_reads','Too_Short_Reads':'Filter_reads','Too_Many_N_Reads':'Filter_reads',
    'Low_Quality_Reads':'Filter_reads','Unique_Mapped_Reads':'Clean_reads','Chimeric_Reads':'Clean_reads',
    'Multi_Mapping_Reads':'Clean_reads','Unmapping_Read':'Clean_reads','DuPlication_Reads':'Unique_Mapped_Reads',
    'Unique_Reads':'Unique_Mapped_Reads'
    }
    parents_dict_short = {'Total_reads':'','Barcode_Mapping':'Total_reads','UnMapping':'Total_reads',
    'Filter_reads':'Barcode_Mapping','Clean_reads':'Barcode_Mapping', 'Umi_Filter_Reads':'Filter_reads',
    'Too_Long_Reads':'Filter_reads','Too_Short_Reads':'Filter_reads','Too_Many_N_Reads':'Filter_reads',
    'Low_Quality_Reads':'Filter_reads','Unique_Mapped_Reads':'Clean_reads','Chimeric_Reads':'Clean_reads',
    'Multi_Mapping_Reads':'Clean_reads','Unmapping_Read':'Clean_reads'
    }
    name_pro = []
    df = [['labels','parents','value','text']]
    if len(values) == len(GD.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"].keys()):
        for k,v in parents_dict.items():
            df.append([k.replace('_',' '),v.replace('_',' '),str(eval(k)),hovertext_dict[k]])
            # name_pro.append(str(round(eval(k),2))+'M')
            if k == 'Total_reads':
                name_pro.append('{}'.format(GD.tran2human(round(eval(k),2))))
            else:
                name_pro.append('{}({}%)'.format(GD.tran2human(round(eval(k),2)),round(eval(k)/eval(parents_dict[k])*100,2)))
    else:
        for k,v in parents_dict_short.items():
            df.append([k.replace('_',' '),v.replace('_',' '),str(eval(k)),hovertext_dict[k]])
            # name_pro.append(str(round(eval(k),2))+'M')
            if k == 'Total_reads':
                name_pro.append('{}'.format(GD.tran2human(round(eval(k),2))))
            else:
                name_pro.append('{}({}%)'.format(GD.tran2human(round(eval(k),2)),round(eval(k)/eval(parents_dict[k])*100,2)))
    
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
            'colors':['#CC99CC','#FF9999','#FF99CC','#9999CC','#CCCCFF',
            '#66CCFF','#99CCFF','#3399CC','#6699CC','#99CCFF','#66CCCC','#CCFFCC','#CCFFFF','#99CCCC',
            '#336633','#669933'],
            # 'line':{'color':'green','width':2},
            'colorscale':'YlGnBu'},
        
    ))
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0),height=450)
    return fig