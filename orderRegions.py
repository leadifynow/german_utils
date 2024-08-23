import pandas as pd

# Read the data from the local CSV file
file_path = r'D:\malej\Downloads\Quinterock - Mayo (2).csv'  # Use raw string notation for Windows file path
df = pd.read_csv(file_path)

# Create a mapping from Publication to its index
publication_order = {pub: i for i, pub in enumerate(df['Publication'])}

# Sort REGION based on the Publication order
ordered_regions = df.set_index('Publication').loc[df['Publication']].reset_index()['REGION']

# Create a new DataFrame with the ordered REGION
ordered_regions_df = pd.DataFrame({'REGION': ordered_regions})

# Print the ordered list of REGION
print("Ordered list of REGION:")
print(ordered_regions_df)

# Save the ordered list of REGION to a new CSV file
output_file_path = r'D:\malej\Downloads\ordered_Regions.csv'  # Use raw string notation for Windows file path
ordered_regions_df.to_csv(output_file_path, index=False)