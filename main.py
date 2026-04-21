"""
main.py - Entry point for the Stock Tracker application.
"""

from src.fetcher import get_stock_info, get_historical_data


def main():
    ticker = "AAPL"

    print(f"\n📈 Fetching data for {ticker}...\n")

    # Current price
    info = get_stock_info(ticker)
    print(f"Company:       {info['name']}")
    print(f"Symbol:        {info['symbol']}")
    print(f"Current Price: {info['current_price']} {info['currency']}")

    # Historical data
    df = get_historical_data(ticker, period="1mo")
    print(f"\nHistorical data (last 5 rows):")
    print(df[["Open", "Close", "Volume"]].tail())


if __name__ == "__main__":
    main()