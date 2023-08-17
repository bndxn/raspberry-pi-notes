import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import plotly
import plotly.express as px
import numpy as np


def overlapping_temperature_and_humidity(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"], y=df["temperature"], name="Temperature", mode="markers"
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"], y=df["humidity"], name="Humidity", mode="markers"
        ),
        secondary_y=True,
    )

    fig.update_layout(title_text="Temperature and humidity")

    # fig.update_layout(
    # autosize=True
    # )

    # Set x-axis title
    fig.update_xaxes(title_text="Time")

    # Set y-axes titles
    fig.update_yaxes(
        title_text="<b>Temperature</b>", title_font_color="blue", secondary_y=False
    )
    fig.update_yaxes(
        title_text="<b>Humidity</b>", title_font_color="red", secondary_y=True
    )

    return fig


def separate_temperature_and_humidity(df):
    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"], y=df["temperature"], name="Temperature", mode="markers"
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df["timestamp"], y=df["humidity"], name="Humidity", mode="markers"
        ),
        row=2,
        col=1,
    )

    fig.update_layout(autosize=True)

    return fig
