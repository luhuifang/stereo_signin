
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from spatialTrancriptomeReport import app
from apps.login.Register import registerLayout

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'custom-auth-frame', children=[
    	html.H1('Welcome!'),
    	html.Button('sign in'),
    ])
])

@app.callback(Output('custom-auth-frame', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Register':
        return registerLayout()
    elif pathname == '/':
    	return html.Div( children=[
    	html.H1('Welcome!'),
    	html.Button(id='sign_in_button',children=[dcc.Link('sign in', href='/Register')])
    	])
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8080')
