import openai
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_KEY")

# Initialize the DataFrame
df = pd.DataFrame(columns=['sentence', 'conjunction', 'first_noun', 'second_noun'])

def generate_sentences(conjunction_type):
    """ Generate sentences containing specified conjunctions and return the text response. """
    prompt = f"""
    Generate ten simple sentences suitable for creating images, each containing the conjunction '{conjunction_type}'. Ensure both nouns or entities connected by '{conjunction_type}' are to be depicted in the image. After each sentence, list the two connected nouns or entities on new lines.
    Please provide your response in the following format, without any numbers, dashes, or other marks:
    Sentence
    First noun or entity
    Second noun or entity
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a creative assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=350,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    text_response = response['choices'][0]['message']['content'].strip()
    return text_response

def parse_sentences(text_response, conjunction_type):
    """ Parse the generated sentences and append them to the DataFrame. """
    lines = [line.strip() for line in text_response.split('\n') if line.strip()]
    for i in range(0, len(lines), 3):
        try:
            sentence = lines[i]
            first_noun = lines[i + 1] if i + 1 < len(lines) else None
            second_noun = lines[i + 2] if i + 2 < len(lines) else None
        except IndexError:
            print(f"Error processing lines at index {i}: Not enough data for a complete set.")
            continue

        df.loc[len(df)] = [sentence, conjunction_type, first_noun, second_noun]
        print(f"Processed - Sentence: '{sentence}', First Noun: '{first_noun}', Second Noun: '{second_noun}'")

# Generate sentences and parse them for each conjunction type
conjunctions = ["and", "as well as", "both... and...", "along with"]
for conj in conjunctions:
    text_response = generate_sentences(conj)
    parse_sentences(text_response, conj)

# Save the DataFrame to a CSV file
df.to_csv('and_generated_sentences.csv', index=False)
print("DataFrame saved to CSV.")