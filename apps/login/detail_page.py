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


def detail_page(order_id):
    statusDict = {}
    orders = Orders()
    data = orders.getDataByOrderID(order_id)
    CurrentStatus = data.iloc[0]['CurrentStatus']
    orderstatus = OrderStatus()
    allstatus = orderstatus.getAllStatus()
    for eachstatus in allstatus.iloc:
        statusDict[eachstatus['OrderStatusID']] = eachstatus['OrderStatusName']

    layout = html.Div([
            # dbc.Navbar([
            #         html.Div(className='col-md-2',children=[
            #             html.A(               
            #                 dbc.NavbarBrand("Stereo", className="ml-3 text-center"),                            
            #         href="#",
            #         ),]),
            #         html.Div(className='col-md-2 offset-md-8',children=[
            #             html.Div(className='dropdown',children=[
            #                 html.A(children=["Notifications",dbc.Badge(children=['4'],color = 'light',className='ml-1')],id = 'Notifications',href='#'),
            #                 html.Div(className='dropdown-content',children=[
            #                     html.A(children=['sssss'],href='#'),
            #                     html.A(children=['sssss'],href='/')
            #                     ])
            #                 ]),   
            #             ]),           
            #     ],
            #     color='#153057',
            #     dark=True,
            #     className='row'
            #     ),
            dbc.Navbar([
                html.H5(f'Order detail/{order_id}')
                ],className='top-bar'),
            html.Div(className='container',children=[
                html.Div(className='detail-content text-center',children=[
                html.H6('Order Informarion',className='header-format text-white'),
                detial_page_content('OrderID',data.iloc[0]['OrderID']),
                detial_page_content('LoginName',data.iloc[0]['LoginName']),
                detial_page_content('ChipPlat',data.iloc[0]['ChipPlat']),
                detial_page_content('Quantity',data.iloc[0]['Quantity']),
                detial_page_content('ContractNo',data.iloc[0]['ContractNo']),
                detial_page_content('CreateTime',data.iloc[0]['CreateTime']),
                html.H6('Customer Information',className='header-format text-white'),
                detial_page_content('ContactName',data.iloc[0]['ContactName']),
                detial_page_content('Phone',data.iloc[0]['Phone']),
                detial_page_content('Email',data.iloc[0]['Email']),
                detial_page_content('Address',data.iloc[0]['Address']),
                detial_page_content('ZipCode',data.iloc[0]['ZipCode']),
                detial_page_content('Organization',data.iloc[0]['Organization']),
                detial_page_content('ResearchInterests',data.iloc[0]['ResearchInterests']),
                html.H6('Status Information',className='header-format text-white'),
                detial_page_content('CurrentStatus',statusDict[data.iloc[0]['CurrentStatus']]),
                detial_page_content('NextStatus',statusDict[data.iloc[0]['NextStatus']]),
                detial_page_content('Accessory',data.iloc[0]['Accessory']),
                    ]),
            html.Div(className='text-center',children=[
                dbc.Button("Confirm to next status", 
                    id = {'type':"detail_status",'index':f'{order_id}_status_detail'}, className="mr-1 all-button"),
                dbc.Modal([
                        dbc.ModalHeader("Confirm to next status"),
                        dbc.ModalBody(["Are you sure to change the order ", html.B(order_id), " to next status?"]),
                        dbc.ModalFooter([
                            dbc.Button("Confirm",
                             id={'type':"detail_status_confirm_button",'index':f"{order_id}_status_confirm_detail"},
                             href= f'/Manager_console/detail/?orderID={order_id}&{CurrentStatus}',className="ml-auto all-button"),
                            dbc.Button("Cancel",
                             id={'type':"detail_status_close_button",'index':f"{order_id}_status_close_detail"}, className="ml-auto maginRight all-button")]
                            ),],
                        id={'type':"status_model_detail",'index':f"{order_id}_status_modal_detail"}, centered=True,),
                dbc.Button("End", 
                    id = {'type':"detail_end",'index':f'{order_id}_end_detail'}, className="mr-1 all-button"),
                dbc.Modal([
                        dbc.ModalHeader(["End the orders"]),
                        dbc.ModalBody(["Are you sure to end the order ", html.B(order_id), "?"]),
                        dbc.ModalFooter([
                            dbc.Button("Confirm",
                                id={'type':"detail_end_confirm_button",'index':f"{order_id}_end_confirm_detail"},
                                href= f'/Manager_console/detail/?orderID={order_id}&{CurrentStatus}', className="ml-auto all-button"),
                            dbc.Button("Cancel", 
                                id={'type':"detail_end_close_button",'index':f"{order_id}_end_close_detail"}, className="ml-auto maginRight all-button")]
                            ),],
                        id={'type':"end_model_detail",'index':f"{order_id}_end_modal_detail"},centered=True,),
                dbc.Button("Back", 
                    id = {'index':f'back_{order_id}_button','type':'back_button'}, className="mr-1 all-button",href='/Manager_console'),
                ])]),
        ])
    return layout

