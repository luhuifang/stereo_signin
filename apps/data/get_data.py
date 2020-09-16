import json
import pandas as pd
import numpy as np
from decimal import Decimal

import plotly.express as px
import plotly.graph_objects as go
from pandas.core.frame import DataFrame

from apps.data.data_config import Data_Info


class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()    # retain local pointer to value
        return value                        # faster to return than dict lookup

class GetData:
    def __init__(self):
        with open(Data_Info['data_path'],'r') as read_json:
            self.data_json = json.load(read_json)

        self.df_table = pd.DataFrame(
                [list(i.values()) for i in self.data_json["4.TissueCut"]["4.2.TissueCut_Bin_stat"]]  
            )
        self.df_table.columns = ['binSize', 'MeanReads', 'MedianReads', 'MeanGeneType', 'MedianGeneType', 'MeanUmi', 'MedianUmi']
        # print(list(data_json["4.TissueCut"]["4.2.TissueCut_Bin_stat"][0].keys()))

        self.data_dict = Vividict()
        for k1,v1 in self.data_json.items():
            for k2,v2 in v1.items():
                count = 0
                for index in range(len(v2)):
                    if "Sample_id" in v2[index].keys():
                        v2[index]["Sample_id"] = v2[index]["Sample_id"] + f'_{index+1}'
                        self.data_dict[k1][k2][v2[index]["Sample_id"]] = v2[index]
                        continue
                    if "Sample_Name" in v2[index].keys():
                        v2[index]["Sample_Name"] = v2[index]["Sample_Name"] + f'_{index+1}'
                        self.data_dict[k1][k2][v2[index]["Sample_Name"]] = v2[index]
                        continue
                    if "Sample_Id" in v2[index].keys():
                        v2[index]["Sample_Id"] = v2[index]["Sample_Id"] + f'_{index+1}'
                        self.data_dict[k1][k2][v2[index]["Sample_Id"]] = v2[index]
                        continue
                    self.data_dict[k1][k2][count] = v2[index]
                    count += 1

    def tran_data(self,data):
        if 'K' in data:
            return Decimal(float(data.strip('K'))/1000).quantize(Decimal("0.00"))
        elif 'M' in data:
            return Decimal(float(data.strip('M'))).quantize(Decimal("0.00"))
        else:
            return Decimal(float(data)).quantize(Decimal("0.00"))

    def get_data(self,values):
        Reference_Mapping_reads,Chimeric_Reads,Multi_Mapping_Reads,Unique_Mapped_Reads,Unique_Mapped_Reads_RATE,\
        Multi_Mapping_RATE,Chimeric_RATE,Unmapping_RATE,Input_read_num,Unmapping_Read,UnMapping,Raw_Reads,mapped_reads,\
        Q10_Barcode,Q20_Barcode,Q30_Barcode,Q10_UMI,Q20_UMI,Q30_UMI,Low_Quality_Reads,Too_Many_N_Reads,Too_Short_Reads,\
        Too_Long_Reads = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        for value in values:
            # 4.1.TissueCut_Total_Stat
            if "4.TissueCut" in self.data_dict.keys():
                Contour_area = self.data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Contour_area']
                Number_of_DNB_under_tissue = self.data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Number_of_DNB_under_tissue']
                Ratio = self.data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Ratio']
                Total_Gene_type = self.data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Total_Gene_type']
                Raw_reads = self.data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Raw_reads']
                Reads_under_tissue = self.data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Reads_under_tissue']
                Fraction_Reads_in_Spots_Under_Tissue = self.data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Fraction_Reads_in_Spots_Under_Tissue']
            elif "3.Basic" in self.data_dict.keys():
                Total_Umi_Mapping_To_Gene_And_slide = self.data_json["3.Basic"]["3.1.Get_Exp"][0]['Total_Umi_Mapping_To_Gene_And_slide']
                Gene_Number = self.data_json["3.Basic"]["3.1.Get_Exp"][0]['Gene_Number']
                Number_Of_DNB_With_Reads = self.data_json["3.Basic"]["3.1.Get_Exp"][0]['Number_Of_DNB_With_Reads']
                Slide_Area = self.data_json["3.Basic"]["3.1.Get_Exp"][0]['Slide_Area']
                Density_Of_DNB = self.data_json["3.Basic"]["3.1.Get_Exp"][0]['Density_Of_DNB']
            # Clean Reads Data
            # mapping reads
            Unique_Mapped_Reads_single = self.tran_data(self.data_dict["2.Alignment"]["2.2.Uniquely_Mapped_Read"][value]['Mapped_Reads_Number']) 
            Multi_Mapping_Reads_single = self.tran_data(self.data_dict["2.Alignment"]["2.3.Multi_Mapping_Read"][value]['Multiple_Loci'].split('(')[-2]) 
            Chimeric_Reads_single = self.tran_data(self.data_dict["2.Alignment"]["2.5.Chimeric_Read"][value]['Number_Of_Chimeric_Reads'].split('(')[-2]) 

            Unique_Mapped_Reads += self.tran_data(self.data_dict["2.Alignment"]["2.2.Uniquely_Mapped_Read"][value]['Mapped_Reads_Number']) 
            Multi_Mapping_Reads += self.tran_data(self.data_dict["2.Alignment"]["2.3.Multi_Mapping_Read"][value]['Multiple_Loci'].split('(')[-2]) 
            Chimeric_Reads += self.tran_data(self.data_dict["2.Alignment"]["2.5.Chimeric_Read"][value]['Number_Of_Chimeric_Reads'].split('(')[-2]) 

            Reference_Mapping_reads += round(Unique_Mapped_Reads_single + Multi_Mapping_Reads_single + Chimeric_Reads_single,2)

            # Filter and deduplication
            # Pass Filter Data
            # DuPlication_Reads = round(Decimal(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['DUPLICATION_RATE'])/100*tran_data(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['PASS_FILTER']),2)
            Unique_Reads = Decimal(self.tran_data(self.data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['UNIQUE_READS'])).quantize(Decimal("0.00"))
            DuPlication_Reads = Unique_Mapped_Reads - Unique_Reads
            # Fail Filter Data
            # Fail_Filter = round(tran_data(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["TOTAL_READS"])*Decimal(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["FAIL_FILTER_RATE"])/100,2)
            Fail_Filter = Reference_Mapping_reads - (DuPlication_Reads + Unique_Reads)

            # Unmaping reads
            Unmapping_RATE = round(Decimal(self.data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Too_Many_Mismatches"].split('(')[-1].strip('%)'))/100 + Decimal(self.data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Too_Short"].split('(')[-1].strip('%)'))/100 + Decimal(self.data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Other"].split('(')[-1].strip('%)'))/100,2)
            Input_read_num = self.tran_data(self.data_dict["2.Alignment"]["2.1.Input_Read"][value]["Number_Of_Input_Reads"])
            Unmapping_Read += Decimal(Input_read_num*Unmapping_RATE).quantize(Decimal("0.00"))

            # Filiter reads Data
            Raw_Reads += self.tran_data(self.data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"][value]["Raw_Reads"])
            Low_Quality_Reads += self.tran_data(self.data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"][value]["Low_Quality_Reads"])
            Too_Many_N_Reads += self.tran_data(self.data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"][value]["Too_Many_N_Reads"])
            Too_Short_Reads += self.tran_data(self.data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"][value]["Too_Short_Reads"])
            Too_Long_Reads += self.tran_data(self.data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"][value]["Too_Long_Reads"])
            mapped_reads += self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["mapped_reads"].split('(')[-2])
            Umi_Filter_Reads = mapped_reads - Raw_Reads
            
            # UnMapping Data
            UnMapping += self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]) - self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["mapped_reads"].split('(')[-2])
            Clean_reads = Reference_Mapping_reads + Unmapping_Read
            Filter_reads = Umi_Filter_Reads + Too_Long_Reads + Too_Short_Reads + Low_Quality_Reads + Too_Many_N_Reads
            Barcode_Mapping = Filter_reads + Clean_reads
            #Total reads Data
            Total_reads = Barcode_Mapping + UnMapping

            # Barcode and Umi QC Data
            Q10_Barcode_rate = self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q10_bases_in_barcode"].replace('%',''))/100
            Q20_Barcode_rate = self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q20_bases_in_barcode"].replace('%',''))/100
            Q30_Barcode_rate = self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q30_bases_in_barcode"].replace('%',''))/100
            Q10_UMI_rate = self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q10_bases_in_umi"].replace('%',''))/100
            Q20_UMI_rate = self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]['Q20_bases_in_umi'].replace('%',''))/100
            Q30_UMI_rate = self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q30_bases_in_umi"].replace('%',''))/100
            
            Q10_Barcode += round(Q10_Barcode_rate*self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
            Q20_Barcode += round(Q20_Barcode_rate*self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
            Q30_Barcode += round(Q30_Barcode_rate*self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
            Q10_UMI += round(Q10_UMI_rate*self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
            Q20_UMI += round(Q20_UMI_rate*self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
            Q30_UMI += round(Q30_UMI_rate*self.tran_data(self.data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
        
        Q10_Barcode = '{}M({}%)'.format(Q10_Barcode,round(Q10_Barcode/Total_reads*100,2))
        Q20_Barcode = '{}M({}%)'.format(Q20_Barcode,round(Q20_Barcode/Total_reads*100,2))
        Q30_Barcode = '{}M({}%)'.format(Q30_Barcode,round(Q30_Barcode/Total_reads*100,2))
        Q10_UMI = '{}M({}%)'.format(Q10_UMI,round(Q10_UMI/Total_reads*100,2))
        Q20_UMI = '{}M({}%)'.format(Q20_UMI,round(Q20_UMI/Total_reads*100,2))
        Q30_UMI = '{}M({}%)'.format(Q30_UMI,round(Q30_UMI/Total_reads*100,2))

        return Total_reads,Barcode_Mapping,UnMapping,Filter_reads,Fail_Filter,Clean_reads,Umi_Filter_Reads,Too_Long_Reads,Too_Short_Reads,\
        Too_Many_N_Reads,Low_Quality_Reads,Unique_Mapped_Reads,Chimeric_Reads,Multi_Mapping_Reads,Reference_Mapping_reads,Unmapping_Read,\
        DuPlication_Reads,Unique_Reads,Contour_area,Number_of_DNB_under_tissue,Ratio,Total_Gene_type,Raw_reads,Reads_under_tissue,\
        Fraction_Reads_in_Spots_Under_Tissue,Q20_Barcode,Q30_Barcode,Q10_Barcode,Q10_UMI,Q20_UMI,Q30_UMI

    def get_dedup(self):

        DuPlication_Reads = round(Decimal(self.data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['DUPLICATION_RATE'])/100*self.tran_data(self.data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['PASS_FILTER']),2)
        Unique_Reads = Decimal(self.tran_data(self.data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['UNIQUE_READS'])).quantize(Decimal("0.00"))

        return DuPlication_Reads,Unique_Reads

    def get_binsize(self):

        if "4.TissueCut" in self.data_dict.keys():
            bin_size = [i["binSize"] for i in self.data_dict["4.TissueCut"]["4.2.TissueCut_Bin_stat"].values()]
        elif "3.Basic" in self.data_dict.keys():
            bin_size = [i["Bin_Size"].split('x')[0] for i in self.data_dict["3.Basic"]["3.2.Bin"].values()]
        if bin_size[0] == '1':
            bin_size[0] = '20'

        return bin_size