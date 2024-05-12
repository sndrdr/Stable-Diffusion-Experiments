import pandas as pd
import re

def clean_text(text):
    """
    Clean unwanted space patterns and ensure proper punctuation in text.
    """
    # Replace double spaces with single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Remove space before a dot
    text = re.sub(r'\s\.', '.', text)
    # Remove space after a dot
    text = re.sub(r'\.\s', '.', text)
    # Remove space before a comma
    text = re.sub(r'\s,', ',', text)
    # Ensure text ends with a dot
    if not text.endswith('.'):
        text += '.'
    return text

# Load the dataset
df = pd.read_csv('numbers/original_coco_dataframe.csv')

# Clean the 'caption' column
df['caption'] = df['caption'].apply(clean_text)

# Save the filtered data to a new CSV file
df.to_csv('numbers/cleaned_coco_dataframe.csv', index=False)

df_2 = pd.read_csv('numbers/manually_checked_coco_dataframe.csv')
df_2['caption'] = df_2['caption'].apply(clean_text)
df_2 = df_2.head(10000)
df_2.to_csv('numbers/cleaned_checked_coco_dataframe.csv', index=False)