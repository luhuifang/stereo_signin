import dash
import re
import pandas as pd

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from spatialTrancriptomeReport import app
from apps.db.tableService.OrderForm import Orders

def detial_page(order_id):
    orders = Orders()
    data = orders.getDataByOrderID(order_id)
    statusDict = {8:'',1:'Check pending',2:'Verified',3:'Unpaid',4:'Paid',5:'Wait for production',6:'In production',7:'assigned',-1:'end'}
    layout = html.Div([
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
            dbc.Navbar([
                html.H5(f'Detail/{order_id}')
                ],className='top-bar'),
            html.Div(className='container',children=[
                html.Div(className='col',children=[
                html.H6('Order Informarion',className='header-format'),
                detial_page_content('OrderID',data.iloc[0]['OrderID']),
                detial_page_content('LoginName',data.iloc[0]['LoginName']),
                detial_page_content('ChipPlat',data.iloc[0]['ChipPlat']),
                detial_page_content('Quantity',data.iloc[0]['Quantity']),
                detial_page_content('ContractNo',data.iloc[0]['ContractNo']),
                detial_page_content('CreateTime',data.iloc[0]['CreateTime']),
                html.H6('Customer Information',className='header-format'),
                detial_page_content('ContactName',data.iloc[0]['ContactName']),
                detial_page_content('Phone',data.iloc[0]['Phone']),
                detial_page_content('Email',data.iloc[0]['Email']),
                detial_page_content('Address',data.iloc[0]['Address']),
                detial_page_content('ZipCode',data.iloc[0]['ZipCode']),
                detial_page_content('Organization',data.iloc[0]['Organization']),
                detial_page_content('ResearchInterests',data.iloc[0]['ResearchInterests']),
                html.H6('Status Information',className='header-format'),
                detial_page_content('CurrentStatus',statusDict[data.iloc[0]['CurrentStatus']]),
                detial_page_content('NextStatus',statusDict[data.iloc[0]['NextStatus']]),
                detial_page_content('Accessory',data.iloc[0]['Accessory']),
                    ]),
            html.Div(className='text-center',children=[
                dbc.Button("Confirm to next status", id = f'cofirm_{order_id}_button',color="light", className="mr-1 all-button"),
                dbc.Modal([
                        dbc.ModalHeader("Confirm to next status"),
                        dbc.ModalBody(["Are you sure to change the order ", html.B(order_id), " to next status?"]),
                        dbc.ModalFooter([
                            dbc.Button("Confirm", id=f"{order_id}_status_confirm_button", className="ml-auto"),
                            dbc.Button("Cancel", id=f"{order_id}_status_close_button", className="ml-auto maginRight")]
                            ),],id=f"{order_id}_status_detail_modal", centered=True,),
                dbc.Button("End", color="light", id = f'end_{order_id}_button', className="mr-1 all-button"),
                dbc.Modal([
                        dbc.ModalHeader(["End the orders"]),
                        dbc.ModalBody(["Are you sure to end the order ", html.B(order_id), "?"]),
                        dbc.ModalFooter([
                            dbc.Button("Confirm", id=f"{order_id}_end_confirm_button", className="ml-auto "),
                            dbc.Button("Cancel", id=f"{order_id}_end_close_button", className="ml-auto maginRight")]
                            ),],id=f"{order_id}_end_detail_modal",centered=True,),
                dbc.Button("Back", color="light", id = f'back_{order_id}_button', className="mr-1 all-button",href='/Manage_coltrol'),
                ])]),
        ])
    return layout

def detial_page_content(fieldName,content):
    layout = html.Div(className='row',children=[
                html.Div(className='col-md-6 text-right',children=[
                    html.A(fieldName+':')
                    ]),
                html.Div(className='col-md-6 text-left',children=[
                    html.A(content)
                    ])
                ])
    return layout

