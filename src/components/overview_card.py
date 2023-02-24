from dash import html
import dash_bootstrap_components as dbc

from src.components.radio_items import get_radio_items


# card that shows the top gainers of the last 24 hours.
overview_card = dbc.Card(
    [
        html.H4("Overview", className="card-title"),
        html.Div(id="bar_chart"),
        get_radio_items(id="radio_overview", options=["All", "Watchlist", "Tier 1", "Tier 2", "Tier 3", "Tier 4"]),
    ], body=True
)
