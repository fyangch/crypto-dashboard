import pandas as pd

from src.market_data import get_klines, get_gains


def scan_markets(
    coins: dict,
    ) -> pd.DataFrame:
    """
    Scan crypto markets for pumps.

    Args:
        coins
            Dictionary with information about the coins to consider.
    
    Returns:
        Data frame containing the name of the coin and the corresponding gains. 
    """
    name = []
    gain_1h = []
    gain_4h = []
    gain_1d = []
    
    for coin in coins:
        klines, current_price = get_klines(
            symbol=coins[coin]["symbol"],
            exchange=coins[coin]["exchange"],
            interval=15,
            num_klines=100,
            min_age=8,
        )
        gains = get_gains(
            klines=klines,
            look_back=[4, 16, 96],
            current_price=current_price,
        )
        name.append(coin)
        gain_1h.append(gains[0])
        gain_4h.append(gains[1])
        gain_1d.append(gains[2])
    
    return pd.DataFrame(data={
        "name": name,
        "gain_1h": gain_1h,
        "gain_4h": gain_4h,
        "gain_1d": gain_1d,
    })