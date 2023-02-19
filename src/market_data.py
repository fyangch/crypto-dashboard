import pandas as pd
import os
from typing import List, Dict

from src.exchange_data import get_klines
from src.utils import get_info_df


def update_market_data() -> None:
    """
    Update all data frame values using the latest exchange data.
    """
    # TODO: Convert json config to csv file and read df directly here
    # fetch latest kline data
    df = get_info_df()
    kline_dict = get_klines(df, interval=240, num_klines=186)

    # compute gains from lowest lows within last 1D, 1W and 1M
    df = _add_gains(
        df=df, kline_dict=kline_dict, look_back=[6, 42, 186],
        col_names=["gain_1d", "gain_1w", "gain_1m"],
    )

    # compute strengths of current pumps
    df = _add_pump_strengths(df, kline_dict)

    # save updated data
    if not os.path.exists(os.path.join("data", "klines")):
        os.makedirs(os.path.join("data", "klines"))

    df.to_csv(os.path.join("data", "market_data.csv"), index_label="name")
    for name in kline_dict:
        kline_dict[name].to_csv(os.path.join("data", "klines", f"{name}.csv"))


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
            gains[i].append(current_price / lows[i] - 1.)

    for i in range(len(look_back)):
        df[col_names[i]] = gains[i]
    
    return df


def _add_pump_strengths(
    df: pd.DataFrame,
    kline_dict: Dict[str, pd.DataFrame],
    look_back: int = 45,
    ) -> pd.DataFrame:
    """
    Compute the strength of the current pumps. For that, the largest kline range (without wicks) of the 
    last 3 klines is compared with the mean of the absolute kline ranges within the last week.
    """
    strengths = []
    for name in df.index:
        klines = kline_dict[name].iloc[-look_back:]
        ranges = (klines["close"] - klines["open"])
        max_range = ranges.iloc[-3:].max()
        mean = ranges.iloc[:-3].abs().mean()
        strengths.append(max_range / mean - 1.)

    df["pump_strength"] = strengths
    return df
