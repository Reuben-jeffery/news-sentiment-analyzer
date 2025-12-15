News Sentiment Analyzer
A Streamlit-powered dashboard that fetches the latest news, analyzes sentiment using TextBlob, and visualizes trends over time. Built with Python, SQLite, and NewsAPI.

Overview
The News Sentiment Analyzer helps you track how the media is talking about topics like politics, economy, technology, or climate change. It:

Fetches articles from NewsAPI

Stores them in a local SQLite database

Runs sentiment analysis (Positive, Neutral, Negative)

Displays interactive charts and filters in a Streamlit dashboard

Tech Stack
Python 3.10+

Streamlit – interactive dashboard

SQLite – local database

TextBlob – sentiment analysis

NewsAPI – news data source

Pandas – data manipulation

Setup Instructions
1. Clone the repository
bash
git clone https://github.com/<your-username>/news-sentiment-analyzer.git
cd news-sentiment-analyzer

2. Create a virtual environment
bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install dependencies
bash
pip install -r requirements.txt

4. Add your NewsAPI key
Create a .env file in the project root:

Code
NEWS_API_KEY=your_api_key_here

Usage
Fetch latest articles
bash
python scripts/fetch_news.py
Run sentiment analysis
bash
python scripts/analyze_sentiment.py
Launch the dashboard
bash
streamlit run dashboard/app.py
Open your browser at http://localhost:8501.

Features
Sidebar filters for sentiment and keywords

Interactive sentiment distribution chart

Polarity trend line chart over time

Reset filters button

Sample article preview when no matches are found

Deployment
You can deploy this project online using Streamlit Community Cloud:

Push your code to GitHub.

Go to Streamlit Cloud.

Connect your repo and select dashboard/app.py as the entry point.

Add your NEWS_API_KEY in Secrets Manager.

Deploy and share your public app link.

Future Improvements
Topic selection dropdown in dashboard

Automatic refresh with scheduled jobs

Export filtered articles to CSV

Advanced sentiment models (VADER, Hugging Face)

Cloud deployment with Render/Heroku

Author
Built by CodeRonin • Powered by Streamlit & TextBlob