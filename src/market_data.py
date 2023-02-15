import pandas as pd
import os
import time
from typing import List, Dict

from src.exchange_data import get_klines
from src.utils import get_info_df


def update_market_data() -> None:
    """
    Update all data frame values using the latest exchange data.
    Save the updated data frames as "pump_{timestamp}.csv" and "trend_{timestamp}.csv"
    """
    # TODO: Convert json config to csv file and read df directly here
    # fetch latest kline data
    df = get_info_df()
    kline_dict = get_klines(df, interval=240, num_klines=60)

    # compute gains from lowest lows within last 1D, 3D and 1W
    look_back = [6, 18, 42]
    if _get_kline_age(kline_dict["BTC"]) < 120:
        look_back = [x + 1 for x in look_back]
    df = _add_gains(
        df=df, kline_dict=kline_dict, look_back=look_back,
        col_names=["gain_1d", "gain_3d", "gain_1w"],
    )

    # save updated data
    timestamp = int(time.time())
    df.to_csv(os.path.join("data", f"market_data_{timestamp}.csv"), index_label="name")


def _get_kline_age(klines: pd.DataFrame) -> int:
    """
    Return the age of the newest kline (in minutes).
    """
    return int(time.time() - klines["timestamp"].iloc[-1]) // 60


def _add_gains(
    df: pd.DataFrame, 
    kline_dict: Dict[str, pd.DataFrame],
    look_back: List[int],
    col_names: List[str],
    ) -> pd.DataFrame:
    """
    Compute the percentage gains from the lowest lows within the past klines and add them to the data frame.
    Each look-back value thereby defines the number of most recent klines from which the corresponding gain
    will be computed.
    """
    gains = [[] for _ in look_back]
    for name in df.index:
        lows = [kline_dict[name]["low"].iloc[-offset:].min() for offset in look_back]
        current_price = kline_dict[name]["close"].iloc[-1]
        for i in range(len(look_back)):
            gains[i].append((current_price / lows[i] - 1.) * 100.)

    for i in range(len(look_back)):
        df[col_names[i]] = gains[i]
    
    return df
