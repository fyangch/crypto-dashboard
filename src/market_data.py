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

    # compute strengths of current pumps
    df = _add_pump_strengths(df, kline_dict)

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


def _add_pump_strengths(
    df: pd.DataFrame,
    kline_dict: Dict[str, pd.DataFrame],
    look_back: int = 43,
    ) -> pd.DataFrame:
    """
    Compute the strength of the current pumps. For that, the current kline ranges
    are compared with the medians of the absolute kline ranges within the last week.
    """
    strengths = []
    for name in df.index:
        klines = kline_dict[name].iloc[-look_back:]
        ranges = (klines["high"] - klines["low"])
        median = ranges.iloc[:-1].abs().median()
        strengths.append((ranges.iloc[-1] / median - 1.) * 100.)

    df["pump_strength"] = strengths
    return df
