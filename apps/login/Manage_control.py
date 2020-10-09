import dash
import re
import pandas as pd

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from spatialTrancriptomeReport import app



Managelayout =html.Div([
            dbc.Navbar([  
    
                    html.Div(className='col-md-2',children=[
                        html.A(               
                            dbc.NavbarBrand("Stereo", className="ml-3 text-center"),                            
                    href="#",
                    ),]),
                    html.Div(className='col-md-2 offset-md-8',children=[
                        html.Div(className='dropdown',children=[
                            html.A(children=["Notifications",dbc.Badge(children=['4'],color = 'light',className='ml-1')],id = 'Notifications',href='#'),
                            html.Div(className='dropdown-content',children=[
                                html.A(children=['sssss'],href='#'),
                                html.A(children=['sssss'],href='/')
                                ])
                            ]),   
                        ]),           
                ],
                color='#153057',
                dark=True,
                className='row'
                ),
            html.Form(className='con',children=[
                html.Div(className='row',children=[
                    html.Div(className='col-md-2',children=[
                        dbc.Card(
                            dbc.CardBody([
                                    dbc.Navbar(className='brand',children=[dbc.NavbarBrand('Order review',className='box-style-left')]),
                                    html.Div(className='mennu',children=[
                                        html.Li(id = 'all_order',children=[html.P(className='icon'),'All Order'],className="active text"),
                                        html.Li(id = 'need_check_order',children=[html.P(className='icon'),'Need Check Order'],className="text "),
                                        html.Li(id = 'checked_order',children=[html.P(className='icon'),"Checked Order"],className="text "),
                                        html.Li(id = 'runing_order',children=[html.P(className='icon'),"Runing Order"],className="text "),
                                        html.Li(id = 'finish_order',children=[html.P(className='icon'),"Finish Order"],className="text "),
                                        html.Li(id = 'refused_order',children=[html.P(className='icon'),"Refused Prder"],className="text "),
                                    ])
                                ]),className='side'
                            ),
                        ]),
                    html.Div(className='col-md-10',children=[
                                html.Div(className='content',children=[
                                    html.Div(className='search-word',children=[
                                        html.Label('Order ID:',className='label_font_size'),
                                        dcc.Input(id='order_id',
                                                type='text',
                                                className="input_class",
                                                minLength= 8,
                                                maxLength= 25,
                                                value='',
                                                placeholder='Enter Order ID',)
                                        ]),
                                    html.Div(className='search-word',children=[
                                        html.Label('Order Type:',className='label_font_size'),
                                        dcc.Input(id='order_type',
                                                type='text',
                                                className="input_class",
                                                minLength= 8,
                                                maxLength= 25,
                                                value='',
                                                placeholder='Enter Order Type',)
                                        ]),
                                    html.Div(className='search-word',children=[
                                        html.Label('Order Date:',className='label_font_size'),
                                        dcc.DatePickerSingle(
                                                id='my-date-picker-single',
                                                display_format='YYYY-MM-DD',
                                                className='input_class'
                                            )
                                        ]),
                                    html.Button(children=['Search'],id='search_button',type='button')

                                    ]),
                                html.Table()
                        ])
                    ]),
                ])
])

@app.callback(
    [Output('all_order','className'),
    Output('need_check_order','className'),
    Output('checked_order','className'),
    Output('runing_order','className'),
    Output('finish_order','className'),
    Output('refused_order','className'),
    ],
    [Input('all_order','n_clicks'),
    Input('need_check_order','n_clicks'),
    Input('checked_order','n_clicks'),
    Input('runing_order','n_clicks'),
    Input('finish_order','n_clicks'),
    Input('refused_order','n_clicks'),]
    )
def active_change(all_order,need_check_order,checked_order,runing_order,finish_order,refused_order):
    if not all_order and not need_check_order and not checked_order and not runing_order and not finish_order and not refused_order:
        raise PreventUpdate
    if dash.callback_context.triggered[0]['prop_id'] == 'all_order.n_clicks':
        return "active text",'text','text','text','text','text'
    if dash.callback_context.triggered[0]['prop_id'] == 'need_check_order.n_clicks':
        return 'text',"active text",'text','text','text','text'
    if dash.callback_context.triggered[0]['prop_id'] == 'checked_order.n_clicks':
        return 'text',"text",'active text','text','text','text'
    if dash.callback_context.triggered[0]['prop_id'] == 'runing_order.n_clicks':
        return 'text',"text",'text','active text','text','text'
    if dash.callback_context.triggered[0]['prop_id'] == 'finish_order.n_clicks':
        return 'text',"text",'text','text','active text','text'
    if dash.callback_context.triggered[0]['prop_id'] == 'refused_order.n_clicks':
        return 'text',"text",'text','text','text','active text'
