"""
app.py - Streamlit web dashboard for Stock Tracker.

Streamlit works by re-running this entire script from top to bottom
every time the user interacts with a widget. This is important to
understand: there are no event listeners or callbacks — just a
full re-run on every interaction.

Run with:
    streamlit run app.py
"""

import streamlit as st

from src.fetcher import get_stock_info, get_historical_data
from src.analyzer import (
    get_summary,
    add_moving_averages,
    add_daily_returns,
    get_normalized_prices,
)
from src.visualizer import (
    build_line_chart,
    build_candlestick_chart,
    build_sma_chart,
    build_comparison_chart,
)

# --- Page config ---
# Must be the first Streamlit call in the script — always
st.set_page_config(
    page_title="Stock Tracker",
    page_icon="📈",
    layout="wide",
)


# --- Caching ---
# @st.cache_data caches the return value of this function
# If called again with the same arguments, it returns the cached result
# without hitting the API again — faster and avoids rate limits
@st.cache_data
def load_stock_data(ticker: str, period: str):
    """
    Fetch and process stock data with caching.

    Args:
        ticker: Stock symbol
        period: Time period string

    Returns:
        Tuple of (info dict, processed DataFrame, summary dict)
    """
    info = get_stock_info(ticker)
    df = get_historical_data(ticker, period=period)

    # Enrich the DataFrame with calculated indicators
    df = add_moving_averages(df)
    df = add_daily_returns(df)

    summary = get_summary(df, ticker)
    return info, df, summary


# --- Sidebar ---
# st.sidebar makes everything inside appear in the left panel
with st.sidebar:
    st.title("📈 Stock Tracker")
    st.markdown("---")

    # Text input — user types tickers separated by commas
    tickers_input = st.text_input(
        label="Tickers (comma separated)",
        value="AAPL",
        placeholder="AAPL, MSFT, TSLA",
        help="Enter one or more stock symbols separated by commas"
    )

    # Selectbox = dropdown menu
    period = st.selectbox(
        label="Time Period",
        options=["1mo", "3mo", "6mo", "1y", "2y"],
        index=2,        # default to index 2 = "6mo"
    )

    chart_type = st.selectbox(
        label="Chart Type",
        options=["Line", "Candlestick", "Moving Averages", "Comparison"],
    )

    st.markdown("---")
    st.caption("Data provided by Yahoo Finance")


# --- Parse tickers ---
# Clean the raw input into a proper list
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

if not tickers:
    # st.warning shows a yellow warning box
    # st.stop() halts execution — nothing below this runs
    st.warning("Please enter at least one ticker symbol.")
    st.stop()


# --- Page title ---
st.title("Stock Market Dashboard")
st.markdown(f"**Period:** {period} &nbsp;|&nbsp; **Chart:** {chart_type}")
st.markdown("---")


# --- Main loop: one section per ticker ---
for ticker in tickers:

    # st.spinner shows an animated loading message while the block runs
    with st.spinner(f"Loading {ticker}..."):
        try:
            info, df, summary = load_stock_data(ticker, period)
        except ValueError as e:
            # st.error shows a red error box and we skip this ticker
            st.error(f"Could not load **{ticker}**: {e}")
            continue

    # --- Company header ---
    st.subheader(f"{info['name']} ({ticker})")

    # --- Metric cards ---
    # st.columns(4) creates 4 equal columns side by side
    col1, col2, col3, col4 = st.columns(4)

    return_sign = "+" if summary["total_return"] > 0 else ""
    return_value = f"{return_sign}{summary['total_return']}%"

    # st.metric renders a big number with a label
    # The delta parameter adds a colored arrow (green/red automatically)
    col1.metric(
        label="Current Price",
        value=f"${info['current_price']}",
    )
    col2.metric(
        label=f"Total Return ({period})",
        value=return_value,
        delta=return_value,
    )
    col3.metric(
        label="Period High",
        value=f"${summary['period_high']}",
    )
    col4.metric(
        label="Period Low",
        value=f"${summary['period_low']}",
    )

    # --- Chart ---
    # We only show the comparison chart when there are multiple tickers
    if chart_type == "Comparison" and len(tickers) == 1:
        st.info("Add more tickers to use the Comparison chart.")
    elif chart_type != "Comparison":
        # Build the right figure based on chart_type selection
        if chart_type == "Line":
            fig = build_line_chart(df, ticker)
        elif chart_type == "Candlestick":
            fig = build_candlestick_chart(df, ticker)
        elif chart_type == "Moving Averages":
            fig = build_sma_chart(df, ticker)

        # st.plotly_chart renders a Plotly figure inside the dashboard
        # use_container_width=True makes it fill the available width
        st.plotly_chart(fig, use_container_width=True)

    # --- Raw data table (collapsible) ---
    # st.expander creates a section the user can open and close
    with st.expander(f"📄 Raw data — {ticker}"):
        st.dataframe(
            df[["Open", "High", "Low", "Close", "Volume", "SMA_20", "SMA_50", "Daily_Return"]].round(2),
            use_container_width=True,
        )

    st.markdown("---")


# --- Comparison chart ---
# Only shown when multiple tickers AND user selected Comparison
if len(tickers) > 1 and chart_type == "Comparison":
    st.subheader("📊 Normalized Performance Comparison")
    st.caption("All tickers normalized to 100 at the start of the period.")

    # Load DataFrames for all tickers (already cached, no extra API calls)
    tickers_data = {}
    for ticker in tickers:
        try:
            _, df, _ = load_stock_data(ticker, period)
            tickers_data[ticker] = df
        except ValueError:
            continue

    if tickers_data:
        normalized_df = get_normalized_prices(tickers_data)
        fig = build_comparison_chart(normalized_df, tickers)
        st.plotly_chart(fig, use_container_width=True)