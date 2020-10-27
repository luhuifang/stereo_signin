import json
import dash

from decimal import Decimal

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from spatialTrancriptomeReport import app
from apps.data.load_json import data_json,df_table
from apps.data.disposal_sun_data import get_sun_fig




def tran_data(data):
    if 'K' in data:
        return Decimal(float(data.strip('K'))/1000).quantize(Decimal("0.00"))
    elif 'M' in data:
        return Decimal(float(data.strip('M'))).quantize(Decimal("0.00"))
    else:
        return Decimal(float(data)).quantize(Decimal("0.00"))

layout = html.Div(children=[
        dbc.Navbar([
            dbc.Row([
                html.A(
                dbc.Row(
                [
                    dbc.Col(html.Img(src='./apps/data/icon.png', height="30px")),
                    dbc.Col(dbc.NavbarBrand("Stereo", className="ml-3 text-center")),
                ],
                align="center",
                no_gutters=True,
                ),
            href="#",
            ),])],
            color='#153057',
            dark=True,
            ),
        html.Div(className='container',children=[
            html.Div(className='row',children=[
                html.H1('sampleA')
            ]),
            html.Div(className='row',children=[
                html.Div(className='col-md-12',children=[
                    html.Div(className='card-body',children=[
                        html.Div(className='row',children=[
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'mapped_reads', className="card-title text-center text-green"),
                                        html.P("Raw Reads",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'clean_reads', className="card-title text-center text-green"),
                                        html.P("Barcode Mapping",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'mapped_reads1', className="card-title text-center text-green"),
                                        html.P("Clean Reads ",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'clean_reads1', className="card-title text-center text-green"),
                                        html.P("Reference Mapping",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'mapped_reads1', className="card-title text-center text-green"),
                                        html.P("Deduplication",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'clean_reads1', className="card-title text-center text-green"),
                                        html.P("Uniquely Reads",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            ]),
                        html.Div(className='row',children=[
                            html.Div(className='col-md-12',children=[
                                dcc.Dropdown(
                                    id="Sample_dropdown",
                                    options=[{'label':i["Sample_id"],'value':i["Sample_id"]} for i in data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"]],
                                    placeholder='Select the sample',
                                    persistence=False,
                                    searchable=False,
                                    clearable=False,
                                    multi=True,
                                    value= [i["Sample_id"] for i in data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"]],
                                    )
                                ]),
                            ]),
            html.Div(className='row',children=[
                html.Div(className='col-md-4 box-style-left',children=[
                dbc.Table(children = [
                    html.Thead(html.Tr([html.Th([html.H4(["Adapter Filter",
                        dbc.Badge(children=[
                            dbc.Button(
                                "?",
                                id="collapse-button-1",
                                color='light',
                                className='button-style'
                                ),
                            
                        ], color="light",pill=True, className="ml-1 badge-style")])])])),
                    dbc.Collapse(
                                dbc.Card(dbc.CardBody([
                                    html.H4("Number of Reads", className="card-title"),
                                    html.P("Total number of sequencing reads. ",className="text-P"),
                                    html.H4("Types of Usable Barcode", className="card-title"),
                                    html.P("Types of usable barcode on the first-time sequenced debris. ",className=" text-P"),
                                    html.H4("Fixed Sequence Contianing Reads", className="card-title"),
                                    html.P("Number of reads filtered with adapter(TGCCTCTCAG). ",className="text-P"),
                                    html.H4("Barcode misOverlap Reads", className="card-title"),
                                    html.P("Number and ratio of reads that can be mapped back to the first-time sequenced barcode after the fault tolerance(1bp) within a Nucleobase. ",className="text-P"),
                                    html.H4("Barcode withN Reads", className="card-title"),
                                    html.P("Number and ratio of reads that can be mapped back to the first-time sequenced barcode after the 'N' in the barcode is replaced to one of the ATCG. ",className="text-P"),
                                    html.H4("Q30 Bases in Barcode", className="card-title"),
                                    html.P("Ratio of bases whose quality value exceeds Q30 in barcode. ",className=" text-P"),
                                    html.H4("Q30 Bases in UMI", className="card-title"),
                                    html.P("Ratio of bases whose quality value exceeds Q30 in UMI. ",className="text-P"),
                                    ])),id="collapse-1",className='collapse-type'),
                    html.Tbody([
                        html.Tr([html.Td([html.P("Q10 Bases in Barcode",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Q10_Barcode')])]), 
                        html.Tr([html.Td([html.P("Q20 Bases in Barcode",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Q20_Barcode')])]), 
                        html.Tr([html.Td([html.P("Q30 Bases in Barcode",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Q30_Barcode')])]),
                        html.Tr([html.Td([html.P("Q10 Bases in UMI",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Q10_UMI')])]), 
                        html.Tr([html.Td([html.P("Q20 Bases in UMI",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Q20_UMI')])]), 
                        html.Tr([html.Td([html.P("Q30 Bases in UMI",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Q30_UMI')])]),                       
                        ])], bordered=True,className='card-mid'),
                
                ]),
                html.Div(className='col-md-8 box-style-right',children=[
                    dbc.Card(
                        dbc.CardBody([
                            html.Div(className='collapse-type',children=[
                                dcc.Graph(
                                        id='example-graph-2',
                                        figure=get_sun_fig()
                                    )])
                            ]),className='card-big'
                        ),
                    
                        ]),
                    
                        html.Div(className='col-md-4 box-style-left',children=[
                            dbc.Table(children = [
                                html.Thead(html.Tr([html.Th([html.H4(["TissueCut Total Stat",
                                    dbc.Badge(children=[
                                        dbc.Button(
                                            "?",
                                            id="collapse-button-2",
                                            color='light',
                                            className='button-style'
                                            ),
                                        
                                    ], color="light",pill=True, className="ml-1 badge-style")])])])),
                                dbc.Collapse(
                                            dbc.Card(dbc.CardBody([
                                                html.H4("Raw Reads", className="card-title"),
                                                html.P("Number of reads of input data( After filtering adapters). ",className="card-text text-P"),
                                                html.H4("Low Quality Reads", className="card-title"),
                                                html.P("Number of reads filtered due to low quality.",className="card-text text-P"),
                                                html.H4("Too Many N Reads", className="card-title"),
                                                html.P("Number of reads filtered that contain too many N. ",className="card-text text-P"),
                                                html.H4("Too Short Reads", className="card-title"),
                                                html.P("Number of reads filtered which too short. ",className="card-text text-P"),
                                                html.H4("Too Long Reads", className="card-title"),
                                                html.P("Number of reads filtered with too long.",className="card-text text-P"),
                                                ])),id="collapse-2",),
                                html.Tbody([
                                    html.Tr([html.Td([html.P("Contour_area",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Contour_area')])]), 
                                    html.Tr([html.Td([html.P("Number_of_DNB_under_tissue",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Number_of_DNB_under_tissue')])]), 
                                    html.Tr([html.Td([html.P("Ratio",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Ratio')])]), 
                                    html.Tr([html.Td([html.P("Total_Gene_type",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Total_Gene_type')])]), 
                                    html.Tr([html.Td([html.P("Raw_reads",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Raw_Reads')])]),
                                    html.Tr([html.Td([html.P("Reads_under_tissue",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Reads_under_tissue')])]), 
                                    html.Tr([html.Td([html.P("Fraction_Reads_in_Spots_Under_Tissue",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Fraction_Reads_in_Spots_Under_Tissue')])]),                        
                                    ])], bordered=True,className='card-mid'), 
                            ]),
                            html.Div(className='col-md-8 box-style-right',children=[
                                dbc.Table.from_dataframe(df_table.T,
                                    striped=True, hover=True,className='card-mid text-center')
                            ])
                        ]),                            
                    ]),
                ])
            ]),
        ])
    ])


@app.callback(
    Output("collapse-1", "is_open"),
    [Input("collapse-button-1", "n_clicks")],
    [State("collapse-1", "is_open")],
)
def toggle_collapse_1(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-2", "is_open"),
    [Input("collapse-button-2", "n_clicks")],
    [State("collapse-2", "is_open")],
)
def toggle_collapse_2(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    [Output('mapped_reads','children'),
    Output('clean_reads','children'),
    Output('Q20_Barcode','children'),
    Output('Q30_Barcode','children'),
    Output('Q30_UMI','children'),
    Output('Q10_Barcode','children'),
    Output('Q10_UMI','children'),
    Output('Q20_UMI','children'),
    Output('Raw_Reads','children'),
    Output('Contour_area','children'),
    Output('Reads_under_tissue','children'),
    Output('Number_of_DNB_under_tissue','children'),
    Output('Ratio','children'),
    Output('Total_Gene_type','children'),
    Output('Fraction_Reads_in_Spots_Under_Tissue','children')],
    [Input('Sample_dropdown','value')]
    )
def data_set(values):
    unique_reads = data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["UNIQUE_READS"]
    Duplication_rate = data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["DUPLICATION_RATE"]
    Contour_area = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Contour_area']
    Number_of_DNB_under_tissue = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Number_of_DNB_under_tissue']
    Ratio = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Ratio']
    Total_Gene_type = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Total_Gene_type']
    Raw_Reads = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Raw_reads']
    Reads_under_tissue = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Reads_under_tissue']
    Fraction_Reads_in_Spots_Under_Tissue = data_json["4.TissueCut"]["4.1.TissueCut_Total_Stat"][0]['Fraction_Reads_in_Spots_Under_Tissue']
    mapped_reads,clean_reads,Q20_Barcode,Q30_Barcode,Q30_UMI,Q10_Barcode,Q10_UMI,Q20_UMI=0,0,0,0,0,0,0,0
    if values:
        for value in values:
            for i in data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"]:
                if i["Sample_id"] == value:
                    mapped_reads += tran_data(i["mapped_reads"].split('(')[-2])
                    Q20_Barcode = i["Q20_bases_in_barcode"]
                    Q30_Barcode = i["Q30_bases_in_barcode"]
                    Q30_UMI = i["Q30_bases_in_umi"]
                    Q10_Barcode = i["Q10_bases_in_barcode"]
                    Q10_UMI = i["Q10_bases_in_umi"]
                    Q20_UMI = i['Q20_bases_in_umi']
            for i in data_json["1.Filter_and_Map"]["1.2.Filter_Stat"]:
                if i["Sample_Name"] == value:
                    clean_reads += tran_data(i["Clean_Reads"])
            for i in data_json["2.Alignment"]["2.2.Uniquely_Mapped_Read"]:
                if i["Sample_Id"] == value:
                    mapped_reads_ali = i["Mapped_Reads(%)"]
        return mapped_reads,clean_reads,Q20_Barcode,Q30_Barcode,Q30_UMI,Q10_Barcode,Q10_UMI,\
    Q20_UMI,Raw_Reads,Contour_area,Reads_under_tissue,Number_of_DNB_under_tissue,Ratio,Total_Gene_type,\
    Fraction_Reads_in_Spots_Under_Tissue
    else:
        return '','','','','','','','','','','','','','',''
    