#!/usr/bin/env python3

from dash import Dash, html, dcc, dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_daq as daq

import pandas as pd

import requests

# import data functions
from data.ok_data import *
from data.brent_adj import *
from plots.plots import *

# import plots

app = Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])

# import data
brent = brent_adj()
station = ok_data()

#import plots 

app.layout = html.Div(
    children = [
        html.H1(children = 'Brent Crude'),

        dcc.RadioItems(
            id = 'plot_option', 
            options = ['Line Plot', 'Candle Plot'],
            value = 'Line Plot'
        ),

        daq.BooleanSwitch(
            id = 'currency_adj',
            on = False,
            label = 'Adjust to DKK(per Liter)',
            color = '#4C4E52'
            ),

        dcc.Graph(
            id = 'brent',
        )
    ]
)

@app.callback(
        Output('brent', 'figure'),
        [
            Input('plot_option', 'value'),
            Input('currency_adj', 'on'),
         ])
def candle_or_line(choice, adj):
    if choice == 'Candle Plot':
        if adj:
            return PLOTS.brent_ok_candle(brent = brent, station_ok = station, adjust = adj)
        elif not adj:
            return PLOTS.brent_ok_candle(brent = brent, station_ok = station, adjust = adj)
    elif choice == 'Line Plot':
        if adj:
            return PLOTS.brent_ok_fig(brent = brent, station_ok = station, adjust = adj)
        elif not adj:
            return PLOTS.brent_ok_fig(brent = brent, station_ok = station, adjust = adj)


if __name__ == '__main__':
    app.run_server(debug = True)
