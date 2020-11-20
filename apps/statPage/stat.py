import os
import json
import base64
from decimal import Decimal

import visdcc
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from spatialTrancriptomeReport import app

from apps.statPage.load_json import LoadStatJson, LoadStatFigure, number2human
from apps.statPage.disposal_sun_data import get_sun_fig
from apps.statPage.static_info import SPOT_SUMMARY_COLLAPSE, SPOT_SUMMARY_FIELD, QUALITY_COLLAPSE, QUALITY_FIELD, BIN_SUMMARY_COLLAPSE, BIN_SUMMARY_FIELD, IMPORTANT_FIELD, RNA_MAPPING_FIELD, RNA_MAPPING_COLLAPSE ,ANNOTATION_FIELD, ANNOTATION_COLLAPSE ,CELLCUT_BIN_STAT_COLLAPSE, CELLCUT_BIN_STAT_FIELD, CELLCUT_TOTAL_STAT_FIELD, CELLCUT_TOTAL_STAT_COLLAPSE

from apps.statPage.utils import get_dir_from_search_str,get_file_list 

def showImportantData(show_value_list):
    if not isinstance(show_value_list, list):
        return []

    datas = []
    for i in range(len(show_value_list)):
        item = IMPORTANT_FIELD[i]
        child = show_value_list[i]
        datas.append(
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H3(id = item['id'] , className="card-title text-center text-green", children=child),
                        html.H6(item['label'],className="card-text text-center"),
                    ]),
                    outline=True,
                    className='shadow',
                    style={'height':'125px'}
                ),
            ]),
        )
    return datas


def showCollapse(info_list):
    collapse = []
    for info in info_list:
        collapse.append(html.H6(info['title'], className="card-title text-blue"))
        collapse.append(html.Span(info['content'],className="card-text "))
        collapse.append(html.Hr())
    return collapse


def showTableStat(table_title, id_name, collapse_info=[], table_body_list=[], values=[]):
    return dbc.Table(children = [
        html.Thead(html.Tr([html.Th([
            dbc.Row([
                dbc.Col([
                    html.H6([
                        table_title,
                        dbc.Button("?", id=f'{id_name}-button',color="light",size='sm', className='ml-2' )
                    ])
                ], width=6),
            ])
        ])])),
        dbc.Collapse(
            dbc.Card(dbc.CardBody(showCollapse(collapse_info))),
            id=id_name,
        ),
        showTableBody(table_body_list, values),                    
    ], bordered=True,className='card-mid'),

def showTableBody(field_list, values):
    child = []
    for field in field_list:
        value = ''
        if values:
            value = values[field['id']]
        child.append(
            html.Tr([html.Td([
                dbc.Row([
                    dbc.Col(html.Span(field['label']), width=7),
                    dbc.Col(html.Span(value, id=field['id'], className='text-right')),
                ],justify="between"),   
            ])]), 
        )
    return html.Tbody(child)

def showBinTable(df_table):
    Thead = []
    Tbody = []
    for i in df_table.iloc:
        Thead = []
        row_Td = []
        for colname in df_table.columns.values.tolist():
            Thead.append(html.Th(colname))
            row_Td.append(html.Td(i[colname]))

        Tbody.append(html.Tr(row_Td))
        
    return html.Table(className='gridtable',children=[
        html.Thead(html.Tr(Thead)),
        html.Tbody(Tbody)
    ]),


def showPicTabs(pics):
    tab_child = []
    count = 0
    for bin_size, pics_one in sorted(pics.items(),key=lambda x:eval(x[0])):
        print(bin_size,pics_one)
        pic_row = []
        for pic_type, pic_path in pics_one.items():
            title = os.path.basename(pic_path)
            image = 'data:image/png;base64,{}'.format(base64.b64encode(open(pic_path, 'rb').read()).decode('ascii'))
            col = dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Img(src=image, id = {'id': f'{count}', 'type':'img'}, n_clicks=0,className='bin-img'),
                        dbc.Modal([
                            dbc.ModalHeader(title),
                            dbc.ModalBody(html.Img(src=image, width='750px',height="auto")),
                        ], id= {'id':f'{count}', 'type':'modal'}, size="lg", centered=True)
                    ],className='text-center'),
                ], className="card-fig mt-3", style={'height': '400px'}),
            ], width=12)
            pic_row.append(col)
            count += 1
        tab_child.append(dbc.Tab(dbc.Row(pic_row), label=f'Bin-{bin_size}', tab_id=f'Bin-{bin_size}'))
    return dbc.Tabs(tab_child, id="card-tabs")

