import pandas as pd
import dash_bootstrap_components as dbc


col_names = ["binance_spot_usd", "binance_spot_btc", "binance_perps", "bybit_spot", "bybit_perps"]
link_names = ["Binance Spot (USD)", "Binance Spot (BTC)", "Binance Perpetuals", "Bybit Spot", "Bybit Perpetuals"]


def get_exchange_dropdown(df: pd.DataFrame, name: str) -> dbc.DropdownMenu:
    urls = df.loc[name, col_names]

    return dbc.DropdownMenu(
        label="Exchanges",
        children=[
            dbc.DropdownMenuItem(link_names[i], target="_blank", href=urls[i])
            for i in range(len(col_names)) if type(urls[i]) == str
        ],
        align_end=True,
        color="link",
        style={"float": "right", "marginRight": "-0.5em"},
    )
