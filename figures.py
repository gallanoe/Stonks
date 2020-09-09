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

def overview_fig(value, start, end, stock_df):

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

def gain_loss_fig(value, start, end, stock_df):

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

def stationary_fig(value, start, end, stock_df):

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

def stationary_details_fig(value, start, end, stock_df):
    
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