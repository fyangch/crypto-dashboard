import pandas as pd
import os
from datetime import datetime

from dash import html, callback, Output, Input
import dash_bootstrap_components as dbc

from src.utils import get_info_df


layout = dbc.Container([            
    html.H1("Pump Screener"),
    html.P("TODO!", id="last_update_text"),

    html.Div(dbc.Row([
        dbc.Col(html.H5("Priority 1 Coins")),
        dbc.Col(html.Div(id="last_update_1", style={"text-align": "center"})),
        dbc.Col(html.Div(dbc.Button("Update", id="update_1", size="sm"), style={"text-align": "right"})),
    ])),
    html.Div(id="gains_1"),

    html.Div(dbc.Row([
        dbc.Col(html.H5("Priority 2 Coins")), 
        dbc.Col(html.Div(id="last_update_2", style={"text-align": "center"})),
        dbc.Col(html.Div(dbc.Button("Update", id="update_2", size="sm"), style={"text-align": "right"})),
    ])),
    html.Div(id="gains_2"),

    html.Div(dbc.Row([
        dbc.Col(html.H5("Priority 3 Coins")),
        dbc.Col(html.Div(id="last_update_3", style={"text-align": "center"})),
        dbc.Col(html.Div(dbc.Button("Update", id="update_3", size="sm"), style={"text-align": "right"})),
    ])),
    html.Div(id="gains_3"),

    html.Div(dbc.Row([
        dbc.Col(html.H5("Priority 4 Coins")), 
        dbc.Col(html.Div(id="last_update_4", style={"text-align": "center"})),
        dbc.Col(html.Div(dbc.Button("Update", id="update_4", size="sm"), style={"text-align": "right"})),
    ])),
    html.Div(id="gains_4"),
])


@callback(Output("gains_1", "children"), Output("last_update_1", "children"), Input("update_1", "n_clicks"))
def update_gains_1(n_clicks):
    return update_tables(1)

@callback(Output("gains_2", "children"), Output("last_update_2", "children"), Input("update_2", "n_clicks"))
def update_gains_2(n_clicks):
    tables = update_tables(2)
    return tables

@callback(Output("gains_3", "children"), Output("last_update_3", "children"), Input("update_3", "n_clicks"))
def update_gains_3(n_clicks):
    return update_tables(3)

@callback(Output("gains_4", "children"), Output("last_update_4", "children"), Input("update_4", "n_clicks"))
def update_gains_4(n_clicks):
    return update_tables(4)


def get_empty_tables():
    headers = [
        [html.Thead(html.Tr([html.Th("Coin"), html.Th(f"{time_frame} Gain"), html.Th("Links")]))]
        for time_frame in ["1H", "4H", "1D"]
    ]

    return dbc.Row([
        dbc.Col(
            dbc.Table(headers[i], bordered=True, dark=True, hover=True, responsive=True, striped=True)
        )
        for i in range(3)
    ])


def get_table_body(df, info_df, gain):
    coins = df.index.values
    rows = [
        html.Tr([
            html.Td(coin), 
            html.Td("{:.2f}%".format(df.loc[coin, gain])),
            html.Td([
                html.A("Exchange", href=df.loc[coin, "exchange_link"], target="_blank"), " ",
                html.A("TradingView", href=df.loc[coin, "tradingview_link"], target="_blank"),
            ])
        ])
        for coin in coins
    ]

    return [html.Tbody(rows)]


def update_tables(priority, num_results=5):
    info_df = get_info_df()
    info_df = info_df[info_df["priority"] == priority]

    if len(info_df.index) == 0:
        return get_empty_tables(), ""

    headers = [
        [html.Thead(html.Tr([html.Th("Coin"), html.Th(f"{time_frame} Gain"), html.Th("Links")]))]
        for time_frame in ["1H", "4H", "1D"]
    ]
    
    df = pd.read_csv(os.path.join("data", "pump_1674815967.csv"), index_col="name")
    bodies = [
        get_table_body(df.sort_values(by=[gain], ascending=False).iloc[:num_results], info_df, gain)
        for gain in ["gain_1h", "gain_4h", "gain_1d"]
    ]

    tables = dbc.Row([
        dbc.Col(
            dbc.Table(headers[i] + bodies[i], bordered=True, dark=True, hover=True, responsive=True, striped=True)
        )
        for i in range(3)
    ])

    return tables, f"(Last update: {datetime.now().strftime('%H:%M:%S')})"
