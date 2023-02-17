from dash import html
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable, FormatTemplate


percentage = FormatTemplate.percentage(2)

table_style_args = {
    "page_size": 30,
    "style_cell": {"border": "0px solid black"},
    "style_header": {
        "backgroundColor": "rgb(55, 90, 127)",
        "color": "white",
        "fontWeight": "bold",
        "border": "0px solid black",
    },
    "style_data": {
        "backgroundColor": "rgb(48, 48, 48)",
        "color": "white"
    },
    "style_data_conditional": [{
        "if": {"row_index": "odd"},
        "backgroundColor": "rgb(32, 32, 32)",
    }],
    "style_as_list_view": True,
}

pump_card = dbc.Card(
    html.Div(
        [
            html.H4("Pump Screener"),
            DataTable(
                id="pump_table",
                data=list(), 
                columns=[
                    dict(id="name", name="Name"),
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

trend_card = dbc.Card() # TODO