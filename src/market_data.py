import os
import time
import numpy as np
import pandas as pd
from typing import List, Dict

from src.exchange_data import get_klines


def update_market_data() -> None:
    """
    Update and save all market data values using the latest exchange data.
    """
    # fetch latest kline data
    df = pd.read_csv(os.path.join("data", "config.csv"), index_col="name")
    kline_dict = get_klines(df, interval=240, num_klines=200)

    # discard coins/tokens for which errors occured during the kline retrieval
    df = df.loc[kline_dict.keys()]

    # compute gains from lowest lows within last 1D, 1W and 1M
    df = _add_gains(
        df=df, kline_dict=kline_dict, look_back=[6, 42, 186],
        col_names=["gain_1d", "gain_1w", "gain_1m"],
    )

    # compute strength of current uptrends
    df = _add_trend_strengths(df, kline_dict)

    # compute strength of current pumps
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


def _add_trend_strengths(
    df: pd.DataFrame,
    kline_dict: Dict[str, pd.DataFrame],
    ) -> pd.DataFrame:
    """
    Compute the strength of the current uptrends. For that, EMAs with lengths 12, 21 and 50 are computed
    and compared with each other. The most recent klines will be discarded for the computation if they 
    are less than 1 hour old.
    """
    strengths = []
    for name in df.index:
        klines = kline_dict[name]

        # discard last kline if it is less than 1 hour old
        if time.time() - klines["timestamp"].iloc[-1] < 3600:
            klines = klines.iloc[:-1]

        # compute most EMAs
        ema_12 = klines["close"].ewm(span=12).mean()
        ema_21 = klines["close"].ewm(span=21).mean()
        ema_50 = klines["close"].ewm(span=50).mean()

        # compute strength of uptrend using EMA values
        scores = np.array([
            ema_12.iloc[-1] / ema_21.iloc[-1],
            ema_21.iloc[-1] / ema_50.iloc[-1],
        ])
        strengths.append(scores.mean() - 1.)

    df["trend_strength"] = strengths
    return df


def _add_pump_strengths(
    df: pd.DataFrame,
    kline_dict: Dict[str, pd.DataFrame],
    look_back: int = 42,
    ) -> pd.DataFrame:
    """
    Compute the strength of the current pumps. For that, the largest kline range (without wicks) of the 
    last 3 klines is compared with the mean and std of the absolute kline ranges within the last week.
    """
    strengths = []
    for name in df.index:
        klines = kline_dict[name].iloc[-look_back:]
        ranges = (klines["close"] - klines["open"])
        max_range = ranges.iloc[-3:].max()
        mean = ranges.iloc[:-3].abs().mean()
        std = ranges.iloc[:-3].abs().std()

        if max_range > mean + 2 * std:
            strengths.append(max_range / mean - 1.)
        else:
            strengths.append(0.)

    df["pump_strength"] = strengths
    return df
