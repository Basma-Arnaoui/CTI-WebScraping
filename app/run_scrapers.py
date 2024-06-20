# scripts/scraper.py

from scripts.bleepingcomputer_scraper import bleepingcomputer_scraper
from scripts.hackernews_scraper import hackernews_scraper
from scripts.infosecurity_scraper import infosecurity_scraper
from scripts.securityweek_scraper import securityweek_scraper
from scripts.thehackernews import thehackernews_scraper

def run_all_scrapers():
    bleepingcomputer_articles = bleepingcomputer_scraper()
    hackernews_articles = hackernews_scraper()
    infosecurity_articles = infosecurity_scraper()
    securityweek_articles = securityweek_scraper()
    thehackernews_articles = thehackernews_scraper()

    print(f"Bleeping Computer: {len(bleepingcomputer_articles)} articles fetched")
    print(f"Hacker News: {len(hackernews_articles)} articles fetched")
    print(f"Info Security: {len(infosecurity_articles)} articles fetched")
    print(f"Security Week: {len(securityweek_articles)} articles fetched")
    print(f"The Hacker News: {len(thehackernews_articles)} articles fetched")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        keywords = sys.argv[1].split(',')
    else:
        keywords = ["cti", "data", "cyber", "ai", "machine", "ransomware", "spyware", "vulnerability"]
    run_all_scrapers(keywords)