def showCellPicTabs(pics):
    tab_child = []
    pic_row = []
    count = 0
    for bin_size, pics_one in sorted(pics.items(),key=lambda x:eval(x[0])):
        for pic_type, pic_path in pics_one.items():
            title = os.path.basename(pic_path)
            image = 'data:image/png;base64,{}'.format(base64.b64encode(open(pic_path, 'rb').read()).decode('ascii'))
            col = dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Img(src=image, id = {'id': f'{count}', 'type':'img'}, n_clicks=0,className='bin-img'),
                        dbc.Modal([
                            dbc.ModalHeader(title),
                            dbc.ModalBody(html.Img(src=image, width='750px',height="auto")),
                        ], id= {'id':f'{count}', 'type':'modal'}, size="lg", centered=True)
                    ],className='text-center'),
                ], className="card-fig mt-3", style={'height': '400px'}),
            ], width=12)
            pic_row.append(col)
            count += 1
    tab_child.append(dbc.Tab(dbc.Row(pic_row),label='Bin Figure'))
    return dbc.Tabs(tab_child, id="card-tabs")

def BinData(file_dir):
    loadJson =LoadStatJson(file_dir)
    data_json = loadJson.data_json
    df_table = loadJson.getDfTable(data_json)
    flag, spot_summary = loadJson.getSpotSummary(data_json)
    is_cell,total_stat_summary, bin_stat_summary = loadJson.IsCell(data_json)
    pictures = LoadStatFigure(file_dir).getPicDict()
    final_collapse_info =[]
    table_body_list = []

    if not is_cell:
        if flag == '4':
            final_collapse_info = SPOT_SUMMARY_COLLAPSE
            table_body_list = SPOT_SUMMARY_FIELD
        elif  flag == '3':
            final_collapse_info = BIN_SUMMARY_COLLAPSE
            table_body_list = BIN_SUMMARY_FIELD
        total_stat = dbc.Col(
                            showTableStat(
                                table_title="TissueCut Total Stat", 
                                id_name="collapse-2", 
                                collapse_info=final_collapse_info, 
                                table_body_list=table_body_list, 
                                values=spot_summary
                            ), 
                            sm=4, xs=12
                        )
        bin_stat = dbc.Col(id = 'bin_table', sm=8, xs=12, children=showBinTable(df_table))
        bin_picture = showPicTabs(pictures)
    else: 
        total_stat = dbc.Col(
                        showTableStat(
                            table_title="CellCut Total Stat", 
                            id_name="collapse-2", 
                            collapse_info=CELLCUT_TOTAL_STAT_COLLAPSE, 
                            table_body_list=CELLCUT_TOTAL_STAT_FIELD, 
                            values=total_stat_summary
                        ), 
                        sm=6, xs=12
                    )
        bin_stat = dbc.Col(
                showTableStat(
                    table_title="CellCut Bin Stat", 
                    id_name="collapse-5", 
                    collapse_info=CELLCUT_BIN_STAT_COLLAPSE, 
                    table_body_list=CELLCUT_BIN_STAT_FIELD, 
                    values=bin_stat_summary
                ), 
                sm=6, xs=12
            )
        bin_picture = showCellPicTabs(pictures)
    return total_stat,bin_stat,bin_picture

