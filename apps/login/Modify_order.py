import dash
import json
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

class ModifyPage():
    def __init__(self,OrderID):
        self.order_id = OrderID
        self.statusDict = {}
        self.orders = Orders(self.order_id)
        self.data = self.orders.getDataByOrderID(self.order_id)
        self.CurrentStatus = self.data.iloc[0]['CurrentStatus']
        self.orderstatus = OrderStatus()
        self.allstatus = self.orderstatus.getAllStatus()
        for eachstatus in self.allstatus.iloc:
            self.statusDict[eachstatus['OrderStatusID']] = eachstatus['OrderStatusName']
    
    def headContent(self):
        return dbc.Navbar([
                    html.H5(f'Modify Order/{self.order_id}',id='head_title')
                    ],className='top-bar')

    def bodyContent(self):
        return html.Div(className='container',id='modify_div',children=[
                html.Div(id='modify_div2',children=[
                    html.Div(className='detail-content text-center',children=[
                    html.H6('Order Information',className='header-format text-white'),
                    self.modify_orderinfo_content('OrderID',self.data.iloc[0]['OrderID']),
                    self.modify_orderinfo_content('LoginName',self.data.iloc[0]['LoginName']),
                    self.modify_orderinfo_content('ChipPlat',self.data.iloc[0]['ChipPlat']),
                    self.modify_orderinfo_content('Quantity',self.data.iloc[0]['Quantity']),
                    html.H6('Customer Information',className='header-format text-white'),
                    self.modify_customerinfo_content('ContactName',self.data.iloc[0]['ContactName']),
                    self.modify_customerinfo_content('Phone',self.data.iloc[0]['Phone']),
                    self.modify_customerinfo_content('Email',self.data.iloc[0]['Email']),
                    self.modify_customerinfo_content('Address',self.data.iloc[0]['Address']),
                    self.modify_customerinfo_content('ZipCode',self.data.iloc[0]['ZipCode']),
                    self.modify_customerinfo_content('Organization',self.data.iloc[0]['Organization']),
                    self.modify_customerinfo_content('ResearchInterests',self.data.iloc[0]['ResearchInterests']),
                        ]),
                html.Div(className='text-center',children=[
                    dbc.Button("Submit", 
                        id = {'type':"modify_submit",'index':f'{self.order_id}_submit_modify'}, className="mr-1 all-button"),
                    dbc.Modal([
                            dbc.ModalHeader("Confirm"),
                            dbc.ModalBody(["Are you sure to submit the modify of order ", html.B(self.order_id)]),
                            dbc.ModalFooter([
                                dbc.Button("Confirm",
                                 id={'type':"modify_submit_confirm_button",'index':f"{self.order_id}_submit_confirm_modify"},
                                 className="ml-auto all-button"),
                                dbc.Button("Cancel",
                                 id={'type':"modify_submit_close_button",'index':f"{self.order_id}_submit_close_modify"}, className="ml-auto maginRight all-button")]
                                ),],
                            id={'type':"submit_model_modify",'index':f"{self.order_id}_submit_modal_modify"}, centered=True,),
                    dbc.Button("Back", 
                        id = {'index':f'back_{self.order_id}_button','type':'back_button'}, 
                        className="mr-1 all-button",href='/Customer_console'),
                    ])
                ])
            ])


    def modify_page(self):
        layout = html.Div(id='Modifypage',children=[
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
                self.headContent(),
                self.bodyContent()
            ])
        return layout

    def modify_orderinfo_content(self,fieldName,content):
        layout = html.Div(className='row',children=[
                    html.Div(className='col-md-5 modify-text-right',children=[
                        html.A(fieldName+':')
                        ]),
                    html.Div(className='col-md-7 modify-text-left',children=[
                        html.A(content)
                    ]),])

        return layout

    def modify_customerinfo_content(self,fieldName,content):
        layout = html.Div(className='row',children=[
                    html.Div(className='col-md-5 modify-text-right',children=[
                        html.A(fieldName+':')
                        ]),
                    html.Div(className='col-md-7 text-left',children=[
                        dcc.Input(id={'type':'customerinfo','index':f'{fieldName}'},
                                            type='text',
                                            className="modify_input",
                                            value=content,
                                            placeholder=f'Enter {fieldName}',)
                        ])
                    ])
        return layout

    def modifySuccessfulLayout(self,order_id):
        return html.Div(className='findPassWd_content', children = [
            html.Span('modify successful!'),
            html.Br(),
            dbc.Button('Back',id='backModify',color='link', href=f'/Customer_console/Modify_order/?orderID={order_id}'),
        ])

    def forbidmodifyLayout(self,order_id):
        return html.Div(className='findPassWd_content', children = [
            html.Span(f'Order {order_id} is prohibited to modify!'),
            html.Br(),
            dbc.Button('Back',id='backModify',color='link', href=f'/Customer_console'),
        ])

