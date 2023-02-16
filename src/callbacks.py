import pandas as pd
from datetime import datetime
import time

from dash import Dash, html, dcc, no_update, ctx, callback, Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from src.market_data import update_market_data


def register_callbacks(app: Dash):
    @app.long_callback(
        Output("timestamp", "data"),
        Input("update_button", "n_clicks"),
        running=[
            (Output("update_button", "disabled"), True, False),
            (Output("update_button", "children"), [dbc.Spinner(size="sm"), " Updating..."], "Update Data"),
        ]
    )
    def update_data(n_clicks):
        # update market data on startup or when button clicked
        timestamp = int(time.time())
        update_market_data()
        return timestamp


    @callback(
        Output("last_update_text", "children"),
        Input("timestamp", "data"),
        prevent_initial_call=True,
    )
    def set_last_update_text(timestamp):
        return f"Last update: {datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y, %H:%M')}"

    
    @callback(
        # TODO: dashtable as outputs
        Input("timestamp", "data"),
        # TODO: All filters etc as inputs
        prevent_initial_call=True,
    )
    def update_pump_table():
        id = ctx.triggered_id
        # TODO: distinguish between data update and filter etc.
    
    # TODO: Repeat for all other tables
