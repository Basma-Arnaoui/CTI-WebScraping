# scripts/scraper.py

from scripts.bleepingcomputer_scraper import bleepingcomputer_scraper
from scripts.hackernews_scraper import hackernews_scraper
from scripts.infosecurity_scraper import infosecurity_scraper
from scripts.securityweek_scraper import securityweek_scraper
from scripts.thehackernews import thehackernews_scraper
from scripts.cisa_scraper import scrape_cisa_known_exploited_vulnerabilities
from scripts.borncity_scraper import borncity_scraper
from scripts.zataznews_scraper import zataz_scraper
from scripts.apisecurity_scraper import api_security_scraper
from app.models import insert_cve_data

def run_all_scrapers():
    bleepingcomputer_articles = bleepingcomputer_scraper()
    #hackernews_articles = hackernews_scraper()
    infosecurity_articles = infosecurity_scraper()
    securityweek_articles = securityweek_scraper()
    thehackernews_articles = thehackernews_scraper()
    borncity_articles = borncity_scraper(3)
    zataz_articles = zataz_scraper()
    apisecurity_articles = api_security_scraper(10)


    print(f"Bleeping Computer: {len(bleepingcomputer_articles)} articles fetched")
    #print(f"Hacker News: {len(hackernews_articles)} articles fetched")
    print(f"Info Security: {len(infosecurity_articles)} articles fetched")
    print(f"Security Week: {len(securityweek_articles)} articles fetched")
    print(f"The Hacker News: {len(thehackernews_articles)} articles fetched")
    print(f"Born City: {len(borncity_articles)} articles fetched")
    print(f"Zatas News: {len(zataz_articles)} articles fetched")
    print(f"Api Security: {len(apisecurity_articles)} articles fetched")


    #cve_data = scrape_cisa_known_exploited_vulnerabilities()
    #insert_cve_data(cve_data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        keywords = sys.argv[1].split(',')
    else:
        keywords = ["cti", "data", "cyber", "ai", "machine", "ransomware", "spyware", "vulnerability"]
    run_all_scrapers(keywords)
