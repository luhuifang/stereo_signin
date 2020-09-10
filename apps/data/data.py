import json
import dash

from decimal import Decimal

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from spatialTrancriptomeReport import app
from apps.data.load_json import data_json,df_table,data_dict
from apps.data.disposal_sun_data import get_sun_fig
from apps.data.get_data import get_data,tran_data


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
            # html.Div(className='row',children=[
            #     html.H1('sampleA')
            # ]),
            html.Div(className='row',children=[
                html.Div(className='col-md-12',children=[
                    html.Div(className='card-body',children=[
                        html.Div(className='row',id='key_indicator',children=[
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'raw_reads', className="card-title text-center text-green"),
                                        html.P("Raw Reads",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'mapped_reads', className="card-title text-center text-green"),
                                        html.P("Barcode Mapping",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'clean_reads', className="card-title text-center text-green"),
                                        html.P("Clean Reads ",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'reference_mapping_reads', className="card-title text-center text-green"),
                                        html.P("Reference Mapping",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'deduplication_reads', className="card-title text-center text-green"),
                                        html.P("Deduplication",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            dbc.Card(
                                dbc.CardBody([
                                        html.H4(children = [],id = 'uniquely_reads', className="card-title text-center text-green"),
                                        html.P("Uniquely Reads",className="card-text text-center"),
                                    ]),className=' card-sma'
                                ),
                            ]),
                        html.Div(className='row',children=[
                            html.Div(className='col-md-2',children=[
                               
                                html.H4('Select Sample:',className='text-P')
                                        
                                ]),
                            html.Div(className='col-md-10',children=[
                                dcc.Dropdown(
                                    id="Sample_dropdown",
                                    options=[{'label':i["Sample_id"],'value':i["Sample_id"]} for i in data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"]],
                                    placeholder='Select the sample',
                                    persistence=False,
                                    searchable=False,
                                    clearable=False,
                                    multi=True,
                                    value= [i for i in data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"].keys()],
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
                                    html.H4("Q10 Bases in Barcode", className="card-title"),
                                    html.P("Ratio of bases whose quality value exceeds Q10 in barcode. ",className="text-P"),
                                    html.H4("Q20 Bases in Barcode", className="card-title"),
                                    html.P("Ratio of bases whose quality value exceeds Q20 in barcode. ",className=" text-P"),
                                    html.H4("Q30 Bases in Barcode", className="card-title"),
                                    html.P("Ratio of bases whose quality value exceeds Q30 in barcode. ",className=" text-P"),
                                    html.H4("Q10 Bases in UMI", className="card-title"),
                                    html.P("Ratio of bases whose quality value exceeds Q10 in UMI. ",className="text-P"),
                                    html.H4("Q20 Bases in UMI", className="card-title"),
                                    html.P("Ratio of bases whose quality value exceeds Q20 in UMI. ",className="text-P"),
                                    html.H4("Q30 Bases in UMI", className="card-title"),
                                    html.P("Ratio of bases whose quality value exceeds Q30 in UMI. ",className="text-P"),
                                    ])),id="collapse-1",className='collapse-type'),
                    html.Tbody([
                        html.Tr([html.Td([html.P("Q10 Bases in Barcode",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q10_Barcode')])]), 
                        html.Tr([html.Td([html.P("Q20 Bases in Barcode",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q20_Barcode')])]), 
                        html.Tr([html.Td([html.P("Q30 Bases in Barcode",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q30_Barcode')])]),
                        html.Tr([html.Td([html.P("Q10 Bases in UMI",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q10_UMI')])]), 
                        html.Tr([html.Td([html.P("Q20 Bases in UMI",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q20_UMI')])]), 
                        html.Tr([html.Td([html.P("Q30 Bases in UMI",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q30_UMI')])]),                       
                        ])], bordered=True,className='card-mid'),
                
                ]),
                html.Div(className='col-md-8 box-style-right',children=[
                    dbc.Card(
                        dbc.CardBody([
                            html.Div(id='sunburst-fig',className='collapse-type',children=[
                                ])
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
                                                html.H4("Contour area", className="card-title"),
                                                html.P("Number of reads of input data( After filtering adapters). ",className="card-text text-P"),
                                                html.H4("Number of DNB under tissue", className="card-title"),
                                                html.P("Number of reads filtered due to low quality.",className="card-text text-P"),
                                                html.H4("Ratio", className="card-title"),
                                                html.P("Number of reads filtered that contain too many N. ",className="card-text text-P"),
                                                html.H4("Total Gene type", className="card-title"),
                                                html.P("Number of reads filtered which too short. ",className="card-text text-P"),
                                                html.H4("Raw reads", className="card-title"),
                                                html.P("Number of reads filtered with too long.",className="card-text text-P"),
                                                html.H4("Reads under tissue", className="card-title"),
                                                html.P("Number of reads filtered with too long.",className="card-text text-P"),
                                                html.H4("Fraction Reads in Spots Under Tissue", className="card-title"),
                                                html.P("Number of reads filtered with too long.",className="card-text text-P"),                                                
                                                ])),id="collapse-2",),
                                html.Tbody([
                                    html.Tr([html.Td([html.P("Contour area",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Contour_area')])]), 
                                    html.Tr([html.Td([html.P("Number of DNB under tissue",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Number_of_DNB_under_tissue')])]), 
                                    html.Tr([html.Td([html.P("Ratio",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Ratio')])]), 
                                    html.Tr([html.Td([html.P("Total Gene type",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Total_Gene_type')])]), 
                                    html.Tr([html.Td([html.P("Raw reads",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Raw_Reads')])]),
                                    html.Tr([html.Td([html.P("Reads under tissue",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Reads_under_tissue')])]), 
                                    html.Tr([html.Td([html.P("Fraction Reads in Spots Under Tissue",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Fraction_Reads_in_Spots_Under_Tissue')])]),                        
                                    ])], bordered=True,className='card-mid'), 
                            ]),
                            html.Div(className='col-md-8 box-style-right',id = 'bin_table',children=[
                                
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
    Output('sunburst-fig','children'),
    [Input('Sample_dropdown','value')]
    )
def sunburst_fig(values):
    if values:
        fig = get_sun_fig(values)
        return dcc.Graph(figure=fig)
    else:
        return ''

@app.callback(
    Output('bin_table','children'),
    [Input('Sample_dropdown','value')]
    )
def sunburst_fig(values):
    if values:
        return dbc.Table.from_dataframe(df_table,
        striped=True, hover=True,className='gridtable')
    else:
        return ''

@app.callback(
    Output('key_indicator','children'),
    [Input('Sample_dropdown','value')]
    )
def key_indic(values):
    DuPlication_Reads = round(Decimal(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['DUPLICATION_RATE'])/100*tran_data(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['PASS_FILTER']),2)
    Unique_Reads = Decimal(tran_data(data_dict["2.Alignment"]["2.6.Filter_And_Deduplication"][0]['UNIQUE_READS'])).quantize(Decimal("0.00"))
    if values:
        if len(values) == len(data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"].keys()):
            return [dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'raw_reads', className="card-title text-center text-green"),
                                html.P("Raw Reads",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'mapped_reads', className="card-title text-center text-green"),
                                html.P("Barcode Mapping",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'clean_reads', className="card-title text-center text-green"),
                                html.P("Clean Reads ",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'reference_mapping_reads', className="card-title text-center text-green"),
                                html.P("Reference Mapping",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = str(DuPlication_Reads)+'M',id = 'deduplication_reads', className="card-title text-center text-green"),
                                html.P("Deduplication",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = str(Unique_Reads)+'M',id = 'uniquely_reads', className="card-title text-center text-green"),
                                html.P("Uniquely Reads",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),]
        else:
            return [dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'raw_reads', className="card-title text-center text-green"),
                                html.P("Raw Reads",className="card-text text-center"),
                            ]),className=' card-sma-1'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'mapped_reads', className="card-title text-center text-green"),
                                html.P("Barcode Mapping",className="card-text text-center"),
                            ]),className=' card-sma-1'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'clean_reads', className="card-title text-center text-green"),
                                html.P("Clean Reads ",className="card-text text-center"),
                            ]),className=' card-sma-1'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'reference_mapping_reads', className="card-title text-center text-green"),
                                html.P("Reference Mapping",className="card-text text-center"),
                            ]),className=' card-sma-1'
                        ),]

    else:
        return [dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'raw_reads', className="card-title text-center text-green"),
                                html.P("Raw Reads",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'mapped_reads', className="card-title text-center text-green"),
                                html.P("Barcode Mapping",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'clean_reads', className="card-title text-center text-green"),
                                html.P("Clean Reads ",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = [],id = 'reference_mapping_reads', className="card-title text-center text-green"),
                                html.P("Reference Mapping",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = '',id = 'deduplication_reads', className="card-title text-center text-green"),
                                html.P("Deduplication",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),
                    dbc.Card(
                        dbc.CardBody([
                                html.H4(children = '',id = 'uniquely_reads', className="card-title text-center text-green"),
                                html.P("Uniquely Reads",className="card-text text-center"),
                            ]),className=' card-sma'
                        ),]

@app.callback(
    [Output('mapped_reads','children'),
    Output('clean_reads','children'),
    Output('Q20_Barcode','children'),
    Output('Q30_Barcode','children'),
    Output('Q30_UMI','children'),
    Output('Q10_Barcode','children'),
    Output('Q10_UMI','children'),
    Output('Q20_UMI','children'),
    Output('Contour_area','children'),
    Output('Reads_under_tissue','children'),
    Output('Number_of_DNB_under_tissue','children'),
    Output('Ratio','children'),
    Output('Total_Gene_type','children'),
    Output('Raw_Reads','children'),
    Output('Fraction_Reads_in_Spots_Under_Tissue','children'),
    Output('raw_reads','children'),
    Output('reference_mapping_reads','children'),],
    [Input('Sample_dropdown','value')]
    )
def data_set(values):
    if values:
        raw_reads,Barcode_Mapping,UnMapping,Filter_reads,Fail_Filter,clean_reads,Umi_Filter_Reads,Too_Long_Reads,Too_Short_Reads,\
        Too_Many_N_Reads,Low_Quality_Reads,Reference_Mapping_reads,Unmapping_Read,DuPlication_Reads,Unique_Reads,Contour_area,\
        Number_of_DNB_under_tissue,Ratio,Total_Gene_type,Raw_Reads,Reads_under_tissue,Fraction_Reads_in_Spots_Under_Tissue,\
        Q20_Barcode,Q30_Barcode,Q10_Barcode,Q10_UMI,Q20_UMI,Q30_UMI = get_data(values)

        return str(Barcode_Mapping)+'M',str(clean_reads)+'M',Q20_Barcode,Q30_Barcode,Q30_UMI,Q10_Barcode,Q10_UMI,\
    Q20_UMI,Contour_area,Reads_under_tissue,Number_of_DNB_under_tissue,Ratio,Total_Gene_type,\
    Raw_Reads,Fraction_Reads_in_Spots_Under_Tissue,str(raw_reads)+'M',str(Reference_Mapping_reads)+'M'
    else:
        return '','','','','','','','','','','','','','','','',''
    