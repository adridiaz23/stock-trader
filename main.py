"""
main.py - Entry point for the Stock Tracker application.
"""

import argparse

from src.fetcher import get_stock_info, get_historical_data
from src.visualizer import (
    plot_price_history,
    plot_candlestick,
    plot_with_moving_averages,
    plot_comparison,
)
from src.analyzer import (
    get_summary,
    add_moving_averages,
    add_daily_returns,
    get_normalized_prices,
)
from src.exporter import export_to_csv, export_report


def parse_args():
    parser = argparse.ArgumentParser(
        description="Stock Tracker — fetch and visualize stock market data."
    )

    # nargs="+" means one or more values — this enables multiple tickers
    # e.g. python main.py AAPL MSFT TSLA
    parser.add_argument(
        "tickers",
        type=str,
        nargs="+",
        help="One or more stock ticker symbols (e.g. AAPL MSFT TSLA)"
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
        choices=["line", "candlestick", "sma", "both", "compare"],
        help="Chart type to display (default: both)"
    )
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export data to CSV and generate a text report"
    )
    return parser.parse_args()


def print_summary(summary: dict) -> None:
    """Print a formatted summary of financial metrics."""
    return_sign = "+" if summary["total_return"] > 0 else ""

    print(f"\n📊 Period Summary — {summary['ticker']}")
    print(f"{'─' * 30}")
    print(f"Period High:    ${summary['period_high']}")
    print(f"Period Low:     ${summary['period_low']}")
    print(f"Average Price:  ${summary['avg_price']}")
    print(f"Total Return:   {return_sign}{summary['total_return']}%")
    print(f"{'─' * 30}")


def main():
    args = parse_args()

    # Normalize all tickers to uppercase
    tickers = [t.upper() for t in args.tickers]

    # We store each ticker's DataFrame here for the comparison chart
    tickers_data = {}

    for ticker in tickers:
        print(f"\n📈 Fetching data for {ticker}...\n")

        # --- Current price info ---
        info = get_stock_info(ticker)
        print(f"Company:       {info['name']}")
        print(f"Symbol:        {info['symbol']}")
        print(f"Current Price: {info['current_price']} {info['currency']}")

        # --- Historical data ---
        df = get_historical_data(ticker, period=args.period)

        # --- Analysis ---
        df = add_moving_averages(df)
        df = add_daily_returns(df)

        summary = get_summary(df, ticker)
        print_summary(summary)

        # Store for comparison chart later
        tickers_data[ticker] = df

        # --- Export (only if --export flag is passed) ---
        if args.export:
            csv_path = export_to_csv(df, ticker, args.period)
            report_path = export_report(summary, ticker, args.period)
            print(f"\n💾 Data exported to:   {csv_path}")
            print(f"📄 Report saved to:    {report_path}")

        # --- Single ticker charts ---
        # These only make sense for one ticker at a time
        if len(tickers) == 1:
            print("\n📊 Opening charts...")

            if args.chart in ("line", "both"):
                plot_price_history(df, ticker)

            if args.chart in ("candlestick", "both"):
                plot_candlestick(df, ticker)

            if args.chart in ("sma", "both"):
                plot_with_moving_averages(df, ticker)

    # --- Comparison chart (only when multiple tickers or --chart compare) ---
    if len(tickers) > 1 or args.chart == "compare":
        print("\n📊 Opening comparison chart...")
        normalized_df = get_normalized_prices(tickers_data)
        plot_comparison(normalized_df, tickers)


if __name__ == "__main__":
    main()