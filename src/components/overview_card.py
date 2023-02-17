from dash import html
import dash_bootstrap_components as dbc


# TODO: replace dummy card
overview_card = dbc.Card(
    [
        html.H4("Overview", className="card-title"),
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