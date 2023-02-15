import pandas as pd
from datetime import datetime
from typing import List, Tuple

from dash import html, dcc, no_update, callback, Output, Input
import dash_bootstrap_components as dbc

from src.utils import get_market_data


layout = dbc.Container([
    # to save data in the browser session of the user
    dcc.Store(id="state"),

    html.H1("Pump Screener"),
    html.P("Last update:", id="last_update_text"),
    
    # tables for each tier
    dbc.Row([
        dbc.Col([
            html.H5("Best Tier 1 Coins"), 
            html.Div(id="gains_1"),
            html.H5("Best Tier 2 Coins"), 
            html.Div(id="gains_2"),
        ]),
        dbc.Col([
            html.H5("Best Tier 3 Coins"), 
            html.Div(id="gains_3"),
            html.H5("Best Tier 4 Coins"), 
            html.Div(id="gains_4"),
        ])
    ]),
], fluid="sm")

header = html.Thead(html.Tr([
    html.Th("Coin"), 
    html.Th("1D Gain"),
    html.Th("3D Gain"),
    html.Th("1W Gain"),
    html.Th("Links"),
]))

table_options = {
    "bordered": True, 
    "dark": True, 
    "hover": True, 
    "responsive": True, 
    "striped": True,
}


@callback(
    Output("last_update_text", "children"),
    Output("gains_1", "children"),
    Output("gains_2", "children"),
    Output("gains_3", "children"),
    Output("gains_4", "children"),
    Input("state", "data"),
)
def update_tables(n_clicks) -> Tuple[str, dbc.Table, dbc.Table, dbc.Table, dbc.Table]:
    # TODO: Add other stuff: interval update, sorting, "conservative" checkbox, etc.
    return get_tables(num_results=[5, 5, 5, 10])


def get_empty_table() -> dbc.Table:
    return dbc.Table(header, **table_options)


def get_table_body(df: pd.DataFrame) -> html.Tbody:
    coins = df.index.values
    rows = [
        html.Tr([
            html.Td(coin), 
            html.Td("{:.2f}%".format(df.loc[coin, "gain_1d"])),
            html.Td("{:.2f}%".format(df.loc[coin, "gain_3d"])),
            html.Td("{:.2f}%".format(df.loc[coin, "gain_1w"])),
            html.Td([
                html.A("Exchange", href=df.loc[coin, "exchange_link"], target="_blank"), " ",
                html.A("TradingView", href=df.loc[coin, "tradingview_link"], target="_blank"),
            ]),
        ])
        for coin in coins
    ]

    return html.Tbody(rows)


def get_tables(num_results: List[int]) -> Tuple[str, dbc.Table, dbc.Table, dbc.Table, dbc.Table]:
    df, timestamp = get_market_data()
    if df is None:
        return no_update, *[get_empty_table() for _ in range(4)]

    last_update_text = f"(Last update: {datetime.utcfromtimestamp(timestamp).strftime('%d/%m/%Y, %H:%M')} UTC)"

    tables = []
    for i in range(1, 5):
        curr_df = df[df["priority"] == i]
        body = get_table_body(curr_df.sort_values(by=["gain_1d"], ascending=False).iloc[:num_results[i-1]])
        tables.append(dbc.Table([header] + [body], **table_options))

    return last_update_text, *tables
