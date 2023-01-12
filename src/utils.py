import pandas as pd
import json

def get_info_df():
    with open("coins.json", "r") as f:
        coins = json.load(f)

    names = coins.keys()
    return pd.DataFrame(
        index=names,
        data={
            "symbol": [coins[name]["symbol"] for name in names],
            "priority": [coins[name]["priority"] for name in names],
            "watchlist": [coins[name]["watchlist"] for name in names],
            "pump_screener": [coins[name]["pump_screener"] for name in names],
            "trend_screener": [coins[name]["trend_screener"] for name in names],
            "exchange": [coins[name]["exchange"] for name in names],
            "exchange_link": [coins[name]["exchange_link"] for name in names],
            "tradingview_link": [coins[name]["tradingview_link"] for name in names],
        }
    )