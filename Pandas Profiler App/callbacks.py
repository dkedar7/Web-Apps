import dash_table
import plotly.graph_objs as go
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from pandas_profiling import ProfileReport

def create_report(df):
    return ProfileReport(df, title='Pandas Profiling Report',
     html={'style':{'full_width':True}})