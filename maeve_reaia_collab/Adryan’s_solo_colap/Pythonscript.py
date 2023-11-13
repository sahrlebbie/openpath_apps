import os
import requests
from configparser import ConfigParser

# Read API token from token.ini
config = ConfigParser()
config.read("/Applications/Splunk/etc/apps/api_calls/token.ini")
API_TOKEN = config.get("API", "TOKEN")

OUTPUT_DIRECTORY = "/Applications/Splunk/etc/apps/api_calls/log"  # Update this with the desired directory path
INPUT_DIRECTORY = "/Applications/Splunk/etc/system/local"  # Add leading slash to the path

# Define API endpoints
API_ENDPOINTS = [
    "https://api.recordedfuture.com/v2/ip/demoevents?limit=1000",
    "https://api.recordedfuture.com/v2/hash/demoevents?limit=1000",
    "https://api.recordedfuture.com/v2/domain/demoevents?limit=1000",
    "https://api.recordedfuture.com/v2/url/demoevents?limit=1000",
    "https://api.recordedfuture.com/v2/vulnerability/demoevents?limit=1000"
]

# Ensure the output directory exists
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# Map entity types to index and sourcetype values
entity_type_mapping = {
    "ip": {"index": "ip_index", "sourcetype": "ip_sourcetype"},
    "hash": {"index": "hash_index", "sourcetype": "hash_sourcetype"},
    "domain": {"index": "domain_index", "sourcetype": "domain_sourcetype"},
    "url": {"index": "url_index", "sourcetype": "url_sourcetype"},
    "vulnerability": {"index": "vuln_index", "sourcetype": "vuln_sourcetype"}
}

# List to store created JSON files
created_files = []

# Loop through API endpoints and make requests
for endpoint in API_ENDPOINTS:
    entity_name = endpoint.split("/")[-2].lower()
    filename = f"{entity_name}_demo_events.json"
    file_path = os.path.join(OUTPUT_DIRECTORY, filename)

    headers = {"X-RFToken": API_TOKEN}
    response = requests.get(endpoint, headers=headers)

    with open(file_path, "w") as file:
        file.write(response.text)

    created_files.append((file_path, entity_name))
    print(f"Data fetched from {endpoint} and saved to {file_path}")

# Generate inputs.conf content
inputs_conf_content = ""
for file_path, entity_name in created_files:
    file_name = os.path.basename(file_path).split(".")[0]
    index = entity_type_mapping[entity_name]["index"]
    sourcetype = entity_type_mapping[entity_name]["sourcetype"]
    inputs_conf_content += f"\n[monitor://{file_path}]\nindex = {index}\nsourcetype = {sourcetype}\ndisabled = false\n"

# Write inputs.conf content to file
inputs_conf_path = os.path.join(INPUT_DIRECTORY, "inputs.conf")
with open(inputs_conf_path, "w") as inputs_conf_file:
    inputs_conf_file.write(inputs_conf_content)

print(f"inputs.conf content written to {inputs_conf_path}")
