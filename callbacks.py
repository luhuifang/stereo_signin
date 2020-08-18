from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from spatialTrancriptomeReport import app
import country_dict as Dis
import re
from apps.db.tableService.Users import Users
from apps.db.tableService.UserRole import UserRole
from dash.exceptions import PreventUpdate


@app.callback(
    Output('country_div', 'children'),
    [Input('District', 'value')]
)
def set_neighborhood(District):
    neighborhoods = [i for i in Dis.options[District]["childrens"].keys()]
    return dcc.Dropdown(
        id='Country',
        value=neighborhoods[0],
        options=[{'label': v, 'value': v} for v in neighborhoods],
        persistence_type='session',
        persistence=District
            )

@app.callback(
    Output('province_div', 'children'),
    [Input('Country', 'value'),
    Input('District', 'value')]
)
def set_province_neighborhood(country,District):
    try:
        province_neigh = [ii for ii in Dis.options[District]["childrens"][country]["childrens"]]
        # print(Dis.options[District]["childrens"][country]["childrens"])
        if province_neigh:
            return dcc.Dropdown(
                id='Province',
                value=province_neigh[0],
                options=[{'label': v, 'value': v} for v in province_neigh],
                persistence_type='session',
                persistence=country
            )
        else:
            return dcc.Dropdown(
                id='Province',
                value='',
                options=[{'label': v, 'value': v} for v in province_neigh],
                persistence_type='session',
                persistence=country
            )
    except:
        return dcc.Dropdown(
                id='Province',
                value='',
                options=[],
                persistence_type='session',
                persistence=country
            ) 

@app.callback(
    Output('city_div', 'children'),
    [Input('Country', 'value'),
    Input('District', 'value'),
    Input('Province','value')]
)
def set_city_neighborhood(country,District,Province):
    try:
        city_neigh = [ii for ii in Dis.options[District]["childrens"][country]["childrens"][Province]['childrens']]
        # print(Dis.options[District]["childrens"][country]["childrens"])
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
    except:
        return dcc.Dropdown(
                id='City',
                value='',
                options=[],
                persistence_type='session',
                persistence=country
            ) 

@app.callback(
    Output('Username_error', 'children'),
    [Input('Username', 'value'),
    Input('Username_form','n_clicks')])
def update_username_info(Username,n_click):
    conn = Users(username=Username)
    if not Username:
        raise PreventUpdate
    if not re.search(r'^[a-zA-Z]+[a-zA-Z0-9_]*',Username) :
        return html.Div('The username is incorrect, please re-enter!')
    elif re.search(r'^[a-zA-Z]+[a-zA-Z0-9_]*',Username):
        res=conn.checkExists()
        if res:
            return html.Div('Username already exists, please re-enter!')
        else:
            return html.Div('Username is available!')

@app.callback(
    Output('Password_error', 'children'),
    [Input('Password', 'value'),
    Input('Password_form','n_clicks')])
def update_username_info(Password,n_click):
    if not Password:
        raise PreventUpdate
    if not re.search(r'^(?![a-zA-z]+$)(?!\d+$)(?![!@#$%^&*.,?]+$)(?![a-z\d]+$)(?![A-Z\d]+$)(?![a-z!@#$%^&*,.?]+$)(?![A-Z!@#$%^&*,.?]+$)(?![\d!@#$%^&*,.?]+$)[a-zA-Z\d!@#$%^&*,.?]{8,25}$',Password):
        return html.Div('The password input format is wrong, please input according to the rules!')

@app.callback(
    Output('Repassword_error', 'children'),
    [Input('RePassword', 'value'),
    Input('Password', 'value'),
    Input('Repassword_form','n_clicks')])
def update_username_info(Repassword,Password,n_click):
    if not Repassword:
        raise PreventUpdate
    if not re.search(r'^(?![a-zA-z]+$)(?!\d+$)(?![!@#$%^&*.,?]+$)(?![a-z\d]+$)(?![A-Z\d]+$)(?![a-z!@#$%^&*,.?]+$)(?![A-Z!@#$%^&*,.?]+$)(?![\d!@#$%^&*,.?]+$)[a-zA-Z\d!@#$%^&*,.?]{8,25}$',Repassword):
        return html.Div('The password input format is wrong, please input according to the rules!')
    if Password != Repassword and n_click>1:
        return html.Div('The two password entries are different, please re-enter!')

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
    conn = Users(username=Username)
    if Username and Password and RePassword and Email and Organization and n_clicks > 0:
        update_info = Users(Username, '',Realname,Email,Phone,District,Country,City,Organization)
        if not re.search(r'^[a-zA-Z]+[a-zA-Z0-9_]*',Username):
            return html.Div('The username is incorrect, please re-enter!')
        else:
            res=conn.checkExists()
            if res:
                return html.Div('Username already exists, please re-enter!')
        if not re.search(r'^(?![a-zA-z]+$)(?!\d+$)(?![!@#$%^&*.,?]+$)(?![a-z\d]+$)(?![A-Z\d]+$)(?![a-z!@#$%^&*,.?]+$)(?![A-Z!@#$%^&*,.?]+$)(?![\d!@#$%^&*,.?]+$)[a-zA-Z\d!@#$%^&*,.?]{8,25}$',Password) and not re.search(r'^(?![a-zA-z]+$)(?!\d+$)(?![!@#$%^&*.,?]+$)(?![a-z\d]+$)(?![A-Z\d]+$)(?![a-z!@#$%^&*,.?]+$)(?![A-Z!@#$%^&*,.?]+$)(?![\d!@#$%^&*,.?]+$)[a-zA-Z\d!@#$%^&*,.?]{8,25}$',RePassword):
            return html.Div('The password input format is wrong, please input according to the rules!')
        if Password != RePassword:
            return html.Div('The two password entries are different, please re-enter!')
        update_info.add()
        update_info.password = Password
        return html.Div('Registration is successful, click Cancel to return to login.')
    elif n_clicks >= 1:
        return html.Div('*Part of the content is required, please fill in completely!')


@app.callback(
    [Output('Username', 'value'),
    Output('Password', 'value'),
    Output('RePassword','value'),
    Output('Realname','value'),
    Output('Email','value'),
    Output('Phone','value'),
    Output('Organization','value')],
    [Input('clear_button', 'n_clicks')])
def clear_input(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    if n_clicks > 0:
        return '','','','','','',''
        
    