import requests
from bs4 import BeautifulSoup
import re
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import get_db_connection, Article, get_cve_db_connection




def borncity_scraper(max_pages):
    base_url = 'https://borncity.com/win/category/security/page/'
    articles = []

    for page in range(1, max_pages + 1):
        url = base_url + str(page)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('div', class_='post')

        for post in posts:
            try:
                title_element = post.find('h2', class_='entry-title').find('a')
                summary_element = post.find('div', class_='entry-summary')
                date_element = post.find('div', class_='entry-meta')

                if not title_element or not summary_element or not date_element:
                    print("Missing title, summary, or date element")
                    continue

                title = title_element.text.strip()
                summary = summary_element.text.strip()
                date = date_element.text.strip()
                url = title_element['href']

                # Extract the date part from the string
                extracted_date_str = re.search(r'\d{4}-\d{2}-\d{2}', date).group()

                # Parse the extracted date string
                date_obj = datetime.strptime(extracted_date_str, "%Y-%m-%d")

                # Convert to the uniform format
                uniform_date = date_obj.strftime("%Y-%m-%d")

                keyword_article = Article(
                    title=title,
                    url=url,
                    summary=summary,
                    date=uniform_date,
                    source='Born City',
                    image="https://borncity.com/win/wp-content/uploads/sites/2/2014/12/cropped-header04.jpg"
                )

                articles.append(keyword_article)
                keyword_article.save_to_db()

            except Exception as e:
                print(f"Error parsing post: {e}")

    return articles

