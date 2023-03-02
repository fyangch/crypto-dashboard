import pandas as pd
import copy
import plotly.graph_objects as go
from dash import dcc


figure_args = {
    "title_x": 0.5,
    "title_y": 0.98,
    "title_xanchor": "center",
    "title_yanchor": "top",
    "title_xref": "paper",
    "xaxis": {"tickformat": "%b %d", "fixedrange": True},
    "yaxis": {"fixedrange": True},
    "showlegend": False,
    "margin": {"b": 0, "l": 0, "r": 0, "t": 30},
    "height": 300,
}

h_line_args = {
    "line_width": 1.5, 
    "line_dash": "dot", 
    "line_color": "rgb(55, 90, 127)",
}

arrow_args = {
    "xref": "x",
    "yref": "y",
    "axref": "x",
    "ayref": "y",
    "text": "",
    "arrowhead": 2,
    "arrowwidth": 1,
    "arrowside": "end+start",
    "arrowcolor": "white",
    "standoff": 5,
    "startstandoff": 5,
}

box_args = {
    "xref": "x",
    "yref": "y",
    "font": {"color": "white", "size": 12},
    "showarrow": False,
    "bordercolor": "white",
    "borderwidth": 1,
    "borderpad": 2,
    "bgcolor": "rgb(55, 90, 127)",
}


def get_bar_figure(names: pd.Series, gains: pd.Series) -> dcc.Graph:
    """ Return bar figure with top gainers of the last 24 hours. """
    figure = go.Figure(data=go.Bar(
        x=names,
        y=gains,
        marker_color="rgb(55, 90, 127)",
    ))

    args = copy.deepcopy(figure_args)
    args["xaxis"]["tickmode"] = "linear"
    args["height"] = 328

    figure.update_layout(
        title_text="Top Gainers (1D)",
        yaxis_tickformat = ".1%",
        **args,
    )

    return dcc.Graph(figure=figure, config={"displayModeBar": False})


def get_candlestick_figure(title: str, klines: pd.DataFrame) -> dcc.Graph:
    """ Create and return a candlestick chart using the passed kline data. """
    datetime = pd.to_datetime(klines.index, unit="s")
    
    figure = go.Figure(data=go.Candlestick(
        x=datetime,
        open=klines["open"], high=klines["high"], 
        low=klines["low"], close=klines["close"],
    ))
    figure.update_layout(
        title_text=title,
        xaxis_rangeslider_visible=False,
        hovermode=False,
        **figure_args,
    )

    # add EMAs
    for col in ["ema_12", "ema_21", "ema_50"]:
        if col in klines.columns:
            figure.add_scatter(x=datetime, y=klines[col], mode="lines")

    # required values for the chart annotations
    lowest_low = klines["low"].min()
    current_close = klines["close"].iloc[-1]
    timestamp_low = klines["low"][klines["low"] == lowest_low].index[0]
    datetime_low = pd.to_datetime(timestamp_low, unit="s")
    gain = (current_close / lowest_low - 1.) * 100.

    # horizontal lines that mark the price levels of the lowest low
    # and the current close
    figure.add_hline(y=lowest_low, **h_line_args)
    figure.add_hline(y=current_close, **h_line_args)

    # vertical arrow that visualizes the current gain
    figure.add_annotation(
        x=datetime_low,
        y=current_close,
        ax=datetime_low,
        ay=lowest_low,
        **arrow_args,
    )

    # annotation box containing the gain value
    figure.add_annotation(
        x=datetime_low,
        y=0.5 * (current_close + lowest_low),
        text="{:.1f}".format(gain) + "%",
        **box_args,
    )

    return dcc.Graph(figure=figure, config={"displayModeBar": False})
