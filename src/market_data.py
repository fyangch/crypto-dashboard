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
    info_df = get_info_df() 
    pump_df = _update_pump_data(info_df)
    trend_df = _update_trend_data(info_df)

    # save data frames
    timestamp = int(time.time())
    pump_df.to_csv(os.path.join("data", f"pump_{timestamp}.csv"))
    trend_df.to_csv(os.path.join("data", f"trend_{timestamp}.csv"))


def _update_pump_data(info_df: pd.DataFrame) -> pd.DataFrame:
    """
    Return data frame with newly updated values for the pump screener.
    """
    df = info_df[info_df["pump_screener"] == True]
    kline_dict = get_klines(df, interval=15, num_klines=100)

    look_back = [4, 16, 96]
    if _get_kline_age(kline_dict["BTC"]) < 8:
        look_back = [x + 1 for x in look_back]
    
    df = _add_gains(
        df=df, kline_dict=kline_dict, look_back=look_back,
        gain_col_names=["gain_1h", "gain_4h", "gain_1d"],
        flag_col_names=["gains_1h_cons", "gain_4h_cons", "gain_1d_cons"],
    )

    return df


def _update_trend_data(info_df: pd.DataFrame) -> pd.DataFrame:
    """
    Return data frame with newly updated values for the trend screener.
    """
    df = info_df[info_df["trend_screener"] == True]
    kline_dict = get_klines(df, interval=240, num_klines=100)

    # TODO
    return df


def _get_kline_age(klines: pd.DataFrame) -> int:
    """
    Return the age of the newest kline (in minutes).
    """
    return int(time.time() - klines["timestamp"].iloc[-1]) // 60


def _add_gains(
    df: pd.DataFrame, 
    kline_dict: Dict[str, pd.DataFrame],
    look_back: List[int],
    gain_col_names: List[str],
    flag_col_names: List[str],
    ) -> pd.DataFrame:
    """
    Compute the percentage gains from the lowest lows within the past klines and add them to the data frame.
    Each look-back value thereby defines the number of most recent klines from which the corresponding gain
    will be computed.
    Gains will be flagged as 'conservative' if the current closing price is higher than the highest high within
    the first 50% of the corresponding look-back klines.
    """
    gains = [[] for _ in look_back]
    flags = [[] for _ in look_back]
    for name in df.index:
        lows = [kline_dict[name]["low"].iloc[-offset:].min() for offset in look_back]
        highs = [kline_dict[name]["high"].iloc[-offset:-(offset//2)].max() for offset in look_back]
        current_price = kline_dict[name]["close"].iloc[-1]
        for i in range(len(look_back)):
            gains[i].append((current_price / lows[i] - 1.) * 100.)
            flags[i].append(current_price > highs[i])

    for i in range(look_back):
        df[gain_col_names[i]] = gains[i]
        df[flag_col_names[i]] = flags[i]
    
    return df
