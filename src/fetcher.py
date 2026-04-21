"""
fetcher.py - Module responsible for retrieving stock market data.
"""

import yfinance as yf
import pandas as pd


def get_stock_info(ticker: str) -> dict:
    """
    Fetch basic information and current price for a given stock ticker.

    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'MSFT')

    Returns:
        Dictionary with stock name, symbol, and current price.

    Raises:
        ValueError: If the ticker is invalid or data is unavailable.
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    if not info or "currentPrice" not in info:
        raise ValueError(f"Could not retrieve data for ticker '{ticker}'.")

    return {
        "symbol": ticker.upper(),
        "name": info.get("longName", "N/A"),
        "current_price": info.get("currentPrice"),
        "currency": info.get("currency", "USD"),
        "market_cap": info.get("marketCap"),
    }


def get_historical_data(ticker: str, period: str = "1mo") -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a given stock.

    Args:
        ticker: Stock symbol (e.g., 'AAPL')
        period: Time period — valid values: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y

    Returns:
        DataFrame with columns: Open, High, Low, Close, Volume
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)

    if df.empty:
        raise ValueError(f"No historical data found for ticker '{ticker}'.")

    return df