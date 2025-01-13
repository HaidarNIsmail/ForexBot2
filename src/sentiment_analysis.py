import os
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
SEARCH_TERM = "forex"  # You can change this to any topic you want to analyze


def fetch_news(api_key, query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data['articles']


def analyze_sentiment(articles):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_data = []

    for article in articles:
        title = article['title']
        text = article['description'] if article['description'] else ''
        sentiment_score = analyzer.polarity_scores(text)['compound']
        sentiment_data.append({"title": title, "sentiment_score": sentiment_score})

    return pd.DataFrame(sentiment_data)


def main():
    if not NEWS_API_KEY:
        raise Exception("API key for NewsAPI is not set. Please configure it in your environment variables.")

    print("Fetching news articles for:", SEARCH_TERM)
    articles = fetch_news(NEWS_API_KEY, SEARCH_TERM)
    print("Analyzing sentiment for", len(articles), "articles...")
    sentiment_df = analyze_sentiment(articles)

    sentiment_df.to_csv('C:/Users/haida/PycharmProjects/ForexBot2/data/news_sentiment_results.csv', index=False)
    print("Sentiment analysis results saved to 'news_sentiment_results.csv'.")


if __name__ == "__main__":
    main()


