import requests
import csv
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
import os
import time
import random

# ✅ Smart token loading (local + Streamlit Cloud)
try:
    import streamlit as st
    BEARER_TOKENS = st.secrets["TWITTER_BEARER_TOKENS"].split(",")
    print("🔐 Tokens loaded from Streamlit secrets.")
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    BEARER_TOKENS = os.getenv("TWITTER_BEARER_TOKENS", "").split(",")
    print("🔐 Tokens loaded from .env")

# Remove any empty tokens
BEARER_TOKENS = [token.strip() for token in BEARER_TOKENS if token.strip()]
current_token_index = 0
token_cooldown = {}  # Track when tokens can be used again

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

# ✅ Get current active token
def get_current_token():
    global current_token_index
    
    # Check if current token is in cooldown
    current_token = BEARER_TOKENS[current_token_index]
    if current_token in token_cooldown and token_cooldown[current_token] > time.time():
        # Find next available token
        for i in range(len(BEARER_TOKENS)):
            next_index = (current_token_index + i) % len(BEARER_TOKENS)
            next_token = BEARER_TOKENS[next_index]
            if next_token not in token_cooldown or token_cooldown[next_token] <= time.time():
                current_token_index = next_index
                return next_token
        
        # If all tokens are in cooldown, use the one with shortest cooldown
        soonest_token = min(token_cooldown.keys(), key=lambda k: token_cooldown[k])
        return soonest_token
    
    return current_token

# ✅ Fetch Tweets from Twitter API with token rotation
def get_tweets(query, max_results=50):
    global current_token_index  # Yahan global declare karo
    print("📡 Fetching tweets...")
    url = "https://api.twitter.com/2/tweets/search/recent"
    
    # Get current token
    bearer_token = get_current_token()
    print(f"Using token index: {current_token_index}")
    
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    params = {
        "query": f"{query} lang:en -is:retweet",
        "max_results": min(max_results, 100),
        "tweet.fields": "created_at,text,lang"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        
        # Check for rate limit
        if response.status_code == 429:
            print(f"❌ Rate limit hit for token {current_token_index}")
            # Set cooldown for this token (15 minutes)
            token_cooldown[bearer_token] = time.time() + 900  # 15 minutes
            raise Exception(f"❌ Twitter API rate limit reached. Token {current_token_index} on cooldown.")
        
        if response.status_code != 200:
            raise Exception(f"❌ Twitter API error: {response.status_code} - {response.text}")

        return response.json().get("data", [])
    
    except Exception as e:
        if "rate limit" in str(e).lower():
            # Rotate to next token
            current_token_index = (current_token_index + 1) % len(BEARER_TOKENS)
            print(f"Rotating to token index: {current_token_index}")
            
            # Try again with new token after short delay
            time.sleep(1)
            return get_tweets(query, max_results)
        else:
            raise e

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
    plt.close()  # Close to prevent memory issues
    print("📊 Graph saved as 'sentiment_graph.png'")

# ✅ Main (optional: only used when running locally as CLI)
print("📂 File loaded...")
if __name__ == "__main__":
    print("🔥 Sentiment Analyzer Script")
    print(f"Available tokens: {len(BEARER_TOKENS)}")
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