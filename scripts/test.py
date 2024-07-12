import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "https://www.infosecurity-magazine.com/news/"

# Send a request to fetch the HTML content of the page
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all articles on the page
articles = soup.find_all('li', class_='webpage-item')

# Extract and print the details of each article
for article in articles:
    # Extract the image URL
    img_tag = article.find('img', class_='webpage-thumb')
    img_url = img_tag['src'] if img_tag else 'No image'

    # Extract the article title and URL
    title_tag = article.find('h2', class_='h3 webpage-title').find('a')
    title = title_tag.text.strip()
    article_url = title_tag['href']

    # Extract the publication date
    time_tag = article.find('time')
    publication_date = time_tag['datetime'] if time_tag else 'No date'

    # Extract the summary
    summary_tag = article.find('p', class_='webpage-summary')
    summary = summary_tag.text.strip() if summary_tag else 'No summary'

    # Print the extracted details
    print(f"Title: {title}")
    print(f"URL: {article_url}")
    print(f"Image URL: {img_url}")
    print(f"Publication Date: {publication_date}")
    print(f"Summary: {summary}")
    print("-" * 80)
