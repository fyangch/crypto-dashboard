from dash import html
import dash_bootstrap_components as dbc

from src.components.radio_items import get_radio_items


# card with details about Bitcoin (chart, TradingView link, exchange links)
bitcoin_card = dbc.Card(
    [
        dbc.Row([
            dbc.Col(html.H4("Bitcoin Chart", className="card-title")),
            dbc.Col(get_radio_items(id="radio_btc_chart", options=["1W", "1M"], alignment="right")),
        ]),
        html.Div(id="bitcoin_chart"),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(id="bitcoin_tradingview"),
                dbc.Col(id="bitcoin_exchanges", style={"textAlign": "right"}),
            ], 
            style={"marginBottom": "-0.5em"},
        ),
    ], body=True
)

# card with details about the currently selected altcoin (charts, TradingView links, exchange links)
altcoin_card = dbc.Card(
    [
        dbc.Row([
            dbc.Col(html.H4("Altcoin Charts", className="card-title")),
            dbc.Col(get_radio_items(id="radio_altcoin_chart", options=["1W", "1M"], alignment="right")),
        ]),
        html.H6("Click on any table row to see more details about the corresponding altcoin.", className="card-subtitle"),
        html.Br(),
        dbc.Row([
            dbc.Col([dbc.Row(dbc.Col(id="altcoin_usd_chart", width=12))], width=6),
            dbc.Col([dbc.Row(dbc.Col(id="altcoin_btc_chart", width=12))], width=6),
        ]),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(id="altcoin_tradingview"),
                dbc.Col(id="altcoin_exchanges", style={"textAlign": "right"}),
            ],
            style={"marginBottom": "-0.5em"},
        ),
    ], body=True
)
