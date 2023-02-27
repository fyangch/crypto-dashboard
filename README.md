# Cryptocurrency Dashboard

This repository contains the source code for an interactive cryptocurrency dashboard that monitors over 450 coins and tokens and creates rankings based on the strength of the current uptrends and breakouts.
This dashboard can be used as a tool to find strong coins and tokens that are outperforming Bitcoin or showing a sudden increase in volatility to the upside. It is mostly intended for finding setups for swing/position trades and rotations from one sector to another. It may not be suitable for short term trades and the metrics shown in the dashboard are useless during downtrends.

![](/imgs/dashboard.png "Description")


## Details
This cryptocurrency dashboard was created using [Dash & Plotly](https://plotly.com/) and it currently supports kline (candlestick) data retrieval from Binance, Bybit, Huobi and KuCoin.

- 4 hour klines are used for the charts and the computation of all metrics.
- Gains are measured from the lowest low within the last day/week/month to the current close. *(For my use case, this is more useful than measuring the gains from the opening price of the day/week/month.)*
- EMAs with lengths 12, 21 and 50 are used to determine the strength of the current uptrends.
- The maximum kline range (without wicks) among the 3 most recent klines is compared with the mean and standard deviation of the absolute kline ranges from the last 7 days to determine the strength of the current "pumps". There might be some false positives among the shown pumps.


## Setup
Clone this repository and go to the root directory of the project. Run the following commands to create a new environment and install all dependencies:

1. `python -m venv venv`
2. `.\venv\Scripts\Activate.ps1`
3. `pip install -r requirements.txt`

## Usage
Run `python app.py` and open http://127.0.0.1:8050/ in your browser. Depending on the scaling settings of your device and the resolution of your screen, you may need to adjust the zoom level in your browser.