def statLayout(file_dir, sn=''):
    loadJson =LoadStatJson(file_dir)
    data_json = loadJson.data_json
    data_dict = loadJson.getDataDict(data_json)
    filter_stat = data_dict["1.Filter_and_Map"]["1.2.Filter_Stat"]
    filter_dropdown_children = []
    summary_filter_dropdown_children = []
    summaryReport_file_dir = os.path.join(file_dir, 'filter')
    SummaryFile = get_file_list(summaryReport_file_dir, shuffix='summaryReport.html')
    if SummaryFile:
        for sample_dir in SummaryFile:
            summaryfile_basename = os.path.basename(sample_dir)
            sample_name = summaryfile_basename.strip('summaryReport.html')
            summary_filter_dropdown_children.append(dbc.DropdownMenuItem(
                html.A(
                    sample_name, 
                    href = '{0}{1}?path={2}'.format('/Stereo-Draftsman/static_file/', summaryfile_basename, sample_dir),
                    target='_blank'
                )
            ))
        summary_filter_stat_dropdown = dbc.DropdownMenu(summary_filter_dropdown_children, label='View summary report', nav=True, in_navbar=True)
    else:
        summary_filter_stat_dropdown=''
    for sample_name, v in filter_stat.items():
        basename = os.path.basename(v['Remarks'])
        dirname = '/'.join([file_dir, os.path.dirname(v['Remarks'])])
        filter_dropdown_children.append(dbc.DropdownMenuItem(
            html.A(
                sample_name, 
                href = '{0}{1}?path={2}'.format('/Stereo-Draftsman/static_file/', basename, dirname),
                target='_blank'
            )
        ))
    filter_stat_dropdown = dbc.DropdownMenu(filter_dropdown_children, label='View fastp report', nav=True, in_navbar=True)
    total_stat,bin_stat,bin_picture = BinData(file_dir)

    return dbc.Container([
        dbc.Row(dbc.Col(
            dbc.NavbarSimple(
                [summary_filter_stat_dropdown,
                filter_stat_dropdown,],
                brand=sn,
                color="dark",dark=True, className='mb-2'
            )
        )),
        dbc.Row(id='key_indicator', className='mb-4', children=showImportantData(['','','','',''])),
        dbc.Row([
            dbc.Col([
                dbc.Form(
                    dbc.FormGroup([
                        dbc.Label(html.H6('Select Sample:')),
                        dcc.Dropdown(
                            id="Sample_dropdown",
                            options=[{'label':i,'value':i} for i in data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"].keys()],
                            placeholder='Select the sample',
                            persistence=False,
                            searchable=False,
                            clearable=False,
                            multi=True,
                            value= [i for i in data_dict["1.Filter_and_Map"]["1.1.Adapter_Filter"].keys()],
                        )
                    ]),
                )
            ])
        ]),
        dbc.Row([
            dbc.Col(
                showTableStat(table_title="Adapter Filter", id_name="collapse-1", collapse_info=QUALITY_COLLAPSE, table_body_list=QUALITY_FIELD),
                sm=4, xs=12
            ),
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Div(id='sunburst-fig',)
                    ]),
                    className='card-mid'
                ),
            ], sm=8, xs=12),
        ], className='mb-1'),
        dbc.Row([ 
            dbc.Col(
                showTableStat(table_title="RNA Mapping", id_name="collapse-3", 
                collapse_info=RNA_MAPPING_COLLAPSE, table_body_list=RNA_MAPPING_FIELD),
                sm=6, xs=12
            ),
            dbc.Col(
                showTableStat(table_title="Annotation", id_name="collapse-4", 
                collapse_info=ANNOTATION_COLLAPSE, table_body_list=ANNOTATION_FIELD),
                sm=6, xs=12),
        ], className='mb-1'),
        dbc.Row([
            total_stat,
            bin_stat,
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                    bin_picture
                    ], className='card-tabs' )
                ], className='card-lg')
            ],width=12)
        ])
    ], className='mt-5 pt-2 font-DIN')


@app.callback(
    Output({'id': ALL,'type':'modal'}, 'is_open'),
    [Input({'id': ALL,'type':'img'}, 'n_clicks')],
    [State({'id': ALL,'type':'modal'}, 'is_open')]
)
def toggle_modal(*args):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    triggered = dash.callback_context.triggered[0]
    
    old_open = args[1]
    index = eval(json.loads(triggered['prop_id'].replace('.n_clicks', ''))['id'])
    old_open[index] = not old_open[index]
    return old_open

