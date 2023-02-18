from dash import html
import dash_bootstrap_components as dbc


overview_card = dbc.Card(
    [
        html.H4("Overview", className="card-title"),
        html.Div(id="bar_chart"),
    ], body=True
)