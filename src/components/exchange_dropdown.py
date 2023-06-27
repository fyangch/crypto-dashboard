import pandas as pd
import dash_bootstrap_components as dbc


# data frame column names
col_names = ["spot_usd", "spot_btc", "perps"]

# labels of the buttons that open the corresponding exchange sites
labels = ["Spot (USD)", "Spot (BTC)", "Perpetuals"]


def get_exchange_dropdown(df: pd.DataFrame, name: str) -> dbc.DropdownMenu:
    """ Return a dropdown with links for all available exchange sites for a given coin/token. """
    urls = df.loc[name, col_names]

    return dbc.DropdownMenu(
        label="Exchanges",
        children=[
            dbc.DropdownMenuItem(labels[i], target="_blank", href=urls[i])
            for i in range(len(col_names)) if type(urls[i]) == str and len(urls[i]) > 0
        ],
        align_end=True,
        color="link",
        style={"float": "right", "marginRight": "-0.5em"},
    )
