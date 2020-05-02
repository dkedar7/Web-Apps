import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

### Header

### Title
header = dbc.Row(
            dbc.Col(
                [
                    html.H1('Machine Comprehension')
                ], style = {'text-align':'center',
                'padding':'3% 0% 0% 3%',
                'font-family':'Verdana'} 
            )
)

body_paragraph = dbc.Row(
    [
        dbc.Col(
            [
                html.P(
                    [
                    "Welcome to my Machine Comprehension web application. ",
                    html.Br(),
                    "See how a modern Machine Learning model answers questions from a passage."
                    ]
                )
            ]
        )
    ],
    style = {'text-align':'center'}
)

### Dropdown for selecting passages

### Input text
input_text = dbc.Row(
    [
        dbc.Col(
            [
                dcc.Textarea(
                    id = "input_text",
                    placeholder =  "Input passage here",
                    style = {'padding':'2% 0% 2% 0%',
                            'width': '100%', 
                            'height': 200}
)
            ]
        )
    ],
    style = {'padding':'2% 0% 2% 0%'}
)

### Input_question
input_question = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Input(
                    id='input_question',
                    value = 'What is this passage about?',
                    style = {'padding':'2% 0% 2% 0%'}
                )
            ]
        )
    ],
    style = {'padding':'2% 0% 2% 0%'}
)

### Submit button
submit_button = dbc.Row(
    [
        dbc.Col(
            [
               dbc.Button("Submit", id="submit_button", color="primary", className="mr-1")
            ]
        )
    ],
                style = {'align':'center'},
                justify = 'center'
)

### Output text
output_text = dbc.Row(
    [
        dbc.Col(
            [
                html.P(id='output_text', 
                children=['']
                )
            ]
        )
    ],
    style = {'text-align':'center'}
)

### Footer


### Bring it together
layout = dbc.Container(
    [
        dcc.Store(id='memory-output', storage_type='memory'),
        header,
        body_paragraph,
        input_text,
        input_question,
        submit_button,
        output_text
    ],
    fluid = False
)