import pandas as pd
import mysql.connector
import csv

# Connect to your MySQL database
conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="admin",
    database="leadifydb"
)

# Function to compare emails
def compare_emails(csv_email, db_emails):
    return csv_email in db_emails

# Read the CSV file
csv_data = pd.read_csv("D:\\malej\\Downloads\\Aviation_Cleansed.csv")

# Extract the 'email' column from the CSV data
csv_emails = csv_data['Email'].tolist()

# Fetch all 'lead_email' values from the interested table
cur = conn.cursor()
cur.execute("SELECT lead_email FROM interested")
db_emails = [row[0] for row in cur.fetchall()]

# List to store non-existing emails and their corresponding rows
non_existing_rows = []

# Compare emails and append non-existing emails to the list
for index, row in csv_data.iterrows():
    email = row['Email']
    if not compare_emails(email, db_emails):  # Enter if compare_emails returns False
        print(f"Email '{email}' does not exist in the 'lead_email' column of the interested table.")
        # Append the entire row to the list of non-existing rows
        non_existing_rows.append(row)

# Close database connection
conn.close()

# Save non-existing rows to a CSV file
output_file = "Aviation_Cleansed_noemails.csv"
if non_existing_rows:
    # Convert the list of non-existing rows to a DataFrame
    non_existing_df = pd.DataFrame(non_existing_rows)
    # Save the DataFrame to a CSV file
    non_existing_df.to_csv(output_file, index=False)

print(f"Non-existing emails saved to '{output_file}'.")
