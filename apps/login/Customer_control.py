import dash
import re
import time
import pandas as pd
from datetime import date

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from spatialTrancriptomeReport import app
from apps.db.tableService.OrderForm import Orders
from apps.db.tableService.OrderStatus import OrderStatus
from apps.login.notificationEmail import Send_email

class CustomerControl():
    def __init__(self, searchstatus='',Orderid='',ChipPlatType='',DateStart=None,DateEnd=None,page_count=1,PAGE_SIZE=5):
        self.searchstatus = searchstatus
        self.Orderid = Orderid
        self.ChipPlatType = ChipPlatType
        self.DateStart = DateStart
        self.DateEnd = DateEnd
        self.page_count = page_count
        self.PAGE_SIZE = PAGE_SIZE
        self.orders = Orders()
        self.orderstatus = OrderStatus()
        self.allstatus = self.orderstatus.getAllStatus()
        self.data = self.orders.getAllData().loc[:,['OrderID','ChipPlat','Quantity','ContactName','CurrentStatus','NextStatus','CreateTime','isdelete']]
        self.statusDict2Name = {}
        self.statusDict2ID = {}
        for self.eachstatus in self.allstatus.iloc:
            self.statusDict2ID[self.eachstatus['OrderStatusName']] = self.eachstatus['OrderStatusID']
            self.statusDict2Name[self.eachstatus['OrderStatusID']] = self.eachstatus['OrderStatusName']

    def data_get(self, status, searchstatus='',Orderid='',ChipPlatType='',DateStart=None,DateEnd=None):
        self.data = self.data[self.data['isdelete']==False]
        if status == 'all_order':
            self.data = self.data
        elif status == 'search':
            self.data = self.orders.getDataBySearch(searchstatus,Orderid,ChipPlatType,DateStart,DateEnd).loc[:,['OrderID','ChipPlat','Quantity','ContactName','CurrentStatus','NextStatus','CreateTime','isdelete']]
            self.data = self.data[self.data['isdelete']==False]
        else:
            self.data = self.data[self.data['CurrentStatus']==self.statusDict2ID[status.replace('_',' ')]]
        # print(self.data)
        return self.data

    def tableShown(self, data, Orderid='',ChipPlatType='',DateStart=None,DateEnd=None,page_count=1,PAGE_SIZE=5):
        self.Orderid = Orderid
        self.ChipPlatType = ChipPlatType
        self.DateStart = DateStart
        self.DateEnd = DateEnd
        self.page_count = page_count
        self.PAGE_SIZE = PAGE_SIZE
        self.data = data
        Tbody = []
        row_nums = self.data.shape[0]
        if row_nums/self.PAGE_SIZE == 0:
            total_page_num = 1
        elif row_nums/self.PAGE_SIZE > row_nums//self.PAGE_SIZE:
            total_page_num = row_nums//self.PAGE_SIZE + 1
        elif row_nums/self.PAGE_SIZE == row_nums//self.PAGE_SIZE:
            total_page_num = row_nums//self.PAGE_SIZE

        for i in self.data.iloc[int(self.PAGE_SIZE*int(self.page_count))-self.PAGE_SIZE:int(self.PAGE_SIZE*int(self.page_count))].iloc:
            OrderID=i['OrderID']; Quantity = i['Quantity']; ChipPlat=i['ChipPlat']; ContactName=i['ContactName']
            CurrentStatus=self.statusDict2Name[i['CurrentStatus']]; NextStatus=self.statusDict2Name[i['NextStatus']]; CreateTime=i['CreateTime']
            
            Tbody.append(html.Tr([html.Td(OrderID), html.Td(ChipPlat), html.Td(Quantity), html.Td(ContactName),
                html.Td(id={'type':'custo_CurrentStatus_td','index':f'{OrderID}_CurrentStatus'},children=CurrentStatus), 
                html.Td(id={'type':'custo_NextStatus_td','index':f'{OrderID}_NextStatus'},children=NextStatus), html.Td(CreateTime), 
                html.Td([html.Div([
                    html.Ul(className='operation',children=[
                        html.Li([
                            dbc.Button(children=['Detail'],href=f'/Customer_console/detail/?orderID={OrderID}',
                                color="link",
                                id=f'custo_{OrderID}_detail',className='collapse-type'),
                            html.I('|',className='cut-off-rule'),
                            dbc.Button(children=['DataManager'],href=f'/Customer_console/DataManager/?orderID={OrderID}',
                                color="link",className='collapse-type'),
                            html.I('|',className='cut-off-rule'),
                            dbc.Button(children=['Modify'],href=f'/Customer_console/Modify_order/?orderID={OrderID}',
                                color="link",className='a-type collapse-type',
                                id={'type':"custo_modify",'index':f'{OrderID}_status'}),
                            html.I('|',className='cut-off-rule'),
                            dbc.Button(children=['Cancel'],className='a-type collapse-type',color="link ",
                                id={'type':"custo_cancel",'index':f'{OrderID}_cancel'}),
                            dbc.Modal([
                                dbc.ModalHeader(["Cancel the orders"]),
                                dbc.ModalBody(["Are you sure to cancel the order ", html.B(OrderID), "?"]),
                                dbc.ModalFooter([
                                    dbc.Button("Confirm", 
                                        id={'type':"custo_cancel_confirm_button",'index':f"{OrderID}_cancel_confirm"}, className="ml-auto all-button"),
                                    dbc.Button("Cancel", 
                                        id={'type':"custo_cancel_close_button",'index':f"{OrderID}_cancel_close"}, className="ml-auto maginRight all-button")]
                                    ),
                                ],
                                id={'type':"custo_cancel_model",'index':f"{OrderID}_cancel_modal"},
                                centered=True,
                            ),
                            ])
                        ])
                    ])])]),)

        layout = html.Div(className='content',children=[
                        html.Div(className='operation',children=[
                            html.Div(className='search-word',children=[
                                html.Label('Order ID:',className='label_font_size'),
                                dcc.Input(id='custo_search_order_id',
                                        type='text',
                                        className="input_class",
                                        minLength= 8,
                                        maxLength= 25,
                                        value=self.Orderid,
                                        placeholder='Enter Order ID',)
                                ]),
                            html.Div(className='search-word',children=[
                                html.Label('Chip Plat:',className='label_font_size'),
                                dcc.Input(id='custo_search_order_type',
                                        type='text',
                                        className="input_class",
                                        minLength= 8,
                                        maxLength= 25,
                                        value=self.ChipPlatType,
                                        placeholder='Enter Order Type',)
                                ]),
                            html.Div(className='search-word',children=[
                                html.Label('Order Date:',className='label_font_size'),
                                dcc.DatePickerRange(
                                        id='custo_search_date',
                                        display_format='YYYY-MM-DD',
                                        className='date_input_class',
                                        clearable=True,
                                        start_date=self.DateStart,
                                        end_date = self.DateEnd,
                                    )
                                ]),
                            html.Div(className='search-word',children=[
                                dbc.Button(children=['Search'],id='custo_search_button',
                                    className='search-button'),
                                ]),
                            ]),
                            html.Div(children=[
                                        html.Div(className='gridtable',children=[
                                            html.Table(className='aps-table aps-ani-transition aps-widget order_form',children=[
                                                html.Thead(
                                                    html.Tr([html.Th('OrderID'),html.Th('ChipPlat'),html.Th('Quantity'),html.Th('ContactName'),
                                                        html.Th('CurrentStatus'),html.Th('NextStatus'),html.Th('CreateTime'),html.Th('Operation')])),
                                                html.Tbody(Tbody)
                                            ]),
                                            html.Div(className='row previous-next-container', children=[
                                                dbc.Button(className='all-button',children=['First'],id='custo_first_page', disabled=True),
                                                dbc.Button(className='all-button',children=['Prev'],id='custo_previous_page', disabled=True),
                                                dcc.Input(id='custo_page_number',
                                                        type='text',
                                                        className="page-input",
                                                        pattern = '^[0-9]*$',
                                                        value=1,),
                                                html.I('/',className='page-off',id = 'custo_page_off'),
                                                html.Div(total_page_num,id='custo_total_page_num',className='total-page-num'),
                                                
                                                dbc.Button(className='all-button',children=['Next'],id='custo_next_page'),
                                                dbc.Button(className='all-button',children=['Last'],id='custo_last_page'),
                                                dcc.Dropdown(
                                                    id = 'custo_page_size',
                                                    options=[{'label': v, 'value': v} for v in [1,2,5,10,20,50]],
                                                    value=self.PAGE_SIZE,
                                                    clearable=False,
                                                    className= 'page-size-select',
                                                    ),
                                                html.I('/',className='page-off'),
                                                html.Div('page',className='each-page-num'),

                                            ])
                                        ]),
                                    ]), 
                    ])

        return layout

    def bodycontent(self):
        menus = [html.A(id = {'index':'all_order','type':'custo_menus_id'},
            href='#all_order',
            children=[html.P(className='icon'),'All Order'],className="active text"),]
        for i in self.statusDict2Name.values():
            if i == '' or i == 'end':
                continue
            else:
                ii = i.replace(' ','_')
                single_mennu = html.A(id = {'index':ii,'type':'custo_menus_id'},
                    href=f'#{ii}',
                    children=[html.P(className='icon'), i],className="text")
                menus.append(single_mennu)
        menus.append(html.A(id = {'index':'end','type':'custo_menus_id'},
            href='#end',
            children=[html.P(className='icon'),"Finish Order"],className="text "))

        return html.Form(className='con',children=[
                    html.Div(className='row',children=[
                        html.Div(className='col-md-2 col-xs-4',children=[
                            dbc.Card(
                                dbc.CardBody([
                                        dbc.Navbar(className='brand',children=[dbc.NavbarBrand('Order review',className='box-style-left')]),
                                        html.Div(className='mennu',children=menus
                                        )
                                    ]),className='side'
                                ),
                            ]),
                        html.Div(id='custo_order_table',className='col-md-10 col-xs-8',children=self.tableShown(self.data),
                            )
                        ]),
                    ])

    def Headcontent(self):
        return dbc.Navbar([
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
                    )

    def Managelayout(self):
        return html.Div(id= 'custo_main_div',children=[self.Headcontent(),self.bodycontent()])


@app.callback(
    [Output({'type':"custo_modify",'index':ALL}, "disabled"),
    Output({'type':"custo_cancel",'index':ALL}, "disabled"),],
    [Input({'type':"custo_modify",'index':ALL}, "id"),
    ]
)
def status_button_disabled(status_id):
    orders = Orders()
    res_status = []
    res_cancel = []
    for each_status_id in status_id:
        order_id = each_status_id['index'].split('_status')[0]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if CurrentStatus <= 3 and CurrentStatus != -1:
            res_status.append(False)
            res_cancel.append(False)
        elif CurrentStatus == -1:
            res_status.append(True)
            res_cancel.append(True)
        else:
            res_status.append(True)
            res_cancel.append(True)
    return res_status,res_cancel


@app.callback(
    Output({'type':"custo_cancel_model",'index':ALL}, "is_open"),
    [Input({'type':"custo_cancel",'index':ALL}, "n_clicks"),
    Input({'type':"custo_cancel_confirm_button",'index':ALL}, "n_clicks"),
    Input({'type':"custo_cancel_close_button",'index':ALL}, "n_clicks")],
    [State({'type':"custo_cancel",'index':ALL}, "id"),
    State({'type':"custo_cancel_model",'index':ALL}, "is_open")]
)
def change_cancel_button(status_click, status_confirm, status_close, status_id, status_modal):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    for index in range(len(status_id)):
        order_id = status_id[index]['index'].split('_cancel')[0]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_cancel","type":"custo_cancel"}.n_clicks' or dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_cancel_close","type":"custo_cancel_close_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_cancel_confirm","type":"custo_cancel_confirm_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
    return status_modal

@app.callback(
    Output('custo_main_div','children'),
    [Input({'type':"custo_cancel_confirm_button",'index':ALL},'n_clicks'),],
    [State({'type':"custo_cancel",'index':ALL}, "id"),
    State({'type':"custo_cancel",'index':ALL},'children')
    ]
    )
def cancel_order(n_clicks,status_id,custo_cancel):
    # print(dash.callback_context.triggered)
    if not dash.callback_context.triggered or not dash.callback_context.triggered[0]['value']:
        raise PreventUpdate
    customercontrol = CustomerControl()
    for index in range(len(status_id)):
        order_id = status_id[index]['index'].split('_cancel')[0]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_cancel_confirm","type":"custo_cancel_confirm_button"}.n_clicks':
            order = Orders(order_id)
            order.updateByisdelete(True)

    return customercontrol.Headcontent(),customercontrol.bodycontent() 


@app.callback(
        Output({'type':"custo_menus_id",'index':ALL},'className'),
        [Input('url','hash')],
        )
def change_menus_class(url_hash):
    click_status_propid = url_hash.strip('#')
    # 读取数据库状态表，并转换为以状态名为key的字典，字典value值为菜单的className
    statusDict = {'all_order':'text'}
    orderstatus = OrderStatus()
    allstatus = orderstatus.getAllStatus()
    for eachstatus in allstatus.iloc:
        if eachstatus['OrderStatusName'] == 'end' or eachstatus['OrderStatusName'] == '' :
            continue
        else:
            statusDict[eachstatus['OrderStatusName'].replace(' ','_')] = 'text'
    statusDict['end'] = 'text'
    if not url_hash:
        return [statusDict[i] for i in statusDict]
    elif click_status_propid in statusDict:
        statusDict[click_status_propid] = 'active text'

    return [statusDict[i] for i in statusDict]


@app.callback(
    [
    Output('custo_order_table','children'),
    Output('custo_page_number','value'),
    ],
    [
    Input('url','hash'),
    Input('custo_search_button','n_clicks'),
    Input('custo_first_page','n_clicks'),
    Input('custo_previous_page','n_clicks'),
    Input('custo_next_page','n_clicks'),
    Input('custo_last_page','n_clicks'),
    Input('custo_search_order_id','n_submit'),
    Input('custo_search_order_type','n_submit'),
    Input('custo_search_date','n_submit'),
    Input('custo_page_number','n_submit'),
    Input('custo_page_size','value'),
    ],
    [State('custo_search_order_id','value'),
    State('custo_search_order_type','value'),
    State('custo_search_date','start_date'),
    State('custo_search_date','end_date'),
    State('custo_page_number','value'),
    State('custo_total_page_num','children'),
    State('url','href')]
    )
def table_shown(url_hash,search_button,first_page,previous_page,next_page,last_page,\
    search_order_id_submit,search_order_type_submit,search_date_submit,page_number_submit,page_size,\
    search_order_id,search_order_type,search_start_date,search_end_date,page_number,total_page_num,url_href):
    # print(dash.callback_context.triggered)
    if not url_hash:
        if url_href.split('/')[-1].strip('#') == 'Customer_console':
            current_status = 'all_order'
        else:
            raise PreventUpdate
    else:
        current_status = url_hash.strip('#')
    customercontrol = CustomerControl()
    if not re.search(r'^[0-9]*$',str(page_number)):
        page_number = 1
    else:
        page_number = int(page_number)
    data = customercontrol.data_get(current_status)

    if dash.callback_context.triggered[0]['prop_id'] == 'custo_search_button.n_clicks' or\
        dash.callback_context.triggered[0]['prop_id'] == 'custo_search_order_id.n_submit' or\
        dash.callback_context.triggered[0]['prop_id'] == 'custo_search_order_type.n_submit' or\
        dash.callback_context.triggered[0]['prop_id'] == 'custo_search_date.n_submit':
        data = customercontrol.data_get('search',current_status,search_order_id,search_order_type,search_start_date,search_end_date)
        page_number = 1
    
    if search_order_id or search_order_type or search_start_date or search_end_date and \
    dash.callback_context.triggered[0]['prop_id'] != 'url.hash':
        data = customercontrol.data_get('search',current_status,search_order_id,search_order_type,search_start_date,search_end_date)
    
    if dash.callback_context.triggered[0]['prop_id'] == 'url.hash'\
    or dash.callback_context.triggered[0]['prop_id'] == 'custo_first_page.n_clicks'\
    or dash.callback_context.triggered[0]['prop_id'] == 'custo_page_size.value':
        page_number = 1
        # data = customercontrol.data_get(current_status)
        # search_order_id,search_order_type,search_start_date,search_end_date = '','',None,None

    if dash.callback_context.triggered[0]['prop_id'] == 'custo_previous_page.n_clicks':
        if page_number <= 1:
            page_number = 1
        else:
            page_number -= 1
    if dash.callback_context.triggered[0]['prop_id'] == 'custo_next_page.n_clicks':
        if page_number >= total_page_num:
            page_number = total_page_num
        else:
            page_number += 1
    if dash.callback_context.triggered[0]['prop_id'] == 'custo_last_page.n_clicks':
        page_number = int(total_page_num)
    if dash.callback_context.triggered[0]['prop_id'] == 'custo_page_number.n_submit':
        if page_number > int(total_page_num):
            page_number = int(total_page_num)
        elif page_number < 1:
            page_number = 1
    return customercontrol.tableShown(data=data,page_count=page_number,Orderid=search_order_id,ChipPlatType=search_order_type,\
        DateStart=search_start_date,DateEnd=search_end_date,PAGE_SIZE=page_size),page_number

@app.callback(
    [Output('custo_first_page','disabled'),
    Output('custo_previous_page','disabled'),
    Output('custo_next_page','disabled'),
    Output('custo_last_page','disabled'),],
    [Input('custo_page_number','value')],
    [State('custo_total_page_num','children')])
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

