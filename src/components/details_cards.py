from dash import html, dcc
import dash_bootstrap_components as dbc


# TODO: replace dummy card
bitcoin_card = dbc.Card(
    [
        html.H4("Bitcoin Chart", className="card-title"),        
        html.Div(id="bitcoin_chart"),
        html.Br(),
        html.Div([
            dbc.CardLink("Card link", href="#"),
            dbc.CardLink("External link", target="_blank", href="https://google.com"),
        ]),
    ], body=True
)

altcoin_card = dbc.Card(
    [
        html.H4("Altcoin Charts", className="card-title"),
        html.H6("Click on any table row to see more details about the corresponding altcoin.", className="card-subtitle"),
        html.Br(),
        dbc.Row([
            dbc.Col([dbc.Row(dbc.Col(id="altcoin_usd_chart", width=12))], width=6),
            dbc.Col([dbc.Row(dbc.Col(id="altcoin_btc_chart", width=12))], width=6),
        ]),
        html.Br(),
        html.Div([
            dbc.CardLink("Card link", href="#"),
            dbc.CardLink("External link", target="_blank", href="https://google.com"),
        ]),
    ], body=True
)