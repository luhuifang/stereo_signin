import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import json
from pymysql import connect
import country as Dis
import re
from apps.db.tableService.Users import Users
from apps.db.tableService.UserRole import UserRole
from apps.db.tableService.ConnectMYSQL import ConnectMYSQL
from apps.db.database_settings import MYSQL_LOCAL as MYSQL
from spatialTrancriptomeReport import app
import callbacks


layout=html.Div(id='father_div',children=[
    html.H1(children='Register'),
        html.Form(id='Username_form',children=[
            html.Label('UserName: ',id='Username_label'),
            html.Br(),
            dcc.Input(
                id='Username',
                type='text',
                value='',
                placeholder='Enter Username',
                autoFocus=True,
                # required=True,
                # pattern= '^[a-zA-Z]+[a-zA-Z0-9_]*'
                ),
            html.Div(id='Username_error'),
            ]
            ),
        html.Form(id='Password_form',n_clicks=0,children=[
            html.Label('PassWord: ',id='Password_label'),
            html.Br(),
            dcc.Input(
                id='Password',
                type='password',
                minLength= 8,
                maxLength= 25,
                value='',
                # required=True,
                placeholder='Enter Password',
                # pattern='^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$'
                ),
            html.Div(id='Password_error')
            ]
            ),
        html.Form(id='Repassword_form',n_clicks=0,children=[
            html.Label('RePassWord: ',id='Repassword_label'),
            html.Br(),
            dcc.Input(
                id='RePassword',
                type='password',
                minLength= 8,
                maxLength= 25,
                value='',
                # required=True,
                placeholder='Re-enter Password',
                # pattern='^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$'
                ),
            html.Div(id='Repassword_error')
            ]
            ),
        html.Form([
            html.Label('RealName: ',id='realname_label'),
            html.Br(),
            dcc.Input(
                id='Realname',
                type='text',
                value='',
                placeholder='Enter your Real Name',
                # pattern= '^[a-zA-Z][a-zA-Z0-9_]*'
                )
            ]
            ),
        html.Form([
            html.Label('Email: ',id='Email_label'),
            html.Br(),
            dcc.Input(
                id='Email',
                # type='email',
                value='',
                placeholder='Enter Email Address',
                # inputMode='email'
                # pattern= '^[a-zA-Z][a-zA-Z0-9_]*'
                )
            ]
            ),
        html.Form([
            html.Label('Phone: ',id='phone_label'),
            html.Br(),
            dcc.Input(
                id='Phone',
                type='tel',
                value='',
                placeholder='Enter the Telephone',
                inputMode='numeric',
                # pattern= '^[0-9]{2}[+]?[0-9]+'
                )
            ]
            ),
        html.Label('District: ',id= 'District_label'),
        html.Br(),
        html.Div([
            dcc.Dropdown(
                options=[{'label':i,'value':i} for i in Dis.options.keys()],
                id='District',
                value="Asia",
                persistence=True
                )
            ],id='District_div'
            ),
        html.Label('Country: ',id='Country_label',
    ),
        html.Br(),
        html.Div([
            dcc.Dropdown(id='Country')
            ],id='country_div'
            ),
        html.Label('Province: ',id='Province_label',
    ),
        html.Br(),
        html.Div([
            dcc.Dropdown(id='Province')
            ],id='province_div'
            ),
        html.Label('City: ',id='City_label',
    ),
        html.Br(),
        html.Div([
            dcc.Dropdown(id='City')
            ],id='city_div'
            ),
        html.Div([
            html.Label('Organization: ',id='Organization_label'),
            html.Br(),
            dcc.Input(
                id='Organization',
                type='text',
                placeholder='Enter Organization',
                value=''
                )
            ],id='Organization_div'
            # ,style={'position':'relative','bottom':'-150px','float': 'right','width': '60%','height': '40px','digplay':'inline-block','margin': '2px'}
            ),
        html.Div(id='button_div',children=[
            html.Button('Create account',id='create_button',n_clicks=0),
            html.Button([dcc.Link('Cancel', href='/')],id='Cancel_button',n_clicks=0),
            html.Button('Reset',id='clear_button',n_clicks=0)
            ]
            # ,style=styles['button']
            ),
        html.Div(id='account_result')
    ])
