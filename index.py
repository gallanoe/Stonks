import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import plotly.colors as colors
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

from dash.dependencies import Input, Output, State
from datetime import datetime as dt

def create_sidebar():
    return html.Div(
            id="menu-container",
            children=[
                html.H1(
                    children="S"
                )
            ]
        )

def create_overview():
    return html.Div(
        id="overview",
        className="graph-container", 
        style={"height": "500px"},
        children=[
            html.Div(
                id="overview-header",
                className="graph-header",
                children=[
                    html.Span(
                        children=html.H2(children="Overview"),
                        style={"float": "left"} 
                    ),
                    html.Span(
                        children=dcc.DatePickerRange(
                            id="overview-datepicker",
                            end_date=dt(2017,6,21),
                            display_format='MM/DD/YYYY',
                            ),
                        style={"float": "right", "margin-top": "12px"}
                    ),
                    html.Div(style={"clear": "both"})
                ]
            ),
            html.Div(
                style={'display': 'flex', 'height': 'calc(85% - 10px)', 'padding': '0px', 'margin': '0px'},
                children=[
                    html.Div(
                        style={'width': 'calc(70% - 20px)', 'height': 'calc(100% - 20px)', 
                               'border-right': '1px solid #dee2e6', 'padding': '10px', 'margin': '0px'},
                        children=[
                            dcc.Graph(id="close-fig", figure={},
                                      config={'displayModeBar': False, 'scrollZoom': False, 'responsive': True},
                                      style={'width': '100%', 'height': '100%'})
                        ]),
                    html.Div(style={'width': 'calc(30% - 20px)', 'height': 'calc(100% - 20px)', 'padding': '10px',
                                    'margin': '0px', 'display': 'block', 'color': '#3D9970'},
                             children=[
                                html.Div(
                                    id="gain-loss-text",
                                    className="gain",
                                    style={'width': '100%', 'margin': '0px', 'padding': '5px', 'height': 'calc(25% - 10px)',
                                           'font-size': 'xxx-large', 'text-align': 'center'},
                                    children=[
                                        html.Span(
                                            id="gain-loss-value", 
                                            children="3,210.00",
                                        ),
                                        html.Div(
                                            id="gain-loss-per",
                                            style={'width': '100%', 'font-size': 'medium', 'color': '#495057'}, 
                                            children="Gain: 29.94%"
                                        )
                                    ]
                                ),
                                html.Div(
                                    style={'width': 'calc(100%-10px)', 'margin': '0px', 'padding': '5px', 'height': 'calc(75% - 10px)'},
                                    children=[
                                        dcc.Graph(id="gain-loss-fig", figure={},
                                        config={'displayModeBar': False, 'scrollZoom': False, 'responsive': True},
                                        style={'width': '100%', 'height': '100%'})
                                    ]
                                )
                             ])
                ]
            )
        ]
    )

def create_stationary():
    return html.Div(
        id="stationary", 
        className="graph-container", 
        style={"height": '500px'},
        children=[
            html.Div(
                id="stationary-header",
                className="graph-header", 
                children=[
                    html.Span(
                        children=html.H2(children="Stationary Overview"),
                        style={"float": "left"}),
                    html.Div(
                        style={"width": "15%", "float": "right", "height": "80%",
                               "margin-top": "10px", "display": "flex"},
                        children=[
                            html.Div(children="Average period:",
                                     style={"margin-left": "5px", "margin-right": "10px", 
                                            "vertical-align": "middle", "margin-top": "7px"}),
                            dcc.Dropdown(id="stationary-select-window-size",
                                        options=[
                                            {"label": "1 day", "value": 1},
                                            {"label": "5 days", "value": 5},
                                            {"label": "10 days", "value": 10},
                                            {"label": "15 days", "value": 15},
                                            {"label": "1 month", "value": 20}],
                                        value=1,
                                        clearable=False, 
                                        style={"width": "80%", "vertical-align": "middle",
                                               "top": "10px"}
                                        )
                        ]),
                    html.Div(
                        style={"width": "15%", "float": "right", "height": "80%",
                               "margin-top": "10px", "display": "flex",
                               "margin-right": "10px"},
                        children=[
                            html.Div(children="Gap period:",
                                     style={"margin-left": "5px", "margin-right": "10px", 
                                            "vertical-align": "middle", "margin-top": "7px"}),
                            dcc.Dropdown(id="stationary-select-gap-size",
                                        options=[
                                            {"label": "1 day", "value": 1},
                                            {"label": "5 days", "value": 5},
                                            {"label": "10 days", "value": 10},
                                            {"label": "15 days", "value": 15},
                                            {"label": "1 month", "value": 20}],
                                        value=1,
                                        clearable=False, 
                                        style={"width": "80%", "vertical-align": "middle",
                                               "top": "10px"}
                                        )
                        ]),
                    ]
            ),
            html.Div(
                style={'display': 'flex', 'height': 'calc(85% - 10px)', 'padding': '0px', 'margin': '0px'},
                children=[
                    html.Div(
                        style={'width': 'calc(70% - 20px)', 'height': 'calc(100% - 20px)', 
                               'border-right': '1px solid #dee2e6', 'padding': '10px', 'margin': '0px'},
                        children=[
                            dcc.Graph(id="stationary-fig", figure={},
                                      config={'displayModeBar': False, 'scrollZoom': False, 'responsive': True},
                                      style={'width': '100%', 'height': '100%'}),
                        ]),
                    html.Div(style={'width': 'calc(30% - 20px)', 'height': 'calc(100% - 20px)', 'padding': '10px',
                                    'margin': '0px', 'display': 'block', 'color': '#495057'},
                             children=[
                                html.Div(
                                    style={'width': 'calc(100%-10px)', 'margin': '0px', 'padding': '5px', 'height': 'calc(100% - 10px)'},
                                    children=[
                                        dcc.Graph(id="stationary-details-fig", figure={},
                                        config={'displayModeBar': False, 'scrollZoom': False, 'responsive': True},
                                        style={'width': '100%', 'height': '100%'}),
                                    ])
                             ])
                ]
            )
        ]
    )