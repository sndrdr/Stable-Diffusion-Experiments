import pandas as pd

# Load the data from two CSV files
df1 = pd.read_csv('and/and_generated_sentences_1.csv')
df2 = pd.read_csv('and/and_generated_sentences_2.csv')

# Concatenate the two dataframes
combined_df = pd.concat([df1, df2])

# Take only the first 50 rows of the united DataFrame
final_df = combined_df.head(50)

# Print the first few rows to check the DataFrame
print(final_df.head())

final_df.to_csv('and/and_generated_sentences.csv', index=False)