import dash_core_components as dcc
import dash_html_components as html

from spatialTrancriptomeReport import app

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'custom-auth-frame', children=[
    	html.H1('Welcome!'),
    	html.Button('sign in'),
    ])
])



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8080')