def detial_page_content(fieldName,content):
    layout = html.Div(className='row',children=[
                html.Div(className='col-md-5 text-right',children=[
                    html.A(fieldName+':')
                    ]),
                html.Div(className='col-md-7 text-left',children=[
                    html.A(content)
                    ])
                ])
    return layout

@app.callback(
    [Output({'type':"detail_status",'index':ALL}, "disabled"),
    Output({'type':"detail_end",'index':ALL}, "disabled"),],
    [Input({'type':"detail_status",'index':ALL}, "id"),
    ]
)
def status_button_disabled_detail(status_id):
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
    Output({'type':"status_model_detail",'index':ALL}, "is_open"),
    [Input({'type':"detail_status",'index':ALL}, "n_clicks"),
    Input({'type':"detail_status_confirm_button",'index':ALL}, "n_clicks"),
    Input({'type':"detail_status_close_button",'index':ALL}, "n_clicks")],
    [State({'type':"detail_status",'index':ALL}, "id"),
    State({'type':"status_model_detail",'index':ALL}, "is_open")]
)
def change_status_button_detail(status_click, status_confirm, status_close, status_id, status_modal):
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
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_status_detail","type":"detail_status"}.n_clicks' or dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_status_close_detail","type":"detail_status_close_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_status_confirm_detail","type":"detail_status_confirm_button"}.n_clicks':
            if CurrentStatus != last_status_id and NextStatus != last_status_id:
                orders.updateCurrentStatus(int(statusID_list[statusID_list.index(CurrentStatus)+1]),order_id)
                orders.updateNextStatus(int(statusID_list[statusID_list.index(NextStatus)+1]),order_id)
            elif  NextStatus==last_status_id:
                orders.updateCurrentStatus(int(statusID_list[statusID_list.index(CurrentStatus)+1]),order_id)
                orders.updateNextStatus(-1,order_id)
            else:
                orders.updateCurrentStatus(-1,order_id)
                orders.updateNextStatus(-2,order_id)
            Send_email(order_id)
            status_modal[index] = not status_modal[index]
    return status_modal

@app.callback(
    Output({'type':"end_model_detail",'index':ALL}, "is_open"),
    [Input({'type':"detail_end",'index':ALL}, "n_clicks"),
    Input({'type':"detail_end_confirm_button",'index':ALL}, "n_clicks"),
    Input({'type':"detail_end_close_button",'index':ALL}, "n_clicks")],
    [State({'type':"detail_end",'index':ALL}, "id"),
    State({'type':"end_model_detail",'index':ALL}, "is_open")]
)
def change_end_button_detail(status_click, status_confirm, status_close, status_id, status_modal):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    orders = Orders()
    for index in range(len(status_id)):
        order_id = status_id[index]['index'].split('_end')[0]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_end_detail","type":"detail_end"}.n_clicks' or dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_end_close_detail","type":"detail_end_close_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_end_confirm_detail","type":"detail_end_confirm_button"}.n_clicks':
            orders.updateCurrentStatus(-1,order_id)
            orders.updateNextStatus(-2,order_id)
            Send_email(order_id)
            status_modal[index] = not status_modal[index]
    return status_modal

# @app.callback(
#     Output('url','href'),
#     [Input({'type':"detail_end_confirm_button",'index':ALL}, "n_clicks"),
#     Input({'type':"detail_status_confirm_button",'index':ALL}, "n_clicks"),
#     Input({'type':"back_button",'index':ALL}, "n_clicks")
#     ])
# def detail_page_update(detail_end_confirm_button,detail_status_confirm_button,back_button):
#     # print(dash.callback_context.triggered)
#     # if dash.callback_context.triggered[0]['prop_id']:
#     #     if re.search(r'{"index":"\d+_end_confirm_detail","type":"detail_end_confirm_button"',dash.callback_context.triggered[0]['prop_id'].split('.')[0]) or\
#     #     re.search(r'{"index":"\d+_status_confirm_detail","type":"detail_status_confirm_button"',dash.callback_context.triggered[0]['prop_id'].split('.')[0]):
#     #         return True
#     pass