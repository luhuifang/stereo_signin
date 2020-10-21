
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from spatialTrancriptomeReport import app
from apps.login.Register import registerLayout
from apps.login.Login import loginLayout
from apps.login.forgot import forgotLayout
from apps.data.data import layout
from apps.login.Manage_control import Managelayout, detial_page

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'custom-auth-frame', children=[
    	html.H1('Welcome!'),
    	html.Button('sign in'),
        html.Button('data analysis'),
        html.Button('Login')
    ])
])

@app.callback(Output('custom-auth-frame', 'children'),
              [Input('url', 'pathname'),
              Input('url','search')])
def display_page(pathname,search):
    if pathname == '/Register':
        return registerLayout()
    elif pathname == '/Data_analysis':
        return layout
    elif pathname == '/Login':
        return loginLayout()
    elif pathname == '/forgot':
        return forgotLayout()
    elif pathname == '/Manage_coltrol':
        return Managelayout()
    elif pathname == '/Manage_coltrol/detail/':
        order_id = search.split('=')[1]
        return detial_page(order_id)
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
