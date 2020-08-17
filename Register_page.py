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

styles={
    'label':{'float': 'left','width': '20%','height': '40px','digplay':'inline-block',
    'margin': '2px','text-align': 'center','font-size': '18px','font-weight': '300','color': 'black','line-height': '20px'},
    'input':{'float': 'right','width': '60%','height': '40px','digplay':'inline-block','margin': '2px'},
    'dropdown':{'position':'relative','left':'350px','bottom':'-250px','width': '300px','display': 'inline-block','margin': '30px'},
    'button':{'position':'relative','left':'30px','bottom':'-130px','float': 'right','width': '55%','height': '40px','digplay':'inline-block','margin': '2px','digplay':'inline-block'}
}

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__,title='Register')

layout=html.Div(children=[
    html.H1(children='Register',style={'text-align':'center'}),
        html.Form(id='Username_form',n_clicks=0,children=[
            html.Label('*UserName: ',style=styles['label']),
            dcc.Input(
                id='Username',
                type='text',
                value='',
                placeholder='请输入用户名',
                autoFocus=True,
                # required=True,
                pattern= '^[a-zA-Z]+[a-zA-Z0-9_]*'
                ),
            # html.Label('可以包含数字，字母，下划线；不能包含空格和特殊字符')
            ]
            ,style=styles['input']
            ),html.Div(id='Username_error',style={'position':'absolute','left':'980px','bottom':'645px','color':'red','font-size': '12px'}),
        html.Form(id='Password_form',n_clicks=0,children=[
            html.Label('*PassWord: ',style=styles['label']),
            dcc.Input(
                id='Password',
                type='password',
                minLength= 8,
                maxLength= 25,
                value='',
                # required=True,
                placeholder='请输入密码',
                pattern='^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$'
                ),
            # html.Label('不能为空，至少8个字符，最多25个字符，必须且只能包含数字，字母，下划线中的2种及以上')
            ]
            ,style=styles['input']
            ),html.Div(id='Password_error',style={'position':'absolute','left':'980px','bottom':'600px','color':'red','font-size': '12px'}),
        html.Form(id='Repassword_form',n_clicks=0,children=[
            html.Label('*Re-type PassWord: ',style=styles['label']),
            dcc.Input(
                id='RePassword',
                type='password',
                minLength= 8,
                maxLength= 25,
                value='',
                # required=True,
                placeholder='请重新输入密码',
                pattern='^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$'
                ),
            # html.Label('不能为空，至少8个字符，最多25个字符，必须且只能包含数字，字母，下划线中的2种及以上')
            ]
            ,style=styles['input']
            ),html.Div(id='Repassword_error',style={'position':'absolute','left':'980px','bottom':'555px','color':'red','font-size': '12px'}),
        html.Div([
            html.Label('RealName: ',style=styles['label']),
            dcc.Input(
                id='Realname',
                type='text',
                value='',
                placeholder='请输入姓名',
                pattern= '^[a-zA-Z][a-zA-Z0-9_]*'
                )
            ]
            ,style=styles['input']
            ),
        html.Div([
            html.Label('*Email: ',style=styles['label']),
            dcc.Input(
                id='Email',
                type='email',
                value='',
                placeholder='请输入邮箱',
                inputMode='email'
                # pattern= '^[a-zA-Z][a-zA-Z0-9_]*'
                )
            ]
            ,style=styles['input']
            ),
        html.Div([
            html.Label('Phone: ',style=styles['label']),
            dcc.Input(
                id='Phone',
                type='tel',
                value='',
                placeholder='请输入电话',
                inputMode='numeric',
                pattern= '^[0-9]{2}[+]?[0-9]+'
                )
            ]
            ,style=styles['input']
            ),
        html.Label('*District: ',style={'position':'relative','left':'550px','bottom':'-45px','float': 'left','width': '20%','height': '40px','digplay':'inline-block',
    'margin': '2px','text-align': 'center','font-size': '18px','font-weight': '200','color': 'black','line-height': '20px'}),
        html.Div([
            dcc.Dropdown(
                options=[{'label':i,'value':i} for i in Dis.options.keys()],
                id='District',
                value="Asia",
                persistence=True
                )
            ]
            ,style={'position':'relative','left':'760px','bottom':'-230px','width': '165px','display': 'inline-block','margin': '30px'}
            ),
        html.Label('*Country: ',style={'position':'relative','left':'550px','bottom':'-50px','float': 'left','width': '20%','height': '40px','digplay':'inline-block',
    'margin': '2px','text-align': 'center','font-size': '18px','font-weight': '200','color': 'black','line-height': '20px'}),
        html.Div([
            dcc.Dropdown(id='Country')
            ],id='country_div'
            ,style={'position':'relative','left':'535px','bottom':'-280px','width': '165px','display': 'inline-block','margin': '30px'}
            ),
        html.Label('*City: ',style={'position':'relative','left':'250px','bottom':'-100px','float': 'left','width': '20%','height': '40px','digplay':'inline-block',
    'margin': '2px','text-align': 'center','font-size': '18px','font-weight': '200','color': 'black','line-height': '20px'}),
        html.Div([
            
            dcc.Dropdown(id='City')
            ],id='city_div'
            ,style={'position':'relative','left':'760px','bottom':'-230px','width': '165px','display': 'inline-block','margin': '30px'}
            ),
        html.Div([
            html.Label('*Organization: ',style=styles['label']),
            dcc.Input(
                id='Organization',
                type='text',
                placeholder='请输入所在机构',
                value=''
                )
            ]
            ,style={'position':'relative','bottom':'-110px','float': 'right','width': '60%','height': '40px','digplay':'inline-block','margin': '2px'}
            ),
        html.Div([
            html.Button('Create account',id='create_button',n_clicks=0,style={'margin-left':'5px','margin-right':'5px','color':'black'}),
            html.Button([dcc.Link('Cancel', href='/')],id='Cancel_button',n_clicks=0,style={'margin-left':'5px','margin-right':'5px','color':'black'})
            ]
            ,style=styles['button']
            ),
        html.Div(id='account_result',
            style={'position':'relative','left':'650px','bottom':'-100px','float': 'left','width': '20%','height': '40px','digplay':'inline-block',
    'margin': '2px','text-align': 'center','font-size': '14px','font-weight': '200','color': 'red','line-height': '20px'})
    ])


