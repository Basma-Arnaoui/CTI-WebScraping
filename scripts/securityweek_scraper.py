import feedparser
import re
from bs4 import BeautifulSoup
from Article import Article


def securityweek_scraper(keywords):
    rss_url = "https://feeds.feedburner.com/securityweek"
    feed = feedparser.parse(rss_url)

    keyword_articles = []

    for entry in feed.entries:
        title = entry.title
        summary = BeautifulSoup(entry.summary, "html.parser").get_text()
        url = entry.link
        date = entry.published if 'published' in entry else 'N/A'

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

    return keyword_articles

if __name__ == "__main__":
    keywords = ['automation', 'cyber attack', 'data breach', 'ransomware']
    articles = securityweek_scraper(keywords)
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        article_dict = article.to_dict()
        print(f"Title: {article_dict['title']}")
        print(f"URL: {article_dict['url']}")
        print(f"Summary: {article_dict['summary']}")
        print(f"Date: {article_dict['date']}")
        print(f"Keywords: {article_dict['keywords']}")
        print("\n")
