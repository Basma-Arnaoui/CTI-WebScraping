# scripts/scraper.py

from scripts.bleepingcomputer_scraper import bleepingcomputer_scraper
from scripts.hackernews_scraper import hackernews_scraper
from scripts.infosecurity_scraper import infosecurity_scraper
from scripts.securityweek_scraper import securityweek_scraper
from scripts.thehackernews import thehackernews_scraper

def run_all_scrapers():
    keywords = ["cti", "data", "cyber", "ai", "machine", "ransomware", "spyware", "vulnerability"]

    # Fetch articles from all scrapers
    bleepingcomputer_articles = bleepingcomputer_scraper(keywords)
    hackernews_articles = hackernews_scraper(keywords)
    infosecurity_articles = infosecurity_scraper(keywords)
    securityweek_articles = securityweek_scraper(keywords)
    thehackernews_articles = thehackernews_scraper(keywords)

    print(f"Bleeping Computer: {len(bleepingcomputer_articles)} articles fetched")
    print(f"Hacker News: {len(hackernews_articles)} articles fetched")
    print(f"Info Security: {len(infosecurity_articles)} articles fetched")
    print(f"Security Week: {len(securityweek_articles)} articles fetched")
    print(f"The Hacker News: {len(thehackernews_articles)} articles fetched")

if __name__ == "__main__":
    run_all_scrapers()
