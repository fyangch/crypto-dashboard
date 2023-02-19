import dash_bootstrap_components as dbc
from typing import List


def get_radio_items(
        id: str,
        options: List[str],
        alignment: str = "center",
    ) -> dbc.RadioItems:

    return dbc.RadioItems(
        id=id,
        options=options, 
        value=options[0], 
        inline=True,
        style={"text-align": alignment},
        className="dbc dbc-row-selectable",
    )