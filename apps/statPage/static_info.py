SPOT_SUMMARY_COLLAPSE=[
    {'title':"Contour area", 'content':"Contour area"},
    {'title':"Number of DNB under tissue", 'content':"Number of DNB in tissue area"},
    {'title':"Total Gene type", 'content':"Total gene types in contour area"},
    {'title':"UMI under tissue", 'content': 'Number of UMI in tissue area'},
    {'title':"Reads under tissue", 'content': "Number of Reads in tissue area"},
    {'title':"Fraction Reads in Spots Under Tissue", 'content':"Fraction Reads in tissue area"},
]

SPOT_SUMMARY_FIELD = [
    {'label': "Contour area", 'id':'Contour_area'},
    {'label': "Number of DNB under tissue", 'id':'Number_of_DNB_under_tissue'},
    {'label': "Ratio", 'id':'Ratio'},
    {'label': "Total Gene type", 'id': 'Total_Gene_type'},
    {'label': "UMI under tissue", 'id':'Umi_counts'},
    {'label': "Reads under tissue", 'id':'Reads_under_tissue'},
    {'label': "Fraction Reads in Spots Under Tissue", 'id':'Fraction_Reads_in_Spots_Under_Tissue'},
]

BIN_SUMMARY_COLLAPSE=[
    {'title':"Total_Umi_Mapping_To_Gene_And_slide", 'content':"Total number of UMIs mapped to gene region"},
    {'title':"Gene_Number", 'content':"Number of types of genes that captured"},
    {'title':"Number_Of_DNB_With_Reads", 'content':"Number of DNB that captured mRNA"},
    {'title':"Slide_Area", 'content':"Area of debris"},
    {'title':"Density_Of_DNB", 'content':"Ratio of mRNA and DNB that are captured(Number_Of_DNB_With_Reads/Slide_Area*100)"},
]

BIN_SUMMARY_FIELD = [
    {'label': "Total Umi Mapping To Gene And slide", 'id':'Total_Umi_Mapping_To_Gene_And_slide'},
    {'label': "Gene Number", 'id':'Gene_Number'},
    {'label': "Number Of DNB With Reads", 'id':'Number_Of_DNB_With_Reads'},
    {'label': "Slide Area", 'id':'Slide_Area'},
    {'label': "Density Of DNB", 'id':'Density_Of_DNB'}
]

CELLCUT_TOTAL_STAT_COLLAPSE =[
    {'content': "Total Contour Area", 'title':'Total_contour_area'},
    {'content': "Number of DNB Under Cell", 'title':'Number_of_DNB_under_cell'},
    {'content': "Ratio", 'title':'Ratio'},
    {'content': "Total Gene type", 'title':'Total_Gene_type'},
    {'content': "Total Umi Under Cell", 'title':'Total_umi_under_cell'},
    {'content': "Reads Under Cell", 'title':'Reads_under_cell'},
    {'content': "Fraction Reads in Spots Under Tissue", 'title':'Fraction_Reads_in_Spots_Under_Tissue'}
]

CELLCUT_TOTAL_STAT_FIELD =[
    {'label': "Total Contour Area", 'id':'Total_contour_area'},
    {'label': "Number of DNB Under Cell", 'id':'Number_of_DNB_under_cell'},
    {'label': "Ratio", 'id':'Ratio'},
    {'label': "Total Gene type", 'id':'Total_Gene_type'},
    {'label': "Total Umi Under Cell", 'id':'Total_umi_under_cell'},
    {'label': "Reads Under Cell", 'id':'Reads_under_cell'},
    {'label': "Fraction Reads in Spots Under Tissue", 'id':'Fraction_Reads_in_Spots_Under_Tissue'}
]

CELLCUT_BIN_STAT_COLLAPSE =[
    {'content': "Total Cell Count", 'title':'Total_cell_count'},
    {'content': "Mean Reads", 'title':'Mean_reads'},
    {'content': "Median Reads", 'title':'Median_reads'},
    {'content': "Mean Gene Type Per Cell", 'title':'Mean_Gene_type_per_cell'},
    {'content': "Median Gene Type Per Cell", 'title':'Median_Gene_type_per_cell'},
    {'content': "Mean MID Per Cell", 'title':'Mean_MID_per_cell'},
    {'content': "Median MID Per Cell", 'title':'Median_MID_per_cell'},
    {'content': "Mean Cell Area", 'title':'Mean_cell_area'},
    {'content': "Mean DNB Per Cell", 'title':'Mean_DNB_per_cell'},
    {'content': "Median DNB Per Cell", 'title':'Median_DNB_per_cell'}
]

