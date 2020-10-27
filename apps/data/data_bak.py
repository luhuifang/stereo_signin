import json
import dash
from decimal import Decimal

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from spatialTrancriptomeReport import app
from apps.data.load_json import data_json
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
                    dbc.Tabs(children=[
                        # table1 Filter and Map
                        dbc.Tab(children=[
                                html.Div(className='card-body',children=[
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
                                html.Div(className='col-md-6 box-style-right',children=[
                                dbc.Card(
                                    dbc.CardBody([
                                            html.H2(children = [],id = 'mapped_reads', className="card-title text-center text-green"),
                                            html.P("Reads Mapped to Genome ",className="card-text text-center"),
                                        ]),className='card-sma'
                                    ),
                                dbc.Card(
                                    dbc.CardBody([
                                            html.H2(children = [],id = 'clean_reads', className="card-title text-center text-green"),
                                            html.P("Clean Reads ",className="card-text text-center"),
                                        ]),className='card-sma'
                                    ),
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
                                        html.Tr([html.Td([html.P("Sample ID",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Sample_id')])]), 
                                        html.Tr([html.Td([html.P("Number of Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='number_reads')])]), 
                                        html.Tr([html.Td([html.P("Types of Usable Barcode",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Usable_Barcode')])]), 
                                        html.Tr([html.Td([html.P("Fixed Sequence Contianing Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='fixed_sequence_contianing_reads')])]), 
                                        html.Tr([html.Td([html.P("Barcode misOverlap Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Barcode_MisOverlap_Reads')])]),
                                        html.Tr([html.Td([html.P("Barcode withN Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='barcode_withN_reads')])]),
                                        html.Tr([html.Td([html.P("Q30 Bases in Barcode",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Q30_Barcode')])]),
                                        html.Tr([html.Td([html.P("Q30 Bases in UMI",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Q30_UMI')])]),
                                        ])], bordered=True,className='card-mid'),
                                dbc.Table(children = [
                                    html.Thead(html.Tr([html.Th([html.H4(["Filter Stat",
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
                                        html.Tr([html.Td([html.P("Raw Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Raw_Reads')])]), 
                                        html.Tr([html.Td([html.P("Low Quality Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Low_Quality_Reads')])]), 
                                        html.Tr([html.Td([html.P("Too Many N Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Too_Many_N_Reads')])]), 
                                        html.Tr([html.Td([html.P("Too Short Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Too_Short_Reads')])]), 
                                        html.Tr([html.Td([html.P("Too Long Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Too_Long_Reads')])]),
                                        ])], bordered=True,className='card-sma'),
                                ]),
                                html.Div(className='col-md-6 box-style-left',children=[
                                dbc.Card(
                                    dbc.CardBody([
                                        html.Div(className='collapse-type',children=[
                                            dcc.Graph(
                                                    id='example-graph-2',
                                                    figure=get_sun_fig()
                                                )])
                                        ]),className='card-big'
                                    ),
                                dbc.Table(children = [
                                    html.Thead(html.Tr([html.Th([html.H4(["Sample",
                                        dbc.Badge(children=[
                                            dbc.Button(
                                                "?",
                                                id="collapse-button-3",
                                                color='light',
                                                className='button-style'
                                                ),
                                            
                                        ], color="light",pill=True, className="ml-1 badge-style")])])])),
                                    dbc.Collapse(
                                                dbc.Card(dbc.CardBody([
                                                    html.H4("Number of Reads", className="card-title"),
                                                    html.P("Total number of read pairs that were assigned to this library in demultiplexing. ",className="card-text text-P"),
                                                    html.H4("Valid Barcodes", className="card-title"),
                                                    html.P("Fraction of reads with barcodes that match the whitelist after barcode correction. ",className="card-text text-P"),
                                                    html.H4("Valid UMIs", className="card-title"),
                                                    html.P("Fraction of reads with valid UMIs; i.e. UMI sequences that do not contain Ns and that are not homopolymers. ",className="card-text text-P"),
                                                    html.H4("Sequencing Saturation", className="card-title"),
                                                    html.P("The fraction of reads originating from an already-observed UMI. This is a function of library complexity and sequencing depth. More specifically, this is the fraction of confidently mapped, valid spot-barcode, valid UMI reads that had a non-unique (spot-barcode, UMI, gene). ",className="card-text text-P"),
                                                    html.H4("Q30 Bases in Barcode", className="card-title"),
                                                    html.P("Fraction of spot barcode bases with Q-score >= 30, excluding very low quality/no-call (Q <= 2) bases from the denominator. ",className="card-text text-P"),
                                                    html.H4("Q30 Bases in RNA Read", className="card-title"),
                                                    html.P("Fraction of RNA read bases with Q-score >= 30, excluding very low quality/no-call (Q <= 2) bases from the denominator. This is Read 2 for the Visium v1 chemistry.",className="card-text text-P"),
                                                    html.H4("Q30 Bases in UMI", className="card-title"),
                                                    html.P("Fraction of UMI bases with Q-score >= 30, excluding very low quality/no-call (Q <= 2) bases from the denominator. ",className="card-text text-P"),
                                                    ])),id="collapse-3",),
                                    html.Tbody([
                                        html.Tr([html.Td("Sample ID")]), 
                                        html.Tr([html.Td("Sample Description")]), 
                                        html.Tr([html.Td("Chemistry")]),
                                        html.Tr([html.Td("Slide Serial Number")]),
                                        html.Tr([html.Td("Reference Path")]),
                                        html.Tr([html.Td("Transcriptome")]),
                                        html.Tr([html.Td("Pipeline Version")]),
                                        ])], bordered=True,className='card-mid'),
                                ]),
                                ]),                            
                            ]),
                       ], label="Filter and Map"),
                        # table2 Alignment
                        dbc.Tab(children=[
                                html.Div(className='card-body',children=[
                                    html.Div(className='row',children=[
                                        html.Div(className='col-md-12',children=[
                                            dcc.Dropdown(
                                                id="Alignment_dropdown",
                                                options=[{'label':i["Sample_id"],'value':i["Sample_id"]} for i in data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"]],
                                                placeholder='Select the sample',
                                                persistence=False,
                                                searchable=False,
                                                clearable=False,
                                                value=data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"][0]["Sample_id"],
                                                )
                                            ]),
                                        ]),
                            html.Div(className='row',children=[
                                html.Div(className='col-md-6',children=[
                                dbc.Card(
                                    dbc.CardBody([
                                            html.H2(children = [],id = 'mapped_reads_ali', className="card-title text-center text-green"),
                                            html.P("Reads Mapped to Genome ",className="card-text text-center"),
                                        ]),className='card-sma'
                                    ),
                                dbc.Card(
                                    dbc.CardBody([
                                            html.H2(children = [],id = 'unique_reads', className="card-title text-center text-green"),
                                            html.P("Unique Reads ",className="card-text text-center"),
                                        ]),className='card-sma'
                                    ),
                                dbc.Card(
                                    dbc.CardBody([
                                            html.H2(children = [],id = 'Duplication_rate', className="card-title text-center text-green"),
                                            html.P("Duplication Rate ",className="card-text text-center"),
                                        ]),className='card-sma'
                                    ),
                                dbc.Table(children = [
                                    html.Thead(html.Tr([html.Th([html.H4(["Adapter Filter",
                                        dbc.Badge(children=[
                                            dbc.Button(
                                                "?",
                                                id="collapse-button-4",
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
                                                    ])),id="collapse-4",className='collapse-type'),
                                    html.Tbody([
                                        html.Tr([html.Td([html.P("Sample ID",className='col-md-8 col-sm-8 text-td'),html.P(className='col-md-4 col-sm-4 text-td text-right',id='Sample_id1')])]), 
                                        html.Tr([html.Td([html.P("Number of Reads",className='col-md-8 col-sm-8 text-td'),html.P(className='col-md-4 col-sm-4 text-td text-right',id='number_reads1')])]), 
                                        html.Tr([html.Td([html.P("Types of Usable Barcode",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Usable_Barcode1')])]), 
                                        html.Tr([html.Td([html.P("Fixed Sequence Contianing Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='1fixed_sequence_contianing_reads')])]), 
                                        html.Tr([html.Td([html.P("Barcode misOverlap Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Barcode_MisOverlap_Reads1')])]),
                                        html.Tr([html.Td([html.P("Barcode withN Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='barcode_withN_reads1')])]),
                                        html.Tr([html.Td([html.P("Q30 Bases in Barcode",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Q30_Barcode1')])]),
                                        html.Tr([html.Td([html.P("Q30 Bases in UMI",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Q30_UMI1')])]),
                                        ])], bordered=True,className='card-mid'),
                                dbc.Table(children = [
                                    html.Thead(html.Tr([html.Th([html.H4(["Filter Stat",
                                        dbc.Badge(children=[
                                            dbc.Button(
                                                "?",
                                                id="collapse-button-5",
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
                                                    ])),id="collapse-5",),
                                    html.Tbody([
                                        html.Tr([html.Td([html.P("Raw Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Raw_Reads1')])]), 
                                        html.Tr([html.Td([html.P("Low Quality Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Low_Quality_Reads1')])]), 
                                        html.Tr([html.Td([html.P("Too Many N Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Too_Many_N_Reads1')])]), 
                                        html.Tr([html.Td([html.P("Too Short Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Too_Short_Reads1')])]), 
                                        html.Tr([html.Td([html.P("Too Long Reads",className='col-md-8 text-td'),html.P(className='col-md-4 text-td text-right',id='Too_Long_Reads1')])]),
                                        ])], bordered=True,className='card-sma'),
                                ]),
                                html.Div(className='col-md-6',children=[
                                dbc.Card(
                                    dbc.CardBody([
                                            dcc.Graph(
                                                    id='example-graph-2',
                                                    figure=get_sun_fig()
                                                )
                                        ]),className='card-big'
                                    ),
                                dbc.Table(children = [
                                    html.Thead(html.Tr([html.Th([html.H4(["Sample",
                                        dbc.Badge(children=[
                                            dbc.Button(
                                                "?",
                                                id="collapse-button-6",
                                                color='light',
                                                className='button-style'
                                                ),
                                            
                                        ], color="light",pill=True, className="ml-1 badge-style")])])])),
                                    dbc.Collapse(
                                                dbc.Card(dbc.CardBody([
                                                    html.H4("Number of Reads", className="card-title"),
                                                    html.P("Total number of read pairs that were assigned to this library in demultiplexing. ",className="card-text text-P"),
                                                    html.H4("Valid Barcodes", className="card-title"),
                                                    html.P("Fraction of reads with barcodes that match the whitelist after barcode correction. ",className="card-text text-P"),
                                                    html.H4("Valid UMIs", className="card-title"),
                                                    html.P("Fraction of reads with valid UMIs; i.e. UMI sequences that do not contain Ns and that are not homopolymers. ",className="card-text text-P"),
                                                    html.H4("Sequencing Saturation", className="card-title"),
                                                    html.P("The fraction of reads originating from an already-observed UMI. This is a function of library complexity and sequencing depth. More specifically, this is the fraction of confidently mapped, valid spot-barcode, valid UMI reads that had a non-unique (spot-barcode, UMI, gene). ",className="card-text text-P"),
                                                    html.H4("Q30 Bases in Barcode", className="card-title"),
                                                    html.P("Fraction of spot barcode bases with Q-score >= 30, excluding very low quality/no-call (Q <= 2) bases from the denominator. ",className="card-text text-P"),
                                                    html.H4("Q30 Bases in RNA Read", className="card-title"),
                                                    html.P("Fraction of RNA read bases with Q-score >= 30, excluding very low quality/no-call (Q <= 2) bases from the denominator. This is Read 2 for the Visium v1 chemistry.",className="card-text text-P"),
                                                    html.H4("Q30 Bases in UMI", className="card-title"),
                                                    html.P("Fraction of UMI bases with Q-score >= 30, excluding very low quality/no-call (Q <= 2) bases from the denominator. ",className="card-text text-P"),
                                                    ])),id="collapse-6",),
                                    html.Tbody([
                                        html.Tr([html.Td("Sample ID")]), 
                                        html.Tr([html.Td("Sample Description")]), 
                                        html.Tr([html.Td("Chemistry")]),
                                        html.Tr([html.Td("Slide Serial Number")]),
                                        html.Tr([html.Td("Reference Path")]),
                                        html.Tr([html.Td("Transcriptome")]),
                                        html.Tr([html.Td("Pipeline Version")]),
                                        ])], bordered=True,className='card-mid'),
                                ]),
                                ]),                            
                            ]),                             
                            ], label="Alignment"),
                        # table3 Basic
                        dbc.Tab([
                            html.Div(
                                [
                                html.P("Filter and Map", className="card-text"),
                                dbc.Button("Click here", color="success"),
                                ]),
                            ], label="Basic"),
                            ])
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
    Output('number_reads','children'),
    Output('Q30_Barcode','children'),
    Output('Q30_UMI','children'),
    Output('Sample_id','children'),
    Output('Usable_Barcode','children'),
    Output('fixed_sequence_contianing_reads','children'),
    Output('Barcode_MisOverlap_Reads','children'),
    Output('barcode_withN_reads','children'),
    Output('Raw_Reads','children'),
    Output('Low_Quality_Reads','children'),
    Output('Too_Many_N_Reads','children'),
    Output('Too_Short_Reads','children'),
    Output('Too_Long_Reads','children'),
    Output('mapped_reads_ali','children'),
    Output('unique_reads','children'),
    Output('Duplication_rate','children')],
    [Input('Sample_dropdown','value')]
    )
def data_set(values):
    unique_reads = data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["UNIQUE_READS"]
    Duplication_rate = data_json["2.Alignment"]["2.6.Filter_And_Deduplication"][0]["DUPLICATION_RATE"]
    mapped_reads,clean_reads,number_reads,Q30_Barcode,Q30_UMI,sample_id,Usable_Barcode,\
    fixed_sequence_contianing_reads,Barcode_MisOverlap_Reads,barcode_withN_reads,Raw_Reads,\
    Low_Quality_Reads,Too_Many_N_Reads,Too_Short_Reads,Too_Long_Reads,mapped_reads_ali,\
    unique_reads,Duplication_rate=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    if values:
        for value in values:
            for i in data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"]:
                if i["Sample_id"] == value:
                    mapped_reads += tran_data(i["mapped_reads"].split('(')[-2])
                    number_reads += tran_data(i["total_reads"])
                    Q30_Barcode = i["Q30_bases_in_barcode"]
                    Q30_UMI = i["Q30_bases_in_umi"]
                    sample_id = i["Sample_id"]
                    Usable_Barcode += tran_data(i["getBarcodePositionMap_uniqBarcodeTypes"])
                    fixed_sequence_contianing_reads += tran_data(i['fixed_sequence_contianing_reads'].split('(')[-2])
                    Barcode_MisOverlap_Reads += tran_data(i['barcode_misOverlap_reads'].split('(')[-2])
                    barcode_withN_reads += tran_data(i['barcode_withN_reads'].split('(')[-2])
            for i in data_json["1.Filter_and_Map"]["1.2.Filter_Stat"]:
                if i["Sample_Name"] == value:
                    clean_reads += tran_data(i["Clean_Reads"])
                    Raw_Reads += tran_data(i['Raw_Reads'])
                    Low_Quality_Reads += tran_data(i['Low_Quality_Reads'])
                    Too_Many_N_Reads += tran_data(i['Too_Many_N_Reads'])
                    Too_Short_Reads += tran_data(i['Too_Short_Reads'])
                    Too_Long_Reads += tran_data(i['Too_Long_Reads'])
            for i in data_json["2.Alignment"]["2.2.Uniquely_Mapped_Read"]:
                if i["Sample_Id"] == value:
                    mapped_reads_ali = i["Mapped_Reads(%)"]
        return mapped_reads,clean_reads,number_reads,Q30_Barcode,Q30_UMI,sample_id,Usable_Barcode,\
    fixed_sequence_contianing_reads,Barcode_MisOverlap_Reads,barcode_withN_reads,Raw_Reads,\
    Low_Quality_Reads,Too_Many_N_Reads,Too_Short_Reads,Too_Long_Reads,mapped_reads_ali,\
    unique_reads,Duplication_rate
    else:
        return '','','','','','','','','','','','','','','','','',''
    