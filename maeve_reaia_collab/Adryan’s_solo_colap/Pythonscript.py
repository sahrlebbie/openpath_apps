import requests
import json

# API endpoints for different types of entities
api_endpoints = {
    "Netscreen Firewall Data": "https://api.recordedfuture.com/v2/ip/IP_Address_Demo_Events",
    "Symantec EP Data": "https://api.recordedfuture.com/v2/hash/Hash_Demo_Events",
    "ISC Bind": "https://api.recordedfuture.com/v2/domain/Domain_Demo_Events",
    "Squid Proxy Data": "https://api.recordedfuture.com/v2/url/URL_Demo_Events",
    "Tenable SC": "https://api.recordedfuture.com/v2/vulnerability/Vulnerability_Demo_Events"
}

# Function to fetch data from API and write to files
def fetch_and_write_data(api_endpoint, entity_name):
    response = requests.get(api_endpoint)
    if response.status_code == 200:
        data = response.json()["data"][:500]  # Get the first 500 events
        with open(f"{entity_name}_demo_events.json", "w") as file:
            json.dump(data, file, indent=4)
            print(f"Data for {entity_name} fetched and saved to {entity_name}_demo_events.json")
    else:
        print(f"Failed to fetch data for {entity_name}. Status code: {response.status_code}")

# Fetch data from each API endpoint and write to files
for entity_name, api_endpoint in api_endpoints.items():
    fetch_and_write_data(api_endpoint, entity_name)
