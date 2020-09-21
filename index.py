
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from spatialTrancriptomeReport import app
from apps.login.Register import registerLayout
from apps.login.Login import loginLayout
from apps.login.forgot import forgotLayout
from apps.data.data import layout

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
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Register':
        return registerLayout()
    elif pathname == '/Data_analysis':
        return layout
    elif pathname == '/Login':
        return loginLayout()
    elif pathname == '/forgot':
        return forgotLayout()
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
    app.run_server(debug=True, host='0.0.0.0', port='8080')
