# smart_insights.py
import streamlit as st

def show_page(company=None, bearer_tokens=None, max_requests=None):
    st.subheader("💡 Smart Insights")
    insights = [
        "Public sentiment increased by 15% over the last week",
        "Negative news correlation detected with recent price movement",
        "Twitter sentiment predicts ~78% accuracy for next-day direction (mock)",
        "Volume spike detected near earnings",
        "Retail buzz suggests increased interest"
    ]
    for i in insights:
        st.success(f"• {i}")

    st.header("📊 Performance Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Sentiment Accuracy", "78%", "+5%")
    c2.metric("News Correlation", "0.82", "+0.10")
    c3.metric("Prediction Score", "A-", "Stable")
