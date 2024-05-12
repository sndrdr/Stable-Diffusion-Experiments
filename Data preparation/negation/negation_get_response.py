import openai
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_KEY")

# Initialize the DataFrame with appropriate columns for negation
df = pd.DataFrame(columns=['sentence', 'negation', 'negated_noun'])

def generate_sentences():
    """ Generate sentences containing negations and return the text response. """
    prompt = f"""
    Generate five simple sentences suitable for creating images, each containing a negation. 
    Ensure it is clear from the sentence that the negated noun or entity should not be depicted in the image. 
    After each sentence, list the negation used and the noun or entity that is negated, each on new lines.
    Please provide your response in the following format, without any numbers, dashes, or other marks:
    Sentence
    Negation
    Negated noun or entity
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a creative assistant."},
                  {"role": "user", "content": prompt}],
        max_tokens=250,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    text_response = response['choices'][0]['message']['content'].strip()
    return text_response

def parse_sentences(text_response):
    """ Parse the generated sentences and append them to the DataFrame. """
    lines = [line.strip() for line in text_response.split('\n') if line.strip()]
    print("Filtered Lines:", lines)  # Debug to see filtered lines

    for i in range(0, len(lines), 3):
        try:
            sentence = lines[i]
            negation = lines[i + 1] if i + 1 < len(lines) else None
            negated_noun = lines[i + 2] if i + 2 < len(lines) else None
        except IndexError:
            print(f"Error processing lines at index {i}: Not enough data for a complete set.")
            continue

        # Append to the DataFrame
        df.loc[len(df)] = [sentence, negation, negated_noun]
        print(f"Processed - Sentence: '{sentence}', Negation: '{negation}', Negated Noun: '{negated_noun}'")

# Generate sentences and parse them
for _ in range(6):
    text_response = generate_sentences()
    parse_sentences(text_response)

# Save the DataFrame to a CSV file
df.to_csv('negation_generated_sentences.csv', index=False)
print("DataFrame saved to CSV.")