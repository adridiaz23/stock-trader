"""
main.py - Entry point for the Stock Tracker application.
"""

# argparse is a built-in Python library for handling command-line arguments
# No need to install it — it comes with Python
import argparse

from src.fetcher import get_stock_info, get_historical_data
from src.visualizer import plot_price_history, plot_candlestick


def parse_args():
    """
    Define and parse command-line arguments.

    This keeps argument logic separate from the main business logic,
    which is cleaner and easier to test.
    """

    # ArgumentParser is the main object that manages our CLI arguments
    parser = argparse.ArgumentParser(
        description="Stock Tracker — fetch and visualize stock market data."
    )

    # First argument: the stock ticker (required)
    # It's positional — the user just writes it after the script name
    parser.add_argument(
        "ticker",
        type=str,
        help="Stock ticker symbol (e.g. AAPL, MSFT, TSLA)"
    )

    # Second argument: the time period (optional, defaults to 3mo)
    # It's optional — the user can omit it and get the default
    parser.add_argument(
        "--period",
        type=str,
        default="3mo",
        choices=["1mo", "3mo", "6mo", "1y", "2y"],  # only valid values allowed
        help="Historical data period (default: 3mo)"
    )

    # Third argument: which chart to show (optional, defaults to both)
    parser.add_argument(
        "--chart",
        type=str,
        default="both",
        choices=["line", "candlestick", "both"],
        help="Chart type to display (default: both)"
    )

    return parser.parse_args()


def main():
    # Parse the arguments the user passed in the terminal
    args = parse_args()

    # Now ticker comes from the user, not hardcoded
    ticker = args.ticker.upper()

    print(f"\n📈 Fetching data for {ticker}...\n")

    # --- Current price info ---
    info = get_stock_info(ticker)
    print(f"Company:       {info['name']}")
    print(f"Symbol:        {info['symbol']}")
    print(f"Current Price: {info['current_price']} {info['currency']}")

    # --- Historical data ---
    # period also comes from the user now
    df = get_historical_data(ticker, period=args.period)
    print(f"\nHistorical data (last 5 trading days):")
    print(df[["Open", "Close", "Volume"]].tail())

    # --- Charts ---
    # We show only what the user asked for
    print("\n📊 Opening charts...")

    if args.chart in ("line", "both"):
        plot_price_history(df, ticker)

    if args.chart in ("candlestick", "both"):
        plot_candlestick(df, ticker)


if __name__ == "__main__":
    main()