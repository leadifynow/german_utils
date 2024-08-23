import pandas as pd
import re
from unidecode import unidecode

file_path = "D:\\malej\\Downloads\\Saas Leadify.csv"
df = pd.read_csv(file_path)

def clean_company_name(name):
    if pd.isna(name):
        return name
    cleaned_name = re.sub(r'[^\w\s]', '', str(name), flags=re.IGNORECASE)
    cleaned_name = unidecode(cleaned_name)
    return cleaned_name

df['Company Name for Emails'] = df['Company Name for Emails'].apply(clean_company_name)

cleaned_file_path = "D:\\malej\\Downloads\\Saas Leadify_Cleansed.csv"
df.to_csv(cleaned_file_path, index=False)
print(df.head())
