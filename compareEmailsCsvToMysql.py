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
csv_data = pd.read_csv("D:\malej\Downloads\instantly_leads.csv")

# Extract the 'email' column from the CSV data
csv_emails = csv_data['email'].tolist()

# Fetch all 'lead_email' values from the interested table
cur = conn.cursor()
cur.execute("SELECT lead_email FROM interested")
db_emails = [row[0] for row in cur.fetchall()]

# List to store non-existing emails
non_existing_emails = []

# Compare emails and append non-existing emails to the list
for email in csv_emails:
    if not compare_emails(email, db_emails):  # Enter if compare_emails returns False
        print(f"Email '{email}' does not exist in the 'lead_email' column of the interested table.")
        # Append the non-existing email to the list
        non_existing_emails.append(email)

# Close database connection
conn.close()

# Save non-existing emails to a CSV file
output_file = "non_existing_emails.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['email'])  # Write header
    for email in non_existing_emails:
        writer.writerow([email])

print(f"Non-existing emails saved to '{output_file}'.")
