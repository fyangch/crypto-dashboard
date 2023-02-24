import dash_bootstrap_components as dbc
from typing import List


def get_radio_items(
        id: str,
        options: List[str],
        alignment: str = "center",
    ) -> dbc.RadioItems:
    """ Return radio items with the passed options. """
    return dbc.RadioItems(
        id=id,
        options=options, 
        value=options[0], 
        inline=True,
        style={
            "textAlign": alignment,
            "marginRight": "-1em",
        },
        className="dbc dbc-row-selectable",
    )
