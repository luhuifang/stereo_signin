import dash
import re
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import apps.login.Verification_code as Ver
from spatialTrancriptomeReport import app
from apps.db.tableService.Users import Users
from apps.login.Register import registerLayout


def formlayout(err_msg='', Username='', Password=''):

    return html.Form(role='form',className="login_form",children=[
        html.Div(className = 'login_err_div', children=[
            html.P(id='login_result',className='subwrong text-center text-danger', children=err_msg)
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('UserName: ',id='login_username_label',htmlFor='Username',className='label_font_size'),
            dcc.Input(
                id='login_Username',
                type='text',
                value=Username,
                className="form-control input_part",
                placeholder='Enter Username',
                autoFocus=True,
            ),
            # html.Span(
            #     id='Username_info',
            #     children='Username can contain numbers, letters and underscores, cannot be empty, and cannot contain spaces and special characters',
            #     className='help-block'
            # ),
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('PassWord: ',id='login_password_label',htmlFor='Password',className='label_font_size'),
            dcc.Input(
                id='login_Password',
                type='password',
                className="form-control input_part",
                minLength= 8,
                maxLength= 25,
                value=Password,
                placeholder='Enter Password',
            ),
            # html.Span(
            #     id='Password_info',
            #     children='The password cannot be empty (8-25 characters), and must contain more than three types of lowercase letters, uppercase letters, numbers and special characters',
            #     className='help-block'
            # ),
            dcc.Link('Forget Password',href='/forgot')
        ]),
        html.Div(className = 'row clearfix', children=[
            html.Button('Sign in',id='login_button',type='button',n_clicks=0,className="login_button col-sm-12 col-md-12 column text-white"),
            # html.Button(children=[dcc.Link('Register', href='/Register',className='text-white')],id='register_button',type='button',n_clicks=0,className="register_button col-sm-5 col-md-5 column")
        ]),
        html.Div(className='row',children=[
            html.P(children = ['Not registered yet?',dcc.Link('Register', href='/Register',className='text-primary')],className='m-auto margin_top_15px')
            ])
    ])


def loginCommonLayout(children):
    return html.Div(className='container', children = [
        html.Div(className = 'row clearfix ', children=[
            html.Div(className='col-sm-1 col-md-3 column'),
            html.Div(className='col-sm-10 col-md-6 column findPassWd',children=[
                html.Div(className='findPassWd_header text-center', children=[
                    html.H2(children='Login for Stereomics'),
                ]),
                html.Div(id='login_content', children = children)        
            ]),
            html.Div(className='col-sm-1 col-md-3 column'),
        ])
    ])

def loginLayout():
    return loginCommonLayout(formlayout())

def loginSuccessfulLayout():
    return html.Div(className='findPassWd_content', children = [
        html.Span('Login successful!'),
        html.Br(),
        dcc.Link('OK', href='/'),
    ])

def loginFailedLayout():
    return html.Div(className='findPassWd_content', children = [
        html.Span('Login failed, please try again later'),
        html.Br(),
        dcc.Link('OK', href='/Login'),
    ])

@app.callback(
    Output('login_content', 'children'),
    [Input('login_button', 'n_clicks')],
    [State('login_Username','value'),
    State('login_Password','value')]
    )
def login_in(n_clicks,Username,Password):
    if not n_clicks :
        raise PreventUpdate
    if Username and Password:
        u = Users(username=Username)
        if  u.checkExists() and u.verifyPassword(Password):
            return loginSuccessfulLayout()
        else:
            err_msg = 'The account password is wrong, please confirm whether it is entered correctly!'
        print(u.checkExists(),u.verifyPassword(Password))
    else:
        raise PreventUpdate
    
    return formlayout(err_msg=err_msg, Username='', Password='')

