import pandas as pd
import re
from unidecode import unidecode

file_path = "D:\\malej\\Downloads\\instantly_leads (2).csv"
df = pd.read_csv(file_path)

def clean_company_name(name):
    if pd.isna(name):
        return name
    cleaned_name = re.sub(r'[^\w\s]', '', str(name), flags=re.IGNORECASE)
    cleaned_name = unidecode(cleaned_name)
    return cleaned_name

# Apply the cleaning function
df['companyName'] = df['companyName'].apply(clean_company_name)

# Filter the dataframe: keep rows where 'companyName' starts with an uppercase letter
filtered_df = df[df['companyName'].str.match(r'^[A-Z]')]

# Save the filtered rows in another list (not saved to a file but stored in-memory as a DataFrame)
filtered_rows_list = filtered_df.copy()

# Save the filtered DataFrame to a new CSV file
cleaned_file_path = "D:\\malej\\Downloads\\instantly_leads (2)_upper.csv"
filtered_df.to_csv(cleaned_file_path, index=False)

# Print the head of the filtered DataFrame to verify
print(filtered_df.head())