@app.callback(
    Output("collapse-1", "is_open"),
    [Input("collapse-1-button", "n_clicks")],
    [State("collapse-1", "is_open")],
)
def toggle_collapse_1(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-2", "is_open"),
    [Input("collapse-2-button", "n_clicks")],
    [State("collapse-2", "is_open")],
)
def toggle_collapse_2(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-3", "is_open"),
    [Input("collapse-3-button", "n_clicks")],
    [State("collapse-3", "is_open")],
)
def toggle_collapse_3(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-4", "is_open"),
    [Input("collapse-4-button", "n_clicks")],
    [State("collapse-4", "is_open")],
)
def toggle_collapse_4(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output("collapse-5", "is_open"),
    [Input("collapse-5-button", "n_clicks")],
    [State("collapse-5", "is_open")],
)
def toggle_collapse_5(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('sunburst-fig','children'),
    [Input('Sample_dropdown','value')],
    [State('url', 'search')]
)
def sunburst_fig(values, url_search):
    file_dir = get_dir_from_search_str(url_search)
    if values:
        fig = get_sun_fig(values, file_dir)
        graph = dcc.Graph(figure=fig, config = {'displaylogo' : False})
        return graph
    else:
        return ''

@app.callback(
    Output('key_indicator','children'),
    [Input('Sample_dropdown','value')],
    [State('url', 'search')]
    )
def key_indic(values, url_search):
    file_dir = get_dir_from_search_str(url_search)
    loadJson = LoadStatJson(file_dir)
    DuPlication_Reads, Unique_Reads = loadJson.getDupUniqReads(values)
    if values:
        if len(values) == len(loadJson.data_json["1.Filter_and_Map"]["1.1.Adapter_Filter"]):
            return showImportantData(['','','','',number2human(Unique_Reads)])
        else:
            return showImportantData(['','','',''])
    else:
        return showImportantData(['','','','', ''])

@app.callback(
    [Output('raw_reads','children'),
     Output('mapped_reads','children'),
     Output('clean_reads','children'),
     Output('reference_mapping_reads','children'),
     Output('Total_Reads','children'),
     Output('Q30_Barcode','children'),
     Output('Q30_UMI','children'),
     Output('Input_read','children'),
     Output('Uniquely_Mapped_Read','children'),
     Output('Multi_Mapping_Read','children'),
     Output('RNA_Unmapping_Read','children'),
     Output('Chimeric_Read','children'),
     Output('Exonic','children'),
     Output('Intronic','children'),
     Output('Intergenic','children'),
     Output('Transcriotome','children'),
     Output('Antisense','children'),
    ],
    [Input('Sample_dropdown','value')],
    [State('url', 'search')]
    )
def data_set(values, url_search):
    file_dir = get_dir_from_search_str(url_search)
    if values:
        loadJson = LoadStatJson(file_dir)
        Total_reads, Barcode_Mapping, UnMapping, Clean_reads, Filter_reads, Reference_Mapping_reads, \
        Unique_Mapped_Reads, Multi_Mapping_Reads, Chimeric_Reads, Unmapping_Read, Umi_Filter_Reads, \
        Too_Short_Reads, Too_Long_Reads, Too_Many_N_Reads, Low_Quality_Reads, DuPlication_Reads, \
        Unique_Reads, Fail_Filter, Raw_Reads, mapped_reads, \
        Q10_Barcode,Q20_Barcode,Q30_Barcode,Q10_UMI,Q20_UMI,Q30_UMI,\
        Exonic, Intronic, Intergenic, Transcriotome, Antisense,\
        Input_read, Uniquely_Mapped_Read, Multi_Mapping_Read, RNA_Unmapping_Read, Chimeric_Read = loadJson.getReadsStatData(values)

        return number2human(Total_reads), number2human(Barcode_Mapping), number2human(Clean_reads), number2human(Reference_Mapping_reads), \
            number2human(Total_reads),Q30_Barcode,Q30_UMI,number2human(Input_read), number2human(Uniquely_Mapped_Read), number2human(Multi_Mapping_Read),\
            number2human(RNA_Unmapping_Read), number2human(Chimeric_Read), number2human(Exonic), number2human(Intronic),\
            number2human(Intergenic), number2human(Transcriotome), number2human(Antisense)
    else:
        return '','','','','','','','','',''
