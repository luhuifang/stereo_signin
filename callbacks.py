import re
import country_dict as Dis
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
from spatialTrancriptomeReport import app
from apps.db.tableService.Users import Users
from apps.db.tableService.UserRole import UserRole
from dash.dependencies import Input, Output, State


@app.callback(
    Output('Country', 'options'),
    [Input('District', 'value')]
)
def set_neighborhood(District):
    if not District:
        raise PreventUpdate
    neighborhoods = [i for i in Dis.options[District]["childrens"].keys()]
    return [{'label': v, 'value': v} for v in neighborhoods]
@app.callback(
    Output('Province', 'options'),
    [Input('Country', 'value'),
    Input('District', 'value')]
)
def set_province_neighborhood(country,District):
    try:
        province_neigh = [ii for ii in Dis.options[District]["childrens"][country]["childrens"]]
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
        city_neigh = [ii for ii in Dis.options[District]["childrens"][country]["childrens"][Province]['childrens']]
        return [{'label': v, 'value': v} for v in city_neigh]
    except:
        return [{'label': 'None', 'value': 'None'}]

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
        if not re.search(r'^[0-9a-zA-Z_]+$',Username):
            return html.Div('The username is incorrect, please re-enter!')
        else:
            res=conn.checkExists()
            if res:
                return html.Div('Username already exists, please re-enter!')
        if not re.search(r'^(?=.*[a-zA-Z])(?=.*[1-9])(?=.*[\W]).{8,25}$',Password) and not re.search(r'^(?=.*[a-zA-Z])(?=.*[1-9])(?=.*[\W]).{8,25}$',RePassword):
            return html.Div('The password input format is wrong, please input according to the rules!')
        if Password != RePassword:
            return html.Div('The two password entries are different, please re-enter!')
        if not re.search(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',Email):
            return html.Div('The email format is wrong, please re-enter!')
        update_info.add()
        update_info.password = Password
        return html.Div('Registration is successful, click Return to login.')
    elif n_clicks >= 1:
        return html.Div('*Part of the content is required, please fill in completely!')


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
    Output('Organization','value')],
    [Input('clear_button', 'n_clicks')])
def clear_input(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    if n_clicks > 0:
        return '','','','','','','','','','',''    
    