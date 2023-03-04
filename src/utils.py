import pandas as pd
from typing import List


def filter_df(df: pd.DataFrame, filter: str) -> pd.DataFrame:
    """ Filter and return data frame according to the current radio item selection. """
    if filter == "All":
        return df
    elif filter == "Watchlist":
        return df[df["watchlist"] == 1]
    else:
        tier_number = int(filter.replace("Tier ", ""))
        return df[df["tier"] == tier_number]


def get_emas(close: pd.Series, ema_lengths: List[int]) -> List[pd.Series]:
    """ Compute and return EMAs given the close values and EMA lengths. """
    return [
        close.ewm(span=length).mean()
        for length in ema_lengths
    ]


def add_emas(klines: pd.DataFrame, ema_lengths: List[int]) -> pd.DataFrame:
    """ Compute and add EMAs to the given kline data frame. """
    emas = get_emas(klines["close"], ema_lengths)
    for i in range(len(ema_lengths)):
        klines[f"ema_{ema_lengths[i]}"] = emas[i]
    return klines
