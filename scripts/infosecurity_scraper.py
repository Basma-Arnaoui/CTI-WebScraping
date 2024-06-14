import requests
from bs4 import BeautifulSoup
from datetime import datetime


def contains_keyword(text, keywords):
    for keyword in keywords:
        if keyword.lower() in text.lower():
            return True
    return False


def scrape_infosecurity_magazine(keywords):
    url = 'https://www.infosecurity-magazine.com/news/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('li', class_='webpage-item')

        if not articles:
            print("No articles container found.")
            return

        for article in articles:
            title_tag = article.find('h2', class_='h3 webpage-title')
            summary_tag = article.find('p', class_='webpage-summary')
            meta_tag = article.find('span', class_='webpage-meta')

            if title_tag and summary_tag and meta_tag:
                title = title_tag.get_text(strip=True)
                summary = summary_tag.get_text(strip=True)
                date_str = meta_tag.get_text(strip=True)

                # Attempt to extract the date from the string
                try:
                    date = datetime.strptime(date_str, "%d %B %Y")
                except ValueError:
                    date = None

                link = article.find('a')['href']
                if not link.startswith('http'):
                    link = 'https://www.infosecurity-magazine.com' + link

                if contains_keyword(title, keywords) or contains_keyword(summary, keywords):
                    print(f"Title: {title}")
                    print(f"URL: {link}")
                    print(f"Summary: {summary}")
                    print(f"Date: {date_str}")
                    print('-' * 80)


if __name__ == "__main__":
    keywords = ["ransomware", "spyware", "vulnerability"]  # Add your keywords here
    scrape_infosecurity_magazine(keywords)
