import pandas as pd
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.auth import HTTPBasicAuth
import json
from queue import Queue

# Function to clean the site string based on the given rules
def clean_site(site):
    site = re.sub(r'\\\.', '.', site)  # Replace \. with .
    site = re.sub(r'\(\.\*\)', '', site)  # Remove (.*)
    site = re.sub(r'/\*', '', site)  # Remove /*
    site = re.sub(r'\.\.', '.', site)  # Replace .. with .
    site = site.replace('^', '')  # Remove ^
    return site

# Function to get URL score from IBM X-Force Exchange API
def get_url_score(site, api_token, api_password):
    base_url = "https://api.xforce.ibmcloud.com/url/"
    full_url = base_url + site
    headers = {'Accept': 'application/json'}
    auth = HTTPBasicAuth(api_token, api_password)
    
    try:
        response = requests.get(full_url, headers=headers, auth=auth)
        if response.status_code == 200:
            data = response.json()
            score = data.get('result', {}).get('score', None)
            return site, score
        else:
            return site, None
    except Exception as e:
        print(f"Error processing {site}: {e}")
        return site, None

# Worker function to process URLs from the queue
def worker(queue, api_token, api_password, results):
    while not queue.empty():
        index, site = queue.get()
        score = get_url_score(site, api_token, api_password)
        if score is not None:
            results.append((index, site, score[1]))
            print(f"Site: {site}, Score: {score[1]}")
        else:
            print(f"Failed to retrieve score for {site}")
        queue.task_done()

# Main function to process the Excel file and perform operations
def process_excel(file_path, api_token, api_password):
    df = pd.read_excel(file_path, usecols=[1, 2], header=None, names=['B', 'C'])
    results = []

    # Collecting sites to process
    queue = Queue()

    for index, row in df.iterrows():
        if row['B'] == 'Site' or row['B'] == 'Regular Expression':
            site = clean_site(row['C'])
            queue.put((index, site))

    print(f"First 20 sites to process: {list(queue.queue)[:20]}")

    # Using ThreadPoolExecutor to perform API requests in parallel
    with ThreadPoolExecutor(max_workers=50) as executor:
        for _ in range(50):
            executor.submit(worker, queue, api_token, api_password, results)
        queue.join()  # Wait for all tasks to be done

    # Saving results to a JSON file for backup
    with open('site_scores.json', 'w') as f:
        json.dump(results, f, indent=4)

    # Writing the scores back to the DataFrame
    for index, site, score in results:
        df.at[index, 'Score'] = score
    
    # Saving the updated DataFrame back to Excel
    df.to_excel('updated_file.xlsx', index=False)

# Example usage
api_token = "0b2b0df4-594f-45a8-b136-3583d9e3811a"  # Replace with your actual API token
api_password = "e1e93529-7371-4a02-ae8e-7f29abf80642"  # Replace with your actual API password
file_path = "links.xlsx"  # Replace with your actual Excel file path

process_excel(file_path, api_token, api_password)
