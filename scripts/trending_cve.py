import requests
from datetime import datetime, timedelta

# Function to get today's CVEs from NVD
def get_trending_cves(num_results, metric):
    # Get today's date in the required format
    today = datetime.utcnow().date()
    start_date = today.isoformat()
    end_date = (today + timedelta(days=1)).isoformat()  # To ensure we get all today's CVEs

    # NVD 2.0 API URL
    URL = f'https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate={start_date}T00:00:00.000Z&pubEndDate={end_date}T00:00:00.000Z'
    print(URL)
    # Send a request to the URL
    response = requests.get(URL)
    response.raise_for_status()

    # Parse the JSON response
    try:
        cve_data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print("JSONDecodeError: Unable to parse response as JSON")
        print(response.text)
        return []

    # Extract CVE items
    cve_items = cve_data.get('vulnerabilities', [])

    # Define a function to get the score based on the chosen metric
    def get_score(cve, metric):
        try:
            return cve['cve']['metrics']['cvssMetricV31'][0][metric]
        except (KeyError, IndexError):
            return 0

    # Sort CVEs based on the chosen metric
    cve_items.sort(key=lambda x: get_score(x, metric), reverse=True)

    # Get the top X trending CVEs
    top_cves = cve_items[:num_results]

    return top_cves

# Function to display the CVEs
def display_cves(cves):
    for cve in cves:
        cve_id = cve['cve']['id']
        description = cve['cve']['descriptions'][0]['value']
        print(f"{cve_id}: {description}")

# Main function
def main():
    # Number of results to display
    num_results = int(input("Enter number of results to display: "))

    # Available metrics for sorting
    metrics = {
        "1": "baseScore",
        "2": "exploitabilityScore",
        "3": "impactScore"
    }

    # Display metrics options to the user
    print("Choose a metric to sort by:")
    print("1: Base Score")
    print("2: Exploitability Score")
    print("3: Impact Score")

    # Get the user's choice
    metric_choice = input("Enter the number corresponding to the metric: ")

    # Validate the user's choice
    if metric_choice not in metrics:
        print("Invalid choice. Please run the script again and choose a valid option.")
        return

    # Get the selected metric
    metric = metrics[metric_choice]

    # Get trending CVEs based on the selected metric
    trending_cves = get_trending_cves(num_results, metric)

    # Display the trending CVEs
    print(f"\nTop {num_results} trending CVEs sorted by {metric}:")
    display_cves(trending_cves)

if __name__ == "__main__":
    main()
