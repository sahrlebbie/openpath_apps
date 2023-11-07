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

# API token for authentication
api_token = b99387003c734a009de5bba715578b93

# Function to fetch data from API and save to file
def fetch_and_save_data(endpoint, filename):
    headers = {
        "X-RFToken": api_token
    }
    response = requests.get(endpoint, headers=headers, params={"limit": 500})
    if response.status_code == 200:
        data = response.json()
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data fetched from {endpoint} and saved to {filename}")
    else:
        print(f"Failed to fetch data from {endpoint}. Status code: {response.status_code}")

# Fetch data from each API endpoint and save to files
for entity, endpoint in api_endpoints.items():
    formatted_entity_name = entity.replace(" ", "_").lower()
    filename = f"{formatted_entity_name}_demo_events.json"
    fetch_and_save_data(endpoint, filename)
