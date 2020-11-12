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
from apps.login.UserActionLog import logit_detail
from apps.db.tableService.Users import Users
from apps.db.tableService.Groups import Groups
from apps.db.tableService.OrderForm import Orders
from apps.db.tableService.OrderStatus import OrderStatus
from apps.db.tableService.Product import Product
from apps.login.notificationEmail import Send_email
from apps.login.Login import loginLayout


def customer_detail_page(order_id):
    statusDict = {}
    orders = Orders()
    product = Product()
    productData = product.getProductByOrderId(order_id)
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
                html.H6('Order Information',className='header-format text-white'),
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
                html.H6('Data Information',className='header-format text-white'),
                html.Div(Datainfo_content(productData))
               
                ]),
            html.Div(className = 'login_err_div', children=[
                html.P(id='assign_res',className='subwrong text-center text-danger')
            ]),
            html.Div(className='text-center',children=[
                dbc.Button("DataManager", 
                    href=f'/Customer_console/DataManager/?orderID={order_id}', className="mr-1 all-button"),
                dbc.Button("Modify", 
                    href=f'/Customer_console/Modify_order/?orderID={order_id}', 
                    id = {'type':"detail_modify",'index':f'{order_id}_modify_detail'},
                    className="mr-1 all-button"),
                dbc.Button("Cancel", 
                    id = {'type':"detail_cancel",'index':f'{order_id}_cancel_detail'}, className="mr-1 all-button"),
                dbc.Modal([
                        dbc.ModalHeader(["Cancel the orders"]),
                        dbc.ModalBody(["Are you sure to cancel the order ", html.B(order_id), "?"]),
                        dbc.ModalFooter([
                            dbc.Button("Confirm",href='/Customer_console',
                                id={'type':"detail_cancel_confirm_button",'index':f"{order_id}_cancel_confirm_detail"},
                                className="ml-auto all-button"),
                            dbc.Button("Cancel", 
                                id={'type':"detail_cancel_close_button",'index':f"{order_id}_cancel_close_detail"}, className="ml-auto maginRight all-button")]
                            ),],
                        id={'type':"cancel_model_detail",'index':f"{order_id}_cancel_modal_detail"},centered=True,),
                dbc.Button("Back", 
                    className="mr-1 all-button",href='/Customer_console'),
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

def Datainfo_content(productData):
    datainfo_layout = []
    if not productData.empty:
        datainfo_layout.append(html.Div(className='row',children=[
                html.Div(className='col-md-2 datainfo-text',children=[
                    html.A('SN')
                    ]),
                html.Div(className='col-md-4 datainfo-text',children=[
                    html.A('Assign to users')
                    ]),
                html.Div(className='col-md-4 datainfo-text',children=[
                    html.A('Assign to group')
                    ]),
                html.Div(className='col-md-2 datainfo-text',children=[
                    html.A('Submit')
                    ]),
                ]))
        for eachProduct in productData.iloc:
            user = Users(userid=eachProduct['SharedUser'])
            groups = Groups(GroupName=eachProduct['SharedGroup'])
            username = user.getName()
            groupsname = groups.getName()
            datainfo_layout.append(html.Div(className='row',children=[
                html.Div(className='col-md-2 all-text',children=[
                    html.A(eachProduct['SN'],id='snID',className='all-text')
                    ]),
                html.Div(className='col-md-4 datainfo-text',children=[
                    dcc.Input(id='assignUser',
                            type='text',
                            className="custodetial-input",
                            value=username,
                            placeholder='Enter LoginName',)
                    ]),
                html.Div(className='col-md-4 datainfo-text',children=[
                    dcc.Input(id='assignGroup',
                            type='text',
                            className="custodetial-input",
                            value=groupsname,
                            placeholder='Enter GroupName',)
                    ]),
                html.Div(className='col-md-2',children=[
                    dbc.Button("Submit",
                        id="detail_Submit_button",
                        className="ml-auto custoSubmit-button"),
                    ]),
                ]))
    else:
        return html.Div(className='row',children=[
                html.Div(className='col-md-12 text-center',children=[
                    html.A('No chip assigned yet!'),
                    ]),
                html.Div(className='row',children=[
                    html.Div([
                        html.A(id='snID',className='all-text')
                        ]),
                    html.Div([
                        html.A(id='assignUser',)
                        ]),
                    html.Div([
                        html.A(id='assignGroup')
                        ]),
                    html.Div([
                        html.P(id="detail_Submit_button"),
                    ]),
                ])
                ])
    return datainfo_layout

@app.callback(
    Output({'type':"cancel_model_detail",'index':ALL}, "is_open"),
    [Input({'type':"detail_cancel",'index':ALL}, "n_clicks"),
    Input({'type':"detail_cancel_confirm_button",'index':ALL}, "n_clicks"),
    Input({'type':"detail_cancel_close_button",'index':ALL}, "n_clicks")],
    [
    State({'type':"detail_cancel",'index':ALL}, "id"),
    State({'type':"cancel_model_detail",'index':ALL}, "is_open")]
)
def change_end_button_detail(status_click, status_confirm, status_close, status_id, status_modal):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    for index in range(len(status_id)):
        order_id = status_id[index]['index'].split('_cancel')[0]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_cancel_detail","type":"detail_cancel"}.n_clicks' or dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_cancel_close_detail","type":"detail_cancel_close_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_cancel_confirm_detail","type":"detail_cancel_confirm_button"}.n_clicks':
            status_modal[index] = not status_modal[index]
    return status_modal

@app.callback(
    [Output({'type':"detail_modify",'index':ALL}, "disabled"),
    Output({'type':"detail_cancel",'index':ALL}, "disabled"),],
    [Input({'type':"detail_modify",'index':ALL}, "id"),
    ]
)
def status_button_disabled(modify_id):
    orders = Orders()
    res_modify = []
    res_cancel = []
    for each_modify_id in modify_id:
        order_id = each_modify_id['index'].split('_modify')[0]
        CurrentStatus = int(orders.getDataByOrderID(order_id).iloc[0]['CurrentStatus'])
        NextStatus = int(orders.getDataByOrderID(order_id).iloc[0]['NextStatus'])
        if CurrentStatus <= 3 and CurrentStatus != -1:
            res_modify.append(False)
            res_cancel.append(False)
        elif CurrentStatus == -1:
            res_modify.append(True)
            res_cancel.append(True)
        else:
            res_modify.append(True)
            res_cancel.append(True)
    return res_modify,res_cancel

@app.callback(
    Output({'type':"detail_cancel",'index':ALL},'children'),
    [Input({'type':"detail_cancel_confirm_button",'index':ALL},'n_clicks'),],
    [State({'type':"detail_cancel",'index':ALL}, "id"),
    State({'type':"detail_cancel",'index':ALL},'children')
    ]
    )
def cancel_order(n_clicks,status_id,custo_cancel):
    # print(dash.callback_context.triggered)
    if not dash.callback_context.triggered:
        raise PreventUpdate
    for index in range(len(status_id)):
        order_id = status_id[index]['index'].split('_cancel')[0]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_cancel_confirm_detail","type":"detail_cancel_confirm_button"}.n_clicks':
            order = Orders(order_id)
            order.updateByisdelete(True)
    logit_detail('Cancel the order',order_id)
    return custo_cancel

@app.callback(
    [
    Output("assignUser",'value'),
    Output("assignGroup",'value'),
    Output('assign_res','children')
    ],
    [Input("detail_Submit_button",'n_clicks'),],
    [
    State('snID','children'),
    State("assignUser",'value'),
    State("assignGroup",'value'),
    ]
    )
def assignSubmit(n_clicks,snID,assignUser,assignGroup):
    # print(dash.callback_context.triggered)
    if not dash.callback_context.triggered:
        raise PreventUpdate
    product = Product(snID)
    user = Users(username=assignUser)
    groups = Groups(GroupName=assignGroup)
    userID = user.getId()
    GroupID = groups.getId()
    if not assignUser and not assignGroup:
        err_msg = 'Username and Groupname does not exists, please re-enter!'
    elif assignUser and not assignGroup:
        if not user.checkExists():
            err_msg = 'Username does not exists, please re-enter!'
        else:
            product.updateSharedUser(userID)
            err_msg = 'successfully added'
            logit_detail('Assign the order')
    elif not assignUser and assignGroup:
        if not groups.checkExists():
            err_msg = 'Groupname does not exists, please re-enter!'
        else:
            product.updateSharedGroup(GroupID)
            err_msg = 'successfully added'
            logit_detail('Assign the order')
    elif assignUser and assignGroup:
        if user.checkExists() and not groups.checkExists():
            err_msg = 'Groupname does not exists, please re-enter!'
        elif not user.checkExists() and groups.checkExists():
            err_msg = 'Username does not exists, please re-enter!'
        elif not user.checkExists() and not groups.checkExists():
            err_msg = 'Username and Groupname does not exists, please re-enter!'
        else:
            product.updateSharedUser(userID)
            product.updateSharedGroup(GroupID)
            err_msg = 'successfully added'
            logit_detail('Assign the order')
    # print(err_msg)
    return assignUser,assignGroup,err_msg