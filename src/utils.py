import pandas as pd
import json
import sys
import os
import psutil
import time
from datetime import datetime


def check_parent_process() -> None:        
    """
    Terminate the current process if the parent process is not running anymore. 
    """
    if not psutil.pid_exists(os.getppid()):
        sys.exit()


def clean_up_files() -> None:
    """
    Keep CSV files with market data from the previous two updates
    and delete the remaining files.
    """
    # TODO
    raise NotImplementedError("Clean up function not implemented yet.")


# TODO: Use csv config file for coins/tokens and remove this function
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