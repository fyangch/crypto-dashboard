import pandas as pd
import json
import sys
import os
import psutil
from typing import Literal, Optional


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
    for type in ["pump", "trend"]:
        files = sorted([file for file in os.listdir("data") if type in file])
        if len(files) > 2:
            for file in files[:-2]:
                os.remove(os.path.join("data", file))


def new_market_data_available(timestamp: int) -> bool:
    """
    Return True if there are market data files that have been created after the given timestamp.
    """
    files = [file for file in os.listdir("data") if "pump" in file]
    timestamps = [int(file.replace(".csv", "").replace("pump_", "")) for file in files]

    return max(timestamps) > timestamp


def get_market_data(type: Literal["pump", "trend"]) -> Optional[pd.DataFrame]:
    """
    Return data frame with the most recent market data.
    Return None if there are no files available.
    """

    files = sorted([file for file in os.listdir("data") if type in file])
    if len(files) == 0:
        return None

    return pd.read_csv(os.path.join("data", files[-1]), index_col="name")
    

# TODO: Use csv config file for coins/tokens and remove this function
def get_info_df():
    with open(os.path.join("data", "coins.json"), "r") as f:
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