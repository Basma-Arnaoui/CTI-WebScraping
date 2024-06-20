import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os

# Add the parent directory of 'app' to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from app.models
from app.models import Article

def contains_keyword(text, keywords):
    for keyword in keywords:
        if keyword.lower() in text.lower():
            return True
    return False

def infosecurity_scraper():
    url = 'https://www.infosecurity-magazine.com/news/'
    response = requests.get(url)
    articles_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('li', class_='webpage-item')

        if not articles:
            print("No articles container found.")
            return articles_data

        for article in articles:
            title_tag = article.find('h2', class_='h3 webpage-title')
            summary_tag = article.find('p', class_='webpage-summary')
            meta_tag = article.find('span', class_='webpage-meta')
            image_tag = article.find('img')

            if title_tag and summary_tag and meta_tag:
                title = title_tag.get_text(strip=True)
                summary = summary_tag.get_text(strip=True)
                date_str = meta_tag.get_text(strip=True)

                # Correct the date extraction logic
                try:
                    date = datetime.strptime(date_str, "%d %b %Y").strftime('%Y-%m-%d')
                except ValueError:
                    date = "N/A"

                link = article.find('a')['href']
                image = image_tag['src'] if image_tag else None

                if not link.startswith('http'):
                    link = 'https://www.infosecurity-magazine.com' + link


                keyword_article = Article(
                        title=title,
                        url=link,
                        summary=summary,
                        date=date,
                        source='Info Security',
                        image=image
                    )
                keyword_article.save_to_db()
                articles_data.append(keyword_article)

    return articles_data

if __name__ == "__main__":
    keywords = ["ransomware", "spyware", "vulnerability"]  # Add your keywords here
    articles = infosecurity_scraper(keywords)
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Summary: {article.summary}")
        print(f"Date: {article.date}")
        print(f"Keywords: {article.keywords}")
        print("\n")
