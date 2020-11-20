import os
import re
import json
import pandas as pd

from decimal import Decimal
from apps.statPage.utils import get_file_list


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

def tran_data(data):
    prefix = {'K': 1000, 'M': 1000000, 'G': 1000000000, 'T': 1000000000000, 'P': 1000000000000000, 'E': 1000000000000000000, 'Z': 1000000000000000000000, 'Y': 1000000000000000000000000}
    if is_number(data):
        return Decimal(float(data))
    else:
        symbol = data[-1]
        number = eval(data[:-1])
        return Decimal(number*prefix[symbol])
        
def number2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {'K': 1000, 'M': 1000000, 'G': 1000000000, 'T': 1000000000000, 'P': 1000000000000000, 'E': 1000000000000000000, 'Z': 1000000000000000000000, 'Y': 1000000000000000000000000}
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.2f%s' % (value,s)
    return '%s' % n

'''
def tran_data(data):
    if 'K' in data:
        return Decimal(float(data.strip('K'))/1000).quantize(Decimal("0.00"))
    elif 'M' in data:
        return Decimal(float(data.strip('M'))).quantize(Decimal("0.00"))
    else:
        return Decimal(float(data)).quantize(Decimal("0.00"))
'''

class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()    # retain local pointer to value
        return value                        # faster to return than dict lookup

