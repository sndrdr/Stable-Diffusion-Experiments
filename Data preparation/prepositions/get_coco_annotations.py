import json
import pandas as pd

# Path to the COCO annotations file in the local directory
path_to_coco = 'coco/annotations/captions_val2017.json'

# Load the annotations from the JSON file
with open(path_to_coco, 'r') as file:
    annotations = json.load(file)

# Create a DataFrame from the annotations
initial_df = pd.DataFrame(annotations['annotations'])

# Shuffle the DataFrame
df = initial_df.sample(frac=1).reset_index(drop=True)

# Save the original DataFrame to a CSV file in the same directory
original_file_path = 'original_coco_dataframe.csv'
initial_df.to_csv(original_file_path, index=False)

# Add new columns with initial values to the shuffled DataFrame
df['preposition'] = None
df['subject'] = None
df['object'] = None
df['verb'] = None
df['wrong_preposition'] = None
df['wrong_caption'] = None

# Display the shuffled DataFrame to verify the initial state
print(df.head())

# Save only the first 1000 rows of the shuffled DataFrame to a new CSV file
first_1000_file_path = 'first_1000_coco_dataframe.csv'
df.head(1000).to_csv(first_1000_file_path, index=False)