import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import sys
import os
import re

# Add the parent directory of 'app' to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from app.models
from app.models import Article

# Function to check if an image URL is reachable
def is_image_url_valid(image_url):
    try:
        response = requests.head(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        return response.status_code == 200
    except requests.RequestException:
        return False

def trendmicro_scraper(limit=50):
    url = 'http://feed.informer.com/digests/G5HRN3DTV4/feeder'
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

    default_image_url = 'https://logowik.com/content/uploads/images/trend-micro7815.logowik.com.webp'

    for item in items[:limit]:
        try:
            title = item.find('title').text.strip()
            link = item.find('link').text.strip()
            pub_date = item.find('pubDate').text.strip()
            description = item.find('description').text.strip()
            enclosure = item.find('enclosure')
            image_url = enclosure.get('url') if enclosure is not None else default_image_url

            # Check if the image URL is valid, else use default image URL
            if not is_image_url_valid(image_url):
                image_url = default_image_url

            # Clean up description and stop at "Read More..."
            description = BeautifulSoup(description, 'html.parser').get_text()
            description = re.split(r'Read More...', description)[0].strip()

            article = Article(
                title=title,
                url=link,
                summary=description,
                date=pub_date,
                source='Trend Micro',
                image=image_url
            )
            article.save_to_db()
            articles.append(article)
        except Exception as e:
            print(f"Error parsing article: {e}")

    return articles

if __name__ == "__main__":
    articles = trendmicro_scraper(limit=10)
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Summary: {article.summary}")
        print(f"Date: {article.date}")
        print(f"Image: {article.image}")
        print("\n")
