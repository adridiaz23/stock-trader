"""
visualizer.py - Module responsible for generating stock charts.

We use Plotly because it produces interactive charts (zoom, hover, etc.)
which is standard in financial dashboards and looks much more
professional than static matplotlib charts.
"""

# plotly.graph_objects gives us full control over chart components
import plotly.graph_objects as go

# pandas is used for type hints — our functions receive DataFrames
import pandas as pd


def plot_price_history(df: pd.DataFrame, ticker: str) -> None:
    """
    Generate an interactive line chart showing closing price over time.

    Args:
        df: DataFrame returned by get_historical_data()
        ticker: Stock symbol, used for the chart title
    """

    # go.Figure is the main container — everything gets added to it
    fig = go.Figure()

    # go.Scatter draws a line chart
    # df.index contains the dates (it's the DataFrame's row index)
    # df["Close"] contains the closing price for each day
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",           # "lines" = line chart (vs "markers" = dots)
        name="Close Price",
        line=dict(color="#00b4d8", width=2)  # clean blue, standard in finance UIs
    ))

    # update_layout controls titles, axes labels, background, etc.
    fig.update_layout(
        title=f"{ticker} — Price History",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark",     # dark theme looks great for finance apps
        hovermode="x unified",      # shows all values when hovering a date
    )

    # .show() opens the chart in your browser automatically
    fig.show()


def plot_candlestick(df: pd.DataFrame, ticker: str) -> None:
    """
    Generate an interactive candlestick chart.

    Candlestick charts are the industry standard in finance —
    they show Open, High, Low and Close for each trading day,
    giving much more information than a simple line chart.

    Args:
        df: DataFrame returned by get_historical_data()
        ticker: Stock symbol, used for the chart title
    """

    fig = go.Figure()

    # go.Candlestick needs all four OHLC values per day
    # Green candle = price went up that day (Close > Open)
    # Red candle   = price went down that day (Close < Open)
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name=ticker
    ))

    fig.update_layout(
        title=f"{ticker} — Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        xaxis_rangeslider_visible=False,  # hides the range slider below (cleaner)
    )

    fig.show()


def plot_with_moving_averages(df: pd.DataFrame, ticker: str) -> None:
    """
    Generate a chart showing price history with SMA_20 and SMA_50 overlaid.

    Moving averages on a price chart is one of the most classic
    visualizations in technical analysis.

    Args:
        df: DataFrame with SMA_20 and SMA_50 columns (from analyzer.py)
        ticker: Stock symbol, used for the chart title
    """

    fig = go.Figure()

    # Main price line
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Close Price",
        line=dict(color="#00b4d8", width=2)
    ))

    # SMA 20 — short term trend (only plot if we have enough data)
    if "SMA_20" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["SMA_20"],
            mode="lines",
            name="SMA 20",
            line=dict(color="#f4a261", width=1.5, dash="dash")
        ))

    # SMA 50 — long term trend
    if "SMA_50" in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["SMA_50"],
            mode="lines",
            name="SMA 50",
            line=dict(color="#e76f51", width=1.5, dash="dot")
        ))

    fig.update_layout(
        title=f"{ticker} — Price with Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        hovermode="x unified",
    )

    fig.show()