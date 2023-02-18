import pandas as pd
import copy
import plotly.graph_objects as go
from dash import dcc


figure_args = {
    "title_x": 0.5,
    "title_y": 0.98,
    "title_xanchor": "center",
    "title_yanchor": "top",
    "xaxis": {"tickformat": "%b %d", "fixedrange": True},
    "yaxis": {"fixedrange": True},
    "margin": {"b": 0, "l": 0, "r": 0, "t": 30},
    "height": 300,
}

def get_bar_figure(names: pd.Series, gains: pd.Series):
    figure = go.Figure(data=go.Bar(
        x=names,
        y=gains,
        marker_color="rgb(55, 90, 127)",
    ))

    args = copy.deepcopy(figure_args)
    args["xaxis"]["tickmode"] = "linear"

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
    
    figure = go.Figure(data=go.Candlestick(
        x=pd.to_datetime(timestamp, unit="s"),
        open=open, high=high, low=low, close=close,
    ))
    figure.update_layout(
        title_text=title,
        xaxis_rangeslider_visible=False,
        hovermode=False,
        **figure_args,
    )

    return dcc.Graph(figure=figure, config={"displayModeBar": False})