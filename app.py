import requests
import csv
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import os

# ✅ Smart token loading (local + Streamlit Cloud)
try:
    import streamlit as st
    BEARER_TOKEN = st.secrets["TWITTER_BEARER_TOKEN"]
    print("🔐 Token loaded from Streamlit secrets.")
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    print("🔐 Token loaded from .env")

# ✅ Sentiment Analysis Function
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "Positive"
    elif polarity == 0:
        return "Neutral"
    else:
        return "Negative"

# ✅ Fetch Tweets from Twitter API
def get_tweets(query, max_results=50):
    print("📡 Fetching tweets...")
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    params = {
        "query": f"{query} lang:en -is:retweet",
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,text,lang"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"❌ Twitter API error: {response.status_code} - {response.text}")

    return response.json().get("data", [])

# ✅ Save to CSV and Remove Duplicates
def save_to_csv(tweets, filename):
    print(f"💾 Saving to '{filename}'...")
    df = pd.DataFrame(tweets)
    df.drop_duplicates(subset="text", inplace=True)
    df["sentiment"] = df["text"].apply(analyze_sentiment)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"✅ Saved {len(df)} unique tweets to '{filename}'")
    return df

# ✅ Plot Sentiment Graph
def plot_sentiment_distribution(df, keyword):
    sentiment_counts = df["sentiment"].value_counts()
    colors = {"Positive": "green", "Negative": "red", "Neutral": "gray"}

    plt.figure(figsize=(6, 4))
    sentiment_counts.plot(kind="bar", color=[colors.get(i, "blue") for i in sentiment_counts.index])
    plt.title(f"Sentiment Distribution for '{keyword}'")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Tweets")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("sentiment_graph.png")
    plt.show()
    print("📊 Graph saved as 'sentiment_graph.png' and displayed.")

# ✅ Main (optional: only used when running locally as CLI)
print("📂 File loaded...")
if __name__ == "__main__":
    print("🔥 Sentiment Analyzer Script")
    try:
        keyword = input("🔍 Enter a keyword to search on Twitter: ")
        tweet_limit = int(input("🔢 How many tweets to analyze (max 100): "))

        tweets = get_tweets(keyword, max_results=tweet_limit)
        print(f"✅ {len(tweets)} tweets fetched.")

        filename = f"{keyword}_tweets.csv"
        df = save_to_csv(tweets, filename)

        plot_sentiment_distribution(df, keyword)

    except Exception as e:
        print(f"❌ Error: {e}")
