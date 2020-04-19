# -*- coding: utf-8 -*-
import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


####### NavBar #######
# nav_bar = 

####### Header #######
header = dbc.Col([
            html.H1('Get an instant data analysis report of your spreadsheets', 
            style={'text-align':'center', "color":"white",
                "font-family": "Verdana; Gill Sans"}),
            html.H3('Using the powerful Pandas Profiling library on Python', 
            style={'text-align':'center', "color":"white",
                "font-family": "Verdana; Gill Sans"})
            ])

####### Upload button #######
upload_button = dbc.Col([
                dcc.Upload(
        id='upload-data',
        children=dbc.Col([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }
    ),
            ])

####### Parameter control #######
parameters = dbc.Col(
    [
        dbc.FormGroup(
            [
                html.Div(id="select-sheet-div",
                    children=
                    [
                        dbc.Label('Select sheet'),
                        dcc.Dropdown(id="select-sheet")
                    ],
                    style= {'display': 'none'}
                ),
                dbc.Label('Skip rows'),
                dcc.Dropdown(id="skiprows",
                    options = [{"label" : rows, "value" : rows} for rows in range(1,11)],
                                value = 0
                            ),

                dbc.Button("Analyze", id = 'analyze-button', size="lg",
                    color="primary", disabled = False,
                    className = "mt-3 mr-3"),

                dbc.Button("Download Report", id = 'download-button', size="lg",
                    color="primary", disabled = False,
                    className = "mt-3 mr-3", href = "", external_link=True)
            ]
        )
    ],
    width = 4
)

####### Analysis report iframe #######

spinner = dbc.Spinner(color="danger", id='spinner')

report_iframe = dbc.Col(id='output-report',
        style={
            'width': '80%',
            'height': '800px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderWidth': '1px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }, loading_state = {'is_loading': True,
        'component_name':'spinner'})

####### Layout #######

layout = dbc.Container([
    dcc.Store(id='memory-output', storage_type='memory'),
    dbc.Row(
        [
            header
        ]
   ,style ={"padding":"5% 0% 5% 0%", "background-color":"#3CB371"}
    ),
    dbc.Row(
        [
            upload_button
        ]
    ),
    dbc.Row(id="upload_intimation"),
    dbc.Row(
        [
            parameters,
            report_iframe
        ]
    )  
]
, fluid = True)