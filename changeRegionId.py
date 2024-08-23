import pandas as pd
import mysql.connector

# Load the CSV file into a DataFrame
csv_file_path = 'D:\\malej\\Downloads\\paraquintero - paragerman.csv.csv'
df = pd.read_csv(csv_file_path)

# Database connection details
db_config = {
    'user': 'admin',
    'password': 'germanMedia',
    'host': 'mediablitz-prod.c1kc0qesii6f.us-east-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'mediablitzdb'
}

# Connect to the database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Update query
update_query = "UPDATE offer SET region_id = %s WHERE id = %s"

# Iterate over the DataFrame and update the database
for index, row in df.iterrows():
    cursor.execute(update_query, (row['region_id'], row['id']))

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Database update complete.")
