import requests
import xml.etree.ElementTree as ET
import sys
import os
from datetime import datetime

# Add the parent directory of 'app' to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from app.models
from app.models import Article

def zataz_scraper():
    url = 'http://feeds.feedburner.com/ZatazNews'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return []

    root = ET.fromstring(response.content)
    channel = root.find('channel')
    items = channel.findall('item')

    articles = []

    for item in items:
        try:
            title = item.find('title').text
            link = item.find('link').text
            pub_date = item.find('pubDate').text
            description = item.find('description').text

            date_obj = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
            uniform_date = date_obj.strftime("%Y-%m-%d")
            # Strip CDATA

            article = Article(
                title=title,
                url=link,
                summary=description,
                date=uniform_date,
                source='Zataz News',
                image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3xY-yZd8S7aCpgsZDOyk5vB2EzE1huDTa8A&s"
            )
            article.save_to_db()
            articles.append(article)
        except Exception as e:
            print(f"Error parsing article: {e}")

    return articles

if __name__ == "__main__":
    articles = zataz_scraper()
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Summary: {article.summary}")
        print(f"Date: {article.date}")
        print(f"Image: {article.image}")
        print("\n")
