import streamlit as st
import pandas as pd
import time
import requests
import os
from dotenv import load_dotenv

# ✅ Load tokens directly in streamlitapp.py
try:
    # Try to get tokens from Streamlit secrets
    BEARER_TOKENS = st.secrets["TWITTER_BEARER_TOKENS"].split(",")
    print("🔐 Tokens loaded from Streamlit secrets.")
except Exception:
    # Fallback to .env file
    load_dotenv()
    BEARER_TOKENS = os.getenv("TWITTER_BEARER_TOKENS", "").split(",")
    print("🔐 Tokens loaded from .env")

# Remove any empty tokens
BEARER_TOKENS = [token.strip() for token in BEARER_TOKENS if token.strip()]
MAX_REQUESTS = len(BEARER_TOKENS)

# Now import from app (after defining BEARER_TOKENS)
from app import get_tweets, save_to_csv, plot_sentiment_distribution

st.set_page_config(page_title="Twitter Stock Sentiment Analyzer", layout="centered")
st.title("📊 Twitter Stock Sentiment Analyzer")

# 🚫 Setup cooldown and usage tracking
COOLDOWN_MINUTES = 16

cooldown_key = "last_request_time"
request_count_key = "request_count"

# 🔍 Input fields
keyword = st.text_input("🔍 Enter keyword (e.g. 'Tesla'):")
tweet_limit = st.slider("🔢 Number of tweets to fetch", 10, 100, 50)

# Display token info
st.sidebar.info(f"🔑 Available tokens: {MAX_REQUESTS}")

# 🔁 Initialize session state
if cooldown_key not in st.session_state:
    st.session_state[cooldown_key] = 0
if request_count_key not in st.session_state:
    st.session_state[request_count_key] = 0

# 🔍 Run when button is clicked
if st.button("Analyze Sentiment"):
    now = time.time()
    last_time = st.session_state[cooldown_key]
    
    # Check if we're in cooldown period
    time_since_last = now - last_time
    wait_time = COOLDOWN_MINUTES * 60
    
    if time_since_last < wait_time and st.session_state[request_count_key] >= MAX_REQUESTS:
        remaining = int((wait_time - time_since_last) / 60)
        st.warning(f"⚠️ You've used all {MAX_REQUESTS} available requests. Please wait {remaining} more minutes before trying again.")
    elif not keyword:
        st.warning("⚠️ Please enter a keyword.")
    else:
        try:
            with st.spinner("Fetching and analyzing tweets..."):
                tweets = get_tweets(keyword, max_results=tweet_limit)
                if not tweets:
                    st.info("No tweets found. Try a different keyword.")
                else:
                    df = save_to_csv(tweets, f"{keyword}_tweets.csv")
                    
                    # Update request count
                    st.session_state[request_count_key] += 1
                    requests_left = MAX_REQUESTS - st.session_state[request_count_key]
                    
                    st.success(f"✅ Analyzed {len(df)} tweets. ({requests_left} requests left before cooldown)")
                    
                    # Show only first few rows to avoid clutter
                    st.dataframe(df[["text", "sentiment"]].head(), use_container_width=True)
                    
                    # Download option
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"{keyword}_tweets.csv",
                        mime="text/csv"
                    )

                    plot_sentiment_distribution(df, keyword)
                    st.image("sentiment_graph.png", caption="Sentiment Distribution", use_column_width=True)

                    # If all requests used, start cooldown timer
                    if st.session_state[request_count_key] >= MAX_REQUESTS:
                        st.session_state[cooldown_key] = time.time()
                        st.info(f"🎯 You've used all {MAX_REQUESTS} requests. Cooldown activated for {COOLDOWN_MINUTES} minutes.")

        except Exception as e:
            if "rate limit" in str(e).lower():
                # If rate limit hit, reset counter and start cooldown
                st.session_state[request_count_key] = MAX_REQUESTS
                st.session_state[cooldown_key] = time.time()
                st.error("❌ Rate limit reached. Starting cooldown period.")
            elif "401" in str(e):
                st.error("❌ Invalid API token. Please check your Twitter Bearer Tokens.")
            else:
                st.error(f"❌ Error: {e}")

# Display remaining requests
if st.session_state[request_count_key] < MAX_REQUESTS:
    requests_left = MAX_REQUESTS - st.session_state[request_count_key]
    st.sidebar.info(f"📊 Requests available: {requests_left}/{MAX_REQUESTS}")
else:
    now = time.time()
    last_time = st.session_state[cooldown_key]
    time_since_last = now - last_time
    wait_time = COOLDOWN_MINUTES * 60
    
    if time_since_last < wait_time:
        remaining = int((wait_time - time_since_last) / 60)
        st.sidebar.warning(f"⏰ Cooldown: {remaining} minutes left")
    else:
        # Reset counter if cooldown is over
        st.session_state[request_count_key] = 0
        st.sidebar.success("✅ Cooldown over! Requests refreshed.")