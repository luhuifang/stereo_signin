from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from spatialTrancriptomeReport import app
import country as Dis
import re
from apps.db.tableService.Users import Users
from apps.db.tableService.UserRole import UserRole
from apps.db.tableService.ConnectMYSQL import ConnectMYSQL
from apps.db.database_settings import MYSQL_LOCAL as MYSQL

@app.callback(
    Output('country_div', 'children'),
    [Input('District', 'value')]
)
def set_neighborhood(District):
    neighborhoods = [i['name_en'] for i in Dis.options[District]["childrens"]]
    return dcc.Dropdown(
        id='Country',
        value=neighborhoods[0],
        options=[{'label': v, 'value': v} for v in neighborhoods],
        persistence_type='session',
        persistence=District
            )
@app.callback(
    Output('city_div', 'children'),
    [Input('Country', 'value'),
    Input('District', 'value')]
)
def set_city_neighborhood(country,District):
    for i in Dis.options[District]["childrens"]:
        # print(country,i['name_en'])
        if i['name_en'] == country:
            city_neigh = [ii['name_en'] for ii in i["childrens"]]
            if city_neigh:
                return dcc.Dropdown(
                    id='City',
                    value=city_neigh[0],
                    options=[{'label': v, 'value': v} for v in city_neigh],
                    persistence_type='session',
                    persistence=country
                )
            else:
                return dcc.Dropdown(
                    id='City',
                    value='',
                    options=[{'label': v, 'value': v} for v in city_neigh],
                    persistence_type='session',
                    persistence=country
                )
@app.callback(
    Output('Username_error', 'children'),
    [Input('Username', 'value'),
    Input('Username_form','n_clicks')])
def update_username_info(Username,n_click):
    conn = ConnectMYSQL(**MYSQL)
    # cursor = conn.cursor()
    sql = 'select UserID from {0} where LoginName="{1}"'.format('users',Username)
    if not re.search(r'^[a-zA-Z]+[a-zA-Z0-9_]*',Username) and n_click > 1:
        return html.Div('用户名输入不正确，请重新输入！')
    elif re.search(r'^[a-zA-Z]+[a-zA-Z0-9_]*',Username):
        res=conn.searchDB(sql)
        if res:
            return html.Div('用户名已存在，请重新输入！')
        else:
            return html.Div('用户名可用！')

@app.callback(
    Output('Password_error', 'children'),
    [Input('Password', 'value'),
    Input('Password_form','n_clicks')])
def update_username_info(Password,n_click):
    if not re.search(r'^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$',Password) and n_click > 1:
        return html.Div('密码输入格式不对，请按规则输入！')

@app.callback(
    Output('Repassword_error', 'children'),
    [Input('RePassword', 'value'),
    Input('Password', 'value'),
    Input('Repassword_form','n_clicks')])
def update_username_info(Repassword,Password,n_click):
    if not re.search(r'^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$',Repassword) and n_click > 1:
        return html.Div('密码输入格式不对，请按规则输入！')
    if Password != Repassword and n_click>1:
        return html.Div('两次密码输入不一样，请重新输入！')

@app.callback(
    Output('account_result', 'children'),
    [Input('create_button', 'n_clicks')],
    [State('Username', 'value'),
    State('Password', 'value'),
    State('RePassword','value'),
    State('Realname','value'),
    State('Email','value'),
    State('Phone','value'),
    State('District','value'),
    State('Country','value'),
    State('City','value'),
    State('Organization','value')])
def update_account(n_clicks,Username, Password,RePassword,Realname,Email,Phone,District,Country,City,Organization):
    if Username and Password and RePassword and Email and Organization and n_clicks > 0:
        update_info = Users(Username, Password,Realname,Email,Phone,District,Country,City,Organization)
        if not re.search(r'^[a-zA-Z]+[a-zA-Z0-9_]*',Username):
            return html.Div('用户名输入不正确，请重新输入！')
        if not re.search(r'^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$',Password) and not re.search(r'^(?![\d]+$)(?![a-zA-Z]+$)(?![_]+$)[\da-zA-Z_]{8,25}$',RePassword):
            return html.Div('密码输入格式不对，请按规则输入！')
        if Password != RePassword:
            return html.Div('两次密码输入不一样，请重新输入！')
        update_info.add()
        return html.Div('注册成功，点击Cancel返回登陆。')
    elif n_clicks >= 1:
        return html.Div('*部份为必填内容，请填写完整！')


