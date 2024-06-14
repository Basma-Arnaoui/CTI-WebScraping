import feedparser
import re


def fetch_hacker_news_rss(keywords):
    rss_url = "https://feeds.feedburner.com/TheHackersNews"
    feed = feedparser.parse(rss_url)

    articles_data = []
    print(f"Fetching articles from RSS feed at {rss_url}...")

    # Create a list of regex patterns for each keyword to match whole words only
    keyword_patterns = [re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE) for keyword in keywords]

    for entry in feed.entries:
        title = entry.title
        url = entry.link
        published = entry.published
        summary = entry.summary

        # Check if any of the keywords are in the title or summary using regex
        if any(pattern.search(title) or pattern.search(summary) for pattern in keyword_patterns):
            articles_data.append({
                "title": title,
                "url": url,
                "published": published,
                "summary": summary
            })
            print(f"Title: {title}")
            print(f"URL: {url}")
            print(f"Published: {published}")
            print(f"Summary: {summary}")
            print('-' * 80)

    print(f"Total articles found: {len(articles_data)}")
    return articles_data


if __name__ == "__main__":
    keywords = ["cybersecurity", "AI", "machine learning"]  # Add your keywords here
    fetch_hacker_news_rss(keywords)
