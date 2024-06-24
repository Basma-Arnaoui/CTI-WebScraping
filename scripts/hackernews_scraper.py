from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import sys
import os

# Add the parent directory of 'app' to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from app.models
from app.models import Article

def hackernews_scraper(max_pages=1):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # E   nsure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set path to chromedriver as per your configuration
    webdriver_service = Service(ChromeDriverManager().install())

    # Choose Chrome Browser
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    try:
        articles_data = []

        for page in range(1, max_pages + 1):
            print(f"Opening Hacker News page {page}...")
            # Open Hacker News page
            driver.get(f"https://news.ycombinator.com/?p={page}")

            # Wait for the page to load
            time.sleep(3)

            # Find all links
            links = driver.find_elements(By.TAG_NAME, 'a')

            for link in links:
                title = link.text
                url = link.get_attribute('href')


                article = Article(
                        title=title,
                        url=url,
                        summary="",  # No summary available from Hacker News
                        date="",  # No date available from Hacker News
                        source='Hacker News',
                    )
                article.save_to_db()
                articles_data.append(article)


    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        print("Driver closed.")

    return articles_data


if __name__ == "__main__":
    keywords = ["cybersecurity", "AI", "machine learning"]  # Add your keywords here
    articles = hackernews_scraper(keywords)
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        print(f"Title: {article.title}")
        print(f"URL: {article.url}")
        print(f"Summary: {article.summary}")
        print(f"Date: {article.date}")
        print(f"Keywords: {article.keywords}")
        print("\n")
