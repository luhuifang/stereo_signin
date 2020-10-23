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


def tableShown(status, searchstatus='',Orderid='',ChipPlatType='',DateStart=None,DateEnd=None,page_count=1,PAGE_SIZE=5):
    orders = Orders()
    Tbody = []
    statusDict = {}
    orderstatus = OrderStatus()
    allstatus = orderstatus.getAllStatus()
    for eachstatus in allstatus.iloc:
        statusDict[eachstatus['OrderStatusID']] = eachstatus['OrderStatusName']
    if status == 'all_order':
        data = orders.getAllData().loc[:,['OrderID','ChipPlat','Quantity','ContactName','CurrentStatus','NextStatus','CreateTime']]
    elif status == 'search':
        data = orders.getDataBySearch(searchstatus,Orderid,ChipPlatType,DateStart,DateEnd).loc[:,['OrderID','ChipPlat','Quantity','ContactName','CurrentStatus','NextStatus','CreateTime']]
    else:
        data = orders.getDataByStatus(status.replace('_',' ')).loc[:,['OrderID','ChipPlat','Quantity','ContactName','CurrentStatus','NextStatus','CreateTime']]

    row_nums = data.shape[0]
    if row_nums/PAGE_SIZE == 0:
        page_num = 1
    elif row_nums/PAGE_SIZE > row_nums//PAGE_SIZE:
        page_num = row_nums//PAGE_SIZE + 1
    elif row_nums/PAGE_SIZE == row_nums//PAGE_SIZE:
        page_num = row_nums//PAGE_SIZE

    for i in data.iloc[int(PAGE_SIZE*int(page_count))-PAGE_SIZE:int(PAGE_SIZE*int(page_count))].iloc:
        OrderID=i['OrderID']; Quantity = i['Quantity']; ChipPlat=i['ChipPlat']; ContactName=i['ContactName']
        CurrentStatus=statusDict[i['CurrentStatus']]; NextStatus=statusDict[i['NextStatus']]; CreateTime=i['CreateTime']
        
        Tbody.append(html.Tr([html.Td(OrderID), html.Td(ChipPlat), html.Td(Quantity), html.Td(ContactName)
            , html.Td(CurrentStatus), html.Td(NextStatus), html.Td(CreateTime), 
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
                                    value=Orderid,
                                    placeholder='Enter Order ID',)
                            ]),
                        html.Div(className='search-word',children=[
                            html.Label('Chip Plat:',className='label_font_size'),
                            dcc.Input(id='search_order_type',
                                    type='text',
                                    className="input_class",
                                    minLength= 8,
                                    maxLength= 25,
                                    value=ChipPlatType,
                                    placeholder='Enter Order Type',)
                            ]),
                        html.Div(className='search-word',children=[
                            html.Label('Order Date:',className='label_font_size'),
                            dcc.DatePickerRange(
                                    id='search_date',
                                    display_format='YYYY-MM-DD',
                                    className='date_input_class',
                                    clearable=True,
                                    start_date=DateStart,
                                    end_date = DateEnd,
                                )
                            ]),
                        html.Div(className='search-word',children=[
                            dbc.Button(children=['Search'],id='search_button',className='search-button'),
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
                                            dbc.Button(className='all-button',children=['First'],id='first_page', disabled=True),
                                            dbc.Button(className='all-button',children=['Prev'],id='previous_page', disabled=True),
                                            dcc.Input(id='page_number',
                                                    type='text',
                                                    className="page-input",
                                                    value=1,),
                                            html.I('/',className='page-off',id = 'page_off',role=status),
                                            html.Div(page_num,id='total_page_num',className='total-page-num'),
                                            
                                            dbc.Button(className='all-button',children=['Next'],id='next_page'),
                                            dbc.Button(className='all-button',children=['Last'],id='last_page'),
                                            dcc.Dropdown(
                                                id = 'page_size',
                                                options=[{'label': v, 'value': v} for v in [5,10,20,50]],
                                                value=PAGE_SIZE,
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

def manager_page():
    return html.Div([
            # dcc.Location(id = 'Url', refresh = False),
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
            html.Div(id="page_body",children=Managelayout())
        ])

def Managelayout():
    statusDict = {}
    menus = [html.A(id = {'index':'all_order','type':'menus_id'},children=[html.P(className='icon'),'All Order'],className="active text"),]
    orderstatus = OrderStatus()
    allstatus = orderstatus.getAllStatus()
    for eachstatus in allstatus.iloc:
        statusDict[eachstatus['OrderStatusID']] = eachstatus['OrderStatusName']
    for i in statusDict.values():
        if i == '' or i == 'end':
            pass
        else:
            ii = i.replace(' ','_')
            single_mennu = html.A(id = {'index':ii,'type':'menus_id'},children=[html.P(className='icon'), i],className="text")
            menus.append(single_mennu)
    menus.append(html.A(id = {'index':'end','type':'menus_id'},children=[html.P(className='icon'),"Finish Order"],className="text "))
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
                        html.Div(id='order_table',className='col-md-10 col-xs-8',children=tableShown('all_order'),
                            )
                        ]),
                    ])
            ])


