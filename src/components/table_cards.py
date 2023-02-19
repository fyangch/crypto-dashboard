from dash import html
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable, FormatTemplate

from src.components.radio_items import get_radio_items


percentage = FormatTemplate.percentage(1)

table_style_args = {
    "page_size": 30,
    "style_cell": {"border": "0px"},
    "style_header": {
        "backgroundColor": "rgb(55, 90, 127)",
        "color": "white",
        "fontWeight": "bold",
        "border": "0px",
    },
    "style_data": {
        "backgroundColor": "rgb(48, 48, 48)",
        "color": "white"
    },
    "style_data_conditional": [
        {
        "if": {"row_index": "odd"},
        "backgroundColor": "rgb(32, 32, 32)",
        },
        {}, # dummy condition to insert highlight conditions
    ],
    "style_as_list_view": True,
}

def get_row_highlight_condition(row_index: int) -> dict:
    return  {
        "if": {"row_index": row_index},
        "backgroundColor": "rgb(0, 188, 140)",
        "border": "0px",
    }

trend_card = dbc.Card(
    html.Div(
        [
            html.H4("Uptrend Screener"),
            get_radio_items(id="radio_trend", options=["All", "Watchlist", "Tier 1", "Tier 2", "Tier 3", "Tier 4"]),
            DataTable(
                id="trend_table",
                data=list(), 
                columns=[
                    dict(id="id", name="Name"),
                    dict(id="trend_strength", name="Trend Strength", type="numeric", format=percentage),
                    dict(id="gain_1d", name="Gain 1D", type="numeric", format=percentage),
                    dict(id="gain_3d", name="Gain 3D", type="numeric", format=percentage),
                    dict(id="gain_1w", name="Gain 1W", type="numeric", format=percentage),
                ],
                **table_style_args,
            )
        ], 
        className="dbc dbc-row-selectable",
    ),
    body=True,
)

pump_card = dbc.Card(
    html.Div(
        [   
            html.H4("Pump Screener"),
            get_radio_items(id="radio_pump", options=["All", "Watchlist", "Tier 1", "Tier 2", "Tier 3", "Tier 4"]),
            DataTable(
                id="pump_table",
                data=list(), 
                columns=[
                    dict(id="id", name="Name"),
                    dict(id="pump_strength", name="Pump Strength", type="numeric", format=percentage),
                    dict(id="gain_1d", name="Gain 1D", type="numeric", format=percentage),
                    dict(id="gain_3d", name="Gain 3D", type="numeric", format=percentage),
                    dict(id="gain_1w", name="Gain 1W", type="numeric", format=percentage),
                ],
                **table_style_args,
            )
        ], 
        className="dbc dbc-row-selectable",
    ),
    body=True,
)
