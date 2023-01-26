import pandas as pd
import requests
from requests.models import Response
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict


"""
API docs:
    - https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data 
    - https://bybit-exchange.github.io/docs/spot/v3/#t-querykline 
    - https://open.huobigroup.com/?name=kline 
    - https://docs.kucoin.com/#get-klines 
"""

BINANCE_ENDPOINT = "https://api.binance.com/api/v3/klines"
BYBIT_ENDPOINT = "https://api-testnet.bybit.com/spot/v3/public/quote/kline"
HUOBI_ENDPOINT = "https://api.huobi.pro/market/history/kline"
KUCOIN_ENDPOINT = "https://api.kucoin.com/api/v1/market/candles"

INTERVALS = {
    "binance": {5: "5m", 15: "15m", 60: "1h", 240: "4h", 1440: "1d"},
    "bybit": {5: "5m", 15: "15m", 60: "1h", 240: "4h", 1440: "1d"},
    "huobi": {5: "5min", 15: "15min", 60: "60min", 240: "4hour", 1440: "1day"},
    "kucoin": {5: "5min", 15: "15min", 60: "1hour", 240: "4hour", 1440: "1day"},
}


def get_klines(
    info_df: pd.DataFrame,
    interval: int,
    num_klines: int = 100,
    ) -> Dict[str, pd.DataFrame]:
    """
    Fetch the most recent klines for all the coins in info_df.

    Args:
        info_df
            Data frame with information about the coins.
        interval
            Kline interval in minutes.
        num_klines
            How many klines to fetch.

    Returns:
        Dictionary containing the klines for each coin.
        Key: name of the coin. Value: data frame containing the kline data.
    """
    responses = _get_all_responses(info_df, interval, num_klines)

    kline_dict = {}
    names = info_df.index.values
    for i in range(len(names)):
        exchange = info_df.loc[names[i], "exchange"]
        if exchange == "binance":
            kline_dict[names[i]] = _get_binance_klines(responses[i])
        elif exchange == "bybit":
            kline_dict[names[i]] = _get_bybit_klines(responses[i])
        elif exchange == "huobi":
            kline_dict[names[i]] = _get_huobi_klines(responses[i])
        elif exchange == "kucoin":
            kline_dict[names[i]] = _get_kucoin_klines(responses[i])
        else:
            raise ValueError(f"Invalid exchange: {exchange}")
    
    return kline_dict


def _get_all_responses(
    info_df: pd.DataFrame,
    interval: int,
    num_klines: int = 100,
    ) -> List[Response]:
    """
    Send kline data requests for all the coins in info_df and return all the response objects.
    """
    # multithreading yields a speedup of approximately 7-10x
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(_get_response, name, info_df, interval, num_klines) 
            for name in info_df.index
        ]
        return [future.result() for future in futures]


def _get_response(
    name: str,
    info_df: pd.DataFrame,
    interval: int,
    num_klines: int,
    ) -> Response:
    """
    Send a kline data request for the given coin and return the response object.
    """
    exchange = info_df.loc[name, "exchange"]
    if exchange == "binance":
        params = {
            "symbol": info_df.loc[name, "symbol"],
            "interval": INTERVALS[exchange][interval],
            "limit": str(num_klines),
        }
        return requests.get(BINANCE_ENDPOINT, params=params)
    elif exchange == "bybit":
        # TODO
        raise NotImplementedError()
    elif exchange == "huobi":
        # TODO
        raise NotImplementedError()
    elif exchange == "kucoin":
        # TODO
        raise NotImplementedError()
    else:
        raise ValueError(f"Invalid exchange: {exchange}")


def _get_binance_klines(response: Response) -> pd.DataFrame:
    """ 
    Return data frame with kline data given a response from the Binance API.
    Format of the kline data is consistent across all exchanges.
    """
    data = response.json()
    n = len(data)

    return pd.DataFrame(data={
        "timestamp": [data[i][0] // 1000 for i in range(n)], # in seconds
        "open": [float(data[i][1]) for i in range(n)],
        "high": [float(data[i][2]) for i in range(n)],
        "low": [float(data[i][3]) for i in range(n)],
        "close": [float(data[i][4]) for i in range(n)],
    })


def _get_bybit_klines(response: Response) -> pd.DataFrame:
    """ 
    Return data frame with kline data given a response from the Bybit API.
    Format of the kline data is consistent across all exchanges.
    """
    # TODO
    raise NotImplementedError()


def _get_huobi_klines(response: Response) -> pd.DataFrame:
    """ 
    Return data frame with kline data given a response from the Huobi API.
    Format of the kline data is consistent across all exchanges.
    """
    # TODO
    raise NotImplementedError()


def _get_kucoin_klines(response: Response) -> pd.DataFrame:
    """ 
    Return data frame with kline data given a response from the KuCoin API.
    Format of the kline data is consistent across all exchanges.
    """
    # TODO
    raise NotImplementedError()
