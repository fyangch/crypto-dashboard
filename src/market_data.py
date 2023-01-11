import pandas as pd
import time
import requests
from typing import Optional, List, Tuple


BINANCE_ENDPOINT = "https://api.binance.com/api/v3/klines"
BYBIT_ENDPOINT = "https://api-testnet.bybit.com/spot/v3/public/quote/kline"
HUOBI_ENDPOINT = "https://api.huobi.pro/market/history/kline"
KUCOIN_ENDPOINT = "https://api.kucoin.com/api/v1/market/candles"

INTERVALS = {
    5: "5m",
    15: "15m",
    60: "1h",
    240: "4h",
    1440: "1d",
}


def get_klines(
    symbol: str, 
    exchange: str,
    interval: int,
    num_klines: int = 100,
    min_age: Optional[int] = None,
    ) -> Tuple[pd.DataFrame, float]:
    """
    Fetch the most recent klines for the given symbol.

    Args:
        symbol
            Name of the trading pair, e.g. BTCBUSD.
        exchange
            Name of the exchange from which the klines will be fetched.
        interval
            Kline interval in minutes.
        num_klines
            How many klines to fetch.
        min_age
            Optional minimum age of the last kline in minutes. 
            The last kline will be discarded if it is younger than this value.

    Returns:
        Data frame containing the klines and the current price.
    """
    if exchange.lower() == "binance":
        klines = _get_binance_klines(symbol, interval, num_klines)
    else:
        raise ValueError(f"Invalid exchange: {exchange}")

    current_price = klines['close'].iloc[-1] # save current price before (possibly) removing the last kline

    if min_age:
        age = (time.time() - klines['timestamp'].iloc[-1]) / 60. # age of last kline in minutes
        if age < min_age:
            klines = klines.iloc[:-1]

    return klines, current_price


def _get_binance_klines(symbol: str, interval: int, num_klines: int):
    """ 
    Fetch klines from Binance. 
    Docs: https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data 
    """
    params = {
        "symbol": symbol,
        "interval": INTERVALS[interval],
        "limit": str(num_klines),
    }
    data = requests.get(BINANCE_ENDPOINT, params=params).json()
    n = len(data)

    return pd.DataFrame(data={
        "timestamp": [data[i][0] // 1000 for i in range(n)], # in seconds
        "open": [float(data[i][1]) for i in range(n)],
        "high": [float(data[i][2]) for i in range(n)],
        "low": [float(data[i][3]) for i in range(n)],
        "close": [float(data[i][4]) for i in range(n)],
    })


def _get_bybit_klines():
    """ 
    Fetch klines from Bybit. 
    Docs: https://bybit-exchange.github.io/docs/spot/v3/#t-querykline 
    """
    # TODO
    return


def _get_huobi_klines():
    """ 
    Fetch klines from Huobi. 
    Docs: https://open.huobigroup.com/?name=kline 
    """
    # TODO
    return


def _get_kucoin_klines():
    """ 
    Fetch klines from KuCoin. 
    Docs: https://docs.kucoin.com/#get-klines 
    """
    # TODO
    return