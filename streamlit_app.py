import streamlit as st
import pandas as pd
from app import get_tweets, save_to_csv, plot_sentiment_distribution

st.set_page_config(page_title="Twitter Stock Sentiment Analyzer", layout="centered")
st.title("📊 Twitter Stock Sentiment Analyzer")

# 🔍 Input fields
keyword = st.text_input("🔍 Enter keyword (e.g. 'Tesla'):")
tweet_limit = st.slider("🔢 Number of tweets to fetch", 10, 100, 50)

# 🔍 Run when button is clicked
if st.button("Analyze Sentiment"):
    if not keyword:
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
        except Exception as e:
            st.error(f"❌ Error: {e}")
