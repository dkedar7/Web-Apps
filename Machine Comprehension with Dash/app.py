import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import flask
from flask import request

import re
from layout import layout

external_stylesheets = [dbc.themes.BOOTSTRAP,
"https://use.fontawesome.com/releases/v5.9.0/css/all.css"]

server = flask.Flask(__name__)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                server=server)
                
app.title = "Machine Comprehension"