import os
import time
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

from dash import Dash, html, dcc, no_update, ctx, Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from src.market_data import update_market_data
from src.components.table_cards import get_row_highlight_condition
from src.components.figures import get_candlestick_figure, get_bar_figure


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
        df = df.loc[df["pump_strength"] > 1.5]
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
        Output("trend_table", "active_cell"), Output("trend_table", "selected_cells"), Output("trend_table", "style_data_conditional"),
        Output("pump_table", "active_cell"), Output("pump_table", "selected_cells"), Output("pump_table", "style_data_conditional"),
        Input("trend_table", "active_cell"),  Input("pump_table", "active_cell"),
        State("trend_table", "style_data_conditional"), State("pump_table", "style_data_conditional"),
        prevent_initial_call=True,
    )
    def select_altcoin(active_cell_trend, active_cell_pump, style_trend, style_pump):
        altcoin = no_update
        if ctx.triggered_id == "trend_table":
            if active_cell_trend:
                condition = get_row_highlight_condition(active_cell_trend["row"])
                style_trend[1] = condition
                style_pump[1] = {}
                altcoin = active_cell_trend["row_id"]
            else:
                style_trend[1] = {}
                style_pump = no_update
        else:
            if active_cell_pump:
                condition = get_row_highlight_condition(active_cell_pump["row"])
                style_pump[1] = condition
                style_trend[1] = {}
                altcoin = active_cell_pump["row_id"]
            else:
                style_pump[1] = {}
                style_trend = no_update
                
        return altcoin, None, [], style_trend, None, [], style_pump

    
    @app.callback(
        Output("bar_chart", "children"),
        Input("timestamp", "data"),
        prevent_initial_call=True,
    )
    def update_overview_card(timestamp):
        df = pd.read_csv(os.path.join("data", "market_data.csv"))
        df = df.rename(columns={"name": "id"})
        df = df.sort_values(by=["gain_1d"], ascending=False).iloc[:30]

        return get_bar_figure(names=df["id"], gains=df["gain_1d"])


    @app.callback(
        Output("bitcoin_chart", "children"),
        Input("timestamp", "data"),
        prevent_initial_call=True,
    )
    def update_bitcoin_card(timestamp):
        df = pd.read_csv(os.path.join("data", "klines", "BTC.csv")).iloc[-42:]
        # TODO: Update chart and exchange links
        return get_candlestick_figure(
            title="BTC / USD",
            timestamp=df["timestamp"],
            open=df["open"], 
            high=df["high"],
            low=df["low"], 
            close=df["close"],
        )


    @app.callback(
        Output("altcoin_usd_chart", "children"), 
        Output("altcoin_btc_chart", "children"), 
        Input("altcoin", "data"),
        prevent_initial_call=True,
    )
    def update_altcoin_card(altcoin):
        if altcoin in [None, ""]:
            raise PreventUpdate
        
        altcoin_df = pd.read_csv(os.path.join("data", "klines", f"{altcoin}.csv")).iloc[-42:]
        btc_df = pd.read_csv(os.path.join("data", "klines", "BTC.csv")).iloc[-42:]

        # TODO: Update chart and exchange links

        usd_chart = get_candlestick_figure(
            title=f"{altcoin} / USD",
            timestamp=altcoin_df["timestamp"],
            open=altcoin_df["open"], 
            high=altcoin_df["high"],
            low=altcoin_df["low"], 
            close=altcoin_df["close"],
        )

        btc_chart = get_candlestick_figure(
            title=f"{altcoin} / BTC",
            timestamp=altcoin_df["timestamp"],
            open=altcoin_df["open"] / btc_df["close"], 
            high=altcoin_df["high"] / btc_df["close"],
            low=altcoin_df["low"] / btc_df["close"], 
            close=altcoin_df["close"] / btc_df["close"],
        )

        return usd_chart, btc_chart
