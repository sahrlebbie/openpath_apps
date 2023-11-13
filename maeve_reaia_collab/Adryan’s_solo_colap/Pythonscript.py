import os
import requests
import json
import random
import string

# API endpoints for different types of entities
api_endpoints = {
    "Netscreen Firewall Data": "https://api.recordedfuture.com/v2/ip/IP_Address_Demo_Events",
    "Symantec EP Data": "https://api.recordedfuture.com/v2/hash/Hash_Demo_Events",
    "ISC Bind": "https://api.recordedfuture.com/v2/domain/Domain_Demo_Events",
    "Squid Proxy Data": "https://api.recordedfuture.com/v2/url/URL_Demo_Events",
    "Tenable SC": "https://api.recordedfuture.com/v2/vulnerability/Vulnerability_Demo_Events"
}

# Splunk configuration parameters
index = "your_index_name"
sourcetype = "your_sourcetype_name"

# Directory for sample logs
log_directory = "var/log/app_test"

# Create the log directory if it doesn't exist
os.makedirs(log_directory, exist_ok=True)

# Output directory for inputs.conf
output_directory = "/opt/splunk/etc/system/local/"

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# API token for authentication
token = "heretoken"

# Function to generate sample log data and save to file
def generate_and_save_sample_data(entity, endpoint):
    formatted_entity_name = entity.replace(" ", "_").lower()
    file_start_name = f"{formatted_entity_name}_sample_logs"
    filename = os.path.join(log_directory, f"{file_start_name}.log")

    sample_data = {
        "timestamp": "2023-11-13T12:00:00Z",
        "event_type": "sample_event",
        "source_ip": f"192.168.1.{random.randint(1, 255)}",
        "destination_ip": f"10.0.0.{random.randint(1, 255)}",
        "message": "This is a sample log message.",
        "hash_value": ''.join(random.choices(string.hexdigits, k=32)),
        "url": f"http://example.com/{formatted_entity_name}",
        "vulnerability_id": f"VULN-{random.randint(1000, 9999)}"
    }

    # Save sample data to file
    with open(filename, "w") as file:
        json.dump(sample_data, file, indent=4)
    print(f"Sample logs generated for {endpoint} and saved to {filename}")

    # Create Splunk inputs.conf monitoring stanza
    inputs_conf_content = f"[monitor://{log_directory}/{file_start_name}*.log]\nindex = {index}\nsourcetype = {sourcetype}\ndisabled = false\n"
    
    # Save inputs.conf content to a file in the specified output directory
    inputs_conf_filename = os.path.join(output_directory, "inputs.conf")
    with open(inputs_conf_filename, "a") as inputs_conf_file:
        inputs_conf_file.write(inputs_conf_content)

# Generate sample logs for each API endpoint
for entity, endpoint in api_endpoints.items():
    generate_and_save_sample_data(entity, endpoint)