def tableShown(status,search1='',search2='',search3='',page_count=1):
    orders = Orders()
    PAGE_SIZE = 1
    Tbody = ''
    statusDict = {8:'',1:'Check pending',2:'Verified',3:'Unpaid',4:'Paid',5:'Wait for production',6:'In production',7:'assigned',-1:'end'}
    if status == 'all_order':
        data = orders.getAllData().loc[:,['OrderID','ChipPlat','Quantity','ContactName','CurrentStatus','NextStatus','CreateTime']]
    elif status == 'search':
        data = orders.getDataBySearch(search1,search2,search3).loc[:,['OrderID','ChipPlat','Quantity','ContactName','CurrentStatus','NextStatus','CreateTime']]
    else:
        data = orders.getDataByStatus(status).loc[:,['OrderID','ChipPlat','Quantity','ContactName','CurrentStatus','NextStatus','CreateTime']]
    row_nums = data.shape[0]
    if row_nums/PAGE_SIZE == 0:
        page_num = 1
    elif row_nums/PAGE_SIZE > row_nums//PAGE_SIZE:
        page_num = row_nums//PAGE_SIZE + 1
    elif row_nums/PAGE_SIZE == row_nums//PAGE_SIZE:
        page_num = row_nums//PAGE_SIZE
    for i in data.iloc[int(PAGE_SIZE*int(page_count))-PAGE_SIZE:int(PAGE_SIZE*int(page_count))].iloc:
        Tbody += '''html.Tr([html.Td('{OrderID}'), html.Td('{ChipPlat}'), html.Td('{Quantity}'), html.Td('{ContactName}')
        , html.Td('{CurrentStatus}'), html.Td('{NextStatus}'), html.Td('{CreateTime}'), 
        html.Td([html.Div([
            html.Ul(className='operation',children=[
                html.Li([
                    dbc.Button(children=['Detail'],href='/Manage_coltrol/detail/?orderID={OrderID}',color="link",id='{OrderID}_detail',className='collapse-type'),
                    html.I('|',className='cut-off-rule',id='{OrderID}_cut_status'),
                    dbc.Button(children=['Confirm to next status'],color="link",className='a-type collapse-type',id='{OrderID}_status'),
                    dbc.Modal([
                        dbc.ModalHeader("Confirm to next status"),
                        dbc.ModalBody(["Are you sure to change the order ", html.B({OrderID}), " to next status?"]),
                        dbc.ModalFooter([
                            dbc.Button("Confirm", id="{OrderID}_status_confirm", className="ml-auto"),
                            dbc.Button("Cancel", id="{OrderID}_status_close", className="ml-auto maginRight")]
                            ),
                        ],
                        id="{OrderID}_status_modal",
                        centered=True,
                    ),
                    html.I('|',className='cut-off-rule',id='{OrderID}_cut_end'),
                    dbc.Button(children=['End'],className='a-type collapse-type',color="link ",id='{OrderID}_end'),
                    dbc.Modal([
                        dbc.ModalHeader(["End the orders"]),
                        dbc.ModalBody(["Are you sure to end the order ", html.B({OrderID}), "?"]),
                        dbc.ModalFooter([
                            dbc.Button("Confirm", id="{OrderID}_end_confirm", className="ml-auto "),
                            dbc.Button("Cancel", id="{OrderID}_end_close", className="ml-auto maginRight")]
                            ),
                        ],
                        id="{OrderID}_end_modal",
                        centered=True,
                    ),
                    ])
                ])
            ])])]),'''.format(OrderID=i['OrderID'],Quantity = i['Quantity'],ChipPlat=i['ChipPlat'],ContactName=i['ContactName'],CurrentStatus=statusDict[i['CurrentStatus']],NextStatus=statusDict[i['NextStatus']],CreateTime=i['CreateTime'])

    layout = html.Div(className='gridtable',children=[
        html.Table(className='aps-table aps-ani-transition aps-widget order_form',children=[
            html.Thead(
                html.Tr([html.Th('OrderID'),html.Th('ChipPlat'),html.Th('Quantity'),html.Th('ContactName'),
                    html.Th('CurrentStatus'),html.Th('NextStatus'),html.Th('CreateTime'),html.Th('Operation')])),
            eval('html.Tbody(['+ Tbody +'])')
        ]),
        html.Div(className='row previous-next-container', children=[
            dbc.Button(className='all-button',children=['first page'],id='first_page'),
            dbc.Button(className='all-button',children=['previous page'],id='previous_page'),
            dcc.Input(id='page_number',
                    type='text',
                    className="page-input",
                    value=1,),
            html.I('/',className='page-off',id = 'page_off',role=status),
            html.Div(page_num,id='total_page_num',className='total-page-num'),
            dbc.Button(className='all-button',children=['next page'],id='next_page'),
            dbc.Button(className='all-button',children=['last page'],id='last_page'),
            ])
        ],)

    return layout


