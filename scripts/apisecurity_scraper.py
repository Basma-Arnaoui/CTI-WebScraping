import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import sys
import os
import re
from datetime import datetime

# Add the parent directory of 'app' to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from app.models
from app.models import Article

def api_security_scraper(limit=50):
    url = 'https://apisecurity.io/feed/index.xml'
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

    for item in items[:limit]:
        try:
            title = item.find('title').text.strip()
            title = re.sub(r'^Issue \d+: ', '', title)  # Remove "Issue X:" prefix
            link = item.find('link').text.strip()
            pub_date = item.find('pubDate').text.strip()
            description = item.find('description').text.strip()
            content_encoded = item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text

            date_obj = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
            uniform_date = date_obj.strftime("%Y-%m-%d")

            # Use BeautifulSoup to parse HTML content
            soup = BeautifulSoup(content_encoded, 'html.parser')
            img_tag = soup.find('img')
            image_url = img_tag['src'] if img_tag and img_tag.has_attr('src') else 'https://via.placeholder.com/150'

            # Clean up description and stop at "Read More..."
            description = BeautifulSoup(description, 'html.parser').get_text()
            description = re.split(r'Read More...', description)[0].strip()

            # Use cropped logo image if image is None
            if not image_url:
                image_url = 'https://cf-assets.www.cloudflare.com/slt3lc6tev37/4I65STqF6B64hjgt6vn9Op/25e544c75886eb560ecf521edc3fd336/API-security-solutions.png'  # Replace with cropped logo URL

            article = Article(
                title=title,
                url=link,
                summary=description,
                date=uniform_date,
                source='API Security News',
                image=image_url
            )
            article.save_to_db()
            articles.append(article)
        except Exception as e:
            print(f"Error parsing article: {e}")

    return articles

if __name__ == "__main__":
    articles = api_security_scraper(limit=50)
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Summary: {article.summary}")
        print(f"Date: {article.date}")
        print(f"Image: {article.image}")
        print("\n")
