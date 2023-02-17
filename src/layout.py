from dash import html, dcc
import dash_bootstrap_components as dbc

from src.components.info_card import info_card
from src.components.overview_card import overview_card
from src.components.details_cards import bitcoin_card, altcoin_card
from src.components.table_cards import trend_card, pump_card


test_card = dbc.Card(
    [
        html.H4("Title", className="card-title"),
        html.H6("Card subtitle", className="card-subtitle"),
        html.P(
            "Some quick example text to build on the card title and make "
            "up the bulk of the card's content.",
            className="card-text",
        ),
        dbc.CardLink("Card link", href="#"),
        dbc.CardLink("External link", href="https://google.com"),
    ], body=True
)

layout = html.Div(
    [
        dcc.Store(id="timestamp", data=0), # timestamp of latest update
        dcc.Store(id="altcoin", data=""), # which altcoin is currently selected
        dbc.Container(
            [
                dbc.Row(dbc.Col(info_card, width=12)),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col(overview_card, width=12)),
                        html.Br(),
                        dbc.Row(dbc.Col(bitcoin_card, width=12)),
                        html.Br(),
                        dbc.Row(dbc.Col(altcoin_card, width=12)),
                    ], width=6),
                    dbc.Col(trend_card, width=3),
                    dbc.Col(pump_card, width=3),
                ]),
            ], fluid=True
        ),
    ], 
    style={"margin": "2em 1em 0em 1em"}, # top right bottom left
)
