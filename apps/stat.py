import os
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

from spatialTrancriptomeReport import app
from apps.statPage.stat import statLayout

from apps.db.tableService.Data import Data
from apps.db.tableService.WorkflowResult import WorkflowResult

def app_layout(DataID):
    if DataID.startswith('DATA_'):
        data = Data(data_id=DataID)
        file_dir = data.getResultPath()
    else:
        file_dir = DataID
    
    if os.path.exists(os.path.join(file_dir, 'new_final_result.json')):
        app_layout = html.Div([
            statLayout(file_dir, 'Test'),
        ])
    else:
        app_layout = html.Div('No result')
    return app_layout
