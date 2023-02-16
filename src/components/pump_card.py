from dash import html, dash_table
import dash_bootstrap_components as dbc


pump_card = dbc.Card(
    [
        html.H4("Pump Screener"),

        dbc.CardLink("Card link", href="#"),
        dbc.CardLink("External link", href="https://google.com"),
    ], body=True
)