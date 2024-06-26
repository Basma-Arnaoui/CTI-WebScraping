import argparse
import json
import time
import requests
import pandas as pd

def scan(url_batch, api_key):
    url = 'https://www.virustotal.com/vtapi/v2/url/scan'
    scan_id_list = []
    for URL in url_batch:
        try:
            params = {'apikey': api_key, 'url': URL}
            response = requests.post(url, data=params)
            response_json = response.json()
            if 'scan_id' in response_json:
                scan_id_list.append(response_json['scan_id'])
            elif 'error' in response_json and response_json['error'] == 'Quota exceeded':
                raise ValueError("Rate limit detected")
        except ValueError as e:
            print("Rate limit detected, switching API key:", e)
            return scan_id_list, False
        except Exception as e:
            print("Error detected:", e)
            continue
    return scan_id_list, True

def report(scan_id_list, api_key):
    url = 'https://www.virustotal.com/vtapi/v2/url/report'
    report_list = []
    for id in scan_id_list:
        try:
            params = {'apikey': api_key, 'resource': id}
            response = requests.get(url, params=params)
            response_json = response.json()
            if 'positives' in response_json:
                report_list.append(response_json)
            elif 'error' in response_json and response_json['error'] == 'Quota exceeded':
                raise ValueError("Rate limit detected")
        except ValueError as e:
            print("Rate limit detected, switching API key:", e)
            return report_list, False
        except Exception as e:
            print("Error detected:", e)
            continue
    return report_list, True

def main():
    parser = argparse.ArgumentParser(description="Scan URLs using VirusTotal API and write results to an Excel file.")
    parser.add_argument('link_fp', help="Path to the Excel file containing the links you want to scan")
    parser.add_argument('output_fp', help="Path to the output Excel file")
    parser.add_argument('api_keys', nargs='+', help='VirusTotal API keys (provide at least two)')
    args = parser.parse_args()

    df = pd.read_excel(args.link_fp)
    urls = df.iloc[:, 0]  # assuming the URLs are in the first column

    # Ensure the second column exists
    if df.shape[1] == 1:
        df.insert(1, "Score", "")

    api_keys = args.api_keys
    current_api_index = 0

    response = []
    report_list = []

    for i in range(len(urls)):
        if i % 4 == 0:
            time.sleep(60)  # Sleep for 60 seconds to avoid rate limits
            url_batch = []
        url_batch.append(urls[i])
        if i % 4 == 3 or i == len(urls) - 1:
            scan_results, success = scan(url_batch, api_keys[current_api_index])
            if not success:
                current_api_index = (current_api_index + 1) % len(api_keys)
                scan_results, success = scan(url_batch, api_keys[current_api_index])
            response += scan_results

    print('Scan complete')

    for i in range(len(response)):
        if i % 4 == 0:
            time.sleep(60)  # Sleep for 60 seconds to avoid rate limits
            scan_list = []
        scan_list.append(response[i])
        if i % 4 == 3 or i == len(response) - 1:
            reportBatch, success = report(scan_list, api_keys[current_api_index])
            if not success:
                current_api_index = (current_api_index + 1) % len(api_keys)
                reportBatch, success = report(scan_list, api_keys[current_api_index])
            report_list += reportBatch

    # Write the report data back to the Excel file
    for i, rep in enumerate(report_list):
        positives = rep.get('positives', 'N/A')
        total = rep.get('total', 'N/A')
        score = f"{positives}/{total}"
        df.iloc[i, 1] = score  # assuming the score should be written to the second column

    df.to_excel(args.output_fp, index=False)

    # Write raw report data to output file
    with open(args.output_fp, 'a') as output_file:
        for r in report_list:
            json.dump(r, output_file)
            output_file.write("\n")

if __name__ == '__main__':
    main()