class LoadStatJson(object):
    def __init__(self, file_dir):
        self.data_json = self.readStatJson(file_dir)

    def readStatJson(self, file_dir):
        f = os.path.join(file_dir, 'new_final_result.json')
        with open(f,'r') as read_json:
            data_json = json.load(read_json)
        return data_json

    def getDfTable(self, data_json):
        if '4.TissueCut' in data_json:
            df_table = pd.DataFrame(
                    [list(i.values()) for i in data_json["4.TissueCut"]["4.2.TissueCut_Bin_stat"]]  
                )
            df_table.columns = ['binSize', 'MeanReads', 'MedianReads', 'MeanGeneType', 'MedianGeneType', 'MeanUmi', 'MedianUmi']
        elif '3.Basic' in data_json:
            df_table = pd.DataFrame(
                    [list(i.values()) for i in data_json["3.Basic"]["3.2.Bin"]]  
                )
            df_table.columns = ['binSize', 'FilterMiniUmi', 'BinNumbers', 'GeneNumbers', 'UmiCounts/Bin', 'GeneCounts/Bin']
        else:
            df_table = pd.DataFrame()
        return df_table
    
    def getSpotSummary(self, data_json):
        flag = 'None'
        spot_summary = []
        if '4.TissueCut' in data_json:
            spot_summary = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]
            flag = '4'
        elif '3.Basic' in data_json:
            spot_summary = data_json["3.Basic"]["3.1.Get_Exp"][0]
            flag = '3'
        return flag, spot_summary
    
    def IsCell(self, data_json):
        is_cell = 'None'
        total_stat_summary = []
        bin_stat_summary = []
        if '4.TissueCut' in data_json:
            is_cell = False
        elif '4.CellCut' in data_json:
            is_cell = True
            total_stat_summary = data_json["4.CellCut"]["4.1.CellCut_Total_Stat"][0]
            bin_stat_summary = data_json["4.CellCut"]["4.3.CellCut_Bin_stat"][0]
        return is_cell,total_stat_summary, bin_stat_summary

    def getDataDict(self, data_json):
        data_dict = Vividict()
        sample_count = Vividict()
        for k1,v1 in data_json.items():
            for k2,v2 in v1.items():
                count = 0
                for i in v2:
                    sample_id = count
                    if "Sample_id" in i.keys():
                        sample_id = i["Sample_id"]
                    elif "Sample_Name" in i.keys():
                        sample_id = i["Sample_Name"]
                    elif "Sample_Id" in i.keys():
                        sample_id = i["Sample_Id"]
                    if sample_id not in data_dict[k1][k2]:
                        sample_count[k1][k2][sample_id] = 0
                    else:
                        sample_count[k1][k2][sample_id] += 1
                        sample_id = '{0}_{1}'.format(sample_id, sample_count[k1][k2][sample_id])
                        
                    data_dict[k1][k2][sample_id] = i
                    count += 1
        return data_dict
    
    def getReadsStatData(self, samples):
        data_dict = self.getDataDict(self.data_json)

        Q10_Barcode,Q20_Barcode,Q30_Barcode,Q10_UMI,Q20_UMI,Q30_UMI = 0, 0, 0, 0, 0, 0

        Total_reads, Barcode_Mapping, UnMapping, Clean_reads, Filter_reads, Reference_Mapping_reads, \
        Unique_Mapped_Reads, Multi_Mapping_Reads, Chimeric_Reads, Unmapping_Read, Umi_Filter_Reads, \
        Too_Short_Reads, Too_Long_Reads, Too_Many_N_Reads, Low_Quality_Reads, DuPlication_Reads, \
        Unique_Reads, Fail_Filter, Raw_Reads, mapped_reads = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

        Input_read, Uniquely_Mapped_Read, Multi_Mapping_Read, RNA_Unmapping_Read, Chimeric_Read= 0,0,0,0,0

        for value in samples:
            
            # Clean Reads Data
            # mapping reads
            Unique_Mapped_Reads += tran_data(data_dict["2.Alignment"]["2.2.Uniquely_Mapped_Read"][value]['Mapped_Reads_Number']) 
            Multi_Mapping_Reads += tran_data(data_dict["2.Alignment"]["2.3.Multi_Mapping_Read"][value]['Multiple_Loci'].split('(')[-2]) 
            Chimeric_Reads += tran_data(data_dict["2.Alignment"]["2.5.Chimeric_Read"][value]['Number_Of_Chimeric_Reads'].split('(')[-2]) 
            Reference_Mapping_reads = round(Unique_Mapped_Reads + Multi_Mapping_Reads + Chimeric_Reads,2)
            # Unmaping reads
            #Unmapping_RATE = round(Decimal(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Too_Many_Mismatches"].split('(')[-1].strip('%)'))/100 + Decimal(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Too_Short"].split('(')[-1].strip('%)'))/100 + Decimal(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Other"].split('(')[-1].strip('%)'))/100,2)
            Clean_reads += tran_data(data_dict["2.Alignment"]["2.1.Input_Read"][value]["Number_Of_Input_Reads"])
            Unmapping_Read = round(Clean_reads-Reference_Mapping_reads, 2)

            # Filter and deduplication
            # Pass Filter Data
            Unique_Reads = Decimal(tran_data(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['UNIQUE_READS'])).quantize(Decimal("0.00"))
            DuPlication_Reads = round(Unique_Mapped_Reads-Unique_Reads,2)
        
            # Fail Filter Data
            Fail_Filter = round(Reference_Mapping_reads - Unique_Reads - DuPlication_Reads, 2)
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
            #Filter_reads = Umi_Filter_Reads + Too_Long_Reads + Too_Short_Reads + Low_Quality_Reads + Too_Many_N_Reads
            Filter_reads = Too_Long_Reads + Too_Short_Reads + Low_Quality_Reads + Too_Many_N_Reads
            # print(Filter_reads , Umi_Filter_Reads , Too_Long_Reads , Too_Short_Reads , Low_Quality_Reads , Too_Many_N_Reads)
            Barcode_Mapping = Filter_reads + Clean_reads
            
            #Total reads Data
            #Total_reads = Barcode_Mapping + UnMapping
            Total_reads = Barcode_Mapping + UnMapping + Umi_Filter_Reads

            # Barcode and Umi QC Data
            Q10_Barcode_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q10_bases_in_barcode"].replace('%',''))/100
            Q20_Barcode_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q20_bases_in_barcode"].replace('%',''))/100
            Q30_Barcode_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q30_bases_in_barcode"].replace('%',''))/100
            Q10_UMI_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q10_bases_in_MID"].replace('%',''))/100
            Q20_UMI_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]['Q20_bases_in_MID'].replace('%',''))/100
            Q30_UMI_rate = tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["Q30_bases_in_MID"].replace('%',''))/100
            
            Q10_Barcode += round(Q10_Barcode_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
            Q20_Barcode += round(Q20_Barcode_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
            Q30_Barcode += round(Q30_Barcode_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
            Q10_UMI += round(Q10_UMI_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
            Q20_UMI += round(Q20_UMI_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)
            Q30_UMI += round(Q30_UMI_rate*tran_data(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"][value]["total_reads"]),2)

            # RNA mapping Data
            Input_read += tran_data(data_dict["2.Alignment"]["2.1.Input_Read"][value]["Number_Of_Input_Reads"])
            Uniquely_Mapped_Read += tran_data(data_dict["2.Alignment"]["2.2.Uniquely_Mapped_Read"][value]["Mapped_Reads_Number"])
            Multi_Mapping_Read += tran_data(data_dict["2.Alignment"]["2.3.Multi_Mapping_Read"][value]["Multiple_Loci"].split('(')[0]) + tran_data(data_dict["2.Alignment"]["2.3.Multi_Mapping_Read"][value]["Many_Loci"].split('(')[0])
            RNA_Unmapping_Read += tran_data(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Too_Many_Mismatches"].split('(')[0]) + tran_data(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Too_Short"].split('(')[0]) + tran_data(data_dict["2.Alignment"]["2.4.Unmapping_Read"][value]["Other"].split('(')[0])
            Chimeric_Read += tran_data(data_dict["2.Alignment"]["2.5.Chimeric_Read"][value]["Number_Of_Chimeric_Reads"].split('(')[0])

        # Annotation Data
        Exonic = tran_data(data_dict["2.Alignment"]["2.7.Annotation"][0]["EXONIC"].split('(')[0])
        Intronic = tran_data(data_dict["2.Alignment"]["2.7.Annotation"][0]["INTRONIC"].split('(')[0])
        Intergenic = tran_data(data_dict["2.Alignment"]["2.7.Annotation"][0]["INTERGENIC"].split('(')[0])
        Transcriotome = tran_data(data_dict["2.Alignment"]["2.7.Annotation"][0]["TRANSCRIPTOME"].split('(')[0])
        Antisense = tran_data(data_dict["2.Alignment"]["2.7.Annotation"][0]["ANTISENSE"].split('(')[0])
        
        print(Input_read, Uniquely_Mapped_Read, Multi_Mapping_Read, RNA_Unmapping_Read, Chimeric_Read)
        Q10_Barcode = '{}({}%)'.format(number2human(Q10_Barcode),round(Q10_Barcode/Total_reads*100,2))
        Q20_Barcode = '{}({}%)'.format(number2human(Q20_Barcode),round(Q20_Barcode/Total_reads*100,2))
        Q30_Barcode = '{}({}%)'.format(number2human(Q30_Barcode),round(Q30_Barcode/Total_reads*100,2))
        Q10_UMI = '{}({}%)'.format(number2human(Q10_UMI),round(Q10_UMI/Total_reads*100,2))
        Q20_UMI = '{}({}%)'.format(number2human(Q20_UMI),round(Q20_UMI/Total_reads*100,2))
        Q30_UMI = '{}({}%)'.format(number2human(Q30_UMI),round(Q30_UMI/Total_reads*100,2))

        return Total_reads, Barcode_Mapping, UnMapping, Clean_reads, Filter_reads, Reference_Mapping_reads, \
        Unique_Mapped_Reads, Multi_Mapping_Reads, Chimeric_Reads, Unmapping_Read, Umi_Filter_Reads, \
        Too_Short_Reads, Too_Long_Reads, Too_Many_N_Reads, Low_Quality_Reads, DuPlication_Reads, \
        Unique_Reads, Fail_Filter, Raw_Reads, mapped_reads, \
        Q10_Barcode,Q20_Barcode,Q30_Barcode,Q10_UMI,Q20_UMI,Q30_UMI,\
        Exonic, Intronic, Intergenic, Transcriotome, Antisense,\
        Input_read, Uniquely_Mapped_Read, Multi_Mapping_Read, RNA_Unmapping_Read, Chimeric_Read
    
    def getDupUniqReads(self, samples):
        data_dict = self.getDataDict(self.data_json)
        DuPlication_Reads = round(Decimal(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['DUPLICATION_RATE'])/100*tran_data(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['PASS_FILTER']),2)
        Unique_Reads = Decimal(tran_data(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['UNIQUE_READS'])).quantize(Decimal("0.00"))
        return DuPlication_Reads, Unique_Reads


class LoadStatFigure(object):
    def __init__(self, file_dir):
        if not os.path.exists(file_dir):
            self.picture = []
        else:
            self.picture = get_file_list(file_dir, shuffix='png')
    
    def getPicDict(self):
        pic_dict = Vividict()
        for pic in self.picture:
            basename = os.path.basename(pic)
            pic_type, bin_size, _ = basename.split('_', 2)
            bin_x, _ = bin_size.split('x')
            pic_dict[bin_x][pic_type] = pic
        return pic_dict


# class loadSummaryInformation(object):
#     def __init__(self,file_dir):
#         file_dir = os.path.join(file_dir, 'filter')
#         self.SummaryFile = get_file_list(file_dir, shuffix='summaryReport.html')

#     def readSummaryReport(self, file_name):
#         with open(file_name,'r') as read_html:
#             summary_report = read_html.read()
#         return summary_report
    
#     def getSummaryData(self,samples):
#         Q30_Reads,Total_Reads = 0,0
#         if self.SummaryFile:
#             for each_summary_file in self.SummaryFile:
#                 summary_report = self.readSummaryReport(each_summary_file)
#                 Total_Reads += tran_data(re.search(r"\['Q30\(%\)', '(\d+(\.\d+)?)'\]",summary_report).group(1)+'M')
#                 Q30_Reads += float(re.search(r"\['TotalReads\(M\)', '(\d+(\.\d+)?)'\]",summary_report).group(1))*tran_data(re.search(r"\['Q30\(%\)', '(\d+(\.\d+)?)'\]",summary_report).group(1)+'M')/100

#         Q30_Reads = '{}({}%)'.format(number2human(Q30_Reads),round(Q30_Reads/Total_Reads*100,2))
#         return Q30_Reads,Total_Reads

