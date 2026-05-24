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

## Features

- 📈 Real-time stock price and company info
- 📅 Historical OHLCV data with configurable time period
- 📊 Interactive charts- 📊 Interactive charts: line, candlestick, moving averages, and multi-ticker comparison: line, candlestick, and moving averages
- 🧮 Financial metrics: period high/low, average price, total return
- 📉 Technical indicators: SMA 20, SMA 50, daily returns
- 💾 Export data to CSV and generate text reports with --export

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

# Compare multiple tickers
python main.py AAPL MSFT TSLA --period 1y

# Comparison chart only
python main.py AAPL MSFT --chart compare
```
## Web Dashboard

Run the interactive Streamlit dashboard:

```bash
streamlit run app.py
```

Opens automatically at `http://localhost:8501`

Features:
- Sidebar controls for ticker, period and chart type
- Live metric cards with return indicators
- Interactive Plotly charts
- Collapsible raw data table
- Multi-ticker comparison chart

## Project Status
🚧 In active development — see commits for progress.