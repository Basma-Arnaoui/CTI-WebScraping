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

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

def cybersecuritydive_scraper(pages=1):
    BASE_URL = 'https://www.cybersecuritydive.com/topic/vulnerability/?page={}'
    all_articles = []

    for page in range(1, pages + 1):
        url = BASE_URL.format(page)
        print(f"Scraping {url}")
        driver.get(url)

        # Wait for page to load
        time.sleep(3)

        # Find all articles on the page
        article_elements = driver.find_elements(By.CLASS_NAME, 'row.feed__item')

        for article in article_elements:
            try:
                title_element = article.find_element(By.CLASS_NAME, 'feed__title')
                title = title_element.text.strip()

                link_element = title_element.find_element(By.TAG_NAME, 'a')
                link = link_element.get_attribute('href')

                summary_element = article.find_element(By.CLASS_NAME, 'feed__description')
                summary = summary_element.text.strip()

                image_element = article.find_element(By.CLASS_NAME, 'feed__image-container').find_element(By.TAG_NAME, 'img')
                image_url = image_element.get_attribute('src')

                # Correctly select the date, accounting for possible "Updated" label
                date_elements = article.find_elements(By.CLASS_NAME, 'secondary-label')
                date = None
                for element in date_elements:
                    text = element.text.strip()
                    if re.match(r'^[A-Z][a-z]+ \d{1,2}, \d{4}$', text):
                        date = text
                    elif text.startswith("Updated"):
                        date = text.replace("Updated", "").strip()

                if not date:
                    print(f"Date not found for article: {title}")

                date_obj = datetime.strptime(date, "%B %d, %Y")
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
                source='Cybersecurity Dive',
                image=article_data['image']
            )
            article.save_to_db()
        except Exception as e:
            print(f"Error saving article to db: {e}")
    driver.quit()
    return all_articles

if __name__ == "__main__":
    pages_to_scrape = 2  # Number of pages you want to scrape
    cybersecuritydive_scraper(pages=pages_to_scrape)

    # Close the browser
    driver.quit()
