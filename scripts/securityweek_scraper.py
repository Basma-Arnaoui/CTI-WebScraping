import requests
from bs4 import BeautifulSoup
import re
import random


def fetch_articles(keywords):
    url = 'https://www.securityweek.com/'

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    ]

    headers = {
        'User-Agent': random.choice(user_agents)
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='node node-article node-teaser clearfix')
    print(f"Found {len(articles)} articles")

    keyword_articles = []
    for article in articles:
        try:
            title_element = article.find('h2', class_='title').find('a')
            summary_element = article.find('div', class_='content')
            if not title_element or not summary_element:
                print("Missing title or summary element")
                continue

            title = title_element.text.strip()
            summary = summary_element.text.strip()
            url = title_element['href']
            if not url.startswith('http'):
                url = 'https://www.securityweek.com' + url

            if any(re.search(r'\b' + re.escape(keyword.lower()) + r'\b', title.lower()) or
                   re.search(r'\b' + re.escape(keyword.lower()) + r'\b', summary.lower()) for keyword in keywords):
                keyword_article = {
                    'title': title,
                    'url': url,
                    'summary': summary,
                    'keywords': ', '.join(keywords)
                }
                keyword_articles.append(keyword_article)
        except Exception as e:
            print(f"Error parsing article: {e}")

    return keyword_articles


if __name__ == "__main__":
    keywords = ['Morocco', 'cyber attack', 'data breach']
    articles = fetch_articles(keywords)
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Summary: {article['summary']}")
        print(f"Keywords: {article['keywords']}")
        print("\n")
