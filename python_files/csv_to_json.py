import pandas as pd
import json
import os

def convert_csv_to_json(csv_file_path, json_file_path):
    # Read CSV file into DataFrame
    df = pd.read_csv(csv_file_path)
    
    # Convert DataFrame to dictionary
    data = {
        "headers": df.columns.tolist(),
        "rows": df.to_dict(orient='records')
    }
    
    # Write dictionary to JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    
    print(f"JSON content saved to {json_file_path}")

# Example usage
csv_files = ["sample1.csv", "sample3.csv"]
for csv_file in csv_files:
    json_file = csv_file.replace('.csv', '.json')
    convert_csv_to_json(csv_file, json_file)
