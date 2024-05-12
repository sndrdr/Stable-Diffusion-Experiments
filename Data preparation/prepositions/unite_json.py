import json
import os

# Directory where JSON files are stored
directory_path = '.'

# Combined data dictionary
combined_data = {}

# Keep track of the next index to use
next_index = 0

# List of JSON file names
file_names = [f"prepositions_responses_{i}.json" for i in range(100, 1100, 100)]

# Loop through each JSON file
for file_name in file_names:
    file_path = os.path.join(directory_path, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Adjust keys and add to the combined dictionary
            new_data = {}
            for key, value in data.items():
                new_data[str(next_index)] = value
                next_index += 1
            combined_data.update(new_data)

# Path for the new combined JSON file
output_file_path = 'combined_prepositions_responses.json'
with open(output_file_path, 'w') as output_file:
    json.dump(combined_data, output_file, indent=4)

print("All JSON files have been combined into one with unique indices.")