import yfinance as yf
import numpy as np
import pandas as pd
import csv 

import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import plotly.colors as colors
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

from dash.dependencies import Input, Output, State
from datetime import datetime as dt

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

symbols = ['AAPL', 'AMD']
# symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'FB', 'INTC', 'AMD', 'NVDA', 'ADBE', 'T', 'NFLX', 'SAP', 'ORCL', 'IBM',
        #    'CRM', 'VMW', 'INTU', 'ADSK', 'PYPL', 'SQ', 'SNAP', 'TWTR', 'DELL', 'HPQ']

frames = []
for symbol in symbols:
    stock_df = yf.Ticker(symbol).history(period='10y', interval='1d')
    stock_df = stock_df.drop(columns=['Dividends', 'Stock Splits'])
    stock_df['Log Diff'] = np.log(stock_df['Close']) - np.log(stock_df['Close'].shift(1))
    # stock_df['Log Diff 5-Day Avg'] = 
    tuples = [(symbol, idx) for idx in stock_df.index]
    index = pd.MultiIndex.from_tuples(tuples, names=['Symbol', 'Date'])
    stock_df.index = index
    frames.append(stock_df)
df = pd.concat(frames)

app = dash.Dash(__name__) #external_stylesheets=external_stylesheets)
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

# HELPER GENERAL FORMATTING TOOLS 
def create_graph_box(id, title, figure, extra=[]):
    return html.Div(
        id=id,
        className="graph-container",
        children=[
            html.Div(
                id=id+"-header",
                className="graph-header",
                # children=title
                children=[
                    html.H3(id=id+"-title",
                            className="graph-title",
                            children=title)
                ]
            ),
            html.Br(),
            dcc.Graph(id=id+"-fig", figure=figure,
                      config={"displayModeBar": False, "scrollZoom": False, "responsive": True}
                    )
        ]
        +extra
    )


