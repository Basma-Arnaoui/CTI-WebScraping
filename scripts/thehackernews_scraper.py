import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def fetch_articles(keywords):
    # Set up undetected ChromeDriver options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')

    # Initialize undetected ChromeDriver with specified version
    print("Initializing ChromeDriver...")
    driver = uc.Chrome(options=options, version_main=125)
    print("ChromeDriver initialized.")

    try:
        driver.get('https://thehackernews.com/')
        print("Page loaded")

        # Wait for the page to load completely and handle Cloudflare challenge
        max_wait_time = 60  # maximum wait time of 60 seconds
        start_time = time.time()

        while "Just a moment..." in driver.page_source:
            if time.time() - start_time > max_wait_time:
                print("Timeout waiting for the challenge to pass.")
                break
            print("Encountered challenge page. Waiting for it to pass...")
            time.sleep(5)

        # Get the page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        print("Page source fetched and driver quit")

        # Print the raw HTML for debugging
        print("HTML Content fetched:")
        print(soup.prettify()[:1000])  # Print the first 1000 characters for a quick look

        articles = soup.find_all('div', class_='body-post')
        print(f"Found {len(articles)} articles")

        keyword_articles = []

        for article in articles:
            try:
                title = article.find('h2', class_='home-title').text.strip()
                summary = article.find('div', class_='home-desc').text.strip()
                url = article.find('a')['href']
                publish_date = article.find('span', class_='home-date').text.strip()

                if any(keyword.lower() in title.lower() or keyword.lower() in summary.lower() for keyword in keywords):
                    keyword_article = {
                        'title': title,
                        'url': url,
                        'summary': summary,
                        'publish_date': publish_date,
                        'keywords': ', '.join(keywords)
                    }
                    keyword_articles.append(keyword_article)
            except Exception as e:
                print(f"Error parsing article: {e}")

        return keyword_articles

    except Exception as e:
        print(f"Error during fetch: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    keywords = ['cybersecurity', 'malware', 'data breach']
    articles = fetch_articles(keywords)
    print(f"Total articles found: {len(articles)}")
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"URL: {article['url']}")
        print(f"Summary: {article['summary']}")
        print(f"Publish Date: {article['publish_date']}")
        print(f"Keywords: {article['keywords']}")
        print("\n")