CELLCUT_BIN_STAT_FIELD =[
    {'label': "Total Cell Count", 'id':'Total_cell_count'},
    {'label': "Mean Reads", 'id':'Mean_reads'},
    {'label': "Median Reads", 'id':'Median_reads'},
    {'label': "Mean Gene Type Per Cell", 'id':'Mean_Gene_type_per_cell'},
    {'label': "Median Gene Type Per Cell", 'id':'Median_Gene_type_per_cell'},
    {'label': "Mean MID Per Cell", 'id':'Mean_MID_per_cell'},
    {'label': "Median MID Per Cell", 'id':'Median_MID_per_cell'},
    {'label': "Mean Cell Area", 'id':'Mean_cell_area'},
    {'label': "Mean DNB Per Cell", 'id':'Mean_DNB_per_cell'},
    {'label': "Median DNB Per Cell", 'id':'Median_DNB_per_cell'}
]

QUALITY_COLLAPSE = [
    {'title':"Q10 Bases in Barcode",  'content': "Ratio of bases whose quality value exceeds Q10 in barcode. "},
    {'title':"Q20 Bases in Barcode",  'content': "Ratio of bases whose quality value exceeds Q20 in barcode. "},
    {'title':"Q30 Bases in Barcode",  'content': "Ratio of bases whose quality value exceeds Q30 in barcode. "},
    {'title':"Q10 Bases in UMI",  'content': "Ratio of bases whose quality value exceeds Q10 in UMI. "},
    {'title':"Q20 Bases in UMI",  'content': "Ratio of bases whose quality value exceeds Q20 in UMI. "},
    {'title':"Q30 Bases in UMI",  'content': "Ratio of bases whose quality value exceeds Q30 in UMI. "},
]
QUALITY_FIELD = [
    {'label': "Total Reads", 'id':'Total_Reads'},
    {'label': "Q30 Bases in Barcode", 'id':'Q30_Barcode'},
    {'label': "Q30 Bases in UMI", 'id':'Q30_UMI'},
    {'label': "Q30 Bases in Reads", 'id':'Q30_Reads'},
]
IMPORTANT_FIELD = [
    {'id' : 'raw_reads', 'label' : "Total Reads"},
    {'id' : 'mapped_reads', 'label' : "Barcode Mapping"},
    {'id' : 'clean_reads', 'label' : "Clean Reads"},
    {'id' : 'reference_mapping_reads', 'label' :"Reference Mapping"},
    {'id' : 'uniquely_reads', 'label' :"Uniquely Reads"},
]
RNA_MAPPING_COLLAPSE = [
    {'content' : 'Input_read', 'title' : "Input Read"},
    {'content' : 'Uniquely_Mapped_Read', 'title' : "Uniquely Mapped Read"},
    {'content' : 'Multi_Mapping_Read', 'title' : "Multi Mapping Read"},
    {'content' : 'RNA_Unmapping_Read', 'title' :"RNA Unmapping Read"},
    {'content' : 'Chimeric_Read', 'title' :"Chimeric Read"},
]
RNA_MAPPING_FIELD = [
    {'id' : 'Input_read', 'label' : "Input Read"},
    {'id' : 'Uniquely_Mapped_Read', 'label' : "Uniquely Mapped Read"},
    {'id' : 'Multi_Mapping_Read', 'label' : "Multi Mapping Read"},
    {'id' : 'RNA_Unmapping_Read', 'label' :"RNA Unmapping Read"},
    {'id' : 'Chimeric_Read', 'label' :"Chimeric Read"},
]
ANNOTATION_COLLAPSE = [
    {'content' : 'Exonic', 'title' : "Exonic"},
    {'content' : 'Intronic', 'title' : "Intronic"},
    {'content' : 'Intergenic', 'title' : "Intergenic"},
    {'content' : 'Transcriotome', 'title' :"Transcriotome"},
    {'content' : 'Antisense', 'title' :"Antisense"},
]
ANNOTATION_FIELD = [
    {'id' : 'Exonic', 'label' : "Exonic"},
    {'id' : 'Intronic', 'label' : "Intronic"},
    {'id' : 'Intergenic', 'label' : "Intergenic"},
    {'id' : 'Transcriotome', 'label' :"Transcriotome"},
    {'id' : 'Antisense', 'label' :"Antisense"},
]

