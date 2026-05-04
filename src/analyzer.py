"""
analyzer.py - Module responsible for calculating financial metrics.

This module takes raw OHLCV data and produces meaningful indicators
that help understand a stock's behavior over time.
All functions receive a DataFrame and return clean, ready-to-use data.
"""

import pandas as pd


def get_summary(df: pd.DataFrame, ticker: str) -> dict:
    """
    Calculate a summary of key metrics for the given period.

    Args:
        df: DataFrame returned by get_historical_data()
        ticker: Stock symbol, used for display purposes

    Returns:
        Dictionary with period high, low, average price and total return.
    """

    # .max() and .min() find the highest and lowest closing price in the period
    period_high = df["Close"].max()
    period_low = df["Close"].min()

    # .mean() calculates the average closing price across all trading days
    avg_price = df["Close"].mean()

    # Total return: how much the stock gained or lost during the period
    # Formula: (last price - first price) / first price * 100
    # .iloc[0] = first row, .iloc[-1] = last row
    first_price = df["Close"].iloc[0]
    last_price = df["Close"].iloc[-1]
    total_return = ((last_price - first_price) / first_price) * 100

    return {
        "ticker": ticker,
        "period_high": round(period_high, 2),
        "period_low": round(period_low, 2),
        "avg_price": round(avg_price, 2),
        "total_return": round(total_return, 2),
    }


def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add Simple Moving Average (SMA) columns to the DataFrame.

    A moving average smooths out price noise by averaging
    the closing price over a rolling window of N days.
    Traders use them to identify trends:
    - Price above SMA → bullish signal (uptrend)
    - Price below SMA → bearish signal (downtrend)

    Args:
        df: DataFrame returned by get_historical_data()

    Returns:
        The same DataFrame with two new columns: SMA_20 and SMA_50
    """

    # .rolling(window) creates a sliding window of N rows
    # .mean() then averages the Close price within that window
    # The first N-1 rows will be NaN because there's not enough data yet
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["SMA_50"] = df["Close"].rolling(window=50).mean()

    return df


def add_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a daily return percentage column to the DataFrame.

    Daily return = how much the stock moved (%) compared to the previous day.
    This is a fundamental metric in quantitative finance.

    Args:
        df: DataFrame returned by get_historical_data()

    Returns:
        The same DataFrame with a new column: Daily_Return
    """

    # .pct_change() calculates (current - previous) / previous for each row
    # * 100 converts it to percentage
    df["Daily_Return"] = df["Close"].pct_change() * 100

    return df