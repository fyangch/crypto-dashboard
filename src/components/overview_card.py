from dash import html
import dash_bootstrap_components as dbc

from src.components.radio_items import get_radio_items


# card that shows the top gainers
overview_card = dbc.Card(
    [
        dbc.Row([
            dbc.Col(html.H4("Bitcoin Chart", className="card-title")),
            dbc.Col(get_radio_items(id="radio_overview_timeframe", options=["1D", "1W", "1M"], alignment="right")),
        ]),
        html.Div(id="bar_chart"),
        get_radio_items(id="radio_overview_filter", options=["All", "Watchlist", "Tier 1", "Tier 2", "Tier 3", "Tier 4"]),
    ], body=True
)
