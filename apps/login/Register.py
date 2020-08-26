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


temp_click = 0

def formlayout(err_msg='', Username='', Password='',RePassword='',Realname='',Email='',Phone='',District='',Country='',Province='',City='',Organization='',Verification_code=''):

    return html.Form(role='form', id='father_div',className=" login_form",children=[
        html.Div(className = 'login_err_div', children=[
            html.P(id='account_result',className='subwrong text-center text-danger', children=err_msg)
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('UserName: ',id='Username_label',htmlFor='Username',className='label_font_size xrequired'),
            dcc.Input(
                id='Username',
                type='text',
                value=Username,
                className="form-control input_part",
                placeholder='Enter Username',
                autoFocus=True,
                # required=True,
                # pattern= '^[a-zA-Z]+[a-zA-Z0-9_]*'
            ),
            html.Span(
                id='Username_info',
                children='Username can contain numbers, letters and underscores, cannot be empty and repeated, and cannot contain spaces and special characters',
                className='help-block'
            ),
        ]),
        html.Div(id='Password_form', className="form-group input_part ",children=[
            html.Label('PassWord: ',id='Password_label',htmlFor='Password',className='label_font_size xrequired'),
            dcc.Input(
                id='Password',
                type='password',
                className="form-control input_part",
                minLength= 8,
                maxLength= 25,
                value=Password,
                placeholder='Enter Password',
                # pattern='^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$'
            ),
            html.Span(
                id='Password_info',
                children='The password cannot be empty (8-25 characters), and must contain more than three types of lowercase letters, uppercase letters, numbers and special characters',
                className='help-block'
            ),
        ]),
        html.Div(id='Repassword_form', className="form-group input_part ",children=[
            html.Label('RePassWord: ',id='Repassword_label',htmlFor='RePassword',className='label_font_size xrequired'),
            dcc.Input(
                id='RePassword',
                type='password',
                className="form-control input_part",
                minLength= 8,
                maxLength= 25,
                value=RePassword,
                placeholder='Re-enter Password',
                # pattern='^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$'
            ),
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('RealName: ',id='realname_label',htmlFor='Realname',className='label_font_size'),
            dcc.Input(
                id='Realname',
                className="form-control input_part",
                type='text',
                value=Realname,
                placeholder='Enter your Real Name',
                # pattern= '^[a-zA-Z][a-zA-Z0-9_]*'
                )
        ]),
        html.Div(id="inputEmail3", className="form-group input_part ",children=[
            html.Label('Email: ',id='Email_label',htmlFor='Email',className='label_font_size xrequired'),
            dcc.Input(
                id='Email',
                # type='email',
                className="form-control input_part",
                value=Email,
                placeholder='Enter Email Address',
                # inputMode='email'
                # pattern= '^[a-zA-Z][a-zA-Z0-9_]*'
            )
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('Phone: ',id='phone_label',htmlFor='Phone',className='label_font_size'),
            dcc.Input(
                id='Phone',
                type='tel',
                className="form-control input_part",
                value=Phone,
                placeholder='Enter the Telephone',
                inputMode='numeric',
                # pattern= '^[0-9]{2}[+]?[0-9]+'
            )
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('District: ',id= 'District_label',htmlFor='District',className='label_font_size xrequired'),
            dcc.Dropdown(
                options=[{'label':i,'value':i} for i in Disoptions.keys()],
                id='District',
                value=District,
                persistence=False,
                placeholder='Select the District',
                # className=" dropdown_font_size input_part"
                )
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('Country: ',id='Country_label',className='label_font_size xrequired'),
            dcc.Dropdown(
                id='Country',
                placeholder='Select the Country',
                persistence=False,
                # className=" dropdown_font_size input_part",
                value=Country,
                )
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('Province: ',id='Province_label',className='label_font_size'),
            dcc.Dropdown(
                id='Province',
                placeholder='Select the Province',
                persistence=False,
                className=" dropdown_font_size input_part",
                value = Province,
                )
        ]),
        html.Div(className="form-group input_part ",children=[
            html.Label('City: ',id='City_label',className='label_font_size'),
            dcc.Dropdown(
                id='City',
                placeholder='Select the City',
                persistence=False,
                className=" dropdown_font_size input_part",
                value=City,
                )
        ]),
        html.Div(id='Organization_div', className="form-group input_part ",children=[
            html.Label('Organization: ',id='Organization_label',className='label_font_size xrequired'),
            dcc.Input(
                id='Organization',
                type='text',
                placeholder='Enter Organization',
                className="form-control input_part",
                value=Organization,
                )
        ]),
        html.Div(id='Verification_code_div', className="form-group input_part",children=[
            html.Label('Verification code: ',id='Verification_code_label',className='label_font_size xrequired'),
            html.Div(className='row',children=[
                html.Div(className='col-md-8 margin-left-15',children=[
                    dcc.Input(
                        id='Verification_code',
                        type='text',
                        placeholder='Enter Verification code',
                        className="col-md-8 form-control input_part",
                        value=Verification_code,
                        )]),
                html.Div(id='countdown_div',className='col-md-4',children=[
                    html.Button(id='countdown',type='button',n_clicks=0,className="btn btn-default margin-left-15",children='Send verification code')
                ])
            ])
        ]),
        html.Div(className = 'row clearfix', children=[
            html.Button('Create account',id='create_button',type='button',n_clicks=0,className="login_button col-sm-12 col-md-12 column"),
        ]),
        html.Div(className = 'row clearfix', children=[
            html.Button('Reset',id='clear_button',type='button',n_clicks=0,className="login_button col-sm-12 col-md-12 column")
        ])
    ])


