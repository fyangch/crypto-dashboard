import pandas as pd
import json
import sys
import os
import psutil
from typing import Optional, Tuple


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
    files = sorted([file for file in os.listdir("data") if "market_data" in file])
    if len(files) > 2:
        for file in files[:-2]:
            os.remove(os.path.join("data", file))


def new_market_data_available(timestamp: int) -> bool:
    """
    Return True if there are market data files that have been created after the given timestamp.
    """
    files = [file for file in os.listdir("data") if "market_data" in file]
    timestamps = [int(file.replace(".csv", "").replace("market_data_", "")) for file in files]

    return max(timestamps) > timestamp


def get_market_data() -> Tuple[Optional[pd.DataFrame], int]:
    """
    Return data frame with the most recent market data and its timestamp.
    Return None if there are no files available.
    """
    files = sorted([file for file in os.listdir("data") if "market_data" in file])
    if len(files) == 0:
        return None, -1

    df = pd.read_csv(os.path.join("data", files[-1]), index_col="name")
    timestamp = int(files[-1].replace(".csv", "").replace("market_data_", ""))
    
    return df, timestamp
    

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
            "exchange": [coins[name]["exchange"] for name in names],
            "exchange_link": [coins[name]["exchange_link"] for name in names],
            "tradingview_link": [coins[name]["tradingview_link"] for name in names],
        }
    )