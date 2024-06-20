import feedparser
import re
from bs4 import BeautifulSoup
import sys
import os

# Add the parent directory of 'app' to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from app.models
from app.models import Article

def thehackernews_scraper(keywords):
    rss_url = "https://feeds.feedburner.com/TheHackersNews"
    feed = feedparser.parse(rss_url)

    keyword_articles = []
    print(f"Fetching articles from RSS feed at {rss_url}...")

    # Create a list of regex patterns for each keyword to match whole words only
    keyword_patterns = [re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE) for keyword in keywords]

    for entry in feed.entries:
        title = entry.title
        url = entry.link
        date = entry.published
        summary = BeautifulSoup(entry.summary, "html.parser").get_text()

        # Extract the image URL from the enclosure field
        image = entry.enclosures[0]['url'] if 'enclosures' in entry and entry.enclosures else None

        # Check if any of the keywords are in the title or summary using regex
        if any(pattern.search(title) or pattern.search(summary) for pattern in keyword_patterns):
            keyword_article = Article(
                title=title,
                url=url,
                summary=summary,
                date=date,
                keywords=', '.join(keywords),
                source='The Hacker News',
                image=image
            )
            keyword_articles.append(keyword_article)
            keyword_article.save_to_db()
            print(f"Title: {title}")
            print(f"URL: {url}")
            print(f"Published: {date}")
            print(f"Summary: {summary}")
            print(f"Image: {image}")
            print('-' * 80)

    print(f"Total articles found: {len(keyword_articles)}")
    return keyword_articles

if __name__ == "__main__":
    keywords = ["cybersecurity", "AI", "machine learning"]  # Add your keywords here
    articles = thehackernews_scraper(keywords)
    for article in articles:
        article_dict = article.to_dict()
        print(f"Title: {article_dict['title']}")
        print(f"URL: {article_dict['url']}")
        print(f"Summary: {article_dict['summary']}")
        print(f"Date: {article_dict['date']}")
        print(f"Keywords: {article_dict['keywords']}")
        print(f"Image: {article.image}")
        print("\n")
