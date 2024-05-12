import os
import openai
import pandas as pd
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_KEY")

# Load dataframe
df = pd.read_csv('first_1000_coco_dataframe.csv')

# Pre-allocate columns for the results
df['preposition'] = None
df['subject'] = None
df['object'] = None
df['verb'] = None

# Function to generate prompt and parse response
def process_caption(caption):
    if pd.isna(caption):
        return None, None, None, None  # Handle NaN values gracefully

    prompt = f"""
    Analyze the given sentence carefully:
    - Identify the first preposition or complex preposition (e.g., 'in front of', 'on top of'). 
    - List the two nouns or entities connected by this preposition.
    - Determine the main verb (predicate) that directly relates to the preposition and its connected nouns. Provide only the first relevant verb that directly follows or corresponds to this noun-preposition construction.
    
    Please provide your response in the following structured format, maintaining the original case of the words and noting 'None' where information is not available or unclear:
    - Preposition: [first preposition / complex preposition or 'None' if not clear]
    - Subject: [first noun/entity directly involved with the preposition or 'None']
    - Object: [second noun/entity directly involved with the preposition or 'None']
    - Verb: [first main verb related to the preposition-noun construction or 'None' if unclear]

    Sentence: '{caption}'
    Ensure your response strictly follows this format.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Please analyze the sentence grammatically, maintaining the exact word case, and provide a structured response."},
                  {"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.5
    )

    text_response = response['choices'][0]['message']['content'].strip()
    return text_response

# Parsing function to extract data from API response
def parse_response(response):
    if not response or isinstance(response, tuple):
        return None, None, None, None  # Handle missing or unexpected responses
    
    data = {}
    lines = response.split('\n')
    for line in lines:
        # Debug print to see how lines are being processed
        # print("Line being processed:", line)
        # Check if line contains the expected pattern before processing
        if ': ' in line:
            key, value = line.split(': ', 1)
            key = key.strip().lower().replace('-', '').strip()  # Removing hyphens and extra spaces
            value = value.strip()
            data[key] = value if value != 'None' else None
            # Debug print to see data entries being added
            # print("Data entry added:", key, data[key])

    preposition = data.get('preposition')
    subject = data.get('subject')
    object = data.get('object')
    verb = data.get('verb')
    
    return preposition, subject, object, verb

# Collect responses and save them
"""
responses = {}
for index, row in df.iterrows():
    response = process_caption(row['caption'])
    responses[str(index)] = response
    print(f"API Response for row {index}: {response}")

# Save to file
with open('prepositions_responses.json', 'w') as f:
    json.dump(responses, f, indent=4)
"""

responses = {}
batch_size = 100  # Define batch size for processing and saving progress
for index, row in df.iterrows():
    if index % batch_size == 0 and index > 0:  # Save periodically
        with open(f'prepositions_responses_{index}.json', 'w') as file:
            json.dump(responses, file, indent=4)
            responses = {}  # Reset the dictionary after saving to minimize memory usage

    response = process_caption(row['caption'])
    responses[index] = response
    print(f"API Response for row {index}: {response}")

# Save all responses at the end
with open('prepositions_responses_final.json', 'w') as file:
    json.dump(responses, file, indent=4)