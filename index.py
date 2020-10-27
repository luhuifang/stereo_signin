
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from spatialTrancriptomeReport import app
from apps.login.Register import registerLayout
from apps.login.Login import loginLayout
from apps.login.forgot import forgotLayout
from apps.data.data import layout
from apps.login.Manage_control import manager_page
from apps.login.Customer_control import Managelayout
from apps.login.detail_page import detail_page

def page_layout():
    return html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'custom-auth-frame', children=[
        dcc.Interval('graph-update', interval = 100, n_intervals = 0),
        html.H1('Welcome!'),
        html.Button('sign in'),
        html.Button('data analysis'),
        html.Button('Login')
    ])
])

app.layout = page_layout

@app.callback(Output('custom-auth-frame', 'children'),
              [Input('url', 'pathname'),
              Input('url','hash'),
              Input('url','search')])
def display_page(pathname,hash,search):
    if pathname == '/Register':
        return registerLayout()
    elif pathname == '/Data_analysis':
        return layout
    elif pathname == '/Login':
        return loginLayout()
    elif pathname == '/forgot':
        return forgotLayout()
    elif pathname == '/Manager_console':
        return manager_page()
    elif pathname == '/Customer_console':
        return Managelayout()
    elif pathname == '/Manager_console/detail/':
        order_id = search.split('=')[1]
        return detail_page(order_id)
    elif pathname == '/':
    	return html.Div( children=[
    	html.H1('Welcome!'),
    	html.Button(id='sign_in_button',children=[dcc.Link('sign in', href='/Register')]),
        html.Button(id='data_analysis_button',children=[dcc.Link('data analysis', href='/Data_analysis')]),
        html.Button(id='login_button',children = [dcc.Link('Login',href='/Login')])
    	])
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8050')
