from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re


def scrape_hacker_news(keywords, max_pages=23):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
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

            print("Finding articles...")
            # Find all links
            links = driver.find_elements(By.TAG_NAME, 'a')

            for link in links:
                title = link.text
                url = link.get_attribute('href')

                if url and any(re.search(r'\b' + re.escape(keyword) + r'\b', title, re.IGNORECASE) or
                               re.search(r'\b' + re.escape(keyword) + r'\b', url, re.IGNORECASE)
                               for keyword in keywords):
                    articles_data.append({"title": title, "url": url})
                    print(f"Title: {title}")
                    print(f"URL: {url}")
                    print('-' * 80)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        print("Driver closed.")


if __name__ == "__main__":
    keywords = ["cybersecurity", "AI", "machine learning"]  # Add your keywords here
    scrape_hacker_news(keywords)
