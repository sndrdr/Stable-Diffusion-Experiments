import pandas as pd
import json
import re

# Load saved responses
with open('cleaned_reindexed_prepositions_responses.json', 'r') as f:
    saved_responses = json.load(f)

# Load dataframe
df = pd.read_csv('cleaned_first_1000_coco_dataframe.csv')

# Pre-allocate columns for the results
df['preposition'] = None
df['subject'] = None
df['object'] = None
df['verb'] = None

# Parsing function to extract data from API response and clean text
def parse_response(response):
    # Default values for cases where response is None or inappropriate format
    default_values = (None, None, None, None)
    
    # Handle case where response is a list with all None values or is empty
    if isinstance(response, list) and (not response or all(r is None for r in response)):
        return default_values
    
    # Handle the string case expected from valid responses
    if isinstance(response, str):
        data = {}
        lines = response.split('\n')
        for line in lines:
            if ': ' in line:
                key, value = line.split(': ', 1)
                key = key.strip().lower().replace('-', '').strip()
                value = re.sub(r'[\'\"]', '', value.strip())  # Remove quotes
                data[key] = value if value not in ['None', ''] else None
        return data.get('preposition'), data.get('subject'), data.get('object'), data.get('verb')

    # Return default values if response format is unexpected
    return default_values

# Update DataFrame using saved responses
response_index = 0
df_index = 0

while response_index < len(saved_responses) and df_index < len(df):
    response = list(saved_responses.values())[response_index]
    preposition, subject, object, verb = parse_response(response)
    
    # Move to the next JSON response if preposition or subject are None
    if preposition is None or subject is None:
        print(f"JSON Index {response_index} skipped - Missing Preposition or Subject.")
        response_index += 1
        continue
    
    # Loop through DataFrame rows starting from the last checked index
    while df_index < len(df):
        caption = df.at[df_index, 'caption'] if 'caption' in df.columns else ""
        
        # Check if both preposition and subject are found in the caption
        if preposition and subject and (caption.lower().find(preposition.lower()) != -1) and (caption.lower().find(subject.lower()) != -1):
            df.at[df_index, 'preposition'] = preposition
            df.at[df_index, 'subject'] = subject
            df.at[df_index, 'object'] = object
            df.at[df_index, 'verb'] = verb
            print(f"Updated Row {df_index} with JSON Index {response_index} - Preposition: {preposition}, Subject: {subject}, Object: {object}, Verb: {verb}")
            response_index += 1  # Move to the next JSON response after a successful update
            df_index += 1  # Move to the next row after a successful update
            break  # Exit while to reset with the next JSON response
        else:
            df_index += 1  # Try the next DataFrame row with the same JSON response
            print(f"Skipped Row {df_index} with JSON Index {response_index} - Preposition '{preposition}' or Subject '{subject}' not in caption: '{caption}'")

# Save the updated dataframe
print(df.head())
df.to_csv('first_1000_coco_augmented_dataframe.csv', index=False)
print("Augmented dataframe saved.")
