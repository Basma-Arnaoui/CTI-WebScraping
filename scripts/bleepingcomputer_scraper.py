import requests
from bs4 import BeautifulSoup
import re
from Article import Article

def bleepingcomputer_scraper(keywords):
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
            date_element = article.find('time')

            if not title_element or not summary_element:
                print("Missing title or summary element")
                continue

            title = title_element.text.strip()
            summary = summary_element.text.strip()
            date = date_element['datetime'].strip() if date_element and date_element.has_attr('datetime') else 'N/A'
            url = title_element['href']
            if not url.startswith('http'):
                url = 'https://www.bleepingcomputer.com' + url

            if any(re.search(r'\b' + re.escape(keyword.lower()) + r'\b', title.lower()) or
                   re.search(r'\b' + re.escape(keyword.lower()) + r'\b', summary.lower()) for keyword in keywords):
                keyword_article = Article(
                    title=title,
                    url=url,
                    summary=summary,
                    date=date,
                    keywords=', '.join(keywords)
                )
                keyword_articles.append(keyword_article)
        except Exception as e:
            print(f"Error parsing article: {e}")

    return keyword_articles

if __name__ == "__main__":
    keywords = ['cti', 'data', 'cyber', 'ai', 'machine']
    articles = bleepingcomputer_scraper(keywords)
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Summary: {article.summary}")
        print(f"Date: {article.date}")
        print(f"Keywords: {article.keywords}")
        print("\n")
