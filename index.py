import dash
import flask
import hashlib
import pandas as pd
from datetime import date


import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from spatialTrancriptomeReport import app
from apps.login.Register import registerLayout
from apps.login.Login import loginLayout
from apps.login.forgot import forgotLayout
from apps.data.data import layout
from apps.login.Manage_control import ManagerControl
from apps.login.Customer_control import CustomerControl
from apps.login.detail_page import detail_page
from apps.login.CustomerDetailPage import customer_detail_page
from apps.login.Modify_order import ModifyPage
from apps.db.tableService.OrderForm import Orders
from apps.db.tableService.Users import Users
from apps.login.token_verification import get_payload,validate_token,create_token,veri_token
from apps.login.UserActionLog import logit

def loginOutSuccessfulLayout():
        return html.Div(className='findPassWd_content', children = [
            html.Span('Login out successful!'),
            html.Br(),
            dcc.Link('OK', href='/',id='back_homepage'),
        ])

def Headcontent():
    header_nav = html.Div([dbc.Navbar([
                    html.Div(className='col-md-2',children=[
                        html.A(               
                            dbc.NavbarBrand("Stereo", className="ml-3 text-center"),                            
                    href="#",
                    ),]),
                    html.Div(className='col-md-2 offset-md-6',children=[
                        html.Div(className='dropdown',children=[
                            html.A(children=["Notifications",
                                dbc.Badge(children=['4'],color = 'light',className='ml-1')],id = 'notifications',href='#'),
                            html.Div(className='dropdown-content',children=[
                                html.A(children=['sssss'],href='#'),
                                html.A(children=['sssss'],href='/')
                                ]),
                            
                            ]),   
                        ]), 
                    html.Div(className='col-md-3',id='main_center',children=[
                            ])          
                ],
                color='#153057',
                dark=True,
                className='row'
                ),
                html.Div(id='login',children=[
                    ]),
    ])

    return header_nav

def notice_login():

    return html.Div(className='findPassWd_content', children = [
        html.Span("You have not login, please login!"),
        html.Br(),
        dbc.Button('OK', href='/Login',color='link'),
        dbc.Button('Back Home',href='/',color='link')
    ])


def page_layout():
    return html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id='login_out_notice',children=[
        html.Div(id = 'custom-auth-frame')
    ])
    ])

app.layout = page_layout()


@app.callback(
    Output('main_center','children'),
    [Input('notifications','href')],
    )
@logit()
def per_center(href):
    user_name,Is_true = veri_token()
    if Is_true:
        return html.Div([
            html.A(user_name,id='loginedName'),
            dbc.Button('log off',color='link',id='login_out')])
    else:
        return html.Div(children=[
            dbc.Button('login',href='/Login',color='link'),
            dbc.Button('Register',href='/Register',color='link')])

    
@app.callback(
    Output('login_out_notice','children'),
    [Input('login_out','n_clicks')]
    )
@logit() 
def is_loginIn(n_clicks):
    print(dash.callback_context.triggered)
    if not dash.callback_context.triggered or not dash.callback_context.triggered[0]['value']:
        raise PreventUpdate
    payload = get_payload()
    token = create_token(payload,exp_time=604800) ## not exp, 7days
    auth_T = hashlib.md5(token).hexdigest()
    dash.callback_context.response.set_cookie('T', auth_T, httponly = True)

    return loginOutSuccessfulLayout()


@app.callback(Output('custom-auth-frame', 'children'),
              [Input('url', 'pathname'),],
              [State('url','search')])
@logit() 
def display_page(pathname,search):
    user_name,Is_true = veri_token()
    if pathname == '/Register':
        return registerLayout()
    elif pathname == '/Data_analysis':
        return layout
    elif pathname == '/Login':
        return loginLayout()
    elif pathname == '/forgot':
        return forgotLayout()
    elif pathname == '/Manager_console':
        user = Users(username=user_name)
        userroleID = user.UserRoleID
        if Is_true and userroleID == 8:
            managercontrol = ManagerControl()
            return managercontrol.manager_page()
        elif not Is_true and userroleID == 8:
            return notice_login()
        else:
            return '404'
    elif pathname == '/Customer_console':
        user = Users(username=user_name)
        userroleID = user.UserRoleID
        if Is_true and userroleID == 1 :
            customercontrol = CustomerControl()
            return customercontrol.Managelayout()
        elif not Is_true:
            return notice_login()
        else:
            return '404'
    elif pathname == '/Manager_console/detail/':
        order_id = search.split('=')[1]
        orders = Orders(order_id)
        user = Users(username=user_name)
        login_name = user.getName()
        if orders.checkExists():
            if Is_true and login_name == user_name:
                return detail_page(order_id)
            elif not Is_true:
                return notice_login()
            else:
                return '404'
        else:
            return '404'
    elif pathname == '/Customer_console/detail/':
        order_id = search.split('=')[1]
        orders = Orders(order_id)
        is_delete = orders.isdelete
        login_name = orders.LoginName
        if orders.checkExists():
            if not is_delete:
                if Is_true and login_name == user_name:
                    return customer_detail_page(order_id)
                elif not Is_true and login_name == user_name:
                    return notice_login()
                else:
                    return '404'
            else:
                return '404'
        else:
            return '404'    
    elif pathname == '/Customer_console/Modify_order/':
        order_id = search.split('=')[1]
        orders = Orders(order_id)
        login_name = orders.LoginName
        is_delete = orders.isdelete
        CurrentStatus = orders.CurrentStatus
        if orders.checkExists():
            if not is_delete:
                modifypage = ModifyPage(order_id)
                if Is_true and login_name == user_name:
                    if CurrentStatus <= 3 and CurrentStatus != -1:
                        return modifypage.modify_page()
                    else:
                        return modifypage.forbidmodifyLayout(order_id)
                elif not Is_true and login_name == user_name:
                    return loginLayout()
                else:
                    return '404'
            else:
                return '404'
        else:
            return '404' 
    elif pathname == '/':
    	return html.Div( children=[
        Headcontent(),
    	html.H1('Welcome!'),
    	html.Button(id='sign_in_button',children=[dcc.Link('sign in', href='/Register')]),
        html.Button(id='data_analysis_button',children=[dcc.Link('data analysis', href='/Data_analysis')]),
        html.Button(id='login_button',children = [dcc.Link('Login',href='/Login')])
    	])
    else:
        return '404'



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8050')
