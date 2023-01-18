import pandas as pd
from typing import Optional, List

from src.exchange_data import get_klines


def update_market_data():
    # TODO
    return


def get_pump_data():
    # TODO: Move the function from pump_screener.py here
    return


def get_gains(
    klines: pd.DataFrame, 
    look_back: List[int],
    current_price: Optional[float] = None,
    ) -> List[float]:
    """
    Compute the current percentage gains from the lowest lows in the past klines.

    Args:
        klines
            Data frame containing the most recent klines.
        loock_back
            List containing the number of most recent klines from which the gains will be computed.
        current_price
            Optional current price in case the last kline was removed after the retrieval. 
            If None, the close price of the last data frame row will be used.
    
    Returns:
        List of percentage gains for each look-back value.
    """
    # TODO: Replace current_price arg by min_age arg. Increase look_back numbers by 1 if last kline is too young.
    lows = [klines['low'].iloc[-offset:].min() for offset in look_back]

    if not current_price:
        current_price = klines['close'].iloc[-1]

    return [((current_price / low) - 1.) * 100. for low in lows]
