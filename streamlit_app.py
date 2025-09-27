# streamlit_app.py
import streamlit as st
from dotenv import load_dotenv
import os

# Load tokens (Streamlit secrets > .env)
try:
    BEARER_TOKENS = st.secrets["TWITTER_BEARER_TOKENS"].split(",")
except Exception:
    load_dotenv()
    tokens = os.getenv("TWITTER_BEARER_TOKENS", "")
    BEARER_TOKENS = tokens.split(",") if tokens else []

BEARER_TOKENS = [t.strip() for t in BEARER_TOKENS if t.strip()]
MAX_REQUESTS = len(BEARER_TOKENS)

# Import pages
import home, live_dashboard, twitter_sentiment, expert_analysis, smart_insights

st.set_page_config(page_title="Stock Analysis Hub", layout="wide", page_icon="📊")

# Sidebar
st.sidebar.title("📊 Stock Analysis Hub")
company = st.sidebar.text_input("🔍 Enter Company Symbol", "INFY").upper()
time_period = st.sidebar.selectbox("📅 Time Period", ["Last 7 Days", "1 Month", "3 Months", "6 Months", "1 Year"])
selection = st.sidebar.radio("Navigate to:", ["🏠 Home", "📈 Live Dashboard", "🐦 Twitter Sentiment", "📰 Expert Analysis", "💡 Smart Insights"])
st.sidebar.info(f"🔑 Available tokens: {MAX_REQUESTS}")

# Session state init
if "last_request_time" not in st.session_state:
    st.session_state["last_request_time"] = 0
if "request_count" not in st.session_state:
    st.session_state["request_count"] = 0

# Router
PAGES = {
    "🏠 Home": home,
    "📈 Live Dashboard": live_dashboard,
    "🐦 Twitter Sentiment": twitter_sentiment,
    "📰 Expert Analysis": expert_analysis,
    "💡 Smart Insights": smart_insights,
}

page_module = PAGES[selection]
page_module.show_page(company=company, bearer_tokens=BEARER_TOKENS, max_requests=MAX_REQUESTS)
