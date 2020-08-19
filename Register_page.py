import re
import dash
import json
import callbacks
import pandas as pd
import country as Dis
import dash_core_components as dcc
import dash_html_components as html
from spatialTrancriptomeReport import app
from apps.db.tableService.Users import Users
from apps.db.tableService.UserRole import UserRole
from dash.dependencies import Input, Output, State


layout=html.Form(id='father_div',className="form-group login_form form_bg",children=[
    html.Div(className="form-group",children=[
        html.H1(children='Register',className='text-center'),
        html.Div(id='Username_form',className='row ',children=[
            html.Label('UserName: ',id='Username_label',htmlFor='Username',className='col-md-offset-4 label_font_size label_before'),
            html.Br(),
            html.Div(className= 'col-md-3 col-md-offset-4',children=[
                dcc.Input(
                    id='Username',
                    type='text',
                    value='',
                    className="form-control input_part",
                    placeholder='Enter Username',
                    autoFocus=True,
                    # required=True,
                    # pattern= '^[a-zA-Z]+[a-zA-Z0-9_]*'
                    )
                ]),
            # html.Div(id='Username_error'),
            html.P(
                id='Username_info',
                children='Username can contain numbers, letters and underscores, cannot be empty and repeated, and cannot contain spaces and special characters',
                className='fill_request'
                ),
            ]),
        html.Div(id='Password_form',className='row',n_clicks=0,children=[
            html.Label('PassWord: ',id='Password_label',htmlFor='Password',className='col-md-offset-4 label_font_size label_before'),
            html.Br(),
            html.Div(className= 'col-md-3 col-md-offset-4',children=[
                dcc.Input(
                    id='Password',
                    type='password',
                    className="form-control input_part",
                    minLength= 8,
                    maxLength= 25,
                    value='',
                    placeholder='Enter Password',
                    # pattern='^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$'
                    )
                ]),
            # html.Div(id='Password_error')
            html.P(
                id='Password_info',
                children='The password cannot be empty (8-25 characters), and must contain more than three types of lowercase letters, uppercase letters, numbers and special characters',
                className='fill_request'
                ),
            ]),
        html.Div(id='Repassword_form',className='row',n_clicks=0,children=[
            html.Label('RePassWord: ',id='Repassword_label',htmlFor='RePassword',className='col-md-offset-4 label_font_size label_before'),
            html.Br(),
            html.Div(className= 'col-md-3 col-md-offset-4',children=[
                dcc.Input(
                    id='RePassword',
                    type='password',
                    className="form-control input_part",
                    minLength= 8,
                    maxLength= 25,
                    value='',
                    placeholder='Re-enter Password',
                    # pattern='^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$'
                    )
                ]),
                # html.Div(id='Repassword_error')
            ]),
        html.Div(className='row',children=[
            html.Label('RealName: ',id='realname_label',htmlFor='Realname',className='col-md-offset-4 label_font_size'),
            html.Br(),
            html.Div(className= 'col-md-3 col-md-offset-4',children=[
                dcc.Input(
                    id='Realname',
                    className="form-control input_part",
                    type='text',
                    value='',
                    placeholder='Enter your Real Name',
                    # pattern= '^[a-zA-Z][a-zA-Z0-9_]*'
                    )
                ])
            ]),
        html.Div(className='row',id="inputEmail3",children=[
            html.Label('Email: ',id='Email_label',htmlFor='Email',className='col-md-offset-4 label_font_size label_before'),
            html.Br(),
            html.Div(className= 'col-md-3 col-md-offset-4',children=[
                dcc.Input(
                    id='Email',
                    # type='email',
                    className="form-control input_part",
                    value='',
                    placeholder='Enter Email Address',
                    # inputMode='email'
                    # pattern= '^[a-zA-Z][a-zA-Z0-9_]*'
                    )
                ])
            ]),
        html.Div(className='row',children=[
            html.Label('Phone: ',id='phone_label',htmlFor='Phone',className='col-md-offset-4 label_font_size'),
            html.Br(),
            html.Div(className= 'col-md-3 col-md-offset-4',children=[
                dcc.Input(
                    id='Phone',
                    type='tel',
                    className="form-control input_part",
                    value='',
                    placeholder='Enter the Telephone',
                    inputMode='numeric',
                    # pattern= '^[0-9]{2}[+]?[0-9]+'
                    )
                ])
            ]),
        html.Div(className='row',children=[
            html.Label('District: ',id= 'District_label',htmlFor='District',className='col-md-offset-4 label_font_size label_before'),
            html.Br(),
            html.Div(className= 'col-md-3 col-md-offset-4',id='District_div',children=[
                dcc.Dropdown(
                    options=[{'label':i,'value':i} for i in Dis.options.keys()],
                    id='District',
                    value="",
                    # persistence=True,
                    placeholder='Select the District',
                    className=" dropdown_font_size input_part"
                    )
                ])
            ]),
        html.Div(className='row',children=[
            html.Label('Country: ',id='Country_label',className='col-md-offset-4 label_font_size label_before'),
            html.Br(),
            html.Div(className= 'col-md-3 col-md-offset-4',id='country_div',children=[
                dcc.Dropdown(
                    id='Country',
                    placeholder='Select the Country',
                    className=" dropdown_font_size input_part"
                    )
                ])
            ]),
        html.Div(className='row',children=[
            html.Label('Province: ',id='Province_label',className='col-md-offset-4 label_font_size label_before'),
            html.Br(),
            html.Div(className= 'col-md-3 col-md-offset-4',id='province_div',children=[
                dcc.Dropdown(
                    id='Province',
                    placeholder='Select the Province',
                    className=" dropdown_font_size input_part"
                    )
                ])
            ]),
        html.Div(className='row',children=[
            html.Label('City: ',id='City_label',className='col-md-offset-4 label_font_size label_before'),
            html.Br(),
            html.Div(className= 'col-md-3 col-md-offset-4',id='city_div',children=[
                dcc.Dropdown(
                    id='City',
                    placeholder='Select the City',
                    className=" dropdown_font_size input_part"
                    )
                ])
            ]),
        html.Div(className= 'row',id='Organization_div',children=[
            html.Label('Organization: ',id='Organization_label',className='col-md-offset-4 label_font_size label_before'),
            html.Br(),
            html.Div(className= 'col-md-3 col-md-offset-4',children=[
                dcc.Input(
                    id='Organization',
                    type='text',
                    placeholder='Enter Organization',
                    className="form-control input_part",
                    value=''
                    )
                ])
            ]),
        html.Div(children=[
            html.Div(id='account_result',className='text-center text-danger')
        ]),
        html.Div(className='row',children=[
            html.Div(id='button_div',className='row',children=[
                html.Button('Create account',id='create_button',type='button',n_clicks=0,className="btn-primary col-md-3 col-md-offset-4 login_button")
                ]),
            html.Div(className='row',children=[
                dcc.Link('Rerurn', href='/',id='Cancel_button',className="btn-primary col-md-3 col-md-offset-4 login_button text-center")
                ]),
            html.Div(className='row',children=[
                html.Button('Reset',id='clear_button',type='button',n_clicks=0,className="btn-primary col-md-3 col-md-offset-4 login_button")
                ])
        ]),
    ])
])

