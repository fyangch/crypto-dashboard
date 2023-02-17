import pandas as pd
import plotly.graph_objects as go
from dash import dcc


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
        title_x=0.5,
        title_y=0.98,
        title_xanchor="center",
        title_yanchor="top",
        xaxis= {"tickformat": "%b %d", "fixedrange": True},
        yaxis= {"fixedrange": True},
        margin={"b": 0, "l": 0, "r": 0, "t": 30},
        height=300,
        hovermode=False,
        xaxis_rangeslider_visible=False,
    )

    return dcc.Graph(figure=figure, config={"displayModeBar": False})