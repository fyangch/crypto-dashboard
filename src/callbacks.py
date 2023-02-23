import os
import time
import pandas as pd
from datetime import datetime

from dash import Dash, no_update, ctx, Output, Input, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from src.market_data import update_market_data
from src.components.table_cards import get_row_highlight_condition
from src.components.figures import get_candlestick_figure, get_bar_figure
from src.components.exchange_dropdown import get_exchange_dropdown
from src.utils import filter_df


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


    @app.callback(
        Output("last_update_text", "children"),
        Input("timestamp", "data"),
        prevent_initial_call=True,
    )
    def set_last_update_text(timestamp):
        return f"Last update: {datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y, %H:%M')}"

    
    @app.callback(
        Output("trend_table", "data"),
        Input("timestamp", "data"),
        Input("radio_trend", "value"),
        prevent_initial_call=True,
    )
    def update_trend_table(timestamp, filter):
        df = pd.read_csv(os.path.join("data", "market_data.csv"))
        df = df.rename(columns={"name": "id"})
        df = filter_df(df, filter)
        df = df[["id", "trend_strength", "gain_1d", "gain_1w", "gain_1m"]]

        return df.to_dict("records")


    @app.callback(
        Output("pump_table", "data"),
        Input("timestamp", "data"),
        Input("radio_pump", "value"),
        prevent_initial_call=True,
    )
    def update_pump_table(timestamp, filter):
        df = pd.read_csv(os.path.join("data", "market_data.csv"))
        df = df.rename(columns={"name": "id"})
        df = filter_df(df, filter)
        df = df.loc[df["pump_strength"] > 2]
        df = df[["id", "pump_strength", "gain_1d", "gain_1w", "gain_1m"]]   
        df = df.sort_values(by=["pump_strength"], ascending=False)

        return df.to_dict("records")


    @app.callback(
        Output("trend_table", "page_current"),
        Output("pump_table", "page_current"),
        Input("timestamp", "data"),
        Input("trend_table", "sort_by"),
    )
    def reset_to_first_page(timestamp, sort_by):
        if ctx.triggered_id == "timestamp":
            return 0, 0
        return 0, no_update


    @app.callback(
        Output("altcoin", "data"),
        Output("trend_table", "active_cell"), Output("trend_table", "selected_cells"), Output("trend_table", "style_data_conditional"),
        Output("pump_table", "active_cell"), Output("pump_table", "selected_cells"), Output("pump_table", "style_data_conditional"),
        Input("trend_table", "active_cell"),  Input("pump_table", "active_cell"), Input("timestamp", "data"),
        Input("radio_trend", "value"),  Input("radio_pump", "value"),
        State("trend_table", "style_data_conditional"), State("pump_table", "style_data_conditional"),
        prevent_initial_call=True,
    )
    def select_altcoin(active_cell_trend, active_cell_pump, timestamp, filter_trend, filter_pump, style_trend, style_pump):
        # remove row highlighting when reloading or applying filters
        if ctx.triggered_id in ["timestamp", "radio_trend", "radio_pump"]:
            style_trend[1] = {}
            style_pump[1] = {}
            return no_update, None, [], style_trend, None, [], style_pump

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
        Input("radio_overview", "value"),
        prevent_initial_call=True,
    )
    def update_overview_card(timestamp, filter):
        df = pd.read_csv(os.path.join("data", "market_data.csv"))
        df = df.rename(columns={"name": "id"})
        df = filter_df(df, filter)
        df = df.sort_values(by=["gain_1d"], ascending=False).iloc[:30]

        return get_bar_figure(names=df["id"], gains=df["gain_1d"])


    @app.callback(
        Output("bitcoin_chart", "children"),
        Input("timestamp", "data"),
        Input("radio_btc_chart", "value"),
        prevent_initial_call=True,
    )
    def update_bitcoin_chart(timestamp, timeframe):
        df = pd.read_csv(os.path.join("data", "klines", "BTC.csv"))
        if timeframe == "1W":
            df = df.iloc[-42:]
        else:
            df = df.iloc[-186:]

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
        Input("timestamp", "data"),
        Input("altcoin", "data"),
        Input("radio_altcoin_chart", "value"), 
        prevent_initial_call=True,
    )
    def update_altcoin_charts(timestamp, altcoin, timeframe):
        if altcoin in [None, ""]:
            raise PreventUpdate
        
        altcoin_df = pd.read_csv(os.path.join("data", "klines", f"{altcoin}.csv"))
        btc_df = pd.read_csv(os.path.join("data", "klines", "BTC.csv"))
        n = altcoin_df.shape[0] 

        if timeframe == "1W":
            altcoin_df = altcoin_df.iloc[-min(42, n):]
            btc_df = btc_df.iloc[-min(42, n):]
        else:
            altcoin_df = altcoin_df.iloc[-min(186, n):]
            btc_df = btc_df.iloc[-min(186, n):]
        
        # index values may not coincide because of missing altcoin data
        # e.g. in case of a new listing
        altcoin_df.index = range(altcoin_df.shape[0])
        btc_df.index = range(btc_df.shape[0])

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
            open=altcoin_df["open"] / btc_df["open"], 
            high=altcoin_df["high"] / btc_df["close"],
            low=altcoin_df["low"] / btc_df["close"], 
            close=altcoin_df["close"] / btc_df["close"],
        )

        return usd_chart, btc_chart


    @app.callback(
        Output("bitcoin_tradingview", "children"),
        Output("bitcoin_exchanges", "children"),
        Input("timestamp", "data"),
        prevent_initial_call=True,
    )
    def update_bitcoin_links(timestamp):
        df = pd.read_csv(os.path.join("data", "config.csv"), index_col="name")
        tradingview_link = dbc.CardLink("TradingView", target="_blank", href=df.loc["BTC", "tradingview_usd"])
        exchange_links = get_exchange_dropdown(df, "BTC")

        return tradingview_link, exchange_links


    @app.callback(
        Output("altcoin_tradingview", "children"),
        Output("altcoin_exchanges", "children"),
        Input("altcoin", "data"),
        prevent_initial_call=True,
    )
    def update_altcoin_links(altcoin):
        df = pd.read_csv(os.path.join("data", "config.csv"), index_col="name")

        tradingview_links = []
        if type(df.loc[altcoin, "tradingview_usd"]) == str:
            tradingview_links.append(dbc.CardLink("TradingView (USD)", target="_blank", href=df.loc[altcoin, "tradingview_usd"]))
        if type(df.loc[altcoin, "tradingview_btc"]) == str:
            tradingview_links.append(dbc.CardLink("TradingView (BTC)", target="_blank", href=df.loc[altcoin, "tradingview_btc"]))

        exchange_links = get_exchange_dropdown(df, altcoin)

        return tradingview_links, exchange_links
