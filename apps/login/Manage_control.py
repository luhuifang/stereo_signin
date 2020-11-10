import dash
import re
import json
import hashlib
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
from apps.login.token_verification import get_payload,validate_token,create_token,veri_token


class ManagerControl():
    def __init__(self, searchstatus='',Orderid='',ChipPlatType='',DateStart=None,DateEnd=None,page_count=1,PAGE_SIZE=5):
        user_name,Is_true = veri_token()
        self.loginName = user_name
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
        self.data = self.orders.getAllData().loc[:,['OrderID','ChipPlat','Quantity','ContactName','CurrentStatus','NextStatus','CreateTime']]
        self.statusDict2Name = {}
        self.statusDict2ID = {}
        for self.eachstatus in self.allstatus.iloc:
            self.statusDict2ID[self.eachstatus['OrderStatusName']] = self.eachstatus['OrderStatusID']
            self.statusDict2Name[self.eachstatus['OrderStatusID']] = self.eachstatus['OrderStatusName']

    def data_get(self, status, searchstatus='',Orderid='',ChipPlatType='',DateStart=None,DateEnd=None):
        # self.data = self.orders.getAllData().loc[:,['OrderID','ChipPlat','Quantity','ContactName','CurrentStatus','NextStatus','CreateTime']]
        if status == 'all_order':
            self.data = self.data
        elif status == 'search':
            self.data = self.orders.getDataBySearch(searchstatus,Orderid,ChipPlatType,DateStart,DateEnd).loc[:,['OrderID','ChipPlat','Quantity','ContactName','CurrentStatus','NextStatus','CreateTime']]
        else:
            self.data = self.data[self.data['CurrentStatus']==self.statusDict2ID[status.replace('_',' ')]]
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
                html.Td(id={'type':'CurrentStatus_td','index':f'{OrderID}_CurrentStatus'},children=CurrentStatus),
                html.Td(id={'type':'NextStatus_td','index':f'{OrderID}_NextStatus'},children=NextStatus), 
                html.Td(CreateTime), 
                html.Td([html.Div([
                    html.Ul(className='operation',children=[
                        html.Li([
                            dbc.Button(children=['Detail'],color="link",
                                href=f'/Manager_console/detail/?orderID={OrderID}',
                                id={'type':'Detail_button','index':f'{OrderID}_detail'},className='collapse-type'),
                            html.I('|',className='cut-off-rule',id=f'{OrderID}_cut_status'),
                            dbc.Button(children=['Confirm to next status'],color="link",className='a-type collapse-type',
                                id={'type':"status",'index':f'{OrderID}_status'}),
                            dbc.Modal([
                                dbc.ModalHeader("Confirm to next status"),
                                dbc.ModalBody(["Are you sure to change the order ", html.B(OrderID), " to next status?"]),
                                dbc.ModalFooter([
                                    dbc.Button("Confirm", 
                                        id={'type':"status_confirm_button",'index':f"{OrderID}_status_confirm"}, className="ml-auto all-button"),
                                    dbc.Button("Cancel", 
                                        id={'type':"status_close_button",'index':f"{OrderID}_status_close"}, className="ml-auto maginRight all-button")]
                                    ),
                                ],
                                id={'type':"status_model",'index':f"{OrderID}_status_modal"},
                                centered=True,
                            ),
                            html.I('|',className='cut-off-rule',id=f'{OrderID}_cut_end'),
                            dbc.Button(children=['End'],className='a-type collapse-type',color="link ",
                                id={'type':"end",'index':f'{OrderID}_end'}),
                            dbc.Modal([
                                dbc.ModalHeader(["End the orders"]),
                                dbc.ModalBody(["Are you sure to end the order ", html.B(OrderID), "?"]),
                                dbc.ModalFooter([
                                    dbc.Button("Confirm", 
                                        id={'type':"end_confirm_button",'index':f"{OrderID}_end_confirm"}, className="ml-auto all-button"),
                                    dbc.Button("Cancel", 
                                        id={'type':"end_close_button",'index':f"{OrderID}_end_close"}, className="ml-auto maginRight all-button")]
                                    ),
                                ],
                                id={'type':"end_model",'index':f"{OrderID}_end_modal"},
                                centered=True,
                            ),
                            ])
                        ])
                    ])])]),)

        layout = html.Div(className='content',children=[
                        html.Div(className='operation',children=[
                            html.Div(className='search-word',children=[
                                html.Label('Order ID:',className='label_font_size'),
                                dcc.Input(id='search_order_id',
                                        type='text',
                                        className="input_class",
                                        minLength= 8,
                                        maxLength= 25,
                                        value=self.Orderid,
                                        placeholder='Enter Order ID',)
                                ]),
                            html.Div(className='search-word',children=[
                                html.Label('Chip Plat:',className='label_font_size'),
                                dcc.Input(id='search_order_type',
                                        type='text',
                                        className="input_class",
                                        minLength= 8,
                                        maxLength= 25,
                                        value=self.ChipPlatType,
                                        placeholder='Enter Chip Plat',)
                                ]),
                            html.Div(className='search-word',children=[
                                html.Label('Order Date:',className='label_font_size'),
                                dcc.DatePickerRange(
                                        id='search_date',
                                        display_format='YYYY-MM-DD',
                                        className='date_input_class',
                                        clearable=True,
                                        start_date=self.DateStart,
                                        end_date = self.DateEnd,
                                    )
                                ]),
                            html.Div(className='search-word',children=[
                                dbc.Button(children=['Search'],id='search_button',
                                    className='search-button'),
                                ]),
                            ]),
                            html.Div(children=[
                                        html.Div(className='',children=[
                                            html.Table(className='aps-table aps-ani-transition aps-widget order_form',children=[
                                                html.Thead(
                                                    html.Tr([html.Th('OrderID'),html.Th('ChipPlat'),html.Th('Quantity'),html.Th('ContactName'),
                                                        html.Th('CurrentStatus'),html.Th('NextStatus'),html.Th('CreateTime'),html.Th('Operation')])),
                                                html.Tbody(Tbody)
                                            ]),
                                            html.Div(className='row previous-next-container', children=[
                                                dbc.Button(className='all-button',children=['First'],id='first_page', disabled=True),
                                                dbc.Button(className='all-button',children=['Prev'],id='previous_page', disabled=True),
                                                dcc.Input(id='page_number',
                                                        type='text',
                                                        className="page-input",
                                                        value=1,
                                                        ),
                                                html.I('/',className='page-off',id = 'page_off'),
                                                html.Div(total_page_num,id='total_page_num',className='total-page-num'),
                                                
                                                dbc.Button(className='all-button',children=['Next'],id='next_page'),
                                                dbc.Button(className='all-button',children=['Last'],id='last_page'),
                                                dcc.Dropdown(
                                                    id = 'page_size',
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
 
    def manager_page(self):
        return html.Div(id='manager_login',children=[
                dbc.Navbar([
                        html.Div(className='col-md-2',children=[
                            html.A(               
                                dbc.NavbarBrand("Stereo", className="ml-3 text-center"),                            
                        href="/",
                        ),]),
                        html.Div(className='col-md-2 offset-md-6',children=[
                            html.Div(className='dropdown',children=[
                                html.A(children=["Notifications",dbc.Badge(children=['4'],color = 'light',className='ml-1')],id = 'Notifications',href='/'),
                                html.Div(className='dropdown-content',children=[
                                    html.A(children=['sssss'],href='/'),
                                    html.A(children=['sssss'],href='/')
                                    ]),
                                ]),   
                            ]), 
                         html.Div(className='col-md-3',id='customer_center',children=[
                            html.A(self.loginName,id='loginedName'),
                            dbc.Button('log off',color='link',id='manager_login_out')
                            ])           
                    ],
                    color='#153057',
                    dark=True,
                    className='row'
                    ),
                html.Div(id="page_body",children=self.Managelayout())
            ])

    def Managelayout(self):
        menus = [html.A(id = {'index':'all_order','type':'menus_id'},
            href='#all_order',
            children=[html.P(className='icon'),'All Order'],className="text"),]
        for i in self.statusDict2Name.values():
            if i == '' or i == 'end':
                pass
            else:
                ii = i.replace(' ','_')
                single_mennu = html.A(id = {'index':ii,'type':'menus_id'},
                    href=f'#{ii}',
                    children=[html.P(className='icon'), i],className="text")
                menus.append(single_mennu)
        menus.append(html.A(id = {'index':'end','type':'menus_id'},
            href='#end',
            children=[html.P(className='icon'),"Finish Order"],className="text"))
        return html.Div(id= 'main_div',children=[
                    html.Form(className='con',children=[
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
                            html.Div(id='order_table',className='col-md-10 col-xs-8',children=self.tableShown(self.data),
                                )
                            ]),
                        ])
                ])

    def loginOutSuccessfulLayout(self):
        return html.Div(className='findPassWd_content', children = [
            html.Span('Login out successful!'),
            html.Br(),
            dcc.Link('OK', href='/'),
        ])


@app.callback(
    [Output({'type':"status",'index':ALL}, "disabled"),
    Output({'type':"end",'index':ALL}, "disabled"),],
    [Input({'type':"status",'index':ALL}, "id"),
    ]
)
def status_button_disabled(status_id):
    orders = Orders()
    res_status = []
    res_end = []
    for each_status_id in status_id:
        order_id = each_status_id['index'].split('_status')[0]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if CurrentStatus != -1:
            res_status.append(False)
            res_end.append(False)
        else:
            res_status.append(True)
            res_end.append(True)
    return res_status,res_end


@app.callback(
    Output({'type':"status_model",'index':ALL}, "is_open"),
    [Input({'type':"status",'index':ALL}, "n_clicks"),
    Input({'type':"status_confirm_button",'index':ALL}, "n_clicks"),
    Input({'type':"status_close_button",'index':ALL}, "n_clicks")],
    [State({'type':"status",'index':ALL}, "id"),
    State({'type':"status_model",'index':ALL}, "is_open")]
)
def change_status_button(status_click, status_confirm, status_close, status_id, status_modal):
    for index in range(len(status_id)):
        order_id = status_id[index]['index'].split('_status')[0]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_status","type":"status"}.n_clicks' or dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_status_close","type":"status_close_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_status_confirm","type":"status_confirm_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
        
    return status_modal

@app.callback(
    [Output({'type':"CurrentStatus_td",'index':ALL}, "children"),
    Output({'type':"NextStatus_td",'index':ALL}, "children"),],
    [
    Input({'type':"status_confirm_button",'index':ALL}, "n_clicks"),
    Input({'type':"end_confirm_button",'index':ALL}, "n_clicks"),],
    [State({'type':"status",'index':ALL}, "id"),]
)
def change_td_status(status_confirm,end_confirm,status_id):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    currentstatus_res = []
    nextstatus_res = []
    statusDict2Name = {}
    orderstatus = OrderStatus()
    allstatus = orderstatus.getAllStatus()
    statusID_list = [eachstatus['OrderStatusID'] for eachstatus in allstatus.iloc][2:]
    last_status_id = statusID_list[-1]
    for eachstatus in allstatus.iloc:
        statusDict2Name[eachstatus['OrderStatusID']] = eachstatus['OrderStatusName']
    orders = Orders()
    for index in range(len(status_id)):
        order_id = status_id[index]['index'].split('_status')[0]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_status_confirm","type":"status_confirm_button"}.n_clicks':
            if CurrentStatus != last_status_id and NextStatus != last_status_id:
                CurrentStatus = int(statusID_list[statusID_list.index(CurrentStatus)+1])
                NextStatus = int(statusID_list[statusID_list.index(NextStatus)+1])
                orders.updateCurrentStatus(CurrentStatus,order_id)
                orders.updateNextStatus(NextStatus,order_id)
            elif  NextStatus == last_status_id:
                CurrentStatus = int(statusID_list[statusID_list.index(CurrentStatus)+1])
                NextStatus = -1
                orders.updateCurrentStatus(CurrentStatus,order_id)
                orders.updateNextStatus(-1,order_id)
            else:
                orders.updateCurrentStatus(-1,order_id)
                orders.updateNextStatus(-2,order_id)
                CurrentStatus = -1
                NextStatus = -2
            Send_email(order_id)
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_end_confirm","type":"end_confirm_button"}.n_clicks':
            orders.updateCurrentStatus(-1,order_id)
            orders.updateNextStatus(-2,order_id)
            CurrentStatus = -1
            NextStatus = -2
            Send_email(order_id)
        currentstatus_res.append(statusDict2Name[CurrentStatus])
        nextstatus_res.append(statusDict2Name[NextStatus])

    return currentstatus_res,nextstatus_res

@app.callback(
    Output({'type':"end_model",'index':ALL}, "is_open"),
    [Input({'type':"end",'index':ALL}, "n_clicks"),
    Input({'type':"end_confirm_button",'index':ALL}, "n_clicks"),
    Input({'type':"end_close_button",'index':ALL}, "n_clicks")],
    [State({'type':"end",'index':ALL}, "id"),
    State({'type':"end_model",'index':ALL}, "is_open")]
)
def change_end_button(status_click, status_confirm, status_close, status_id, status_modal):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    for index in range(len(status_id)):
        order_id = status_id[index]['index'].split('_end')[0]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_end","type":"end"}.n_clicks' or dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_end_close","type":"end_close_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_end_confirm","type":"end_confirm_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
    return status_modal


@app.callback(
    [Output('order_table','children'),
    Output('page_number','value'),
    ],
    [Input('url','hash'),
    Input('search_button','n_clicks'),
    Input('first_page','n_clicks'),
    Input('previous_page','n_clicks'),
    Input('next_page','n_clicks'),
    Input('last_page','n_clicks'),
    Input('search_order_id','n_submit'),
    Input('search_order_type','n_submit'),
    Input('search_date','n_submit'),
    Input('page_number','n_submit'),
    Input('page_size','value'),
    ],
    [State('search_order_id','value'),
    State('search_order_type','value'),
    State('search_date','start_date'),
    State('search_date','end_date'),
    State('page_number','value'),
    State('total_page_num','children'),
    State('url','href')
    ]
    )
def shown_table(url_hash,search_button,first_page,previous_page,next_page,last_page,\
    search_order_id_submit,search_order_type_submit,search_date_submit,page_number_submit,page_size,\
    search_order_id,search_order_type,search_start_date,search_end_date,page_number,total_page_num,url_href):
    print(dash.callback_context.triggered)
    if not url_hash:
        if url_href.split('/')[-1].strip('#') == 'Manager_console':
            current_status = 'all_order'
        else:
            raise PreventUpdate
    else:
        current_status = url_hash.strip('#')
    managercontrol = ManagerControl()
    page_number = int(page_number)
    data = managercontrol.data_get(current_status)

    if dash.callback_context.triggered[0]['prop_id'] == 'search_button.n_clicks' or\
        dash.callback_context.triggered[0]['prop_id'] == 'search_order_id.n_submit' or\
        dash.callback_context.triggered[0]['prop_id'] == 'search_order_type.n_submit' or\
        dash.callback_context.triggered[0]['prop_id'] == 'search_date.n_submit':
        data = managercontrol.data_get('search',current_status,search_order_id,search_order_type,search_start_date,search_end_date)
        page_number = 1
    
    if search_order_id or search_order_type or search_start_date or search_end_date and \
    dash.callback_context.triggered[0]['prop_id'] != 'url.hash':
        data = managercontrol.data_get('search',current_status,search_order_id,search_order_type,search_start_date,search_end_date)
    
    if dash.callback_context.triggered[0]['prop_id'] == 'url.hash'or \
    dash.callback_context.triggered[0]['prop_id'] == 'page_size.value' or\
    dash.callback_context.triggered[0]['prop_id'] == 'first_page.n_clicks':
        page_number = 1
        # data = managercontrol.data_get(current_status)
        # search_order_id,search_order_type,search_start_date,search_end_date = '','',None,None
        
    if dash.callback_context.triggered[0]['prop_id'] == 'previous_page.n_clicks':
        if page_number <= 1:
            page_number = 1
        else:
            page_number -= 1
    if dash.callback_context.triggered[0]['prop_id'] == 'next_page.n_clicks':
        if page_number >= total_page_num:
            page_number = total_page_num
        else:
            page_number += 1
    if dash.callback_context.triggered[0]['prop_id'] == 'last_page.n_clicks':
        page_number = int(total_page_num)
    if dash.callback_context.triggered[0]['prop_id'] == 'page_number.n_submit':
        if page_number > int(total_page_num):
            page_number = int(total_page_num)
        elif page_number < 1:
            page_number = 1
    return managercontrol.tableShown(data=data,page_count=page_number,Orderid=search_order_id,ChipPlatType=search_order_type,\
        DateStart=search_start_date,DateEnd=search_end_date,PAGE_SIZE=page_size),page_number

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

@app.callback(
        Output({'type':"menus_id",'index':ALL},'className'),
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
            pass
        else:
            statusDict[eachstatus['OrderStatusName'].replace(' ','_')] = 'text'
    statusDict['end'] = 'text'
    if not url_hash:
        return [statusDict[i] for i in statusDict]
    elif click_status_propid in statusDict:
        statusDict[click_status_propid] = 'active text'

    return [statusDict[i] for i in statusDict]

@app.callback(
    Output('manager_login','children'),
    [Input('manager_login_out','n_clicks')]
    )
def is_loginIn(n_clicks):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    managercontrol = ManagerControl()
    payload = get_payload()
    token = create_token(payload,exp_time=604800) ## not exp, 7days
    auth_T = hashlib.md5(token).hexdigest()
    dash.callback_context.response.set_cookie('T', auth_T, httponly = True)

    return managercontrol.loginOutSuccessfulLayout()