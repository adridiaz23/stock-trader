"""
main.py - Entry point for the Stock Tracker application.
"""

from src.fetcher import get_stock_info, get_historical_data

# Import our new visualizer functions
from src.visualizer import plot_price_history, plot_candlestick


def main():
    ticker = "AAPL"

    print(f"\n📈 Fetching data for {ticker}...\n")

    # --- Current price info ---
    info = get_stock_info(ticker)
    print(f"Company:       {info['name']}")
    print(f"Symbol:        {info['symbol']}")
    print(f"Current Price: {info['current_price']} {info['currency']}")

    # --- Historical data ---
    # We fetch 3 months now to make the charts more interesting
    df = get_historical_data(ticker, period="3mo")
    print(f"\nHistorical data (last 5 trading days):")
    print(df[["Open", "Close", "Volume"]].tail())

    # --- Charts ---
    # Each chart opens in a new browser tab
    print("\n📊 Opening charts...")
    plot_price_history(df, ticker)
    plot_candlestick(df, ticker)


if __name__ == "__main__":
    main()