@app.callback(
    Output({'type':"submit_model_modify",'index':ALL}, "is_open"),
    [Input({'type':"modify_submit",'index':ALL}, "n_clicks"),
    Input({'type':"modify_submit_confirm_button",'index':ALL}, "n_clicks"),
    Input({'type':"modify_submit_close_button",'index':ALL}, "n_clicks")],
    [State({'type':"modify_submit",'index':ALL}, "id"),
    State({'type':"submit_model_modify",'index':ALL}, "is_open")]
)
def change_status_button_detail(submit_click, submit_confirm, submit_close, submit_id, submit_modal):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    for index in range(len(submit_id)):
        order_id = submit_id[index]['index'].split('_submit')[0]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_submit_modify","type":"modify_submit"}.n_clicks' or \
        dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_submit_close_modify","type":"modify_submit_close_button"}.n_clicks':
            submit_modal[index] = not submit_modal[index]
        if dash.callback_context.triggered[0]['prop_id'] == '{"index":"'+str(order_id)+'_submit_confirm_modify","type":"modify_submit_confirm_button"}.n_clicks':
            submit_modal[index] = not submit_modal[index]
    return submit_modal

@app.callback(
    Output('modify_div','children'),
    [Input({'type':"modify_submit_confirm_button",'index':ALL},'n_clicks')],
    [
    State({'type':'customerinfo','index':ALL},'value'),
    State({'type':'customerinfo','index':ALL},'id'),    
    ]
    )
def submit_modify(n_clicks,customerinfo,customerinfoID):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    order_id = json.loads(dash.callback_context.triggered[0]['prop_id'].split('.')[0])['index'].split('_submit_confirm_modify')[0]
    modifypage = ModifyPage(order_id)
    CurrentStatus = modifypage.CurrentStatus
    
    new_customerinfo = {}
    for index in range(len(customerinfo)):
        new_customerinfo[customerinfoID[index]['index']]=customerinfo[index]
        
    if CurrentStatus <= 3 and CurrentStatus != -1:
        modifypage.orders.updateByContactName(new_customerinfo['ContactName'])
        modifypage.orders.updateByZipCode(new_customerinfo['ZipCode'])
        modifypage.orders.updateByAddress(new_customerinfo['Address'])
        modifypage.orders.updateByEmail(new_customerinfo['Email'])
        modifypage.orders.updateByPhone(new_customerinfo['Phone'])
        modifypage.orders.updateByResearchInterests(new_customerinfo['ResearchInterests'])
        modifypage.orders.updateByOrganization(new_customerinfo['Organization'])
        return modifypage.modifySuccessfulLayout(order_id)
    else:
        return modifypage.forbidmodifyLayout(order_id)

@app.callback(
    Output('Modifypage','children'),
    [Input('backModify','n_clicks')],
    [State('url','search')]
    )
def backmodifypage(n_clicks,url_search):
    if not dash.callback_context.triggered or not dash.callback_context.triggered[0]['value']:
        raise PreventUpdate
    order_id = url_search.split('=')[1]
    modifypage = ModifyPage(order_id)

    return modifypage.headContent(),modifypage.bodyContent()

@app.callback(
    Output('modify_div2','children'),
    [Input('head_title','children')]
    )
def forbidmodify(head_title):
    order_id = head_title.split('/')[1]
    modifypage = ModifyPage(order_id)
    CurrentStatus = modifypage.CurrentStatus
    if CurrentStatus <= 3 and CurrentStatus != -1:
        raise PreventUpdate
    else:
        return modifypage.forbidmodifyLayout(order_id)
