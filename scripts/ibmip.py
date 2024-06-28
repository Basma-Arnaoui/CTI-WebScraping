import pandas as pd
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.auth import HTTPBasicAuth
import json
import queue

# Function to clean and extract the IP address from the input string
def extract_ip(address):
    match = re.search(r'((\d{1,3}\.){3}\d{1,3})', address)
    if match:
        return match.group(0)
    return address

# Function to get IP score from IBM X-Force Exchange API
def get_ip_score(ip, api_token, api_password):
    base_url = "https://api.xforce.ibmcloud.com/ipr/"
    full_url = base_url + ip
    headers = {'Accept': 'application/json'}
    auth = HTTPBasicAuth(api_token, api_password)
    
    try:
        response = requests.get(full_url, headers=headers, auth=auth)
        if response.status_code == 200:
            data = response.json()
            score = data.get('score', None)
            return ip, score
        else:
            return ip, None
    except Exception as e:
        print(f"Error processing {ip}: {e}")
        return ip, None

# Worker function to process IPs from the queue
def worker(ip_queue, results, api_token, api_password):
    while not ip_queue.empty():
        index, ip = ip_queue.get()
        _, score = get_ip_score(ip, api_token, api_password)
        results.append((index, ip, score))
        print(f"Processed IP: {ip}, Score: {score}")
        ip_queue.task_done()

# Main function to process the Excel file and perform operations
def process_excel(file_path, api_token, api_password):
    df = pd.read_excel(file_path, header=None)
    results = []
    ip_queue = queue.Queue()

    # Collecting IPs to process
    for index, row in df.iterrows():
        if row[0] == 'Client':
            ip = extract_ip(row[1])
            ip_queue.put((index, ip))

    print(f"First 20 IPs to process: {list(ip_queue.queue)[:20]}")

    # Using ThreadPoolExecutor to perform API requests in parallel
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        for _ in range(50):
            futures.append(executor.submit(worker, ip_queue, results, api_token, api_password))

        # Ensuring all threads are completed
        for future in as_completed(futures):
            future.result()

    # Saving results to a JSON file for backup
    with open('ip_scores.json', 'w') as f:
        json.dump(results, f, indent=4)

    # Writing the scores back to the DataFrame
    for index, ip, score in results:
        if score is not None:
            df.at[index, 2] = score

    # Saving the updated DataFrame back to Excel
    df.to_excel('updated_file_ip.xlsx', index=False, header=False)

# Example usage
api_token = "f7f2bd07-2e43-417d-88b9-10c75a73eb63"  # Replace with your actual API token
api_password = "72848bdc-8baf-4fd2-935c-138a49956c8b"  # Replace with your actual API password
file_path = "updated_file.xlsx"  # Replace with your actual Excel file path

process_excel(file_path, api_token, api_password)
