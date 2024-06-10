import json

# Load the JSON file
with open('cleaned_prepositions_responses.json', 'r') as file:
    data = json.load(file)

# Create a new dictionary with continuous indices
new_data = {}
index = 0  # Start with index 0
for key in sorted(data.keys(), key=int):  # Ensure keys are sorted
    new_data[str(index)] = data[key]
    index += 1

# Save the updated data back to a JSON file
with open('cleaned_reindexed_prepositions_responses.json', 'w') as file:
    json.dump(new_data, file, indent=4)

print("JSON indices have been updated.")
