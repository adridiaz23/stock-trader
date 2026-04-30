# 📈 Stock Tracker

A Python application to track stock market data, visualize price history,
and analyze financial assets in real time.

> Built as a portfolio project to demonstrate clean, modular Python development
> in a financial context.

## Tech Stack
- Python 3.10+
- [yfinance](https://github.com/ranaroussi/yfinance) — market data
- pandas — data manipulation
- [Plotly](https://plotly.com/python/) — interactive charts

## Setup

```bash
git clone https://github.com/adridiaz23/stock-tracker.git
cd stock-tracker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Basic usage
python main.py AAPL

# Custom time period
python main.py MSFT --period 6mo

# Specific chart type
python main.py TSLA --period 1y --chart candlestick

# Available options
python main.py --help
```

## Project Status
🚧 In active development — see commits for progress.