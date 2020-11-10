import dash
import re
import json
import flask
import hashlib
import pandas as pd
from datetime import date

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from spatialTrancriptomeReport import app
from apps.login.token_verification import get_payload,validate_token,create_token,veri_token

def loginOutSuccessfulLayout():
        return html.Div(className='findPassWd_content', children = [
            html.Span('Login out successful!'),
            html.Br(),
            dcc.Link('OK', href='/'),
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
                    html.Div(className='col-md-3',id='personal_center',children=[
                            ])          
                ],
                color='#153057',
                dark=True,
                className='row'
                ),
                html.Div(id='login',children=[
                    ]),
                # dbc.Modal([
                #         dbc.ModalHeader(["Login out successful!"]),
                #         dbc.ModalBody(["Login out successful! "]),
                #         dbc.ModalFooter([
                #             dbc.Button("OK", id= 'loginOut_back_button',href='/' ,className="ml-auto maginRight all-button")]
                #             ),
                #         ],
                #         id='login_out_modal',
                #         centered=True,
                #     ),
    ])

    return header_nav



@app.callback(
    Output('personal_center','children'),
    [Input('notifications','href')],
    )
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
        
# @app.callback(
#     Output('login_out_modal', "is_open"),
#     [Input('loginOut_back_button', "n_clicks"),
#     Input('login_out','n_clicks')],
#     [State('login_out_modal', "is_open")]
#     )
# def login_out_modal(loginOut_back_button,login_out,is_open):
#     if not dash.callback_context.triggered or not dash.callback_context.triggered[0]['value']:
#         raise PreventUpdate
#     if dash.callback_context.triggered[0]['prop_id'] == 'login_out.n_clicks':
#         return not is_open
#     if dash.callback_context.triggered[0]['prop_id'] == 'loginOut_back_button.n_clicks':
#         return not is_open
#     return is_open

@app.callback(
    Output('login','children'),
    [Input('login_out','n_clicks')]
    )
def is_loginIn(n_clicks):
    print(dash.callback_context.triggered)
    if not dash.callback_context.triggered or not dash.callback_context.triggered[0]['value']:
        raise PreventUpdate
    payload = get_payload()
    token = create_token(payload,exp_time=604800) ## not exp, 7days
    auth_T = hashlib.md5(token).hexdigest()
    dash.callback_context.response.set_cookie('T', auth_T, httponly = True)

    return loginOutSuccessfulLayout()
