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

import index as index_html
import figures as figures_html

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

symbols = ['AAPL', 'AMD']
# symbols = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'FB', 'INTC', 'AMD', 'NVDA', 'ADBE', 'T', 'NFLX', 'SAP', 'ORCL', 'IBM',
        #    'CRM', 'VMW', 'INTU', 'ADSK', 'PYPL', 'SQ', 'SNAP', 'TWTR', 'DELL', 'HPQ']

frames = []
for symbol in symbols:
    stock_df = yf.Ticker(symbol).history(period='10y', interval='1d')
    stock_df = stock_df.drop(columns=['Dividends', 'Stock Splits'])
    stock_df['Log Diff'] = np.log(stock_df['Close']) - np.log(stock_df['Close'].shift(1))
    tuples = [(symbol, idx) for idx in stock_df.index]
    index = pd.MultiIndex.from_tuples(tuples, names=['Symbol', 'Date'])
    stock_df.index = index
    frames.append(stock_df)
df = pd.concat(frames)

app = dash.Dash(__name__) #external_stylesheets=external_stylesheets)
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

app.layout = html.Div(
    children=[
        index_html.create_sidebar(),
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
                index_html.create_overview(),
                index_html.create_stationary(),
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
def general_select_symbol(value):
    start = df.loc[value].index[0]
    end = df.loc[value].index[-1]
    return pd.to_datetime('01-01-2020'), end, start, end

@app.callback(
    [Output(component_id="close-fig", component_property="figure"),
    Output(component_id="gain-loss-fig", component_property="figure"),
    Output(component_id="gain-loss-value", component_property="children"),
    Output(component_id="gain-loss-per", component_property="children"),
    Output(component_id="gain-loss-text", component_property="className")],
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
    gain_loss_class = gain_loss.lower()

    close_fig = figures_html.overview_fig(value, start, end, stock_df)
    gain_loss_fig = figures_html.gain_loss_fig(value, start, end, stock_df)
    return close_fig, gain_loss_fig, gain_loss_value, gain_loss_per, gain_loss_class

@app.callback(
    [Output(component_id="stationary-fig", component_property="figure"),
     Output(component_id="stationary-details-fig", component_property="figure")],
    [Input(component_id="overview-datepicker", component_property="start_date"),
     Input(component_id="overview-datepicker", component_property="end_date")],
    [State(component_id="select-symbol", component_property="value")]
)
def update_stationary(start, end, value):
    stock_df = df.loc[value].loc[start:end]
    stationary_fig = figures_html.stationary_fig(value, start, end, stock_df)
    stationary_details_fig = figures_html.stationary_details_fig(value, start, end, stock_df)
    return stationary_fig, stationary_details_fig

if __name__ == '__main__':
    app.run_server(debug=True)  