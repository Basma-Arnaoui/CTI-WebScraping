import feedparser
import re
from bs4 import BeautifulSoup
import sys
import os
from datetime import datetime
# Add the parent directory of 'app' to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from app.models
from app.models import Article

def securityweek_scraper():
    rss_url = "https://feeds.feedburner.com/securityweek"
    feed = feedparser.parse(rss_url)

    keyword_articles = []

    for entry in feed.entries:
        title = entry.title
        summary_html = entry.summary
        summary = BeautifulSoup(summary_html, "html.parser").get_text()
        url = entry.link

        date = entry.published if 'published' in entry else 'N/A'
        date_obj = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
        uniform_date = date_obj.strftime("%Y-%m-%d")

        # Extract the image from the summary HTML
        summary_soup = BeautifulSoup(summary_html, "html.parser")
        image_element = summary_soup.find('img')
        image = image_element['src'] if image_element else None


        keyword_article = Article(
                title=title,
                url=url,
                summary=summary,
                date=uniform_date,
                source='Security Week',
                image="https://media.licdn.com/dms/image/C4E0BAQH2tHghiPJr0g/company-logo_200_200/0/1675885800622/securityweek_logo?e=2147483647&v=beta&t=OugMo88yYehO7RT_M3Xu3vD-_X_7u-Md3GPbm0bZ8Rc"
            )
        keyword_article.save_to_db()
        keyword_articles.append(keyword_article)

    return keyword_articles


if __name__ == "__main__":
    keywords = ['automation', 'cyber attack', 'data breach', 'deployed']
    articles = securityweek_scraper(keywords)
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        article_dict = article.to_dict()
        print(f"Title: {article_dict['title']}")
        print(f"URL: {article_dict['url']}")
        print(f"Summary: {article_dict['summary']}")
        print(f"Date: {article_dict['date']}")
        print(f"Keywords: {article_dict['keywords']}")
        print(f"Image: {article.image}")
        print("\n")
