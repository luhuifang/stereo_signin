import dash
import re
import hashlib
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import apps.login.Verification_code as Ver
from spatialTrancriptomeReport import app
from apps.db.tableService.Users import Users
from apps.login.Register import registerLayout
from apps.login.connect_redis import r
from apps.login.token_verification import get_payload,validate_token,create_token
# from apps.login.Customer_control import CustomerControl


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

def loginSuccessfulLayout(pathname):
    return html.Div(className='findPassWd_content', children = [
        html.Span('Login successful!'),
        html.Br(),
        dcc.Link('OK', href=pathname),
    ])

def loginFailedLayout():
    return html.Div(className='findPassWd_content', children = [
        html.Span('Login failed, please try again later'),
        html.Br(),
        dcc.Link('OK', href='/Login'),
    ])

@app.callback(
    Output('login_content', 'children'),
    [Input('login_button', 'n_clicks'),
    Input('login_Username','n_submit'),
    Input('login_Password','n_submit')],
    [State('login_Username','value'),
    State('login_Password','value')]
    )
def login_in(n_clicks,login_Username,login_Password,Username,Password):
    if not dash.callback_context.triggered:
        raise PreventUpdate
    if Username and Password:
        u = Users(username=Username)
        if  u.checkExists() and u.verifyPassword(Password):
            user_id = u.getId()
            payload = get_payload(user_id,org=u.Organization,login_flag='logined')
            token = create_token(payload,exp_time=604800) ## not exp, 7days
            auth_T = hashlib.md5(token).hexdigest()
            r.set(auth_T, token, ex=3600)
            # print('payload',payload,'auth_T',auth_T,'\ntoken',token,'\nUsername',Username,'\nuserID',user_id)
            dash.callback_context.response.set_cookie('T', auth_T, httponly = True)
            userRoleid = u.UserRoleID
            if userRoleid == 1 or userRoleid == 2:
                return loginSuccessfulLayout('/Customer_console')
            elif userRoleid == 8:
                return loginSuccessfulLayout('/Manager_console')
        else:
            err_msg = 'The account password is wrong, please confirm whether it is entered correctly!'
        # print(u.checkExists(),u.verifyPassword(Password))
    else:
        err_msg = 'The username and password cannot be empty!'
    
    return formlayout(err_msg=err_msg, Username='', Password='')



# if user.verifyPassword(passwd): ## successful
#     user_id = user.getId()
#     payload = get_payload(user_id, org=user.Organization, login_flag='logined')
#     token = generate_token_from_payload(payload, exp_time=604800) ## not exp, 7days
#     auth_T = hashlib.md5(token).hexdigest()
#     r.set(auth_T, token, ex=3600)
#     if black_count is not None:
#         r.delete(username)
#         href = '/Stereo-Draftsman/report/index'
#         dash.callback_context.response.set_cookie('T', auth_T, httponly = True)

#     return ['', href, True]