labels_color = {'Total_reads':'#F0FFFF','Barcode_Mapping':'Total_reads','UnMapping':'Total_reads','Filter_reads':'Barcode_Mapping',
    'Clean_reads':'Barcode_Mapping', 'Umi_Filter_Reads':'Filter_reads','Too_Long_Reads':'Filter_reads',
    'Too_Short_Reads':'Filter_reads','Too_Many_N_Reads':'Filter_reads','Low_Quality_Reads':'Filter_reads',
    'Reference_Mapping_reads':'Clean_reads','Unmapping_Read':'Clean_reads','DuPlication_Reads':'Reference_Mapping_reads',
    'Fail_Filter':'Reference_Mapping_reads','Unique_Reads':'Reference_Mapping_reads'
}

hovertext_dict = {'Total_reads':'Total number of sequencing reads',
    'Barcode_Mapping':'Number and ratio of reads in the <br>second-time sequenced barcode that can <br>be mapped back to the first-time sequenced barcode, <br>including mapped reads after fault tolerance.<br>( Ratio = Barcode Mapping / Total reads)',
    'UnMapping':'Second sequencing cannot map back <br>the number of reads from the first time.<br>(Ratio = UnMapping / Total reads)',
    'Filter_reads':'Number of filter reads after quality control. <br>(Ratio = Filter reads / Barcode Mapping)',
    'Clean_reads':'Number of reads after quality control. <br>(Ratio = Clean reads / Barcode Mapping)', 
    'Umi_Filter_Reads':'Number of reads filtered with umi, <br>including : umi_with_N_reads , umi_with_polyA_reads , umi_with_low_quality_base_reads. <br>( Ratio = Umi Filter Reads/ Filter reads)',
    'Too_Long_Reads':'Number of reads filtered with too long.<br>(Ratio = Too Long Reads / Filter reads)',
    'Too_Short_Reads':'Number of reads filtered which too short.<br>(Ratio = Too Short Reads / Filter reads)',
    'Too_Many_N_Reads':'Number of reads filtered that contain too many N.<br>(Ratio = Too Many N Reads / Filter reads)',
    'Low_Quality_Reads':'Number of reads filtered due to low quality.<br>(Ratio = Low Quality Reads / Filter reads)',
    'Unique_Mapped_Reads':'Number of reads that are only one matching record on the reference. <br>(Ratio = Unique Mapped Reads / Clean reads)',
    'Chimeric_Reads':'Chimeric reads occur when one sequencing read aligns to <br>two distinct portions of the genome with little or no overlap. <br>Chimeric reads are indicative of structural variation or fusion.<br>(Ratio = Chimeric Reads / Clean reads)',
    'Multi_Mapping_Reads':'Number of reads that are more than one matching record on the reference. <br>(Ratio = Multi Mapping Reads / Clean reads)',
    'Unmapping_Read':'Number of reads there are not matching on the reference.<br>(Ratio = UnMapping Reads/ Clean reads)',
    'DuPlication_Reads':'The same DNA fragment occurs and is sequenced twice.<br>(Ratio = DuPlication Reads / Unique Mapped Reads)',
    'Unique_Reads':'The same DNA fragment occurs and is sequenced only once.<br>(Ratio = Unique Reads/ Unique Mapped Reads)'
}

parents_dict = {'Total_reads':'','Barcode_Mapping':'Total_reads','UnMapping':'Total_reads',
    'Umi_Filter_Reads':'Total_reads','Clean_reads':'Barcode_Mapping', 
    'Too_Long_Reads':'Barcode_Mapping','Too_Short_Reads':'Barcode_Mapping','Too_Many_N_Reads':'Barcode_Mapping',
    'Low_Quality_Reads':'Barcode_Mapping','Unique_Mapped_Reads':'Clean_reads','Chimeric_Reads':'Clean_reads',
    'Multi_Mapping_Reads':'Clean_reads','Unmapping_Read':'Clean_reads','DuPlication_Reads':'Unique_Mapped_Reads',
    'Unique_Reads':'Unique_Mapped_Reads'
}

parents_dict_sort = {'Total_reads':'','Barcode_Mapping':'Total_reads','UnMapping':'Total_reads',
    'Umi_Filter_Reads':'Total_reads','Clean_reads':'Barcode_Mapping', 
    'Too_Long_Reads':'Barcode_Mapping','Too_Short_Reads':'Barcode_Mapping','Too_Many_N_Reads':'Barcode_Mapping',
    'Low_Quality_Reads':'Barcode_Mapping','Unique_Mapped_Reads':'Clean_reads','Chimeric_Reads':'Clean_reads',
    'Multi_Mapping_Reads':'Clean_reads','Unmapping_Read':'Clean_reads'
}
