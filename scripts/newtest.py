from playwright.sync_api import sync_playwright

def fetch_page_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        # Wait for the necessary content to load
        page.wait_for_selector('body')
        # Extract the HTML content of the body
        body_html = page.inner_html('body')
        browser.close()
        return body_html

# Given URL
url = 'https://sitecheck.sucuri.net/results/facebook.com'
data = fetch_page_data(url)
print(data)
