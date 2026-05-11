"""
exporter.py - Module responsible for exporting data and reports.

In real financial applications, exporting data is essential
for auditing, sharing results, and further analysis in Excel or other tools.
"""

import os
from datetime import datetime

import pandas as pd


def export_to_csv(df: pd.DataFrame, ticker: str, period: str) -> str:
    """
    Export historical stock data to a CSV file.

    Args:
        df: DataFrame with historical data and calculated indicators
        ticker: Stock symbol, used for the filename
        period: Time period, used for the filename

    Returns:
        The path of the saved file as a string.
    """

    # Create an exports/ folder if it doesn't exist
    # exist_ok=True means it won't crash if the folder already exists
    os.makedirs("exports", exist_ok=True)

    # We include the date in the filename so exports don't overwrite each other
    # strftime formats a date — %Y%m%d produces e.g. "20240315"
    date_str = datetime.today().strftime("%Y%m%d")
    filename = f"exports/{ticker}_{period}_{date_str}.csv"

    # index=True keeps the date as a column in the CSV
    df.to_csv(filename, index=True)

    return filename


def export_report(summary: dict, ticker: str, period: str) -> str:
    """
    Export a plain text financial report with key metrics.

    Args:
        summary: Dictionary returned by get_summary()
        ticker: Stock symbol
        period: Time period analyzed

    Returns:
        The path of the saved file as a string.
    """

    os.makedirs("exports", exist_ok=True)

    date_str = datetime.today().strftime("%Y%m%d")
    filename = f"exports/{ticker}_{period}_{date_str}_report.txt"

    # Build the report as a multi-line string
    return_sign = "+" if summary["total_return"] > 0 else ""

    report = f"""
=====================================
  STOCK TRACKER — FINANCIAL REPORT
=====================================
Generated:      {datetime.today().strftime("%Y-%m-%d %H:%M")}
Ticker:         {ticker}
Period:         {period}

--- Key Metrics ---
Period High:    ${summary['period_high']}
Period Low:     ${summary['period_low']}
Average Price:  ${summary['avg_price']}
Total Return:   {return_sign}{summary['total_return']}%
=====================================
"""

    # Write the report to disk
    with open(filename, "w") as f:
        f.write(report)

    return filename