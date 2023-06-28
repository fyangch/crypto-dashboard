"""Script to automatically add new Binance listings to the config file."""
import os
import requests
import pandas as pd


NAMES_TO_IGNORE = {
    "ADADOWN", "ADAUP", "BNBDOWN", "BNBUP", "BTCDOWN", "BTCUP", "ETHDOWN", "ETHUP", # leveraged tokens
    "1000LUNC", "1000PEPE", "1000SHIB", "1000XEC", # special names for perpetuals
}


def add_new_name(df: pd.DataFrame, name: str, symbol: str) -> pd.DataFrame:
    """Add new coin to config with default values."""
    print(f"New coin/token: {name}")

    # order of columns: symbol, tier, watchlist, exchange, chart_usd, chart_btc, spot_usd, spot_btc, perps
    df.loc[name] = [symbol, 4, 0, "binance", "", "", "", "", ""]
    return df


def check_spot_listings(df: pd.DataFrame, quote: str) -> pd.DataFrame:
    """Check if there are any new spot listings."""
    if quote not in ["USDT", "BTC"]:
        raise ValueError(f"Invalid quote: {quote}")

    response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
    for x in response.json()["symbols"]:
        if x["quoteAsset"] == quote and x["status"] == "TRADING":
            name = x["baseAsset"]
            symbol = x["symbol"]

            if name in NAMES_TO_IGNORE:
                continue
            
            if name not in df.index:
                add_new_name(df, name, symbol)

            chart_col = "chart_usd" if quote == "USDT" else "chart_btc"
            spot_col = "spot_usd" if quote == "USDT" else "spot_btc"

            spot_url = df.loc[name, spot_col]
            if type(spot_url) != str or len(spot_url) == 0:
                print(f"New spot listing: {symbol}")
                df.loc[name, spot_col] = f"https://www.binance.com/en/trade/{x['baseAsset']}_{quote}"
                df.loc[name, chart_col] = f"https://www.tradingview.com/chart/?symbol=BINANCE%3A{x['baseAsset']}{quote}"
    return df


def check_perps_listings(df: pd.DataFrame) -> pd.DataFrame:
    """Check if there are any new perpetual listings."""
    response = requests.get("https://testnet.binancefuture.com/fapi/v1/exchangeInfo")
    for x in response.json()["symbols"]:
        if x["quoteAsset"] == "USDT" and x["status"] == "TRADING" and x["contractType"] == "PERPETUAL":
            name = x["baseAsset"]
            symbol = x["symbol"]

            if name in NAMES_TO_IGNORE:
                continue

            if name not in df.index:
                add_new_name(df, name, symbol)
            
            perps_url = df.loc[name, "perps"]
            if type(perps_url) != str or len(perps_url) == 0:
                print(f"New perps listing: {symbol}")
                df.loc[name, "perps"] = f"https://www.binance.com/en/futures/{x['baseAsset']}USDT"

                # only add perps chart if there is no spot chart
                chart_url = df.loc[name, "chart_usd"]
                if type(chart_url) != str or len(chart_url) == 0:
                    df.loc[name, "chart_usd"] = f"https://www.tradingview.com/chart/?symbol=BINANCE%3A{x['baseAsset']}USDT.P"
    return df
                

df = pd.read_csv(os.path.join("data", "config.csv"), index_col="name")
df = check_spot_listings(df, "USDT")
df = check_spot_listings(df, "BTC")
df = check_perps_listings(df)
df = df.sort_index()
df.to_csv(os.path.join("data", "config.csv"), index_label="name")
