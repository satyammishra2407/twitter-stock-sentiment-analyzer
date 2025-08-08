import streamlit as st
import pandas as pd
from app import get_tweets, save_to_csv, plot_sentiment_distribution  # Reuse functions from app.py

st.title("📊 Twitter Stock Sentiment Analyzer")

keyword = st.text_input("🔍 Enter keyword (e.g. 'Tesla'):")
tweet_limit = st.slider("🔢 Number of tweets to fetch", 10, 100, 50)

if st.button("Analyze Sentiment"):
    if not keyword:
        st.warning("Please enter a keyword.")
    else:
        try:
            tweets = get_tweets(keyword, max_results=tweet_limit)
            df = save_to_csv(tweets, f"{keyword}_tweets.csv")
            
            st.success(f"✅ Analyzed {len(df)} tweets.")
            st.dataframe(df[["text", "sentiment"]])

            # Plot sentiment
            plot_sentiment_distribution(df, keyword)
            st.image("sentiment_graph.png")

        except Exception as e:
            st.error(f"❌ Error: {e}")
