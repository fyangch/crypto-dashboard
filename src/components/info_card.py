from dash import html
import dash_bootstrap_components as dbc


link_dropdown = dbc.DropdownMenu(
    label="External Links",
    children=[
        dbc.DropdownMenuItem("TokenUnlocks", target="_blank", href="https://token.unlocks.app/"),
        dbc.DropdownMenuItem("CoinMarketCal Events", target="_blank", href="https://coinmarketcal.com/en/"),
        dbc.DropdownMenuItem("CoinMarketCap Events", target="_blank", href="https://coinmarketcap.com/events/"),
    ],
    align_end=True,
)

# card at the top that shows the time of the last update and links to external sites.
info_card = dbc.Card(
    dbc.Row([
        dbc.Col([
            html.H3("Cryptocurrency Dashboard"),
            html.P("Last update:", id="last_update_text"),
        ]),
        dbc.Col(
            dbc.Stack([
                dbc.Button("Update Data", id="update_button"),
                link_dropdown,
            ], direction="horizontal", gap=3, style={"float": "right"}),
            align="center"
        ),
    ]),  
    body=True,
)
