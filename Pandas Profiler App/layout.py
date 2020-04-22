# -*- coding: utf-8 -*-
import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app

####### NavBar #######
navbar = dbc.NavbarSimple(
    children=[
        html.Span(
            [
                html.A(
                    html.I(className = "fa-2x fab fa-github", style={'color':'#ffffff'}),
                href = "https://github.com/dkedar7/Web-Apps/tree/master/Pandas%20Profiler%20App", target="_blank",
                className="footer-social-icons mr-3"
                    ),
                    html.A(
                    html.I(className = "fa-2x fab fa-twitter-square", style={'color':'#ffffff'}),
                href = "https://www.twitter.com/dkedar7/", target="_blank",
                className="footer-social-icons mr-3"
                    ),
                    html.A(
                    html.I(className = "fa-2x fab fa-linkedin", style={'color':'#ffffff'}),
                href = "https://www.linkedin.com/in/dkedar7/", target="_blank",
                className="footer-social-icons mr-3"
                    )
            ]
        ),
    ],
    brand="Data Analyzer",
    brand_href=None,
    color="#40587C",
    dark=True,
    style = {"font-size":"18", "padding":"0% 0% 0% 0%"}
)

####### Header #######
header = dbc.Col([
            html.H1('Get an instant data analysis report of your spreadsheets', 
            style={'text-align':'center', "color":"white",
                "font-family": "Verdana; Gill Sans"}),
            html.H3('Using the powerful Pandas Profiling library on Python', 
            style={'text-align':'center', "color":"white",
                "font-family": "Verdana; Gill Sans"})
            ],
            style ={"padding":"5% 0% 5% 0%", "background-color":"#40587C"})

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
        style={'width': '80%',
            'height': '800px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderWidth': '1px',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }, loading_state = {'is_loading': True,
        'component_name':'spinner'})

####### Footer #######
footer = dbc.Row(
    [
        dbc.Col(
            [
                html.P(
                """
                    Data Analysis report credits go to Pandas Profiling, an open-source
                    project to generate reports from Pandas dataframes. For more information,
                    check out the official project GitHub page.""",
                style = {"color":"white"}
            )
            ],
            className="footer-disclaimer-content ",
            width=8,
        ),
        dbc.Col(
            [
                html.Span(
                    html.A(
                        html.I(className="fa-2x fab fa-github", style={"color":"#ffffff"}),
                        href="https://github.com/ncov19-us/front-end",
                    ),
                ),
                html.Span(
                    "   Copyright 2020", style={"color":"white"}
                ),
            ],
            width={"size" : 3, "offset":1}
        ),
    ],
    style ={"background-color":"#40587C", "padding" : "2% 0% 0% 2%"}
)

####### Layout #######

layout = dbc.Container([
    dcc.Store(id='memory-output', storage_type='memory'),
    dbc.Row(
        [
            dbc.Col(
                [
                    navbar
                ]
            )
        ]
    ,style ={"background-color":"#40587C"}
    ),
    dbc.Row(
        [
            header
        ]
    ),
    dbc.Row(
        [
            upload_button
        ]
    ),
    dbc.Row(id="upload_intimation"),
    dbc.Row(
        [
            parameters
        ]
    , justify = 'center'),
    dbc.Row(
        [
            report_iframe
        ]
    ),
    footer
],
    fluid = False)