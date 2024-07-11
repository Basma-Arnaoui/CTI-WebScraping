import requests
from bs4 import BeautifulSoup
import sqlite3
import os
DATABASE = os.path.join(os.path.dirname(__file__), '..', 'cve.db')

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

def update_cve_table():
    # Connect to the database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get the current count of CVEs in the database
    cursor.execute("SELECT COUNT(*) FROM cves")
    current_cve_count = cursor.fetchone()[0]

    # Fetch the JSON data again to get the current count
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    response = requests.get(url)
    data = response.json()
    json_cve_count = data["count"]

    # If the count in JSON is greater, add new CVEs
    if json_cve_count > current_cve_count:
        # Scrape to get the new CVEs
        new_cves = scrape_cisa_known_exploited_vulnerabilities()
        existing_cves = set(row[0] for row in cursor.execute("SELECT cve_id FROM cves").fetchall())
        for cve_info in new_cves:
            if cve_info["CVE ID"] not in existing_cves:
                cve_info["Score"] = get_cvss_score(cve_info["CVE ID"])
                cursor.execute("""
                    INSERT INTO cves (
                        cve_id, vendor_project, product, vulnerability_name, date_added,
                        short_description, required_action, due_date,
                        known_ransomware_campaign_use, notes, score
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cve_info["CVE ID"], cve_info["Vendor Project"], cve_info["Product"],
                    cve_info["Vulnerability Name"], cve_info["Date Added"],
                    cve_info["Short Description"], cve_info["Required Action"],
                    cve_info["Due Date"], cve_info["Known Ransomware Campaign Use"],
                    cve_info["Notes"], cve_info["Score"]
                ))
        conn.commit()

    conn.close()


if __name__ == "__main__":
    update_cve_table()
