from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import sys
import os
from datetime import datetime

# Add the parent directory of 'app' to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from app.models
from app.models import Article

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chromedriver as per your configuration
webdriver_service = ChromeService(ChromeDriverManager().install())

def developertech_scraper():
    # Choose Chrome Browser
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    url = 'https://www.developer-tech.com/categories/developer-hacking-security/'
    all_articles = []

    try:
        print(f"Scraping {url}")
        driver.get(url)

        # Wait for page to load
        time.sleep(3)

        # Find all articles on the page
        article_elements = driver.find_elements(By.CSS_SELECTOR, 'article.post')

        for article in article_elements:
            try:
                title_element = article.find_element(By.CSS_SELECTOR, 'h3 a')
                title = title_element.text.strip()

                link = title_element.get_attribute('href')

                # Get the summary if it exists
                summary_element = article.find_element(By.CSS_SELECTOR, 'div.post-text')
                summary = summary_element.text.strip() if summary_element else ""

                image_element = article.find_element(By.CSS_SELECTOR, 'div.image a img')
                image_url = image_element.get_attribute('src')

                date_element = article.find_element(By.CSS_SELECTOR, 'div.byline div.content')
                date = date_element.text.strip()

                # Clean up date (remove text after pipe symbol if exists)
                date = date.split('|')[0].strip()
                date_obj = datetime.strptime(date, "%d %B %Y")
                uniform_date = date_obj.strftime("%Y-%m-%d")

                all_articles.append({
                    'title': title,
                    'url': link,
                    'summary': summary,
                    'image': image_url,
                    'date': uniform_date
                })
            except Exception as e:
                print(f"Error extracting article: {e}")

        # Save articles to the database
        for article_data in all_articles:
            try:
                article = Article(
                    title=article_data['title'],
                    url=article_data['url'],
                    summary=article_data['summary'],
                    date=article_data['date'],
                    source='Developer Tech',
                    image=article_data['image']
                )
                article.save_to_db()
            except Exception as e:
                print(f"Error saving article to db: {e}")

    finally:
        # Close the browser
        driver.quit()

    return all_articles

if __name__ == "__main__":
    articles = developertech_scraper()
    print(len(articles))
    # Print the scraped articles for debugging
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Summary: {article['summary']}")
        print(f"Date: {article['date']}")
        print(f"Image: {article['image']}")
        print("\n")