def registerCommonLayout(children):
    return html.Div(className='container', children = [
        html.Div(className = 'row clearfix ', children=[
            html.Div(className='col-sm-1 col-md-3 column'),
            html.Div(className='col-sm-10 col-md-6 column findPassWd',children=[
                html.Div(className='findPassWd_header text-center', children=[
                    html.H2(children='Register for Stereomics'),
                ]),
                html.Div(id='register_content', children = children)        
            ]),
            html.Div(className='col-sm-1 col-md-3 column'),
        ])
    ])

def registerLayout():
    return registerCommonLayout(formlayout())

def registerSuccessfulLayout():
    return html.Div(className='findPassWd_content', children = [
        html.Span('Register successful!'),
        html.Br(),
        dcc.Link('OK', href='/Stereo-Draftsman/login'),
    ])

def registerFailedLayout():
    return html.Div(className='findPassWd_content', children = [
        html.Span('Register failed, please try again later'),
        html.Br(),
        dcc.Link('OK', href='/Stereo-Draftsman/register'),
    ])

@app.callback(
    Output('Country', 'options'),
    [Input('District', 'value')]
)
def set_neighborhood(District):
    try:
        neighborhoods = [i for i in Disoptions[District]["childrens"].keys()]
        return [{'label': v, 'value': v} for v in neighborhoods]
    except:
        return [{'label': 'None', 'value': 'None'}]

@app.callback(
    Output('Province', 'options'),
    [Input('Country', 'value'),
    Input('District', 'value')]
)
def set_province_neighborhood(country,District):
    try:
        province_neigh = [ii for ii in Disoptions[District]["childrens"][country]["childrens"]]
        return [{'label': v, 'value': v} for v in province_neigh]
    except:
        return [{'label': 'None', 'value': 'None'}]

@app.callback(
    Output('City', 'options'),
    [Input('Country', 'value'),
    Input('District', 'value'),
    Input('Province','value')]
)
def set_city_neighborhood(country,District,Province):
    try:
        city_neigh = [ii for ii in Disoptions[District]["childrens"][country]["childrens"][Province]['childrens']]
        return [{'label': v, 'value': v} for v in city_neigh]
    except:
        return [{'label': 'None', 'value': 'None'}]

@app.callback(
    [Output('countdown','children'),
    Output('countdown','disabled')],
    [Input('countdown', 'n_clicks'),
    Input('Email','value')],
    [State('Realname','value'),
    State('Username','value')]
    )
