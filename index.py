import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from spatialTrancriptomeReport import app
from apps.stat import app_layout
from apps.statPage.utils import url_search_to_dict
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'custom-auth-frame', children=[
    	html.H1('Welcome!'),
    	dbc.Button('Sign in', color='primary'),
        dbc.Button('Stat', color='primary', href='/stat?DataID=E:\\01.program\\11.st_RNA\\03.data\\test_new_stat'),
    ]),
])


@app.callback(
    Output('custom-auth-frame', 'children'),
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def display_page(pathname, url_search):
    if pathname == '/stat':
        search = url_search_to_dict(url_search)
        dataID = search['DataID'] if 'DataID' in search else ''
        return app_layout(dataID)
    raise PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8050')
