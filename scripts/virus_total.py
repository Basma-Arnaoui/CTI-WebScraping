import argparse
import json
import os
import time
import requests

def scan(url_batch, api_key):
    url = 'https://www.virustotal.com/vtapi/v2/url/scan'
    scan_id_list = []
    for URL in url_batch:
        try:
            params = {'apikey': api_key, 'url': URL}
            response = requests.post(url, data=params)
            scan_id_list.append(response.json()['scan_id'])
        except ValueError as e:
            print("Rate limit detected:", e)
            continue
        except Exception as e:
            print("Error detected:", e)
            continue
    return scan_id_list

def report(scan_id_list, api_key):
    url = 'https://www.virustotal.com/vtapi/v2/url/report'
    report_list = []
    for id in scan_id_list:
        try:
            params = {'apikey': api_key, 'resource': id}
            response = requests.get(url, params=params)
            report_list.append(response.json())
        except ValueError as e:
            print("Rate limit detected:", e)
            continue
        except Exception as e:
            print("Error detected:", e)
            continue
    return report_list

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('link_fp', help="path to the file containing the links you want to scan")
    parser.add_argument('output_fp', help="path to your output file")
    parser.add_argument('response_fp', help='path to the response file you want to store')
    parser.add_argument('api_key', help='VirusTotal API key')
    args = parser.parse_args()

    url_list = []
    with open(args.link_fp) as f:
        for line in f:
            url_list.append(line.rstrip())

    output_file = open(args.output_fp, 'a')
    response_file = open(args.response_fp, 'a')

    vt_apikey = args.api_key
    response = []
    report_list = []

    for i in range(len(url_list)):
        if i % 4 == 0:
            time.sleep(60)
            url_batch = []
        url_batch.append(url_list[i])
        if i % 4 == 3 or i == len(url_list) - 1:
            response += scan(url_batch, vt_apikey)
            response_file.write('\n'.join(str(t) for t in response))

    print('Scan complete')

    for i in range(len(response)):
        if i % 4 == 0:
            time.sleep(60)
            scan_list = []
        scan_list.append(response[i])
        if i % 4 == 3 or i == len(response) - 1:
            reportBatch = report(scan_list, vt_apikey)
            report_list += reportBatch
            for r in reportBatch:
                json.dump(r, output_file)
                output_file.write("\n")

    output_file.close()
    response_file.close()

if __name__ == '__main__':
    main()
