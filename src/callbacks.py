import os
import time
import pandas as pd
from datetime import datetime


from dash import Dash, html, dcc, no_update, ctx, dash_table, Output, Input, State
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
        #update_market_data() # TODO: UNCOMMENT!
        return timestamp


    @app.callback(
        Output("last_update_text", "children"),
        Input("timestamp", "data"),
        prevent_initial_call=True,
    )
    def set_last_update_text(timestamp):
        return f"Last update: {datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y, %H:%M')}"


    @app.callback(
        Output("pump_table", "data"),
        Input("timestamp", "data"),
        prevent_initial_call=True,
    )
    def update_pump_table(timestamp):
        df = pd.read_csv(os.path.join("data", "market_data.csv"))
        df = df.rename(columns={"name": "id"})
        df = df.loc[df["pump_strength"] > 2]
        df = df[["id", "pump_strength", "gain_1d", "gain_3d", "gain_1w"]]
        df = df.sort_values(by=["pump_strength"], ascending=False)

        return df.to_dict("records")
        
    
    @app.callback(
        Output("trend_table", "data"),
        Input("timestamp", "data"),
        # TODO: All filters etc as inputs
        prevent_initial_call=True,
    )
    def update_trend_table(timestamp):
        df = pd.read_csv(os.path.join("data", "market_data.csv"))
        df = df.rename(columns={"name": "id"})
        #df = df.loc[df["trend_strength"] > -1.] # TODO: Set final threshold
        df = df[["id", "gain_1d", "gain_3d", "gain_1w"]]
        df = df.sort_values(by=["gain_1d"], ascending=False)

        if ctx.triggered_id == "timestamp":
            return df.to_dict("records")
        else:
            # TODO
            # use dcc.Store to store current filter settings?
            raise PreventUpdate


    @app.callback(
        Output("altcoin", "data"),
        Output("trend_table", "active_cell"),
        Output("trend_table", "selected_cells"),
        Output("pump_table", "active_cell"),
        Output("pump_table", "selected_cells"),
        Input("trend_table", "active_cell"), 
        Input("pump_table", "active_cell"),
        prevent_initial_call=True,
    )
    def select_altcoin(active_cell_trend, active_cell_pump):
        if ctx.triggered_id == "trend_table":
            if not active_cell_trend: # happens when you change the current page
                raise PreventUpdate
            return active_cell_trend["row_id"], no_update, no_update, None, []
        else:
            if not active_cell_pump: # happens when you change the current page
                raise PreventUpdate
            return active_cell_pump["row_id"], None, [], no_update, no_update


    @app.callback(
        Output("test", "children"), 
        Input("altcoin", "data"),
        prevent_initial_call=True,
    )
    def update_altcoin_details(altcoin):
        if altcoin in [None, ""]:
            raise PreventUpdate
        
        return altcoin
