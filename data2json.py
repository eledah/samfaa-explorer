import pandas as pd
import json
import numpy as np

# Load the Excel file
df = pd.read_excel('combined_data.xlsx')

# Load province data from JSON file
with open('province.json', 'r', encoding='utf-8') as f:
    province_data = json.load(f)

# Create a mapping from province_id to province name
province_map = {item['value']: item['label'] for item in province_data['data']}

# Select the required columns
selected_columns = [
    'title', 'distribution_title', 'image_url', 'persian_date', 
    'tickets_count', 'venue_count', 'schedule_count', 'final_price', 
    'province_id', 'screening_id'
]
df_selected = df[selected_columns]

# Replace NaN values with empty strings
df_selected = df_selected.replace({np.nan: ''})

# Convert province_id to province name
df_selected['province_id'] = df_selected['province_id'].map(province_map)

# Convert the DataFrame to a list of dictionaries
data_list = df_selected.to_dict(orient='records')

# Save the list of dictionaries as a JSON file
with open('combined_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)

print("Excel data has been converted to JSON and saved to combined_data.json")
