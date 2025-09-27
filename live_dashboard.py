# live_dashboard.py
import streamlit as st
from utils import get_stock_data

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("📈 Live Stock Price")
    if not company:
        st.warning("Enter a company symbol in sidebar.")
        return

    stock_data = get_stock_data(company)
    if stock_data:
        st.metric(
            label=f"{company} Current Price",
            value=f"{stock_data['currency']}{stock_data['current_price']}",
            delta=f"{stock_data['change']} ({stock_data['change_percent']}%)"
        )
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Previous Close:** {stock_data['currency']}{stock_data['previous_close']}")
        with col2:
            st.info(f"**Change:** {stock_data['currency']}{stock_data['change']}")
    else:
        st.warning("Could not fetch stock data. Try tickers like INFY, TCS, TSLA, AAPL.")

    # Financial Metrics placeholders (replace with dynamic calls if available)
    st.subheader("📊 Financial Metrics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue", "3.62M", "-137.96%", delta_color="inverse")
    c2.metric("Gross Profit", "1.48M", "-213.4%", delta_color="inverse")
    c3.metric("Net Profit", "0.57M", "-263.16%", delta_color="inverse")
    c4.metric("Sentiment Score", "72%", "+8%")

    st.subheader("📊 Performance Charts")
    st.info("Charts placeholder — integrate with fundamentals API if available.")
