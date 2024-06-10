import pandas as pd
import numpy as np
import random

def choose_different_preposition(prepositions, current):
    """
    Choose a random preposition from the list that's not the current one.
    """
    choices = [p for p in prepositions if p != current]
    return random.choice(choices) if choices else current

def replace_first_instance(caption, original, replacement):
    """
    Replace the first instance of the original preposition in the caption with the replacement.
    """
    words = caption.split()
    for i, word in enumerate(words):
        # Check if the word matches the original preposition and replace it
        if word == original:
            words[i] = replacement
            break
    return ' '.join(words)

# Load the dataset
df = pd.read_csv('coco_augmented_dataframe.csv')

# List of unique prepositions
unique_prepositions = df['preposition'].dropna().unique().tolist()

# Apply functions to generate wrong_preposition and wrong_caption
df['wrong_preposition'] = df.apply(lambda row: choose_different_preposition(unique_prepositions, row['preposition']), axis=1)
df['wrong_caption'] = df.apply(lambda row: replace_first_instance(row['caption'], row['preposition'], row['wrong_preposition']), axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('final_coco_dataframe.csv', index=False)

print("File saved as 'final_coco_dataframe.csv' with updated 'wrong_preposition' and 'wrong_caption' columns.")