def create_overview():
    return html.Div(
        id="overview",
        className="graph-container", 
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
                            # start_date_placeholder_text='MM DD YYYY',
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
        children=[
            html.Div(
                id="stationary-header",
                className="graph-header", 
                children=[
                    html.Span(
                        children=html.H2(children="Stationary Overview"),
                        style={"float": "left"} 
                    )
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
                                # html.Div(
                                #     style={'width': 'calc(100%-10px)', 'margin': '0px', 'padding': '5px', 'height': 'calc(25% - 10px)'},
                                #     children=[
                                #         dcc.Dropdown(id="select-window-size",
                                #                     options=[
                                #                         {"label": "AMD", "value": "AMD"},
                                #                         {"label": "AAPL", "value": "AAPL"}
                                #                         ],
                                #                     value="AMD",
                                #                     clearable=False
                                #                     )]
                                # ),
                                # html.Div(
                                #     className="gain",
                                #     style={'width': 'calc(100%-10px)', 'margin': '0px', 'padding': '5px', 'height': 'calc(25% - 10px)',
                                #            'font-size': 'xxx-large', 'text-align': 'center', 'background-color': 'green'},
                                # ),
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

app.layout = html.Div(
    children=[
        html.Div(
            id="menu-container",
            children=[
                html.H1(
                    children="S"
                )
            ]
        ),
        html.Div(
            id="body-container",
            children=[
                dcc.Dropdown(id="select-symbol",
                            options=[
                                {"label": "AMD", "value": "AMD"},
                                {"label": "AAPL", "value": "AAPL"}
                                ],
                            value="AMD",
                            clearable=False
                            ),
                create_overview(),
                create_stationary(),
            ]
        )
    ]
)

@app.callback(
    [Output(component_id="overview-datepicker", component_property="start_date"),
     Output(component_id="overview-datepicker", component_property="end_date"),
     Output(component_id="overview-datepicker", component_property="min_date_allowed"),
     Output(component_id="overview-datepicker", component_property="max_date_allowed")],
    [Input(component_id="select-symbol", component_property="value")]
)
def reset_overview(value):
    start = df.loc[value].index[0]
    end = df.loc[value].index[-1]
    return pd.to_datetime('01-01-2020'), end, start, end

@app.callback(
    [Output(component_id="close-fig", component_property="figure"),
    Output(component_id="gain-loss-fig", component_property="figure"),
    Output(component_id="gain-loss-value", component_property="children"),
    Output(component_id="gain-loss-per", component_property="children")],
    [Input(component_id="overview-datepicker", component_property="start_date"),
     Input(component_id="overview-datepicker", component_property="end_date")],
    [State(component_id="select-symbol", component_property="value")]
)
def update_overview(start, end, value):
    stock_df = df.loc[value].loc[start:end]

    gain_loss_value = stock_df['Close'].iloc[-1] - stock_df['Close'].iloc[0]
    gain_loss_per = gain_loss_value / stock_df['Close'].iloc[0]
    gain_loss = "Gain" if gain_loss_value >= 0 else "Loss"
    
    gain_loss_value = "{:0.2f}".format(gain_loss_value)
    gain_loss_per = "{}: {:0.2f}%".format(gain_loss, gain_loss_per)

    close_fig = reset_overview_fig(value, start, end, stock_df)
    gain_loss_fig = reset_gain_loss_fig(value, start, end, stock_df)
    return close_fig, gain_loss_fig, gain_loss_value, gain_loss_per


def reset_overview_fig(value, start, end, stock_df):

    fig = make_subplots(rows=2, cols=1, 
                        shared_xaxes=True,
                        vertical_spacing=0,
                        row_heights=[0.6, 0.4])

    close_plot = go.Candlestick(
                    x=stock_df.index,
                    open=stock_df['Open'],
                    high=stock_df['High'],
                    low=stock_df['Low'],
                    close=stock_df['Close'],
                    showlegend=False,
                    name='OHLC')
    
    breaks = pd.date_range(start=start, end=end).difference(stock_df.index)
    inc_mask = stock_df['Close'] > stock_df['Open']
    dec_mask = stock_df['Close'] < stock_df['Open']

    increase_volume_plot = go.Bar(
        x=stock_df.index[inc_mask],
        y=stock_df['Volume'][inc_mask],
        marker_color='#3D9970',
        showlegend=False,
        name='Volume')

    decrease_volume_plot = go.Bar(
        x=stock_df.index[dec_mask],
        y=stock_df['Volume'][dec_mask],
        marker_color='#FF4136',
        showlegend=False,
        name='Volume')

    fig.add_trace(close_plot, row=1, col=1)
    fig.add_trace(increase_volume_plot, row=2, col=1)
    fig.add_trace(decrease_volume_plot, row=2, col=1)

    fig.update_layout(
        margin={"t": 25, "l": 25, "b": 25, "r": 25},
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#f8f9fa',
        hovermode='x unified')

    for row in [1,2]:

        fig.update_xaxes(
            rangeslider=dict(
                visible=False),
            type="date",
            rangebreaks=[
                dict(values=breaks)],
            showgrid=False,
            row=row, col=1)

        fig.update_yaxes(
            autorange=True,
            fixedrange=False,
            gridcolor='#dee2e6',
            gridwidth=1,
            row=row, col=1)
            

    return fig

def reset_gain_loss_fig(value, start, end, stock_df):

    fig = make_subplots(rows=2, cols=2, 
                        vertical_spacing=0.1,
                        specs=[[{'type':'domain'}, {'type':'domain'}],
                               [{'type':'xy'}, {'type':'xy'}]])

    inc_mask = stock_df['Close'] > stock_df['Open']
    dec_mask = stock_df['Close'] < stock_df['Open']

    cum_gain = abs((stock_df[inc_mask]['Close']-stock_df[inc_mask]['Open']).sum())
    cum_loss = abs((stock_df[dec_mask]['Close']-stock_df[dec_mask]['Open']).sum())

    cum_pie = go.Pie(labels=['Cum. Gain', 'Cum. Loss'], values=[cum_gain, cum_loss],
                     marker=dict(colors=['#3D9970', '#FF4136']),
                     showlegend=False,
                     sort=False,
                     name="Cumulative Gain/Loss Ratio")

    cum_bar = go.Bar(x=['Cum. Gain', 'Cum. Loss'], y=[cum_gain, cum_loss], 
                     marker_color=['#3D9970', '#FF4136'],
                     showlegend=False,
                     name="Cumulative Gain/Loss Values")

    days_gain = len(stock_df[inc_mask])
    days_loss = len(stock_df[dec_mask])

    day_pie = go.Pie(labels=['Days Gain', 'Days Loss'], values=[days_gain, days_loss],
                     marker=dict(colors=['#3D9970', '#FF4136']),
                     showlegend=False,
                     sort=False,
                     name="Days Gain/Loss Ratio")

    day_bar = go.Bar(x=['Days Gain', 'Days Loss'], y=[days_gain, days_loss], 
                     marker_color=['#3D9970', '#FF4136'],
                     showlegend=False,
                     name="Days Gain/Loss Values")

    fig.add_trace(cum_pie, row=1, col=1)
    fig.add_trace(cum_bar, row=2, col=1)
    fig.add_trace(day_pie, row=1, col=2)
    fig.add_trace(day_bar, row=2, col=2)


    fig.update_layout(
        margin={"t": 25, "l": 25, "b": 25, "r": 25},
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#f8f9fa')

    return fig


@app.callback(
    [Output(component_id="stationary-fig", component_property="figure"),
     Output(component_id="stationary-details-fig", component_property="figure")],
    [Input(component_id="overview-datepicker", component_property="start_date"),
     Input(component_id="overview-datepicker", component_property="end_date")],
    [State(component_id="select-symbol", component_property="value")]
)
def reset_stationary(start, end, value):
    stock_df = df.loc[value].loc[start:end]
    stationary_fig = reset_stationary_fig(value, start, end, stock_df)
    stationary_details_fig = reset_stationary_details_fig(value, start, end, stock_df)
    return stationary_fig, stationary_details_fig

def reset_stationary_fig(value, start, end, stock_df):

    breaks = pd.date_range(start=start, end=end).difference(stock_df.index)

    fig = go.Figure(
        data=[
            go.Scatter(
                x=stock_df.index,
                y=stock_df['Log Diff'],
                showlegend=False,
                name='Log Diff',
                marker_color='#3182bd'
            )
        ]
    )

    fig.update_layout(
        margin={"t": 25, "l": 25, "b": 25, "r": 25},
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#f8f9fa',
        hovermode='x unified'
    )

    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=False
            ),
            rangebreaks=[dict(values=breaks)],
            type="date",
            showgrid=False
        ),
        yaxis=dict(
            autorange=True,
            fixedrange=False,
            gridcolor='#dee2e6',
            gridwidth=1
        )
    )

    return fig

def reset_stationary_details_fig(value, start, end, stock_df):

    stock_df = df.loc[value].loc[start:end]

    fig = make_subplots(rows=2, cols=1, 
                        vertical_spacing=0.1,
                        specs=[[{'type':'xy'}], [{'type':'xy'}]])

    log_diff = stock_df['Log Diff'].values

    autocorr_data = np.correlate(log_diff, log_diff, mode='full')
    autocorr_data = autocorr_data[autocorr_data.size//2:]
    n = autocorr_data.size

    autocorr = go.Scatter(
        x=np.arange(autocorr_data.size),
        y=autocorr_data,
        showlegend=False,
        name='Log Diff Autocorr.',
        marker_color='#3182bd')

    dist = go.Histogram(
        x=log_diff,
        marker_color='#3182bd',
        showlegend=False)

    fig.add_trace(autocorr, row=2, col=1)
    fig.add_trace(dist)

    fig.update_layout(
        margin={"t": 25, "l": 25, "b": 25, "r": 25},
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='#f8f9fa',
        hovermode='x unified'
    )

    fig.add_shape(
        type='line',
        x0=0,
        y0=1/np.sqrt(n),
        x1=n,
        y1=1/np.sqrt(n),
        line=dict(
            color="#dee2e6",
            width=1,
            dash="dash"
        ),
        row=2, col=1
    )

    fig.add_shape(
        type='line',
        x0=0,
        y0=-1/np.sqrt(n),
        x1=n,
        y1=-1/np.sqrt(n),
        line=dict(
            color="#dee2e6",
            width=1,
            dash="dash"
        ),
        row=2, col=1
    )

    for row in [1,2]:
        fig.update_xaxes(showgrid=False, row=row, col=1)

        fig.update_yaxes(
            autorange=True,
            fixedrange=False,
            gridcolor='#dee2e6',
            gridwidth=1,
            row=row, col=1)

    return fig

# def reset_noise(value):
    # global df
    # fig = go.Figure(
        # data=[go.Scatter(x=df.index, y=df['Log Diff'], marker_color="#277da1")]
    # )
    
    # fig.update_layout(
        # xaxis=dict(
            # type="date",
            # showgrid=False
        # ),
        # yaxis=dict(
            # autorange=True,
            # fixedrange=False,
            # gridcolor='#dee2e6',inherit
            # gridwidth=1
        # )
    # )

    # fig.update_layout(
        # margin={"t": 50, "l": 50, "b": 50, "r": 25},
        # autosize=True,
        # height=600,
        # plot_bgcolor='#f8f9fa',
        # paper_bgcolor='#f8f9fa',
        # hovermode='x unified'
    # )

    # return fig

if __name__ == '__main__':
    app.run_server(debug=True)  