Managelayout = html.Div(id= 'main_div',children=[
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
                                        html.Li(id = 'Unpaid',children=[html.P(className='icon'),"Unpaid"],className="text "),
                                        html.Li(id = 'Paid',children=[html.P(className='icon'),"Paid"],className="text "),
                                        html.Li(id = 'Wait_for_production',children=[html.P(className='icon'),"Wait for production"],className="text "),
                                        html.Li(id = 'In_production',children=[html.P(className='icon'),"In production"],className="text "),
                                        html.Li(id = 'assigned',children=[html.P(className='icon'),"Assigned"],className="text "),
                                        html.Li(id = 'finish_order',children=[html.P(className='icon'),"Finish Order"],className="text "),
                                        html.Li(id = 'refused_order',children=[html.P(className='icon'),"Refused Order"],className="text "),
                                    ])
                                ]),className='side'
                            ),
                        ]),
                    html.Div(className='col-md-10',children=[
                                html.Div(className='content',children=[
                                    html.Div(className='search-word',children=[
                                        html.Label('Order ID:',className='label_font_size'),
                                        dcc.Input(id='search_order_id',
                                                type='text',
                                                className="input_class",
                                                minLength= 8,
                                                maxLength= 25,
                                                value='',
                                                placeholder='Enter Order ID',)
                                        ]),
                                    html.Div(className='search-word',children=[
                                        html.Label('Order Type:',className='label_font_size'),
                                        dcc.Input(id='search_order_type',
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
                                                id='search_date',
                                                display_format='YYYY-MM-DD',
                                                className='input_class'
                                            )
                                        ]),
                                    dbc.Button(children=['Search'],id='search_button',className='all-button'),
                                    html.Div(id='order_table',children=tableShown('all_order'))
                                    ]),   
                        ])
                    ]),
                ])
])


def page_on_status(current_status,page_number,search_order_id,search_order_type,search_date):
    if current_status == 'all_order':
        return "active text",'text','text','text','text','text','text','text','text','text',tableShown('all_order',page_count=page_number),page_number
    if current_status == 'Check pending':
        return 'text',"active text",'text','text','text','text','text','text','text','text',tableShown('Check pending',page_count=page_number),page_number
    if current_status == 'Verified':
        return 'text',"text",'active text','text','text','text','text','text','text','text',tableShown('Verified',page_count=page_number),page_number
    if current_status == 'Unpaid':
        return 'text',"text",'text','active text','text','text','text','text','text','text',tableShown('Unpaid',page_count=page_number),page_number
    if current_status == 'Paid':
        return 'text',"text",'text','text','active text','text','text','text','text','text',tableShown('Paid',page_count=page_number),page_number
    if current_status == 'Wait for production':
        return 'text',"text",'text','text','text','active text','text','text','text','text',tableShown('Wait for production',page_count=page_number),page_number
    if current_status == 'In production':
        return 'text',"text",'text','text','text','text','active text','text','text','text',tableShown('In production',page_count=page_number),page_number
    if current_status == 'assigned':
        return 'text',"text",'text','text','text','text','text','active text','text','text',tableShown('assigned',page_count=page_number),page_number
    if current_status == 'end':
        return 'text',"text",'text','text','text','text','text','text','active text','text',tableShown('end',page_count=page_number),page_number
    if current_status == 'search':
        return 'text',"text",'text','text','text','text','text','text','text','text',tableShown('search',search_order_id,search_order_type,search_date,page_count=page_number),page_number

