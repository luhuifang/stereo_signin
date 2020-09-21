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
from apps.db.tableService.UserRole import UserRole
from apps.login.country_dict import options as Disoptions
from apps.login.connect_redis import r as conn_redis
from apps.login.Register import registerLayout


def formlayout(err_msg='',Username='', Email='', Password='', RePassword='',Verification_code=''):

    return html.Form(role='form',className="login_form",children=[
        html.Div(className = 'login_err_div', children=[
            html.P(id='forgot_result',className='subwrong text-center text-danger', children=err_msg)
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('UserName: ',id='Username_label',htmlFor='Username',className='label_font_size xrequired'),
            dcc.Input(
                id='for_Username',
                type='text',
                value=Username,
                className="form-control input_part",
                placeholder='Enter Username',
                autoFocus=True,
                # required=True,
                # pattern= '^[a-zA-Z]+[a-zA-Z0-9_]*'
            ),
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('Email: ',id='forgot_email_label',htmlFor='Email',className='label_font_size xrequired'),
            dcc.Input(
                id='forgot_email',
                type='text',
                value=Email,
                className="form-control input_part",
                placeholder='Enter Email',
                autoFocus=True,
            ),
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('New PassWord: ',id='forget_password_label',htmlFor='Password',className='label_font_size xrequired'),
            dcc.Input(
                id='forgot_Password',
                type='password',
                className="form-control input_part",
                minLength= 8,
                maxLength= 25,
                value=Password,
                placeholder='Enter New Password',
            ),
            html.Div(id='Repassword_form', className="form-group input_part ",children=[
            html.Label('RePassWord: ',id='forgot_Repassword_label',htmlFor='RePassword',className='label_font_size xrequired'),
            dcc.Input(
                id='forgot_RePassword',
                type='password',
                className="form-control input_part",
                minLength= 8,
                maxLength= 25,
                value=RePassword,
                placeholder='Re-enter New Password',
            ),
        ]),
            html.Div(id='Verification_code_div', className="form-group input_part",children=[
                html.Label('Verification code: ',id='Verification_code_label',className='label_font_size xrequired'),
                html.Div(className='row',children=[
                    html.Div(className='col-md-6 margin-left-15',children=[
                        dcc.Input(
                            id='forgot_Verification_code',
                            type='text',
                            placeholder='Enter Verification code',
                            className=" form-control input_part",
                            value=Verification_code,
                            )]),
                    html.Div(id='countdown_div',className='col-md-6',children=[
                        html.Button(id='for_countdown',type='button',n_clicks=0,className="btn btn-default ",children='Send verification code')
                    ])
                ])
            ]),
            html.Div(className = 'login_err_div', children=[
                html.P(id='for_sendEmail_res',className='subwrong text-center text-danger')
            ]),
        ]),
        html.Div(className = 'row clearfix', children=[
            html.Button('Reset password',id='reset_button',type='button',n_clicks=0,className="login_button col-sm-12 col-md-12 column text-white"),
        ]),
        html.Div(className='row',children=[
            html.P(children = ['Already registered?',dcc.Link('Login', href='/Login',className='text-primary')],className='m-auto margin_top_15px')
            ])
    ])


def forgotCommonLayout(children):
    return html.Div(className='container', children = [
        html.Div(className = 'row clearfix ', children=[
            html.Div(className='col-sm-1 col-md-3 column'),
            html.Div(className='col-sm-10 col-md-6 column findPassWd',children=[
                html.Div(className='findPassWd_header text-center', children=[
                    html.H2(children='Reset Password'),
                ]),
                html.Div(id='forgot_content', children = children)        
            ]),
            html.Div(className='col-sm-1 col-md-3 column'),
        ])
    ])

def forgotLayout():
    return forgotCommonLayout(formlayout())

def forgotSuccessfulLayout():
    return html.Div(className='findPassWd_content', children = [
        html.Span('Reset password successful!'),
        html.Br(),
        dcc.Link('OK', href='/Login'),
    ])

