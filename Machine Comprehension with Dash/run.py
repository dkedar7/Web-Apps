import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import os

from app import app, server
from layout import layout
from model import answer

app.layout = layout

## Write callbacks

@app.callback(
    [
        Output("output_text", "children"),
        Output('memory-output', 'data')
    ],
    [
        Input("input_text", "value"),
        Input("input_question", "value"),
        Input("submit_button", "n_clicks"),
    ],
    [
        State('memory-output', 'data')
    ]
)
def get_prediction(context, query, n_clicks, data):
    if data is None:
        print ('First if')
        data = {}
        data['clicks'] = 1
        return [''], data

    if n_clicks and data['clicks'] == n_clicks:
        print ('Second if')
        data['clicks'] += 1
        return [answer(context, query)], data

    else:
        print ('Else')
        print (data, n_clicks)
        return [''], data


if __name__ == '__main__':
    app.server.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))