import pandas as pd
from datetime import datetime
from typing import List, Tuple

from dash import html, dcc, no_update, callback, Output, Input
import dash_bootstrap_components as dbc

from src.utils import get_market_data

from src.components.info_card import info_card


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
    # to save data in the browser session of the user
    dcc.Store(id="state"),
    dbc.Container(
        [
            dbc.Row(dbc.Col(info_card, width=12)),
            html.Br(),
            dbc.Row([
                dbc.Col(test_card, width=6),
                dbc.Col(test_card, width=3),
                dbc.Col(test_card, width=3),
            ]),
        ], fluid=True),
    ], 
    style={"margin": "2em 1em 0em 1em"} # top right bottom left
)
