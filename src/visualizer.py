"""
visualizer.py - Module responsible for generating stock charts.

We use Plotly because it produces interactive charts (zoom, hover, etc.)
which is standard in financial dashboards.

Design decision: all functions return a Figure object instead of calling
fig.show() directly. This makes them reusable in both the CLI (main.py)
and the Streamlit dashboard (app.py), where rendering works differently.
"""

import plotly.graph_objects as go
import pandas as pd


def build_line_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Build a line chart showing closing price over time.

    Args:
        df: DataFrame returned by get_historical_data()
        ticker: Stock symbol, used for the chart title

    Returns:
        A Plotly Figure object ready to be displayed.
    """

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Close Price",
        line=dict(color="#00b4d8", width=2)
    ))

    fig.update_layout(
        title=f"{ticker} — Price History",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        hovermode="x unified",
    )

    # We return the figure instead of calling fig.show()
    # The caller decides how to display it
    return fig


def build_candlestick_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Build a candlestick chart showing OHLC data per trading day.

    Candlestick charts are the industry standard in finance —
    green candle = price went up, red candle = price went down.

    Args:
        df: DataFrame returned by get_historical_data()
        ticker: Stock symbol, used for the chart title

    Returns:
        A Plotly Figure object ready to be displayed.
    """

    fig = go.Figure()

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
        xaxis_rangeslider_visible=False,
    )

    return fig


def build_sma_chart(df: pd.DataFrame, ticker: str) -> go.Figure:
    """
    Build a chart showing price history with SMA_20 and SMA_50 overlaid.

    Moving averages smooth out price noise and help identify trends.
    SMA 20 = short term, SMA 50 = long term.

    Args:
        df: DataFrame with SMA_20 and SMA_50 columns (from analyzer.py)
        ticker: Stock symbol, used for the chart title

    Returns:
        A Plotly Figure object ready to be displayed.
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

    # SMA 20 — short term trend
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

    return fig


def build_comparison_chart(normalized_df: pd.DataFrame, tickers: list) -> go.Figure:
    """
    Build a comparison chart for multiple tickers using normalized prices.

    Each ticker starts at 100 so performance is directly comparable
    regardless of absolute price differences.

    Args:
        normalized_df: DataFrame returned by get_normalized_prices()
        tickers: List of ticker symbols

    Returns:
        A Plotly Figure object ready to be displayed.
    """

    colors = ["#00b4d8", "#f4a261", "#2ecc71", "#e74c3c", "#9b59b6"]

    fig = go.Figure()

    for i, ticker in enumerate(tickers):
        color = colors[i % len(colors)]

        fig.add_trace(go.Scatter(
            x=normalized_df.index,
            y=normalized_df[ticker],
            mode="lines",
            name=ticker,
            line=dict(color=color, width=2)
        ))

    # Horizontal reference line at 100 (the starting point)
    # Stocks above 100 are up, below 100 are down
    fig.add_hline(
        y=100,
        line_dash="dash",
        line_color="gray",
        opacity=0.5
    )

    fig.update_layout(
        title="Stock Comparison — Normalized Performance (base 100)",
        xaxis_title="Date",
        yaxis_title="Normalized Price (base 100)",
        template="plotly_dark",
        hovermode="x unified",
    )

    return fig


# --- CLI convenience wrappers ---
# These functions exist only for main.py (the CLI version)
# They call the build_ functions and immediately show the result
# Streamlit never uses these — it calls the build_ functions directly

def plot_price_history(df: pd.DataFrame, ticker: str) -> None:
    """Build and immediately display a line chart (CLI use only)."""
    build_line_chart(df, ticker).show()


def plot_candlestick(df: pd.DataFrame, ticker: str) -> None:
    """Build and immediately display a candlestick chart (CLI use only)."""
    build_candlestick_chart(df, ticker).show()


def plot_with_moving_averages(df: pd.DataFrame, ticker: str) -> None:
    """Build and immediately display a moving averages chart (CLI use only)."""
    build_sma_chart(df, ticker).show()


def plot_comparison(normalized_df: pd.DataFrame, tickers: list) -> None:
    """Build and immediately display a comparison chart (CLI use only)."""
    build_comparison_chart(normalized_df, tickers).show()