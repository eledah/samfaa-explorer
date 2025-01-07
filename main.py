import os
import requests
import pandas as pd
from tqdm import tqdm  # For progress bar

# Create the json_data folder if it doesn't exist
if not os.path.exists('json_data'):
    os.makedirs('json_data')

# Base URL
base_url = "https://panel.samfaa.ir/admin/report/recent_shows"

# Initialize an empty list to store all data
all_data = []

# Iterate over province_id (1 to 31) and screening_id (1400 to 1403)
for province_id in tqdm(range(1, 32), desc="Processing provinces"):
    for screening_id in range(1400, 1404):
        # Define the filename
        filename = f"json_data/province_{province_id}_screening_{screening_id}.json"

        # Skip if the file already exists
        if os.path.exists(filename):
            print(f"Skipping existing file: {filename}")
            continue

        # Construct the URL
        params = {
            "recently": "all",
            "province_id": province_id,
            "screening_id": screening_id,
            "from": "",
            "to": ""
        }

        # Send a GET request to download the JSON file
        response = requests.get(base_url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the JSON file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"Downloaded: {filename}")
        else:
            print(f"Failed to download: {filename} (Status Code: {response.status_code})")
            continue

        # Load the JSON data
        with open(filename, 'r', encoding='utf-8') as f:
            json_data = response.json()

        # Check if the JSON data contains the "data" key
        if "data" in json_data:
            # Add province_id and screening_id to each row in the data
            for item in json_data["data"]:
                item["province_id"] = province_id
                item["screening_id"] = screening_id

            # Append the data to the list
            all_data.extend(json_data["data"])

# Convert the combined data into a DataFrame
df = pd.json_normalize(all_data, sep='_')

# Save the DataFrame to an Excel file
output_file = "combined_data.xlsx"
df.to_excel(output_file, index=False)

print(f"All data has been combined and saved to {output_file}")