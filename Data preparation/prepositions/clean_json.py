import json

# Load the original JSON data
with open('combined_prepositions_responses.json', 'r') as f:
    data = json.load(f)

# Filter out entries that are completely null
cleaned_data = {k: v for k, v in data.items() if not isinstance(v, list) or any(item is not None for item in v)}

# Save the cleaned JSON data
with open('cleaned_prepositions_responses.json', 'w') as f:
    json.dump(cleaned_data, f, indent=4)