def page_on_status(href_content,search_href,page_number,search_order_id,search_order_type,search_start_date,search_end_date,page_size):
    try:
        status = href_content.split('=')[1]
        search_status = href_content.split('=')[1].split('&')[0]
    except:
        status,search_status = '',''
    ## 读取数据库状态表，并转换为以状态名为key的字典，字典value值为菜单的className
    statusDict = {'all_order':'text'}
    orderstatus = OrderStatus()
    allstatus = orderstatus.getAllStatus()
    for eachstatus in allstatus.iloc:
        if eachstatus['OrderStatusName'] == 'end' or eachstatus['OrderStatusName'] == '' :
            pass
        else:
            statusDict[eachstatus['OrderStatusName'].replace(' ','_')] = 'text'
    statusDict['end'] = 'text'
    ## 判断当前的点击在哪一个状态中
    if status in statusDict:
        class_name = []
        res = []
        statusDict[status] = "active text"
        for i in statusDict:
            class_name.append(statusDict[i])
        return [class_name,tableShown(status,page_count=page_number,PAGE_SIZE=page_size),page_number,href_content]  
    elif search_status in statusDict:
        class_name = []
        statusDict[search_status] = "active text"
        for i in statusDict:
            class_name.append(statusDict[i])
        return [class_name,tableShown('search',search_status,search_order_id,search_order_type,search_start_date,search_end_date,page_count=page_number,PAGE_SIZE=page_size),page_number,search_href]

    return ["active text",'text','text','text','text','text','text','text','text'],tableShown('all_order',page_count=page_number,PAGE_SIZE=page_size),page_number,'/Manager_console#status=all_order'

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
    orderstatus = OrderStatus()
    allstatus = orderstatus.getAllStatus()
    statusID_list = [eachstatus['OrderStatusID'] for eachstatus in allstatus.iloc][2:]
    last_status_id = statusID_list[-1]
    if not dash.callback_context.triggered:
        raise PreventUpdate
    orders = Orders()
    for index in range(len(status_id)):
        order_id = status_id[index]['index'].split('_status')[0]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_status","type":"status"}.n_clicks' or dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_status_close","type":"status_close_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_status_confirm","type":"status_confirm_button"}.n_clicks':
            if CurrentStatus != last_status_id and NextStatus != last_status_id:
                orders.updateCurrentStatus(int(statusID_list[statusID_list.index(CurrentStatus)+1]),order_id)
                orders.updateNextStatus(int(statusID_list[statusID_list.index(NextStatus)+1]),order_id)
            elif  NextStatus == last_status_id:
                orders.updateCurrentStatus(int(statusID_list[statusID_list.index(CurrentStatus)+1]),order_id)
                orders.updateNextStatus(-1,order_id)
            else:
                orders.updateCurrentStatus(-1,order_id)
                orders.updateNextStatus(-2,order_id)
            Send_email(order_id)
            status_modal[index] = not status_modal[index]
        
    return status_modal

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
    orders = Orders()
    for index in range(len(status_id)):
        order_id = status_id[index]['index'].split('_end')[0]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_end","type":"end"}.n_clicks' or dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_end_close","type":"end_close_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_end_confirm","type":"end_confirm_button"}.n_clicks':
            orders.updateCurrentStatus(-1,order_id)
            orders.updateNextStatus(-2,order_id)
            Send_email(order_id)
            status_modal[index] = not status_modal[index]
    return status_modal



