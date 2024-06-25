import requests
from bs4 import BeautifulSoup

BASE_URL = "https://cybersecuritynews.com"

CATEGORIES = {
    "threats": "category/threats/",
    "cyber_attack": "category/cyber-attack/",
    "vulnerability": "category/vulnerability/",
    "zero_day": "category/zero-day/",
    "data_breaches": "category/data-breaches/",
    "cyber_ai": "category/cyber-ai/"
}


def get_articles_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for article in soup.find_all('div', class_='td_module_wrap td-animation-stack'):
        title_tag = article.find('h3', class_='entry-title td-module-title')
        title = title_tag.text.strip() if title_tag else "No title"
        link = title_tag.find('a')['href'] if title_tag else "No link"

        date_tag = article.find('time')
        date = date_tag['datetime'] if date_tag else "No date"

        summary_tag = article.find('div', class_='td-excerpt')
        summary = summary_tag.text.strip() if summary_tag else "No summary"

        image_tag = article.find('img', class_='entry-thumb')
        image = image_tag['src'] if image_tag else "No image"

        articles.append({
            'title': title,
            'link': link,
            'date': date,
            'summary': summary,
            'image': image
        })

    return articles


def scrape_articles(category=None, pages=1):
    articles = []

    if category:
        url_template = f"{BASE_URL}/{CATEGORIES[category]}page/{{}}/"
        for page in range(1, pages + 1):
            url = url_template.format(page)
            print(f"Scraping {url}")
            articles.extend(get_articles_from_page(url))
    else:
        url = BASE_URL
        print(f"Scraping {url}")
        articles.extend(get_articles_from_page(url))

        while True:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            load_more_button = soup.find('a', class_='td_ajax_load_more')
            if load_more_button and 'href' in load_more_button.attrs:
                next_page_url = load_more_button['href']
                print(f"Scraping {next_page_url}")
                articles.extend(get_articles_from_page(next_page_url))
                url = next_page_url
            else:
                break

    return articles


if __name__ == "__main__":
    category = "threats"  # Set to None for all categories, or use 'threats', 'cyber_attack', etc.
    pages = 3  # Number of pages to scrape if category is specified

    scraped_articles = scrape_articles(category=category, pages=pages)
    for article in scraped_articles:
        print(article)