# @app.callback(
#     Output('country_div', 'children'),
#     [Input('District', 'value')]
# )
# def set_neighborhood(District):
#     neighborhoods = [i['name_en'] for i in Dis.options[District]["childrens"]]
#     return dcc.Dropdown(
#         id='Country',
#         value=neighborhoods[0],
#         options=[{'label': v, 'value': v} for v in neighborhoods],
#         persistence_type='session',
#         persistence=District
#             )
# @app.callback(
#     Output('city_div', 'children'),
#     [Input('Country', 'value'),
#     Input('District', 'value')]
# )
# def set_city_neighborhood(country,District):
#     for i in Dis.options[District]["childrens"]:
#         # print(country,i['name_en'])
#         if i['name_en'] == country:
#             city_neigh = [ii['name_en'] for ii in i["childrens"]]
#             if city_neigh:
#                 return dcc.Dropdown(
#                     id='City',
#                     value=city_neigh[0],
#                     options=[{'label': v, 'value': v} for v in city_neigh],
#                     persistence_type='session',
#                     persistence=country
#                 )
#             else:
#                 return dcc.Dropdown(
#                     id='City',
#                     value='',
#                     options=[{'label': v, 'value': v} for v in city_neigh],
#                     persistence_type='session',
#                     persistence=country
#                 )
# @app.callback(
#     Output('Username_error', 'children'),
#     [Input('Username', 'value'),
#     Input('Username_form','n_clicks')])
# def update_username_info(Username,n_click):
#     conn = ConnectMYSQL(**MYSQL)
#     # cursor = conn.cursor()
#     sql = 'select UserID from {0} where LoginName="{1}"'.format('users',Username)
#     # print(sql)
#     if not re.search(r'^[a-zA-Z]+[a-zA-Z0-9_]*',Username) and n_click > 1:
#         return html.Div('用户名输入不正确，请重新输入！')
#     elif re.search(r'^[a-zA-Z]+[a-zA-Z0-9_]*',Username):
#         res=conn.searchDB(sql)
#         if res:
#             return html.Div('用户名已存在，请重新输入！')
#         else:
#             return html.Div('OK')

# @app.callback(
#     Output('Password_error', 'children'),
#     [Input('Password', 'value'),
#     Input('Password_form','n_clicks')])
# def update_username_info(Password,n_click):
#     if not re.search(r'^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$',Password) and n_click>1:
#         return html.Div('密码输入格式不对，请按规则输入！')

# @app.callback(
#     Output('Repassword_error', 'children'),
#     [Input('RePassword', 'value'),
#     Input('Password', 'value'),
#     Input('Repassword_form','n_clicks')])
# def update_username_info(Repassword,Password,n_click):
#     if not re.search(r'^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$',Repassword) and n_click>1:
#         return html.Div('密码输入格式不对，请按规则输入！')
#     if Password != Repassword and n_click>1:
#         return html.Div('两次密码输入不一样，请重新输入！')

# @app.callback(
#     Output('account_result', 'children'),
#     [Input('create_button', 'n_clicks')],
#     [State('Username', 'value'),
#     State('Password', 'value'),
#     State('RePassword','value'),
#     State('Realname','value'),
#     State('Email','value'),
#     State('Phone','value'),
#     State('District','value'),
#     State('Country','value'),
#     State('City','value'),
#     State('Organization','value')])
# def update_account(n_clicks,Username, Password,RePassword,Realname,Email,Phone,District,Country,City,Organization):
#     if Username and Password and RePassword and Email and Organization:
#         update_info = Users(Username, Password,Realname,Email,Phone,District,Country,City,Organization)
#         if not re.search(r'^[a-zA-Z]+[a-zA-Z0-9_]*',Username):
#             return html.Div('用户名输入不正确，请重新输入！')
#         if not re.search(r'^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$',Password) and not re.search(r'^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$',RePassword):
#             return html.Div('密码输入格式不对，请按规则输入！')
#         if Password != RePassword:
#             return html.Div('两次密码输入不一样，请重新输入！')
#         update_info.add()
#         return html.Div('注册成功！')
#     else:
#         return html.Div('*部份为必填内容，请填写完整！')

# if __name__ == '__main__':
#     app.run_server(debug=True)