def ver_countdown(n_clicks,email,Realname,Username):
    global temp_click
    if email and Realname and Username:
        if not re.search(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email):
            temp_click = n_clicks
            return 'Examine email and try again!',True
        if temp_click < n_clicks:
            Ver.Send_email(email,Realname,Username)
            temp_click = n_clicks
            return 'Check your email, Please!',True
        temp_click = n_clicks
        return 'Send verification code',False
    else:
        return 'Send verification code',True

@app.callback(
    Output('account_result', 'children'),
    [Input('Username', 'value'),
     Input('Password', 'value'),
     Input('RePassword','value'),
     Input('Email','value')]
)
def update_username(username, new_pw, re_pw, email):
    u = Users(username)
    if u.checkExists():
        return 'Username already exists, please re-enter!'
    elif new_pw and not re.search(r'^(?=.*[a-zA-Z])(?=.*[1-9])(?=.*[\W]).{8,25}$',new_pw):
        return 'The password length must be between 8 and 25 characters, and must contain  numbers, letters and special characters'
    elif re_pw and not re.search(r'^(?=.*[a-zA-Z])(?=.*[1-9])(?=.*[\W]).{8,25}$',re_pw):
        return 'The password length must be between 8 and 25 characters, and must contain  numbers, letters and special characters'
    elif new_pw and re_pw and new_pw != re_pw:
        return 'Different two passwords, please re-enter'
    elif email and not re.search(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email):
        return 'The email format is wrong, please re-enter!'
    else:
        return ''

@app.callback(
    Output('register_content', 'children'),
    [Input('create_button', 'n_clicks')],
    [State('Username', 'value'),
    State('Password', 'value'),
    State('RePassword','value'),
    State('Realname','value'),
    State('Email','value'),
    State('Phone','value'),
    State('District','value'),
    State('Country','value'),
    State('Province', 'value'),
    State('City','value'),
    State('Organization','value'),
    State('Verification_code','value')])
def update_account(n_clicks,
            Username, Password,RePassword,
            Realname,Email,Phone,
            District,Country, Province, City,Organization,Verification_code):

    veri_code = conn_redis.get(Email)
    if not n_clicks :
        raise PreventUpdate

    if Username and Password and RePassword and Email and Organization and Verification_code:
        user = Users(username=Username, realname=Realname, email=Email, phone=Phone, district=District, country=Country, city=City, org=Organization)
        if not re.search(r'^[0-9a-zA-Z_]+$',Username):
            err_msg = 'The username is incorrect, please re-enter!'
        elif user.checkExists():
                err_msg = 'Username already exists, please re-enter!'
        elif not re.search(r'^(?=.*[a-zA-Z])(?=.*[1-9])(?=.*[\W]).{8,25}$',Password) and not re.search(r'^(?=.*[a-zA-Z])(?=.*[1-9])(?=.*[\W]).{8,25}$',RePassword):
            err_msg = 'The password input format is wrong, please input according to the rules!'
        elif Password != RePassword:
            err_msg = 'The two password entries are different, please re-enter!'
        elif not re.search(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',Email):
            err_msg = 'The email format is wrong, please re-enter!'
        elif Verification_code != veri_code:
            err_msg = 'The verification code is incorrect'
        else:
            user.password = Password
            if user.verifyPassword(password=Password):
                return registerSuccessfulLayout()
            else:
                return registerFailedLayout()
    else:
        err_msg = '* Part of the content is required, please fill in completely!'
    return formlayout(err_msg, Username, Password,RePassword,Realname,Email,Phone,'','','','',Organization,Verification_code)


@app.callback(
    [Output('Username', 'value'),
    Output('Password', 'value'),
    Output('RePassword','value'),
    Output('Realname','value'),
    Output('Email','value'),
    Output('Phone','value'),
    Output('District','value'),
    Output('Country','value'),
    Output('Province','value'),
    Output('City','value'),
    Output('Organization','value'),
    Output('Verification_code','value')],
    [Input('clear_button', 'n_clicks')])
def clear_input(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    return '','','','','','','','','','','',''
    