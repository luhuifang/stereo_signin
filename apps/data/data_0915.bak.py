import json
import dash
import base64

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
                                        html.Tr([html.Td([html.P("Q10 Bases in Barcode",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q10_Barcode')],className='row collapse-type')]), 
                                        html.Tr([html.Td([html.P("Q20 Bases in Barcode",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q20_Barcode')],className='row collapse-type')]), 
                                        html.Tr([html.Td([html.P("Q30 Bases in Barcode",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q30_Barcode')],className='row collapse-type')]),
                                        html.Tr([html.Td([html.P("Q10 Bases in UMI",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q10_UMI')],className='row collapse-type')]), 
                                        html.Tr([html.Td([html.P("Q20 Bases in UMI",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q20_UMI')],className='row collapse-type')]), 
                                        html.Tr([html.Td([html.P("Q30 Bases in UMI",className='col-md-7 text-td'),html.P(className='col-md-5 text-td text-right',id='Q30_UMI')],className='row collapse-type')]),                       
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
                                    html.Tr([html.Td([html.P("Contour area",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Contour_area')],className='row collapse-type')]), 
                                    html.Tr([html.Td([html.P("Number of DNB under tissue",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Number_of_DNB_under_tissue')],className='row collapse-type')]), 
                                    html.Tr([html.Td([html.P("Ratio",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Ratio')],className='row collapse-type')]), 
                                    html.Tr([html.Td([html.P("Total Gene type",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Total_Gene_type')],className='row collapse-type')]), 
                                    html.Tr([html.Td([html.P("Raw reads",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Raw_Reads')],className='row collapse-type')]),
                                    html.Tr([html.Td([html.P("Reads under tissue",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Reads_under_tissue')],className='row collapse-type')]), 
                                    html.Tr([html.Td([html.P("Fraction Reads in Spots Under Tissue",className='col-md-8 text-sm'),html.P(className='col-md-4 text-sm text-right',id='Fraction_Reads_in_Spots_Under_Tissue')],className='row collapse-type')]),                        
                                    ])], bordered=True,className='card-mid'), 
                            ]),
                            html.Div(className='col-md-8 box-style-right',id = 'bin_table',children=[                   
                            ]),

                            # figure showing
                            html.Div(className='col-md-12 box-style-left',children=[
                                dbc.Card([
                                    dbc.CardBody(
                                        dbc.Tabs([
                                            dbc.Tab(children=[
                                                html.Div([
                                                dbc.Card(
                                                dbc.CardBody([
                                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/scatter_20x20_umi_gene_counts.png', 'rb').read()).decode('ascii')),
                                                            width='400px', height="400px",id='Bin-20-1-img',n_clicks=0),
                                                    dbc.Modal([
                                                            dbc.ModalHeader("Bin-20"),
                                                            dbc.ModalBody(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/scatter_20x20_umi_gene_counts.png', 'rb').read()).decode('ascii')), 
                                                                width='600px',height="600px")),],
                                                        id="Bin-20-1-modal",size="lg",),
                                                    ]),className="mt-3 col-md-5 card-fig",),
                                            dbc.Card(
                                                dbc.CardBody([
                                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/violin_20x20_umi_gene.png', 'rb').read()).decode('ascii')),
                                                            width='500px', height="400px",id='Bin-20-2-img',n_clicks=0),
                                                    dbc.Modal([
                                                            dbc.ModalHeader("Bin-20"),
                                                            dbc.ModalBody(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/violin_20x20_umi_gene.png', 'rb').read()).decode('ascii')), 
                                                                width='700px',height="600px")),],
                                                        id="Bin-20-2-modal",size="lg",),
                                                    ]),className="mt-3 col-md-6 card-fig",),],className='row'),],
                                            label="Bin-20", tab_id="Bin-20",),

                                            dbc.Tab(children=[
                                                html.Div([
                                                dbc.Card(
                                                dbc.CardBody([
                                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/scatter_50x50_umi_gene_counts.png', 'rb').read()).decode('ascii')),
                                                            width='400px', height="400px",id='Bin-50-1-img',n_clicks=0),
                                                    dbc.Modal([
                                                            dbc.ModalHeader("Bin-50"),
                                                            dbc.ModalBody(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/scatter_50x50_umi_gene_counts.png', 'rb').read()).decode('ascii')), 
                                                                width='600px',height="600px")),],
                                                        id="Bin-50-1-modal",size="lg",),
                                                    ]),className="mt-3 col-md-5 card-fig",),
                                            dbc.Card(
                                                dbc.CardBody([
                                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/violin_50x50_umi_gene.png', 'rb').read()).decode('ascii')),
                                                            width='500px', height="400px",id='Bin-50-2-img',n_clicks=0),
                                                    dbc.Modal([
                                                            dbc.ModalHeader("Bin-50"),
                                                            dbc.ModalBody(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/violin_50x50_umi_gene.png', 'rb').read()).decode('ascii')), 
                                                                width='700px',height="600px")),],
                                                        id="Bin-50-2-modal",size="lg",),
                                                    ]),className="mt-3 col-md-6 card-fig",),],className='row'),],
                                            label="Bin-50", tab_id="Bin-50"),
                                            dbc.Tab(children=[
                                                html.Div([
                                                dbc.Card(
                                                dbc.CardBody([
                                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/scatter_100x100_umi_gene_counts.png', 'rb').read()).decode('ascii')),
                                                            width='400px', height="400px",id='Bin-100-1-img',n_clicks=0),
                                                    dbc.Modal([
                                                            dbc.ModalHeader("Bin-100"),
                                                            dbc.ModalBody(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/scatter_100x100_umi_gene_counts.png', 'rb').read()).decode('ascii')), 
                                                                width='600px',height="600px")),],
                                                        id="Bin-100-1-modal",size="lg",),
                                                    ]),className="mt-3 col-md-5 card-fig",),
                                            dbc.Card(
                                                dbc.CardBody([
                                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/violin_100x100_umi_gene.png', 'rb').read()).decode('ascii')),
                                                            width='500px', height="400px",id='Bin-100-2-img',n_clicks=0),
                                                    dbc.Modal([
                                                            dbc.ModalHeader("Bin-100"),
                                                            dbc.ModalBody(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/violin_100x100_umi_gene.png', 'rb').read()).decode('ascii')), 
                                                                width='700px',height="600px")),],
                                                        id="Bin-100-2-modal",size="lg",),
                                                    ]),className="mt-3 col-md-6 card-fig",),],className='row'),],
                                            label="Bin-100", tab_id="Bin-100"),
                                            dbc.Tab(children=[
                                                html.Div([
                                                dbc.Card(
                                                dbc.CardBody([
                                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/scatter_150x150_umi_gene_counts.png', 'rb').read()).decode('ascii')),
                                                            width='400px', height="400px",id='Bin-150-1-img',n_clicks=0),
                                                    dbc.Modal([
                                                            dbc.ModalHeader("Bin-150"),
                                                            dbc.ModalBody(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/scatter_150x150_umi_gene_counts.png', 'rb').read()).decode('ascii')), 
                                                                width='600px',height="600px")),],
                                                        id="Bin-150-1-modal",size="lg",),
                                                    ]),className="mt-3 col-md-5 card-fig",),
                                            dbc.Card(
                                                dbc.CardBody([
                                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/violin_150x150_umi_gene.png', 'rb').read()).decode('ascii')),
                                                            width='500px', height="400px",id='Bin-150-2-img',n_clicks=0),
                                                    dbc.Modal([
                                                            dbc.ModalHeader("Bin-150"),
                                                            dbc.ModalBody(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/violin_150x150_umi_gene.png', 'rb').read()).decode('ascii')), 
                                                                width='700px',height="600px")),],
                                                        id="Bin-150-2-modal",size="lg",),
                                                    ]),className="mt-3 col-md-6 card-fig",),],className='row'),],
                                            label="Bin-150", tab_id="Bin-150"),
                                            dbc.Tab(children=[
                                                html.Div([
                                                dbc.Card(
                                                dbc.CardBody([
                                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/scatter_200x200_umi_gene_counts.png', 'rb').read()).decode('ascii')),
                                                            width='400px', height="400px",id='Bin-200-1-img',n_clicks=0),
                                                    dbc.Modal([
                                                            dbc.ModalHeader("Bin-200"),
                                                            dbc.ModalBody(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/scatter_200x200_umi_gene_counts.png', 'rb').read()).decode('ascii')), 
                                                                width='600px',height="600px")),],
                                                        id="Bin-200-1-modal",size="lg",),
                                                    ]),className="mt-3 col-md-5 card-fig",),
                                            dbc.Card(
                                                dbc.CardBody([
                                                    html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/violin_200x200_umi_gene.png', 'rb').read()).decode('ascii')),
                                                            width='500px', height="400px",id='Bin-200-2-img',n_clicks=0),
                                                    dbc.Modal([
                                                            dbc.ModalHeader("Bin-200"),
                                                            dbc.ModalBody(html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open('./data/test_stat/violin_200x200_umi_gene.png', 'rb').read()).decode('ascii')), 
                                                                width='700px',height="600px")),],
                                                        id="Bin-200-2-modal",size="lg",),
                                                    ]),className="mt-3 col-md-6 card-fig",),],className='row'),],
                                            label="Bin-200", tab_id="Bin-200"),
                                        ],
                                        id="card-tabs",
                                    ),className='card-tabs')],className='card-lg')
                                ])
                        ]),                            
                    ]),
                ])
            ]),
        ])
    ])

for each_bin in ['Bin-20-1','Bin-20-2','Bin-50-1','Bin-50-2','Bin-100-1','Bin-100-2','Bin-150-1','Bin-150-2','Bin-200-1','Bin-200-2']:

    @app.callback(
        Output("{}-modal".format(each_bin), "is_open"),
        [Input("{}-img".format(each_bin), "n_clicks"),],
        [State("{}-modal".format(each_bin), "is_open")],
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open
        return is_open


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
        Too_Many_N_Reads,Low_Quality_Reads,Unique_Mapped_Reads,Chimeric_Reads,Multi_Mapping_Reads,Reference_Mapping_reads,Unmapping_Read,DuPlication_Reads,Unique_Reads,Contour_area,\
        Number_of_DNB_under_tissue,Ratio,Total_Gene_type,Raw_Reads,Reads_under_tissue,Fraction_Reads_in_Spots_Under_Tissue,\
        Q20_Barcode,Q30_Barcode,Q10_Barcode,Q10_UMI,Q20_UMI,Q30_UMI = get_data(values)

        return str(Barcode_Mapping)+'M',str(clean_reads)+'M',Q20_Barcode,Q30_Barcode,Q30_UMI,Q10_Barcode,Q10_UMI,\
    Q20_UMI,Contour_area,Reads_under_tissue,Number_of_DNB_under_tissue,Ratio,Total_Gene_type,\
    Raw_Reads,Fraction_Reads_in_Spots_Under_Tissue,str(raw_reads)+'M',str(Reference_Mapping_reads)+'M'
    else:
        return '','','','','','','','','','','','','','','','',''
    