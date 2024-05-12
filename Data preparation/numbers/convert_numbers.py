import pandas as pd
import re

# Conversion function
def convert_number_words_to_digits(sentence):
    # Mapping of number words to digits
    number_words_to_digits = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
        "ten": "10", "eleven": "11", "twelve": "12"
    }

    # Split the sentence into words and replace number words with digits
    new_sentence = ' '.join(number_words_to_digits.get(word.lower(), word) for word in sentence.split())

    return new_sentence

# Load the dataset
df = pd.read_csv('numbers/numbers_coco_dataframe.csv')

# Rename the 'caption' column to 'caption_words'
df.rename(columns={'caption': 'caption_words'}, inplace=True)

# Create a new column 'caption_digits' as a copy of 'caption_words'
df['caption_digits'] = df['caption_words'].copy()

df['caption_digits'] = df['caption_digits'].apply(convert_number_words_to_digits)
print(df.head(20))

df.to_csv('numbers/converted_numbers_coco_dataframe.csv', index=False)