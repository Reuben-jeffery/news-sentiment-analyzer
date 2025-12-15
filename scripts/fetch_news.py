import requests
import os
import sqlite3
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

if not API_KEY:
    raise ValueError("Missing NEWS_API_KEY in .env file")

BASE_URL = "https://newsapi.org/v2/everything"
DB_PATH = "data/news.db"

def fetch_articles(query="politics OR economy OR tech", page_size=20, pages=2):
    all_articles = []
    for page in range(1, pages + 1):
        params = {
            "q": query,
            "apiKey": API_KEY,
            "pageSize": page_size,
            "page": page,
            "language": "en",
            "sortBy": "publishedAt"
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code != 200 or "articles" not in data:
            print("Error fetching articles:", data.get("message", "Unknown error"))
            break

        articles = data["articles"]
        print(f"Fetched {len(articles)} articles from page {page}")
        all_articles.extend(articles)

    return all_articles

def store_articles(articles):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            source TEXT,
            published_at TEXT,
            content TEXT,
            sentiment TEXT,
            polarity REAL,
            subjectivity REAL
        )
    ''')

    count = 0
    for article in articles:
        content = article.get("content") or article.get("description") or ""
        if not content:
            continue

        cursor.execute('''
            INSERT INTO articles (title, source, published_at, content)
            VALUES (?, ?, ?, ?)
        ''', (
            article.get("title"),
            article.get("source", {}).get("name"),
            article.get("publishedAt"),
            content
        ))
        count += 1

    conn.commit()
    conn.close()
    print(f"Stored {count} articles.")

if __name__ == "__main__":
    articles = fetch_articles("climate change", page_size=20, pages=3)
    store_articles(articles)
