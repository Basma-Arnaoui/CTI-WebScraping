import argparse
import json
import time
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue, Empty


def scan(url, api_key):
    url_scan = 'https://www.virustotal.com/vtapi/v2/url/scan'
    try:
        params = {'apikey': api_key, 'url': url}
        response = requests.post(url_scan, data=params)
        response_json = response.json()
        if 'scan_id' in response_json:
            return response_json['scan_id']
        elif 'error' in response_json and response_json['error'] == 'Quota exceeded':
            raise ValueError("Rate limit detected")
    except Exception as e:
        print(f"Error detected: {e}")
    return None


def report(scan_id, api_key):
    url_report = 'https://www.virustotal.com/vtapi/v2/url/report'
    try:
        params = {'apikey': api_key, 'resource': scan_id}
        response = requests.get(url_report, params=params)
        response_json = response.json()
        if 'positives' in response_json:
            return response_json
        elif 'error' in response_json and response_json['error'] == 'Quota exceeded':
            raise ValueError("Rate limit detected")
    except Exception as e:
        print(f"Error detected: {e}")
    return None


def worker(api_key, url_queue, df, output_fp, json_fp, thread_id):
    while True:
        try:
            url = url_queue.get(timeout=10)  # Adjust timeout as needed
            print(f"Thread {thread_id} scanning URL: {url}")
            scan_id = scan(url, api_key)
            if scan_id:
                print(f"Thread {thread_id} reporting scan ID: {scan_id}")
                report_result = report(scan_id, api_key)
                if report_result:
                    positives = report_result.get('positives', 'N/A')
                    total = report_result.get('total', 'N/A')
                    score = f"{positives}/{total}"
                    # Update the DataFrame
                    index = df.index[df['URL'] == url].tolist()[0]
                    df.at[index, 'Score'] = score
                    print(f"URL: {url}, Score: {score}")
                    # Save the updated DataFrame to Excel
                    df.to_excel(output_fp, index=False)
                    # Save the report to JSON file
                    with open(json_fp, 'a') as json_file:
                        json.dump(report_result, json_file)
                        json_file.write("\n")
            url_queue.task_done()
        except Empty:
            break
        except ValueError as e:
            print(f"Thread {thread_id} rate limit reached: {e}")
            break
        time.sleep(15)  # Sleep for 15 seconds to avoid rate limits


def main():
    parser = argparse.ArgumentParser(description="Scan URLs using VirusTotal API and write results to an Excel file.")
    parser.add_argument('link_fp', help="Path to the Excel file containing the links you want to scan")
    parser.add_argument('output_fp', help="Path to the output Excel file")
    parser.add_argument('json_fp', help="Path to the output JSON file")
    parser.add_argument('api_keys', nargs='+', help='VirusTotal API keys (provide at least two)')
    args = parser.parse_args()

    df = pd.read_excel(args.link_fp)
    df.columns = ['URL']

    # Ensure the second column exists
    if 'Score' not in df.columns:
        df['Score'] = ""

    url_queue = Queue()
    for url in df['URL']:
        url_queue.put(url)

    with ThreadPoolExecutor(max_workers=len(args.api_keys)) as executor:
        futures = [executor.submit(worker, api_key, url_queue, df, args.output_fp, args.json_fp, i) for i, api_key in
                   enumerate(args.api_keys)]

        for future in as_completed(futures):
            future.result()  # to catch any exceptions raised in threads

    print("All scans complete.")


if __name__ == '__main__':
    main()