orders = Orders()
for each_orderid in orders.getAllData().loc[:,'OrderID']:
    @app.callback(
        [Output("{}_status".format(each_orderid), "disabled"),
        Output("{}_end".format(each_orderid), "disabled")],
        [Input("{}_status".format(each_orderid), "id")]
    )
    def operation_button(status_id):
        orders = Orders()
        order_id = status_id.split('_')[0]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if CurrentStatus != -1:
            return False, False
        else:
            return True, True

    @app.callback(
        Output("{}_status_modal".format(each_orderid), "is_open"),
        [Input("{}_status".format(each_orderid), "n_clicks"),
        Input("{}_status_confirm".format(each_orderid), "n_clicks"),
        Input("{}_status_close".format(each_orderid), "n_clicks")],
        [State("{}_status".format(each_orderid), "id"),
        State("{}_status_modal".format(each_orderid), "is_open")]
    )
    def operation_button(status_click, status_confirm, status_close, status_id, status_modal):
        if not status_click :
            raise PreventUpdate
        orders = Orders()
        order_id = status_id.split('_')[0]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if dash.callback_context.triggered[0]['prop_id'] == f'{order_id}_status.n_clicks' or dash.callback_context.triggered[0]['prop_id'] == f'{order_id}_status_close.n_clicks':
            return not status_modal
        if dash.callback_context.triggered[0]['prop_id'] == f'{order_id}_status_confirm.n_clicks':
            if CurrentStatus != 7 and NextStatus != 7:
                orders.updateCurrentStatus(CurrentStatus+1,order_id)
                orders.updateNextStatus(NextStatus+1,order_id)
            elif  NextStatus==7:
                orders.updateCurrentStatus(CurrentStatus+1,order_id)
                orders.updateNextStatus(-1,order_id)
            else:
                orders.updateCurrentStatus(-1,order_id)
                orders.updateNextStatus(8,order_id)
            return not status_modal
        
        return status_modal

    @app.callback(
        Output("{}_end_modal".format(each_orderid), "is_open"),
        [Input("{}_end".format(each_orderid), "n_clicks"),
        Input("{}_end_confirm".format(each_orderid), "n_clicks"),
        Input("{}_end_close".format(each_orderid), "n_clicks")],
        [State("{}_end".format(each_orderid), "id"),
        State("{}_end_modal".format(each_orderid), "is_open"),]
    )
    def operation_button( end_click, end_confirm, end_close, end_id, end_modal):
        if not end_click:
            raise PreventUpdate
        orders = Orders()
        order_id = end_id.split('_')[0]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if dash.callback_context.triggered[0]['prop_id'] == f'{order_id}_end.n_clicks' or dash.callback_context.triggered[0]['prop_id'] == f'{order_id}_end_close.n_clicks':
            return  not end_modal
        if dash.callback_context.triggered[0]['prop_id'] == f'{order_id}_end_confirm.n_clicks':
            orders.updateCurrentStatus(-1,order_id)
            orders.updateNextStatus(8,order_id)
            return not end_modal
        return end_modal

    @app.callback(
        Output("{}_status_detail_modal".format(each_orderid), "is_open"),
        [Input("cofirm_{}_button".format(each_orderid), "n_clicks"),
        Input("{}_status_confirm_button".format(each_orderid), "n_clicks"),
        Input("{}_status_close_button".format(each_orderid), "n_clicks")],
        [State("cofirm_{}_button".format(each_orderid), "id"),
        State("{}_status_detail_modal".format(each_orderid), "is_open")]
    )
    def operation_button(status_click, status_confirm, status_close, status_id, status_modal):
        if not status_click :
            raise PreventUpdate
        orders = Orders()
        order_id = status_id.split('_')[1]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if dash.callback_context.triggered[0]['prop_id'] == f'cofirm_{order_id}_button.n_clicks' or dash.callback_context.triggered[0]['prop_id'] == f'{order_id}_status_close_button.n_clicks':
            return not status_modal
        if dash.callback_context.triggered[0]['prop_id'] == f'{order_id}_status_confirm_button.n_clicks':
            if CurrentStatus != 7 and NextStatus != 7:
                orders.updateCurrentStatus(CurrentStatus+1,order_id)
                orders.updateNextStatus(NextStatus+1,order_id)
            elif  NextStatus == 7:
                orders.updateCurrentStatus(CurrentStatus+1,order_id)
                orders.updateNextStatus(-1,order_id)
            else:
                orders.updateCurrentStatus(-1,order_id)
                orders.updateNextStatus(8,order_id)
            return not status_modal
        
        return status_modal

    @app.callback(
        Output("{}_end_detail_modal".format(each_orderid), "is_open"),
        [Input("end_{}_button".format(each_orderid), "n_clicks"),
        Input("{}_end_confirm_button".format(each_orderid), "n_clicks"),
        Input("{}_end_close_button".format(each_orderid), "n_clicks")],
        [State("end_{}_button".format(each_orderid), "id"),
        State("{}_end_detail_modal".format(each_orderid), "is_open"),]
    )
    def operation_button( end_click, end_confirm, end_close, end_id, end_modal):
        if not end_click:
            raise PreventUpdate
        orders = Orders()
        order_id = end_id.split('_')[1]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if dash.callback_context.triggered[0]['prop_id'] == f'end_{order_id}_button.n_clicks' or\
         dash.callback_context.triggered[0]['prop_id'] == f'{order_id}_end_close_button.n_clicks':
            return  not end_modal
        if dash.callback_context.triggered[0]['prop_id'] == f'{order_id}_end_confirm_button.n_clicks':
            orders.updateCurrentStatus(-1,order_id)
            orders.updateNextStatus(8,order_id)
            return not end_modal
        return end_modal

