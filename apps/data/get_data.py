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

def get_data(values):
    Reference_Mapping_reads,Chimeric_Reads,Multi_Mapping_Reads,Unique_Mapped_Reads,Unique_Mapped_Reads_RATE,\
    Multi_Mapping_RATE,Chimeric_RATE,Unmapping_RATE,Input_read_num,Unmapping_Read,UnMapping,Raw_Reads,mapped_reads,\
    Q10_Barcode,Q20_Barcode,Q30_Barcode,Q10_UMI,Q20_UMI,Q30_UMI,Low_Quality_Reads,Too_Many_N_Reads,Too_Short_Reads,\
    Too_Long_Reads = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    for value in values:
        # 4.1.TissueCut_Total_Stat
        Contour_area = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Contour_area']
        Number_of_DNB_under_tissue = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Number_of_DNB_under_tissue']
        Ratio = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Ratio']
        Total_Gene_type = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Total_Gene_type']
        Raw_reads = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Raw_reads']
        Reads_under_tissue = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Reads_under_tissue']
        Fraction_Reads_in_Spots_Under_Tissue = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Fraction_Reads_in_Spots_Under_Tissue']

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

        # Unmaping reads
        Unmapping_RATE = round(Decimal(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Too_Many_Mismatches"].split('(')[-1].strip('%)'))/100 + Decimal(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Too_Short"].split('(')[-1].strip('%)'))/100 + Decimal(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Other"].split('(')[-1].strip('%)'))/100,2)
        Input_read_num = tran_data(data_dict["2.Alignment"]["2.1.Input_Read"][value]["Number_Of_Input_Reads"])
        Unmapping_Read += Decimal(Input_read_num*Unmapping_RATE).quantize(Decimal("0.00"))

        # Filiter reads Data
        Raw_Reads += tran_data(data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"][value]["Raw_Reads"])
        Low_Quality_Reads += tran_data(data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"][value]["Low_Quality_Reads"])
        Too_Many_N_Reads += tran_data(data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"][value]["Too_Many_N_Reads"])
        Too_Short_Reads += tran_data(data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"][value]["Too_Short_Reads"])
        Too_Long_Reads += tran_data(data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"][value]["Too_Long_Reads"])
        mapped_reads += tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["mapped_reads"].split('(')[-2])
        Umi_Filter_Reads = mapped_reads - Raw_Reads
        
        # UnMapping Data
        UnMapping += tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]) - tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["mapped_reads"].split('(')[-2])
        Clean_reads = Reference_Mapping_reads + Unmapping_Read
        Filter_reads = Umi_Filter_Reads + Too_Long_Reads + Too_Short_Reads + Low_Quality_Reads + Too_Many_N_Reads
        Barcode_Mapping = Filter_reads + Clean_reads
        #Total reads Data
        Total_reads = Barcode_Mapping + UnMapping

        # Barcode and Umi QC Data
        Q10_Barcode_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q10_bases_in_barcode"].replace('%',''))/100
        Q20_Barcode_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q20_bases_in_barcode"].replace('%',''))/100
        Q30_Barcode_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q30_bases_in_barcode"].replace('%',''))/100
        Q10_UMI_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q10_bases_in_umi"].replace('%',''))/100
        Q20_UMI_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]['Q20_bases_in_umi'].replace('%',''))/100
        Q30_UMI_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q30_bases_in_umi"].replace('%',''))/100
        
        Q10_Barcode += round(Q10_Barcode_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
        Q20_Barcode += round(Q20_Barcode_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
        Q30_Barcode += round(Q30_Barcode_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
        Q10_UMI += round(Q10_UMI_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
        Q20_UMI += round(Q20_UMI_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
        Q30_UMI += round(Q30_UMI_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
    
    Q10_Barcode = '{}M({}%)'.format(Q10_Barcode,round(Q10_Barcode/Total_reads*100,2))
    Q20_Barcode = '{}M({}%)'.format(Q20_Barcode,round(Q20_Barcode/Total_reads*100,2))
    Q30_Barcode = '{}M({}%)'.format(Q30_Barcode,round(Q30_Barcode/Total_reads*100,2))
    Q10_UMI = '{}M({}%)'.format(Q10_UMI,round(Q10_UMI/Total_reads*100,2))
    Q20_UMI = '{}M({}%)'.format(Q20_UMI,round(Q20_UMI/Total_reads*100,2))
    Q30_UMI = '{}M({}%)'.format(Q30_UMI,round(Q30_UMI/Total_reads*100,2))

    return Total_reads,Barcode_Mapping,UnMapping,Filter_reads,Fail_Filter,Clean_reads,Umi_Filter_Reads,Too_Long_Reads,Too_Short_Reads,\
    Too_Many_N_Reads,Low_Quality_Reads,Reference_Mapping_reads,Unmapping_Read,DuPlication_Reads,Unique_Reads,Contour_area,\
    Number_of_DNB_under_tissue,Ratio,Total_Gene_type,Raw_reads,Reads_under_tissue,Fraction_Reads_in_Spots_Under_Tissue,\
    Q20_Barcode,Q30_Barcode,Q10_Barcode,Q10_UMI,Q20_UMI,Q30_UMI