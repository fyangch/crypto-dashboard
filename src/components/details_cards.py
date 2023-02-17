from dash import html, dcc
import dash_bootstrap_components as dbc


# TODO: replace dummy card
bitcoin_card = dbc.Card(
    [
        html.H4("BTC Details", className="card-title"),
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

altcoin_card = dbc.Card(
    [
        html.H4("Altcoin Details", className="card-title"),
        html.H6("Click on any table row to see more details of the corresponding altcoin.", className="card-subtitle"),

        html.Br(),
        dbc.Row([
            dbc.Col([dbc.Row(dbc.Col(id="altcoin_usd_chart", width=12))], width=6),
            dbc.Col([dbc.Row(dbc.Col(id="altcoin_btc_chart", width=12))], width=6),
        ]),
        
        html.Br(),
        dbc.CardLink("Card link", href="#"),
        dbc.CardLink("External link", href="https://google.com"),
    ], body=True
)