# Cryptocurrency Dashboard

This repository contains the source code for an interactive cryptocurrency dashboard that monitors over 350 cryptocurrencies and creates rankings based on the strength of the current uptrends and breakouts.
This dashboard can be used as a tool to find strong coins and tokens that are outperforming Bitcoin or showing a sudden increase in volatility to the upside. It is mostly intended for finding setups for swing/position trades and rotations from one sector to another. It may not be suitable for short term trades and the metrics shown in the dashboard are useless during downtrends.

![](/imgs/dashboard.png "Description")


## Details
This cryptocurrency dashboard was created using [Dash & Plotly](https://plotly.com/) and it is mainly intended to monitor coins and tokens that are listed on Binance. However, cryptocurrencies from other exchanges can be easily added. The dashboard currently supports kline (candlestick) data retrieval from Binance, Bybit, Gate.io, Huobi and KuCoin.

### Dashboard Metrics
- 4 hour klines are used for the charts and the computation of all metrics.
- Gains are measured from the lowest low within the last day/week/month to the current close.
- EMAs with lengths 12, 21 and 50 are used to determine the strength of the current uptrends.
- The maximum kline range (without wicks) among the 3 most recent klines is compared with the mean and standard deviation of the absolute kline ranges from the last 7 days to determine the strength of the current "pumps". There might be some false positives among the shown pumps.


## Setup
Clone this repository and go to the root directory of the project. Run the following commands to create a new environment and install all dependencies:

1. `python -m venv venv`
2. `.\venv\Scripts\Activate.ps1`
3. `pip install -r requirements.txt`

## Usage
Run `python app.py` and open http://127.0.0.1:8050/ in your browser. This dashboard is designed for large monitors and you may need to adjust the zoom level in your browser depending on the scaling settings of your device and the resolution of your screen.

Run `python add_new_binance_listings.py` to automatically add newly listed coins and tokens on Binance to the `data/config.csv` file.

## Customization
The `data/config.csv` file can be edited to customize the dashboard. For that, you can e.g. use the [Excel Viewer](https://marketplace.visualstudio.com/items?itemName=GrapeCity.gc-excelviewer) extension for Visual Studio Code.

### Watchlist and Tiers
To add cryptocurrencies to your watchlist, simply set the corresponding value in the `watchlist` column to 1.
You can also divide the coins and tokens into different tiers from 1-4. For that, simply set the values in the `tier` column to 1, 2, 3 or 4.

### Other exchanges
You can also manually add coins and tokens from Bybit, Gate.io, Huobi and KuCoin. However, only spot listings are supported at the moment. Simply add a new row to the `data/config.csv` file and add the following values for each column:

| Column | Value to enter |
| ------ | --------------- |
| name |  Name to be displayed for the new coin or token. |
| symbol | This value needs to comply with the exchange API! See below. |
| tier | 1, 2, 3 or 4. |
| watchlist | 0 or 1. |
| exchange | bybit, gateio, huobi or kucoin. |
| other | The remaining columns can be used to add optional TradingView or exchange links. |

Note that each exchange API uses a different format for the symbol names:

| Exchange | Symbol format |
| ------ | --------------- |
| bybit |  BTCUSDT |
| gateio | BTC_USDT |
| huobi | btcusdt |
| kucoin | BTC-USDT |
