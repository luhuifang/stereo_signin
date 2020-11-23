import json
import plotly.graph_objects as go
from pandas.core.frame import DataFrame

from apps.statPage.load_json import LoadStatJson, number2human
from apps.statPage.static_info import hovertext_dict, parents_dict, parents_dict_sort

def get_sun_fig(values, file_dir):
    loadJson = LoadStatJson(file_dir)
    data_dict = loadJson.getDataDict(loadJson.data_json)

    Total_reads, Barcode_Mapping, UnMapping, Clean_reads, Filter_reads, Reference_Mapping_reads, \
        Unique_Mapped_Reads, Multi_Mapping_Reads, Chimeric_Reads, Unmapping_Read, MID_Filter_Reads, \
        Too_Short_Reads, Too_Long_Reads, Too_Many_N_Reads, Low_Quality_Reads, DuPlication_Reads, \
        Unique_Reads, Fail_Filter, Raw_Reads, mapped_reads, \
        Q10_Barcode,Q20_Barcode,Q30_Barcode,Q10_MID,Q20_MID,Q30_MID,\
        Exonic, Intronic, Intergenic, Transcriotome, Antisense,\
        Input_read, Uniquely_Mapped_Read, Multi_Mapping_Read, RNA_Unmapping_Read, Chimeric_Read = loadJson.getReadsStatData(values)
    
    
    name_pro = []
    df = [['labels','parents','value','text']]

    if len(values) == len(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"].keys()):
        parents = parents_dict
    else:
        parents = parents_dict_sort

    for k,v in parents.items():
        df.append([k.replace('_',' '),v.replace('_',' '),str(eval(k)),hovertext_dict[k]])
        if k == 'Total_reads':
            name_pro.append('{}'.format(number2human(eval(k))))
            #name_pro.append('{}M'.format(str(round(eval(k),2))))
        else:
            #name_pro.append('{}M({}%)'.format(str(round(eval(k),2)),round(eval(k)/eval(parents_dict[k])*100,2)))
            name_pro.append('{}({}%)'.format(number2human(eval(k)),round(eval(k)/eval(parents_dict[k])*100,2)))
    
    
    df = DataFrame(df)
    df.columns = df.loc[0,:]
    df = df.loc[1:,:]
    fig = go.Figure()

    fig.add_trace(go.Sunburst(
        values=df.value,
        labels=df.labels,
        parents=df.parents,
        hovertext=df.text,
        hoverinfo='label+text',
        text = name_pro,
        branchvalues="total",
        marker = {
            'colors':['#CC99CC','#FF9999','#FF99CC','#FFB6C1','#009ACD','#C6E2FF','#00BFFF',
            '#99CCFF','#99CCFF','#66CCCC','#CCFFCC','#CCFFFF','#99CCCC',
            '#336633','#669933'],
            'colorscale':'YlGnBu'
        },
        
    ))
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0),height=450)
    return fig