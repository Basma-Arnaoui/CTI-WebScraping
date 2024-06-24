from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_virustotal_positives_text(domain):
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
        print("Starting the WebDriver...")
        # Construct the VirusTotal URL
        virustotal_url = f"https://www.virustotal.com/gui/domain/{domain}"
        print(f"Navigating to URL: {virustotal_url}")

        # Navigate to the constructed URL
        driver.get(virustotal_url)

        # Allow some time for the page to load (adjust time as needed)
        print("Waiting for the page to load...")
        time.sleep(10)  # Wait for 10 seconds, you can increase if your internet connection is slow

        # Check if the body content is loaded
        print("Checking if the body content is loaded...")
        body_content = driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML')
        print(body_content)
        print("Body content loaded. Checking for 'positives' class element...")

        # Wait for the element with class 'positives' to be present
        wait = WebDriverWait(driver, 60)  # Wait for up to 60 seconds
        positive_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "positives")))

        print("Element found. Extracting text content...")
        # Get the text content of the element with class 'positives'
        positives_text = positive_element.text

        # Write the text content to a file
        with open("virustotal_positives.txt", "w", encoding="utf-8") as file:
            file.write(positives_text)
        print("Positives text content has been written to 'virustotal_positives.txt'")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the WebDriver
        driver.quit()
        print("Driver closed.")


if __name__ == "__main__":
    domain = "www.facebook.com"  # Replace this with the desired domain
    get_virustotal_positives_text(domain)
