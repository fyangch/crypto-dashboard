from dash import html
import dash_bootstrap_components as dbc


link_dropdown = dbc.DropdownMenu(
    label="External Links",
    children=[
        dbc.DropdownMenuItem("Binance Listings", target="_blank", href="https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48"),
        dbc.DropdownMenuItem("Binance Delistings", target="_blank", href="https://www.binance.com/en/support/announcement/delisting?c=161&navId=161"),
        dbc.DropdownMenuItem("CoinMarketCal Events", target="_blank", href="https://coinmarketcal.com/en/"),
        dbc.DropdownMenuItem("CoinMarketCap Events", target="_blank", href="https://coinmarketcap.com/events/"),
        dbc.DropdownMenuItem("TokenUnlocks", target="_blank", href="https://token.unlocks.app/"),
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
                dbc.Button("Update Data", id="update_button"),
                link_dropdown,
            ], direction="horizontal", gap=3, style={"float": "right"}),
            align="center"
        ),
    ]),  
    body=True,
)
