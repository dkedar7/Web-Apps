import dash
import plotly.graph_objs as go
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory

import base64
import datetime
import io
import os

from layout import layout
from callbacks import *

external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = layout
server = app.server
app.title = "Data Analyzer"

#### File upload intimation
@app.callback(Output('upload_intimation', 'children'),
            [Input('upload-data', 'filename')])
def cb_upload_intimation(filename):
    if filename is not None:
        return dbc.Col(
            [
                html.P(filename + ' successfully uploaded!',
                style = {'text-align':'center'})
            ]
        )

#### Decide if the "anlyze" and "downloads" buttons should be active
@app.callback([Output('analyze-button', 'disabled'),
                Output('download-button', 'disabled')],
              [Input('upload-data', 'filename')])
def cb_button_active(filename):
    return filename is None, filename is None

#### Download report

@server.route("/_intermediate/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory("_intermediate", path, as_attachment=True)

@app.callback(Output('download-button', 'href'),
              [Input('analyze-button', 'n_clicks')])
def cb_download_report(n_clicks):
    if n_clicks is not None:
        return f"_intermediate/{urlquote('report.html')}"
    else:
        return ""



#### Shoe report
@app.callback(Output('output-report', 'children'),
              [Input('upload-data', 'contents'),
              Input('analyze-button', 'n_clicks')],
              [State('upload-data', 'filename')])
def cb_create_report(contents, n_clicks, filename):

    if contents is not None and filename is not None and n_clicks is not None:
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename.lower():
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))

                report = create_report(df).to_html()

                with open('_intermediate/report.html', 'w') as file:
                    file.write(report)
                    file.close()

                return html.Iframe(srcDoc = report,
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

            elif 'xls' in filename.lower():
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded))

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

            else:
                return html.Div([
                'There was an error processing this file.'
            ])

        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))