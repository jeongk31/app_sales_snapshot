import json
import pandas as pd
import os

def convert_json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    # Determine the key that contains the rows
    if 'rows' in data:
        rows = data['rows']
    elif 'data' in data:
        rows = data['data']
    else:
        raise KeyError("JSON response does not contain 'rows' or 'data' keys.")

    # Handle headers
    if 'headers' in data:
        headers = data['headers']
    elif 'header' in data:
        headers = data['header']
    else:
        # Use the first row's keys if headers are not explicitly provided
        headers = rows[0].keys() if isinstance(rows[0], dict) else []

    # Clean rows if necessary
    cleaned_rows = []
    for row in rows:
        if isinstance(row, dict):
            cleaned_rows.append(row.values())
        else:
            cleaned_rows.append(row)
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(cleaned_rows, columns=headers)
    df.to_csv(csv_file_path, index=False)
    print(f"CSV content saved to {csv_file_path}")

# Example usage
json_files = ["edited_output_table.json"]
for json_file in json_files:
    csv_file = json_file.replace('.json', '.csv')
    convert_json_to_csv(json_file, csv_file)
