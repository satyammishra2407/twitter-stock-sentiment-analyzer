import streamlit as st
import pandas as pd
import time
from app import get_tweets, save_to_csv, plot_sentiment_distribution

st.set_page_config(page_title="Twitter Stock Sentiment Analyzer", layout="centered")
st.title("📊 Twitter Stock Sentiment Analyzer")

# 🚫 Setup cooldown
COOLDOWN_MINUTES = 16
cooldown_key = "last_request_time"

# 🔍 Input fields
keyword = st.text_input("🔍 Enter keyword (e.g. 'Tesla'):")
tweet_limit = st.slider("🔢 Number of tweets to fetch", 10, 100, 50)

# 🔁 Track session state
if cooldown_key not in st.session_state:
    st.session_state[cooldown_key] = 0

# 🔍 Run when button is clicked
if st.button("Analyze Sentiment"):
    now = time.time()
    last_time = st.session_state[cooldown_key]

    time_since_last = now - last_time
    wait_time = COOLDOWN_MINUTES * 60

    if time_since_last < wait_time:
        remaining = int((wait_time - time_since_last) / 60)
        st.warning(f"⚠️ Please wait {remaining} more minute(s) before trying again.")
    elif not keyword:
        st.warning("⚠️ Please enter a keyword.")
    else:
        try:
            tweets = get_tweets(keyword, max_results=tweet_limit)
            if not tweets:
                st.info("No tweets found. Try a different keyword.")
            else:
                df = save_to_csv(tweets, f"{keyword}_tweets.csv")
                st.success(f"✅ Analyzed {len(df)} tweets.")
                st.dataframe(df[["text", "sentiment"]], use_container_width=True)

                plot_sentiment_distribution(df, keyword)
                st.image("sentiment_graph.png", caption="Sentiment Distribution", use_column_width=True)

                # ✅ Save current request time
                st.session_state[cooldown_key] = time.time()

        except Exception as e:
            if "429" in str(e):  # Twitter API rate limit hit
                st.error("❌ Twitter API rate limit reached. Please wait and try again later.")
            else:
                st.error(f"❌ Error: {e}")
