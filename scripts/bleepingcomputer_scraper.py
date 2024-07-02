import requests
from bs4 import BeautifulSoup
import re
import sys
import os
from datetime import datetime


# Add the parent directory of 'app' to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from app.models
from app.models import Article

def bleepingcomputer_scraper():
    url = 'https://www.bleepingcomputer.com/news/security/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.select('ul#bc-home-news-main-wrap > li')
    print(f"Found {len(articles)} articles")

    keyword_articles = []
    for article in articles:
        try:
            title_element = article.find('h4').find('a')
            summary_element = article.find('p')
            date_element = article.find('li', class_='bc_news_date')
            image_element = article.find('div', class_='bc_latest_news_img').find('img')

            if not title_element or not summary_element:
                print("Missing title or summary element")
                continue

            title = title_element.text.strip()
            summary = summary_element.text.strip()
            date = date_element.text.strip() if date_element else 'N/A'
            url = title_element['href']
            date_obj = datetime.strptime(date, "%B %d, %Y")
            uniform_date = date_obj.strftime("%Y-%m-%d")

            # Handle lazy-loaded images with `data-src`
            if image_element:
                if image_element.has_attr('data-src'):
                    image = image_element['data-src']
                else:
                    image = image_element['src']
            else:
                image = None

            # Absolute URL for the image if it's relative
            if image and not image.startswith('http'):
                image = 'https://www.bleepingcomputer.com' + image

            if not url.startswith('http'):
                url = 'https://www.bleepingcomputer.com' + url


            keyword_article = Article(
                    title=title,
                    url=url,
                    summary=summary,
                    date=uniform_date,
                    source='Bleeping Computer',
                    image=image
                )
            keyword_article.save_to_db()
            keyword_articles.append(keyword_article)
        except Exception as e:
            print(f"Error parsing article: {e}")

    return keyword_articles

if __name__ == "__main__":
    keywords = ['cti', 'data', 'cyber', 'ai', 'machine']
    articles = bleepingcomputer_scraper()
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Summary: {article.summary}")
        print(f"Date: {article.date}")
        print(article.image)
        print("\n")
