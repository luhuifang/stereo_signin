import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from spatialTrancriptomeReport import app
import Register_page

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'custom-auth-frame')
])

@app.callback(Output('custom-auth-frame', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/Register':
        return Register_page.layout
    elif pathname == '/':
    	return html.Div( children=[
    	html.H1('Welcome!'),
    	html.Button(id='sign_in_button',children=[dcc.Link('sign in', href='/Register')])
    	])
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1', port='8080')
