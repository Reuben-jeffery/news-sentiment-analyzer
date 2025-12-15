import streamlit as st
import sqlite3
import pandas as pd
import subprocess

DB_PATH = "data/news.db"

def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM articles", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

def main():
    st.set_page_config(page_title="News Sentiment Analyzer", layout="wide")
    st.title("🧠 News Sentiment Analyzer")

    df = load_data()

    if df.empty:
        st.warning("No articles found in the database. Please run fetch_news.py first.")
        return

    # Sidebar filters
    st.sidebar.header("Filters")
    sentiment_options = df["sentiment"].dropna().unique().tolist()
    sentiment_filter = st.sidebar.multiselect(
        "Sentiment",
        options=sentiment_options,
        default=sentiment_options
    )
    keyword = st.sidebar.text_input("Search keyword")

    # Reset button
    if st.sidebar.button("Reset Filters"):
        sentiment_filter = sentiment_options
        keyword = ""

    # Apply filters
    filtered_df = df[df["sentiment"].isin(sentiment_filter)]
    if keyword:
        filtered_df = filtered_df[filtered_df["title"].str.contains(keyword, case=False, na=False)]

    st.subheader(f"Showing {len(filtered_df)} articles")
    st.dataframe(filtered_df[["title", "source", "published_at", "sentiment"]])

    if st.sidebar.button("🔄 Refresh News"):
        subprocess.run(["python", "scripts/fetch_news.py"])
        subprocess.run(["python", "scripts/analyze_sentiment.py"])
        st.experimental_rerun()
        
    if not filtered_df.empty:
        # Sentiment distribution
        st.subheader("📊 Sentiment Distribution")
        sentiment_counts = filtered_df["sentiment"].value_counts()
        st.bar_chart(sentiment_counts)

        # Polarity trend
        st.subheader("📈 Polarity Over Time")
        filtered_df["published_at"] = pd.to_datetime(filtered_df["published_at"], errors="coerce")
        polarity_trend = filtered_df.dropna(subset=["published_at"]).groupby(
            filtered_df["published_at"].dt.date)["polarity"].mean()
        polarity_trend = polarity_trend.sort_index()
        st.line_chart(polarity_trend)
    else:
        st.info("No data available for selected filters.")
        st.markdown("### 📰 Sample Article Preview")
        sample = df.iloc[0]
        st.write(f"**Title:** {sample['title']}")
        st.write(f"**Source:** {sample['source']}")
        st.write(f"**Published:** {sample['published_at']}")
        st.write(f"**Sentiment:** {sample['sentiment']}")
        st.write(f"**Content:** {sample['content'][:300]}...")

    st.markdown("---")
    st.caption("Built by Jeffery • Powered by Streamlit & TextBlob")

if __name__ == "__main__":
    main()