@app.callback(
    [
    Output({'type':"menus_id",'index':ALL},'className'),
    Output('order_table','children'),
    Output('page_number','value'),
    Output('url','href')],
    [
    Input({'type':"menus_id",'index':ALL},'n_clicks'),
    # Input('Url','hash'),
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
    Input({'type':"status_confirm_button",'index':ALL}, "n_clicks"),
    Input({'type':"end_confirm_button",'index':ALL}, "n_clicks"),
    ],
    [State('search_order_id','value'),
    State('search_order_type','value'),
    State('search_date','start_date'),
    State('search_date','end_date'),
    State('page_number','value'),
    State('total_page_num','children'),
    State('url','href'),
    State({'type':"detail_end_confirm_button",'index':ALL}, "n_clicks"),
    State({'type':"detail_status_confirm_button",'index':ALL}, "n_clicks"),
    State({'type':"back_button",'index':ALL}, "n_clicks")]
    )
def table_shown(menus_id,search_button,first_page,previous_page,next_page,last_page,\
    search_order_id_submit,search_order_type_submit,search_date_submit,page_number_submit,page_size,status_confirm_button,end_confirm_button,\
    search_order_id,search_order_type,search_start_date,search_end_date,page_number,total_page_num,href_content,\
    detail_end_confirm_button,detail_status_confirm_button,back_button):
    print(dash.callback_context.triggered)
    print(href_content)
    if dash.callback_context.triggered[0]['prop_id']:
        click_status = re.search(r'{"index":"(.*)","type":"menus_id"',dash.callback_context.triggered[0]['prop_id'].split('.')[0])
        if click_status:
            click_status_propid = click_status.group(1)
        else:
            click_status_propid = ''
    ## 读取数据库状态表，并转换为以状态名为key的字典，字典value值为菜单的className
    statusDict = {'all_order':'text'}
    orderstatus = OrderStatus()
    allstatus = orderstatus.getAllStatus()
    for eachstatus in allstatus.iloc:
        if eachstatus['OrderStatusName'] == 'end' or eachstatus['OrderStatusName'] == '' :
            pass
        else:
            statusDict[eachstatus['OrderStatusName'].replace(' ','_')] = 'text'
    statusDict['end'] = 'text'

    page_number = int(page_number)
    orders = Orders()
    try:
        current_status = href_content.split('=')[1].split('&')[0]
    except:
        current_status = 'all_order'
    # print('hash_name:',hash_name)
    ## 设置点击搜索按钮后URL内容
    search_href = '/Manager_console#status={}&order_id={}&order_type={}&order_date={}-{}'.format(current_status,search_order_id,search_order_type,search_start_date,search_end_date)
    if not search_button and not first_page and not previous_page and not next_page and not last_page\
    and not dash.callback_context.triggered[0]['prop_id'] == 'page_number.n_submit'\
    and not dash.callback_context.triggered[0]['prop_id'] == 'search_order_id.n_submit'\
    and not dash.callback_context.triggered[0]['prop_id'] == 'search_order_type.n_submit'\
    and not dash.callback_context.triggered[0]['prop_id'] == 'search_date.n_submit' \
    and not dash.callback_context.triggered[0]['prop_id'] == 'page_size.value' \
    and not dash.callback_context.triggered[0]['prop_id'] == 'search_button.n_clicks' \
    and not dash.callback_context.triggered:
        # raise PreventUpdate
        return page_on_status(href_content,search_href,page_number,search_order_id,search_order_type,search_start_date,search_end_date,page_size)
    if click_status_propid in statusDict:
        class_name = []
        statusDict[click_status_propid] = "active text"
        for i in statusDict:
            class_name.append(statusDict[i])
        return [class_name,tableShown(click_status_propid,PAGE_SIZE=5),1,f'/Manager_console#status={click_status_propid}']
        
    if dash.callback_context.triggered[0]['prop_id'] == 'search_button.n_clicks' or\
        dash.callback_context.triggered[0]['prop_id'] == 'search_order_id.n_submit' or\
        dash.callback_context.triggered[0]['prop_id'] == 'search_order_type.n_submit' or\
        dash.callback_context.triggered[0]['prop_id'] == 'search_date.n_submit' or\
        dash.callback_context.triggered[0]['value'] == '?status=search':
        return page_on_status(href_content+'&order_id',search_href,1,search_order_id,search_order_type,search_start_date,search_end_date,page_size)

    if dash.callback_context.triggered[0]['prop_id'] == 'page_size.value':
        return page_on_status(href_content,search_href,1,search_order_id,search_order_type,search_start_date,search_end_date,page_size)

    if dash.callback_context.triggered[0]['prop_id'] == 'first_page.n_clicks':
        page_number = 1
        return page_on_status(href_content,search_href,page_number,search_order_id,search_order_type,search_start_date,search_end_date,page_size)
    if dash.callback_context.triggered[0]['prop_id'] == 'previous_page.n_clicks':
        page_number -= 1
        return page_on_status(href_content,search_href,page_number,search_order_id,search_order_type,search_start_date,search_end_date,page_size)
    if dash.callback_context.triggered[0]['prop_id'] == 'next_page.n_clicks':
        page_number += 1
        return page_on_status(href_content,search_href,page_number,search_order_id,search_order_type,search_start_date,search_end_date,page_size)
    if dash.callback_context.triggered[0]['prop_id'] == 'last_page.n_clicks':
        page_number = int(total_page_num)
        return page_on_status(href_content,search_href,page_number,search_order_id,search_order_type,search_start_date,search_end_date,page_size)
    if dash.callback_context.triggered[0]['prop_id'] == 'page_number.n_submit':
        if page_number > int(total_page_num):
            return page_on_status(href_content,search_href,int(total_page_num),search_order_id,search_order_type,search_start_date,search_end_date,page_size)
        elif page_number < 1:
            return page_on_status(href_content,search_href,1,search_order_id,search_order_type,search_start_date,search_end_date,page_size)
        return page_on_status(href_content,search_href,page_number,search_order_id,search_order_type,search_start_date,search_end_date,page_size)
    
    if dash.callback_context.triggered[0]['prop_id']:
        if re.search(r'{"index":"\d+_end_confirm","type":"end_confirm_button"',dash.callback_context.triggered[0]['prop_id'].split('.')[0]) or\
        re.search(r'{"index":"\d+_status_confirm","type":"status_confirm_button"',dash.callback_context.triggered[0]['prop_id'].split('.')[0]):
            print('ok')
            return page_on_status(href_content,search_href,page_number,search_order_id,search_order_type,search_start_date,search_end_date,page_size)

    return page_on_status(href_content,search_href,page_number,search_order_id,search_order_type,search_start_date,search_end_date,page_size)


# @app.callback(
#     Output('page_body','children'),
#     [Input({'type':"Detail_button",'index':ALL}, "n_clicks"),Input('Url','search')],
#     [State({'type':"Detail_button",'index':ALL}, "id"),
#     ])
# def detail_page_update(Detail_button,search_content,detail_button_id):
#     if not dash.callback_context.triggered:
#         raise PreventUpdate
#     if not search_content:
#         raise PreventUpdate
#     print(search_content)
#     order_id = search_content.split('=')[1]
#     # print('ok',123,Detail_button)
#     print(dash.callback_context.triggered)
#     # if re.search(r'{"index":"(\d+)_detail","type":"Detail_button"',dash.callback_context.triggered[0]['prop_id'].split('.')[0]):
#     #     order_id = re.search(r'{"index":"(\d+)_detail","type":"Detail_button"',dash.callback_context.triggered[0]['prop_id'].split('.')[0])
#     #     if order_id:
#     #         order_id = order_id[1]
#     #     print(order_id)
#     return detial_page(order_id)
#     # else:
#     #     return Managelayout()

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