def forgotFailedLayout():
    return html.Div(className='findPassWd_content', children = [
        html.Span('Reset password failed, please try again later'),
        html.Br(),
        dcc.Link('OK', href='/Login'),
    ])


@app.callback(
    Output('forgot_result', 'children'),
    [Input('for_Username','value'),
     Input('forgot_Password', 'value'),
     Input('forgot_RePassword','value'),
     Input('forgot_email','value')]
)
def update_username( username, new_pw, re_pw, email):
    u = Users(username=username,email=email)
    if username and not u.checkExists():
        return 'Username not exists, please re-enter!'
    elif email and not u.checkEmailExists():
        return 'Email is not registered, you can choose to register!'
    elif new_pw and not re.search(r'^(?=.*[a-zA-Z])(?=.*[1-9])(?=.*[\W]).{8,25}$',new_pw):
        return 'The password length must be between 8 and 25 characters, and must contain  numbers, letters and special characters'
    elif re_pw and not re.search(r'^(?=.*[a-zA-Z])(?=.*[1-9])(?=.*[\W]).{8,25}$',re_pw):
        return 'The password length must be between 8 and 25 characters, and must contain  numbers, letters and special characters'
    elif new_pw and re_pw and new_pw != re_pw:
        return 'Different two passwords, please re-enter'
    elif email and not re.search(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]{2,6})+$',email):
        return 'The email format is wrong, please re-enter!'
    else:
        return ''

@app.callback(
    [Output('for_countdown','disabled'),
    Output('for_sendEmail_res','children')],
    [Input('for_countdown', 'n_clicks'),
    Input('forgot_email','value'),
    Input('for_Username','value')]
    )
def ver_countdown(n_clicks,email,username):    
    if email:
        if not re.search(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]{2,6})+$',email):
            return True,''
        if dash.callback_context.triggered[0]['prop_id'] == 'for_countdown.n_clicks':
            send_result = Ver.Send_email(email,username)
            if send_result['code'] == 200:
                return True,'Email sent successfully, please check!'
            else:
                return False,'The server is under maintenance, please register later!'
        return False,''
    else:
        return True,''

@app.callback(
    Output('forgot_content', 'children'),
    [Input('reset_button', 'n_clicks')],
    [State('for_Username','value'),
    State('forgot_email', 'value'),
    State('forgot_Password', 'value'),
    State('forgot_RePassword','value'),
    State('forgot_Verification_code','value')])
def update_account(n_clicks, Username, Email, Password, RePassword,Verification_code):
    if not n_clicks :
        raise PreventUpdate
    veri_code = conn_redis.get(Email)
    if Username and Password and RePassword and Email and Verification_code:
        user = Users(username=Username,email=Email)

        if not user.checkExists():
            err_msg = 'Username not exists, please re-enter!'
        elif not user.checkEmailExists():
            err_msg = 'Email is not registered, you can choose to register!'
        elif not re.search(r'^(?=.*[a-zA-Z])(?=.*[1-9])(?=.*[\W]).{8,25}$',Password) and not re.search(r'^(?=.*[a-zA-Z])(?=.*[1-9])(?=.*[\W]).{8,25}$',RePassword):
            err_msg = 'The password input format is wrong, please input according to the rules!'
        elif Password != RePassword:
            err_msg = 'The two password entries are different, please re-enter!'
        elif not re.search(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]{2,6})+$',Email):
            err_msg = 'The email format is wrong, please re-enter!'
        elif Verification_code != veri_code:
            err_msg = 'The verification code is incorrect'
        else:
            user.password = Password
            if user.verifyPassword(password=Password):
                return forgotSuccessfulLayout()
            else:
                return forgotFailedLayout()
    else:
        err_msg = '* Part of the content is required, please fill in completely!'
    return formlayout(err_msg, Username, Email, Password, RePassword, Verification_code)

