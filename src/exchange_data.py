import time
import requests
import pandas as pd
from requests.models import Response
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict


"""
API docs:
    - https://binance-docs.github.io/apidocs/spot/en/#kline-candlestick-data
    - https://binance-docs.github.io/apidocs/futures/en/#mark-price-kline-candlestick-data
    - https://bybit-exchange.github.io/docs/v5/market/kline
    - https://www.gate.io/docs/developers/apiv4/en/#market-candlesticks
    - https://open.huobigroup.com/?name=kline 
    - https://docs.kucoin.com/#get-klines 
"""

BINANCE_ENDPOINT = "https://api.binance.com/api/v3/klines"
BINANCE_PERPS_ENDPOINT = "https://testnet.binancefuture.com/fapi/v1/markPriceKlines"
BYBIT_ENDPOINT = "https://api.bybit.com/v5/market/kline"
GATIO_ENDPOINT = "https://api.gateio.ws/api/v4/spot/candlesticks"
HUOBI_ENDPOINT = "https://api.huobi.pro/market/history/kline"
KUCOIN_ENDPOINT = "https://api.kucoin.com/api/v1/market/candles"

INTERVALS = {
    "binance": {5: "5m", 15: "15m", 60: "1h", 240: "4h", 1440: "1d"},
    "bybit": {5: "5", 15: "15", 60: "60", 240: "240", 1440: "D"},
    "gateio": {5: "5m", 15: "15m", 60: "1h", 240: "4h", 1440: "1d"},
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
        try:
            if exchange == "binance":
                try:
                    kline_dict[names[i]] = _get_binance_klines(responses[i])
                except:
                    # try perps endpoint in case there is no spot listing
                    params = {
                        "symbol": info_df.loc[names[i], "symbol"],
                        "interval": INTERVALS[exchange][interval],
                        "limit": num_klines,
                    }
                    response = requests.get(BINANCE_PERPS_ENDPOINT, params=params)
                    kline_dict[names[i]] = _get_binance_klines(response)
            elif exchange == "bybit":
                kline_dict[names[i]] = _get_bybit_klines(responses[i])
            elif exchange == "gateio":
                kline_dict[names[i]] = _get_gateio_klines(responses[i])
            elif exchange == "huobi":
                kline_dict[names[i]] = _get_huobi_klines(responses[i])
            elif exchange == "kucoin":
                kline_dict[names[i]] = _get_kucoin_klines(responses[i])
        except:
            print(f"Kline retrieval error! Name: {names[i]}, exchange: {exchange}")
    
    return kline_dict


def _get_all_responses(
    info_df: pd.DataFrame,
    interval: int,
    num_klines: int = 100,
    ) -> List[Response]:
    """
    Send kline data requests for all the coins in info_df and return all the response objects.
    """
    with ThreadPoolExecutor(max_workers=50) as executor:
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
            "limit": num_klines,
        }
        return requests.get(BINANCE_ENDPOINT, params=params)
    elif exchange == "bybit":
        params = {
            "category": "spot",
            "symbol": info_df.loc[name, "symbol"],
            "interval": INTERVALS[exchange][interval],
            "limit": num_klines,
        }
        return requests.get(BYBIT_ENDPOINT, params=params)
    elif exchange == "gateio":
        params = {
            "currency_pair": info_df.loc[name, "symbol"],
            "interval": INTERVALS[exchange][interval],
            "limit": num_klines,
        }
        return requests.get(GATIO_ENDPOINT, params=params)
    elif exchange == "huobi":
        params = {
            "symbol": info_df.loc[name, "symbol"].lower(),
            "period": INTERVALS[exchange][interval],
            "size": num_klines,
        }
        return requests.get(HUOBI_ENDPOINT, params=params)
    elif exchange == "kucoin":
        params = {
            "symbol": info_df.loc[name, "symbol"],
            "type": INTERVALS[exchange][interval],
            "startAt": int(time.time()) - interval * num_klines * 60,
        }
        return requests.get(KUCOIN_ENDPOINT, params=params)
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
    data = response.json()["result"]["list"]
    n = len(data)

    # klines are in reversed order (last kline is at index 0)
    return pd.DataFrame(data={
        "timestamp": [int(data[i][0]) // 1000 for i in reversed(range(n))], # in seconds
        "open": [float(data[i][1]) for i in reversed(range(n))],
        "high": [float(data[i][2]) for i in reversed(range(n))],
        "low": [float(data[i][3]) for i in reversed(range(n))],
        "close": [float(data[i][4]) for i in reversed(range(n))],
    })


def _get_gateio_klines(response: Response) -> pd.DataFrame:
    """ 
    Return data frame with kline data given a response from the Gate.io API.
    Format of the kline data is consistent across all exchanges.
    """
    data = response.json()
    n = len(data)

    return pd.DataFrame(data={
        "timestamp": [int(data[i][0]) for i in range(n)],
        "open": [float(data[i][5]) for i in range(n)],
        "high": [float(data[i][3]) for i in range(n)],
        "low": [float(data[i][4]) for i in range(n)],
        "close": [float(data[i][2]) for i in range(n)],
    })


def _get_huobi_klines(response: Response) -> pd.DataFrame:
    """ 
    Return data frame with kline data given a response from the Huobi API.
    Format of the kline data is consistent across all exchanges.
    """
    data = response.json()["data"]
    n = len(data)

    # klines are in reversed order (last kline is at index 0)
    return pd.DataFrame(data={
        "timestamp": [int(data[i]["id"]) for i in reversed(range(n))],
        "open": [float(data[i]["open"]) for i in reversed(range(n))],
        "high": [float(data[i]["high"]) for i in reversed(range(n))],
        "low": [float(data[i]["low"]) for i in reversed(range(n))],
        "close": [float(data[i]["close"]) for i in reversed(range(n))],
    })


def _get_kucoin_klines(response: Response) -> pd.DataFrame:
    """ 
    Return data frame with kline data given a response from the KuCoin API.
    Format of the kline data is consistent across all exchanges.
    """
    data = response.json()["data"]
    n = len(data)

    # klines are in reversed order (last kline is at index 0)
    return pd.DataFrame(data={
        "timestamp": [int(data[i][0]) for i in reversed(range(n))],
        "open": [float(data[i][1]) for i in reversed(range(n))],
        "high": [float(data[i][3]) for i in reversed(range(n))],
        "low": [float(data[i][4]) for i in reversed(range(n))],
        "close": [float(data[i][2]) for i in reversed(range(n))],
    })
