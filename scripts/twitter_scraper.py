import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

def fetch_tweets(keywords):
    query = quote(' '.join(keywords))
    url = f'https://twitter.com/search?q={query}&src=typed_query&f=live'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Fetching URL: {url}")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    print("Page fetched successfully. Parsing tweets...")

    # Check the structure of the tweets
    tweets = soup.find_all('article')
    print(f"Found {len(tweets)} tweets.")

    articles = []
    for tweet in tweets:
        try:
            text_div = tweet.find('div', {'lang': True})
            if not text_div:
                continue
            text = text_div.text
            date = tweet.find('time')['datetime']
            author = tweet.find('a', {'href': re.compile(r'/[A-Za-z0-9_]+')}).get('href').strip('/')
            tweet_id = tweet.find('a', {'href': re.compile(r'/status/[0-9]+')}).get('href').split('/')[-1]
            url = f'https://twitter.com/{author}/status/{tweet_id}'

            article = {
                'title': text,
                'url': url,
                'source': 'Twitter',
                'summary': text[:140],
                'publish_date': date,
                'author': author,
                'keywords': ', '.join(keywords)
            }
            articles.append(article)
        except Exception as e:
            print(f"Error parsing tweet: {e}")

    return articles

if __name__ == "__main__":
    keywords = ['CTI', 'cyber threat intelligence']
    articles = fetch_tweets(keywords)
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Source: {article['source']}")
        print(f"Summary: {article['summary']}")
        print(f"Publish Date: {article['publish_date']}")
        print(f"Author: {article['author']}")
        print(f"Keywords: {article['keywords']}")
        print("\n")