@app.callback(
    [Output('all_order','className'),
    Output('need_check_order','className'),
    Output('checked_order','className'),
    Output('Unpaid','className'),
    Output('Paid','className'),
    Output('Wait_for_production','className'),
    Output('In_production','className'),
    Output('assigned','className'),
    Output('finish_order','className'),
    Output('refused_order','className'),
    Output('order_table','children'),
    Output('page_number','value'),
    ],
    [Input('all_order','n_clicks'),
    Input('need_check_order','n_clicks'),
    Input('checked_order','n_clicks'),
    Input('Unpaid','n_clicks'),
    Input('Paid','n_clicks'),
    Input('Wait_for_production','n_clicks'),
    Input('In_production','n_clicks'),
    Input('assigned','n_clicks'),
    Input('finish_order','n_clicks'),
    Input('refused_order','n_clicks'),
    Input('search_button','n_clicks'),
    Input('first_page','n_clicks'),
    Input('previous_page','n_clicks'),
    Input('next_page','n_clicks'),
    Input('last_page','n_clicks'),],
    [State('search_order_id','value'),
    State('search_order_type','value'),
    State('search_date','date'),
    State('page_number','value'),
    State('total_page_num','children'),
    State('page_off','role')]
    )
def active_change(all_order,need_check_order,checked_order,Unpaid,Paid,Wait_for_production,In_production,\
    assigned,finish_order,refused_order,search_button,first_page,previous_page,next_page,last_page,\
    search_order_id,search_order_type,search_date,page_number,total_page_num,current_status):
    page_number = int(page_number)
    orders = Orders()
    if not all_order and not need_check_order and not checked_order and not Unpaid and not Paid and not search_button\
    and not Wait_for_production and not In_production and not assigned and not finish_order and not refused_order and\
    not first_page and not previous_page and not next_page and not last_page:
        raise PreventUpdate
    if dash.callback_context.triggered[0]['prop_id'] == 'all_order.n_clicks':
        return "active text",'text','text','text','text','text','text','text','text','text',tableShown('all_order'),1
    if dash.callback_context.triggered[0]['prop_id'] == 'need_check_order.n_clicks':
        return 'text',"active text",'text','text','text','text','text','text','text','text',tableShown('Check pending'),1
    if dash.callback_context.triggered[0]['prop_id'] == 'checked_order.n_clicks':
        return 'text',"text",'active text','text','text','text','text','text','text','text',tableShown('Verified'),1
    if dash.callback_context.triggered[0]['prop_id'] == 'Unpaid.n_clicks':
        return 'text',"text",'text','active text','text','text','text','text','text','text',tableShown('Unpaid'),1
    if dash.callback_context.triggered[0]['prop_id'] == 'Paid.n_clicks':
        return 'text',"text",'text','text','active text','text','text','text','text','text',tableShown('Paid'),1
    if dash.callback_context.triggered[0]['prop_id'] == 'Wait_for_production.n_clicks':
        return 'text',"text",'text','text','text','active text','text','text','text','text',tableShown('Wait for production'),1
    if dash.callback_context.triggered[0]['prop_id'] == 'In_production.n_clicks':
        return 'text',"text",'text','text','text','text','active text','text','text','text',tableShown('In production'),1
    if dash.callback_context.triggered[0]['prop_id'] == 'assigned.n_clicks':
        return 'text',"text",'text','text','text','text','text','active text','text','text',tableShown('assigned'),1
    if dash.callback_context.triggered[0]['prop_id'] == 'finish_order.n_clicks':
        return 'text',"text",'text','text','text','text','text','text','active text','text',tableShown('end'),1
    if dash.callback_context.triggered[0]['prop_id'] == 'refused_order.n_clicks':
        return 'text',"text",'text','text','text','text','text','text','text','active text',tableShown('end'),1
    if dash.callback_context.triggered[0]['prop_id'] == 'search_button.n_clicks':
        return 'text',"text",'text','text','text','text','text','text','text','text',tableShown('search',search_order_id,search_order_type,search_date),1

    if dash.callback_context.triggered[0]['prop_id'] == 'first_page.n_clicks':
        page_number = 1
        return page_on_status(current_status,page_number,search_order_id,search_order_type,search_date)
    if dash.callback_context.triggered[0]['prop_id'] == 'previous_page.n_clicks':
        page_number -= 1
        return page_on_status(current_status,page_number,search_order_id,search_order_type,search_date)
    if dash.callback_context.triggered[0]['prop_id'] == 'next_page.n_clicks':
        page_number += 1
        return page_on_status(current_status,page_number,search_order_id,search_order_type,search_date)
    if dash.callback_context.triggered[0]['prop_id'] == 'last_page.n_clicks':
        page_number = int(total_page_num)
        return page_on_status(current_status,page_number,search_order_id,search_order_type,search_date)


@app.callback(
    [Output('first_page','disabled'),
    Output('previous_page','disabled'),
    Output('next_page','disabled'),
    Output('last_page','disabled'),],
    [Input('page_number','value')],
    [State('total_page_num','children')])
def change_page_button_status(page_number,total_page_num):
    total_page_num = int(total_page_num)
    if page_number == 1 and total_page_num !=1 :
        return True, True, False, False
    elif page_number == total_page_num !=1:
        return False, False, True, True
    elif page_number == total_page_num == 1:
        return True, True, True, True
    else:
        return False, False, False, False
