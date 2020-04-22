import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask_caching import Cache

external_stylesheets = [dbc.themes.BOOTSTRAP,
"https://use.fontawesome.com/releases/v5.9.0/css/all.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
cache = Cache(app.server)
app.title = "Data Analyzer"