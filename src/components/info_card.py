from dash import html
import dash_bootstrap_components as dbc


dropdown = dbc.DropdownMenu(
    label="External Links",
    children=[
        dbc.DropdownMenuItem("New Binance Listings", target="_blank", href="https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48"),
        dbc.DropdownMenuItem("Binance Delistings", target="_blank", href="https://www.binance.com/en/support/announcement/delisting?c=161&navId=161"),
        dbc.DropdownMenuItem("CoinMarketCal", target="_blank", href="https://coinmarketcal.com/en/"),
        dbc.DropdownMenuItem("CoinMarketCap Events", target="_blank", href="https://coinmarketcap.com/events/"),
    ],
    align_end=True,
)

info_card = dbc.Card(
    dbc.Row([
        dbc.Col([
            html.H3("Crypto Dashboard"),
            html.P("Last update:", id="last_update_text"),
        ]),
        dbc.Col(
            dbc.Stack([
                dbc.Button("Manual Update", id="manual_update_button"),
                dropdown,
            ], direction="horizontal", gap=3, style={"float": "right"}),
            align="center"
        ),
    ]),  
    body=True,
)
