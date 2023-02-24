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


def get_candlestick_figure(
    title: str,
    timestamp: pd.Series,
    open: pd.Series,
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    ) -> dcc.Graph:
    """ Create and return a candlestick chart using the passed kline data. """
    datetime = pd.to_datetime(timestamp, unit="s")
    
    figure = go.Figure(data=go.Candlestick(
        x=datetime,
        open=open, high=high, low=low, close=close,
    ))
    figure.update_layout(
        title_text=title,
        xaxis_rangeslider_visible=False,
        hovermode=False,
        **figure_args,
    )

    # required values for the chart annotations
    lowest_low = low.min()
    current_close = close.iloc[-1]
    index = low[low == lowest_low].index[0]
    gain = (current_close / lowest_low - 1.) * 100.

    # horizontal lines that mark the price levels of the lowest low
    # and the current close
    figure.add_hline(y=lowest_low, **h_line_args)
    figure.add_hline(y=current_close, **h_line_args)

    # vertical arrow that visualizes the current gain
    figure.add_annotation(
        x=datetime[index],
        y=current_close,
        ax=datetime[index],
        ay=lowest_low,
        **arrow_args,
    )

    # annotation box containing the gain value
    figure.add_annotation(
        x=datetime[index],
        y=0.5 * (current_close + lowest_low),
        text="{:.1f}".format(gain) + "%",
        **box_args,
    )

    return dcc.Graph(figure=figure, config={"displayModeBar": False})
