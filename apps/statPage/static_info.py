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

QUALITY_COLLAPSE = [
    {'title':"Q10 Bases in Barcode",  'content': "Ratio of bases whose quality value exceeds Q10 in barcode. "},
    {'title':"Q20 Bases in Barcode",  'content': "Ratio of bases whose quality value exceeds Q20 in barcode. "},
    {'title':"Q30 Bases in Barcode",  'content': "Ratio of bases whose quality value exceeds Q30 in barcode. "},
    {'title':"Q10 Bases in UMI",  'content': "Ratio of bases whose quality value exceeds Q10 in UMI. "},
    {'title':"Q20 Bases in UMI",  'content': "Ratio of bases whose quality value exceeds Q20 in UMI. "},
    {'title':"Q30 Bases in UMI",  'content': "Ratio of bases whose quality value exceeds Q30 in UMI. "},
]
QUALITY_FIELD = [
    {'label': "Q10 Bases in Barcode", 'id':'Q10_Barcode'},
    {'label': "Q20 Bases in Barcode", 'id':'Q20_Barcode'},
    {'label': "Q30 Bases in Barcode", 'id':'Q30_Barcode'},
    {'label': "Q10 Bases in UMI", 'id':'Q10_UMI'},
    {'label': "Q20 Bases in UMI", 'id':'Q20_UMI'},
    {'label': "Q30 Bases in UMI", 'id':'Q30_UMI'},
]
IMPORTANT_FIELD = [
    {'id' : 'raw_reads', 'label' : "Total Reads"},
    {'id' : 'mapped_reads', 'label' : "Barcode Mapping"},
    {'id' : 'clean_reads', 'label' : "Clean Reads"},
    {'id' : 'reference_mapping_reads', 'label' :"Reference Mapping"},
    {'id' : 'uniquely_reads', 'label' :"Uniquely Reads"},
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
    'Filter_reads':'Barcode_Mapping','Clean_reads':'Barcode_Mapping', 'Umi_Filter_Reads':'Filter_reads',
    'Too_Long_Reads':'Filter_reads','Too_Short_Reads':'Filter_reads','Too_Many_N_Reads':'Filter_reads',
    'Low_Quality_Reads':'Filter_reads','Unique_Mapped_Reads':'Clean_reads','Chimeric_Reads':'Clean_reads',
    'Multi_Mapping_Reads':'Clean_reads','Unmapping_Read':'Clean_reads','DuPlication_Reads':'Unique_Mapped_Reads',
    'Unique_Reads':'Unique_Mapped_Reads'
}

parents_dict_sort = {'Total_reads':'','Barcode_Mapping':'Total_reads','UnMapping':'Total_reads',
    'Filter_reads':'Barcode_Mapping','Clean_reads':'Barcode_Mapping', 'Umi_Filter_Reads':'Filter_reads',
    'Too_Long_Reads':'Filter_reads','Too_Short_Reads':'Filter_reads','Too_Many_N_Reads':'Filter_reads',
    'Low_Quality_Reads':'Filter_reads','Unique_Mapped_Reads':'Clean_reads','Chimeric_Reads':'Clean_reads',
    'Multi_Mapping_Reads':'Clean_reads','Unmapping_Read':'Clean_reads'
}
