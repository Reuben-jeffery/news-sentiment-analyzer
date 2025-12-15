from textblob import TextBlob
import sqlite3

DB_PATH = "data/news.db"

def analyze_sentiment():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, content FROM articles WHERE sentiment IS NULL")
    rows = cursor.fetchall()

    for article_id, content in rows:
        blob = TextBlob(content)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        cursor.execute('''
            UPDATE articles
            SET sentiment = ?, polarity = ?, subjectivity = ?
            WHERE id = ?
        ''', (sentiment, polarity, subjectivity, article_id))

    conn.commit()
    conn.close()
    print(f"Analyzed {len(rows)} articles.")

if __name__ == "__main__":
    analyze_sentiment()
