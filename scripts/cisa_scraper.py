import requests
from bs4 import BeautifulSoup


def scrape_cisa_known_exploited_vulnerabilities():
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    response = requests.get(url)
    data = response.json()

    if "vulnerabilities" not in data:
        print("No vulnerabilities data found.")
        return []

    vulnerabilities_data = data["vulnerabilities"]
    cve_data = []

    for vulnerability in vulnerabilities_data:
        cve_id = vulnerability.get("cveID", "")
        vendor_project = vulnerability.get("vendorProject", "")
        product = vulnerability.get("product", "")
        vulnerability_name = vulnerability.get("vulnerabilityName", "")
        date_added = vulnerability.get("dateAdded", "")
        short_description = vulnerability.get("shortDescription", "")
        required_action = vulnerability.get("requiredAction", "")
        due_date = vulnerability.get("dueDate", "")
        known_ransomware_campaign_use = vulnerability.get("knownRansomwareCampaignUse", "")
        notes = vulnerability.get("notes", "")

        cve_info = {
            "CVE ID": cve_id,
            "Vendor Project": vendor_project,
            "Product": product,
            "Vulnerability Name": vulnerability_name,
            "Date Added": date_added,
            "Short Description": short_description,
            "Required Action": required_action,
            "Due Date": due_date,
            "Known Ransomware Campaign Use": known_ransomware_campaign_use,
            "Notes": notes,
            "Score": None  # Placeholder for the score, to be filled later
        }

        cve_data.append(cve_info)

    return cve_data



def get_cvss_score(cve_id):
    # Construct the URL for the CVE detail page on NVD
    url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"

    # Fetch the page content
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the CVSS v3 score using the first format
    score_element = soup.find('a', {'data-testid': 'vuln-cvss3-panel-score'})

    # If the first format is not found, try the second format
    if not score_element:
        score_element = soup.find('a', {'data-testid': 'vuln-cvss3-cna-panel-score'})


    if score_element:
        score_text = score_element.text.strip()

        return score_text
    else:
        return "Score not found"


if __name__ == "__main__":
    cve_list = scrape_cisa_known_exploited_vulnerabilities()
    no_score_count = 0

    for i, cve in enumerate(cve_list[:100]):
        cve_id = cve['CVE ID']
        score = get_cvss_score(cve_id)
        if score == "Score not found":
            no_score_count += 1
        print(f"CVE ID: {cve_id}, Score: {score}")

    print(f"\nTotal CVEs checked: {min(100, len(cve_list))}")
    print(f"Number of CVEs without a score: {no_score_count}")
