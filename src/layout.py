from dash import html, dcc
import dash_bootstrap_components as dbc

from src.components.info_card import info_card
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
        dcc.Store(id="timestamp", data=0),        
        dbc.Container(
            [
                dbc.Row(dbc.Col(info_card, width=12)),
                html.Br(),
                dbc.Row([
                    dbc.Col(test_card, width=5),
                    dbc.Col(test_card, width=4),
                    dbc.Col(pump_card, width=3),
                ]),
            ], fluid=True
        ),
    ], 
    style={"margin": "2em 1em 0em 1em"}, # top right bottom left
)
