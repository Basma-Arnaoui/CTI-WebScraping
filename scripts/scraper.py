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

    # Create a map for each CVE containing ID, description, and scores
    cve_map = {}
    for cve in cve_items:
        cve_id = cve['cve']['id']
        description = cve['cve']['descriptions'][0]['value']
        metrics_v30 = cve['cve']['metrics'].get('cvssMetricV30', [])
        metrics_v31 = cve['cve']['metrics'].get('cvssMetricV31', [])

        metrics = metrics_v30 + metrics_v31
        scores = {}

        if metrics:
            for metric_data in metrics:
                scores['baseScore'] = metric_data['cvssData']['baseScore']
                scores['exploitabilityScore'] = metric_data.get('exploitabilityScore', 'Score not available')
                scores['impactScore'] = metric_data.get('impactScore', 'Score not available')
        else:
            scores = {'baseScore': 'Score not available', 'exploitabilityScore': 'Score not available', 'impactScore': 'Score not available'}

        cve_map[cve_id] = {'description': description, 'scores': scores}

    # Sort CVEs based on the chosen metric
    sorted_cves = sorted(cve_map.items(), key=lambda x: x[1]['scores'].get(metric, 0), reverse=True)

    # Get the top X trending CVEs
    top_cves = [cve[1] for cve in sorted_cves[:num_results]]
    return top_cves


# Function to display the CVEs with all three scores
def display_cves(cves):
    for cve_id, cve_data in cves.items():
        description = cve_data['description']
        scores = cve_data['scores']
        base_score = scores['baseScore']
        exploitability_score = scores['exploitabilityScore']
        impact_score = scores['impactScore']

        print(f"{cve_id}: {description}")
        print(f"Base Score: {base_score}")
        print(f"Exploitability Score: {exploitability_score}")
        print(f"Impact Score: {impact_score}\n")


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
