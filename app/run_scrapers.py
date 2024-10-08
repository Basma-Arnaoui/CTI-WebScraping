# scripts/scraper.py

from scripts.bleepingcomputer_scraper import bleepingcomputer_scraper
from scripts.infosecurity_scraper import infosecurity_scraper
from scripts.securityweek_scraper import securityweek_scraper
from scripts.thehackernews import thehackernews_scraper
from scripts.borncity_scraper import borncity_scraper
from scripts.zataznews_scraper import zataz_scraper
from scripts.apisecurity_scraper import api_security_scraper
from scripts.trendmicro_scraper import trendmicro_scraper
from scripts.cybersecuritydive_scraper import cybersecuritydive_scraper
from scripts.developertech_scraper import developertech_scraper
from contextlib import closing
import sqlite3
import os

from app.models import initialize_db
ARTICLES_DATABASE = os.path.join(os.path.dirname(__file__), '..', 'articles.db')

def run_all_scrapers():
    bleepingcomputer_articles = bleepingcomputer_scraper()
    #hackernews_articles = hackernews_scraper()
    infosecurity_articles = infosecurity_scraper()
    securityweek_articles = securityweek_scraper()
    thehackernews_articles = thehackernews_scraper()
    borncity_articles = borncity_scraper(3)
    zataz_articles = zataz_scraper()
    apisecurity_articles = api_security_scraper(10)
    trendmicro_articles = trendmicro_scraper(10)
    #cybersecuritydive_articles = cybersecuritydive_scraper(1)
    developertech_articles = developertech_scraper()

    print(f"Bleeping Computer: {len(bleepingcomputer_articles)} articles fetched")
    #print(f"Hacker News: {len(hackernews_articles)} articles fetched")
    print(f"Info Security: {len(infosecurity_articles)} articles fetched")
    print(f"Security Week: {len(securityweek_articles)} articles fetched")
    print(f"The Hacker News: {len(thehackernews_articles)} articles fetched")
    print(f"Born City: {len(borncity_articles)} articles fetched")
    print(f"Zatas News: {len(zataz_articles)} articles fetched")
    print(f"Api Security: {len(apisecurity_articles)} articles fetched")
    print(f"Trend Micro: {len(trendmicro_articles)} articles fetched")
    #print(f"Cybersecurity Dive: {len(cybersecuritydive_articles)} articles fetched")
    print(f"Developer Tech: {len(developertech_articles)} articles fetched")





    #cve_data = scrape_cisa_known_exploited_vulnerabilities()
    #insert_cve_data(cve_data)


