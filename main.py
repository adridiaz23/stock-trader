"""
main.py - Entry point for the Stock Tracker application.
"""

import argparse

from src.fetcher import get_stock_info, get_historical_data
from src.visualizer import plot_price_history, plot_candlestick, plot_with_moving_averages

# Import our new analyzer functions
from src.analyzer import get_summary, add_moving_averages, add_daily_returns


def parse_args():
    parser = argparse.ArgumentParser(
        description="Stock Tracker — fetch and visualize stock market data."
    )
    parser.add_argument(
        "ticker",
        type=str,
        help="Stock ticker symbol (e.g. AAPL, MSFT, TSLA)"
    )
    parser.add_argument(
        "--period",
        type=str,
        default="3mo",
        choices=["1mo", "3mo", "6mo", "1y", "2y"],
        help="Historical data period (default: 3mo)"
    )
    parser.add_argument(
        "--chart",
        type=str,
        default="both",
        choices=["line", "candlestick", "sma", "both"],
        help="Chart type to display (default: both)"
    )
    return parser.parse_args()


def print_summary(summary: dict) -> None:
    """Print a formatted summary of financial metrics."""

    # "+" before a number adds a + sign for positive values
    # This is standard in financial displays
    return_sign = "+" if summary["total_return"] > 0 else ""

    print(f"\n📊 Period Summary")
    print(f"{'─' * 30}")
    print(f"Period High:    ${summary['period_high']}")
    print(f"Period Low:     ${summary['period_low']}")
    print(f"Average Price:  ${summary['avg_price']}")
    print(f"Total Return:   {return_sign}{summary['total_return']}%")
    print(f"{'─' * 30}")


def main():
    args = parse_args()
    ticker = args.ticker.upper()

    print(f"\n📈 Fetching data for {ticker}...\n")

    # --- Current price info ---
    info = get_stock_info(ticker)
    print(f"Company:       {info['name']}")
    print(f"Symbol:        {info['symbol']}")
    print(f"Current Price: {info['current_price']} {info['currency']}")

    # --- Historical data ---
    df = get_historical_data(ticker, period=args.period)

    # --- Analysis ---
    # We enrich the DataFrame with calculated columns before displaying
    df = add_moving_averages(df)
    df = add_daily_returns(df)

    # Print the financial summary
    summary = get_summary(df, ticker)
    print_summary(summary)

    print(f"\nLast 5 trading days:")
    print(df[["Close", "SMA_20", "Daily_Return"]].tail().round(2))

    # --- Charts ---
    print("\n📊 Opening charts...")

    if args.chart in ("line", "both"):
        plot_price_history(df, ticker)

    if args.chart in ("candlestick", "both"):
        plot_candlestick(df, ticker)

    if args.chart in ("sma", "both"):
        plot_with_moving_averages(df, ticker)


if __name__ == "__main__":
    main()