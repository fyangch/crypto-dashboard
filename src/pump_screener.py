import pandas as pd

from src.market_data import get_klines, get_gains
from src.decorators import parallel


@parallel(num_processes=3)
def scan_markets(
    info_df: pd.DataFrame,
    ) -> pd.DataFrame:
    """
    Scan crypto markets for pumps.

    Args:
        info_df
            Data frame with information about the coins to consider.
    
    Returns:
        Data frame containing the name of the coin and the corresponding gains. 
    """
    names = info_df.index.values
    gains_1h = []
    gains_4h = []
    gains_1d = []
    
    for name in names:
        klines, current_price = get_klines(
            symbol=info_df.loc[name, "symbol"],
            exchange=info_df.loc[name, "exchange"],
            interval=15,
            num_klines=100,
            min_age=8,
        )
        gains = get_gains(
            klines=klines,
            look_back=[4, 16, 96],
            current_price=current_price,
        )
        gains_1h.append(gains[0])
        gains_4h.append(gains[1])
        gains_1d.append(gains[2])
    
    return pd.DataFrame(
        index=names,
        data={
            "gain_1h": gains_1h,
            "gain_4h": gains_4h,
            "gain_1d": gains_1d,
        }
    )