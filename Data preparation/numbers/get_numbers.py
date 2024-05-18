import pandas as pd
import re

# Function to check if the sentence contains a digit
def contains_digit(sentence):
    return bool(re.search(r'\d', sentence))

# Function to check if the sentence contains numbers as words
def contains_number_word(sentence):
    number_words = set(["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"])
    return bool(number_words.intersection(sentence.lower().split()))

# Load the dataset
df = pd.read_csv('numbers/cleaned_checked_coco_dataframe.csv')

df_digits_orig = df[df['caption'].apply(contains_digit)]
df_words = df[df['caption'].apply(contains_number_word)]

print(df_digits_orig.head(20))
print(df_words.head(20))

total_with_digits = len(df_digits_orig)
total_with_number_words = len(df_words)

print(f"Total sentences with digits: {total_with_digits}")
print(f"Total sentences with number words: {total_with_number_words}")

df_words.to_csv('numbers/numbers_coco_dataframe.csv', index=False)