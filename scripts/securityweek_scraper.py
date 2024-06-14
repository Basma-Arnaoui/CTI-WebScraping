import feedparser
import re

def fetch_securityweek_rss(keywords):
    rss_url = "https://feeds.feedburner.com/securityweek"
    feed = feedparser.parse(rss_url)

    keyword_articles = []

    for entry in feed.entries:
        title = entry.title
        summary = entry.summary
        url = entry.link
        published = entry.published

        if any(re.search(r'\b' + re.escape(keyword.lower()) + r'\b', title.lower()) or
               re.search(r'\b' + re.escape(keyword.lower()) + r'\b', summary.lower()) for keyword in keywords):
            keyword_article = {
                'title': title,
                'url': url,
                'summary': summary,
                'published': published,
                'keywords': ', '.join(keywords)
            }
            keyword_articles.append(keyword_article)

    return keyword_articles

if __name__ == "__main__":
    keywords = ['automation', 'cyber attack', 'data breach','ransomware']
    articles = fetch_securityweek_rss(keywords)
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Summary: {article['summary']}")
        print(f"Published: {article['published']}")
        print(f"Keywords: {article['keywords']}")
        print("\n")
