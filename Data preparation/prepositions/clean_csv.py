import pandas as pd
import re

def clean_text(text):
    """
    Clean unwanted space patterns in text.
    """
    # Replace double spaces with single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Remove space before a dot
    text = re.sub(r'\s\.', '.', text)
    # Remove space after a dot
    text = re.sub(r'\.\s', '.', text)
    # Remove space before a comma
    text = re.sub(r'\s,', ',', text)
    return text

# Load the dataset
df = pd.read_csv('first_1000_coco_augmented_dataframe.csv')

# Filter out rows where the 'preposition' column is empty
df_filtered = df[df['preposition'].notna()]

# Clean the 'caption' column
df_filtered['caption'] = df_filtered['caption'].apply(clean_text)

# Save the filtered data to a new CSV file
df_filtered.to_csv('coco_augmented_dataframe.csv', index=False)

# Print the number of rows in the filtered DataFrame
print(f"Number of rows in the filtered DataFrame: {df_filtered.shape[0]}")

# Print the number of rows in the original DataFrame for comparison
print(f"Number of rows in the original DataFrame: {df.shape[0]}")