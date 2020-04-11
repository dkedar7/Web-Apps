import dash
import plotly.graph_objs as go
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import base64
import datetime
import io
import os

from layout import layout
from callbacks import *

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = layout
server = app.server


@app.callback(Output('output-report', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename')])
def cb_create_report(contents, filename):

    if contents is not None and filename is not None:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])
        
        # return html.Div([dash_dangerously_set_inner_html.DangerouslySetInnerHTML\
        # (create_report(df).to_html())])
        # profile.to_file(output_file="your_report.html")
    
        return html.Iframe(srcDoc = create_report(df).to_html(),
        style={
            'width': '100%',
            'height': '100%',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        })

if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))