import pandas as pd
import mysql.connector
from datetime import datetime

# MySQL database configuration
db_config = {
    'host': 'db-leadify-prod.c1kc0qesii6f.us-east-2.rds.amazonaws.com',
    'port': 3306,
    'user': 'admin',
    'password': 'Leadify1!',
    'database': 'leadifydb'
}

def format_date(date_str):
    """
    Function to format date string to '%Y-%m-%d %H:%M:%S' format
    """
    if pd.notna(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None

# CSV file path
csv_file = "D:\malej\Downloads\Hoja de cálculo sin título - Instantly.ai Report Tracking - Booked - Instantly.ai Report Tracking - Booked.csv"

# Read only the relevant columns from the CSV file
relevant_columns = ['email', 'first_name', 'last_name', 'name', 'text_reminder_number', 'timezone',
                    'interested_id', 'company_id', 'created_at', 'updated_at', 'workspace_id', 'event_name',
                    'business', 'website', 'meeting_date', 'publicist', 'referral']
df = pd.read_csv(csv_file, usecols=relevant_columns)

# Connect to MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

for index, row in df.iterrows():
    # Replace 'NaN' values with None for each row
    row = row.where(pd.notna(row), None)
    email = row['email']
    meeting_date = format_date(row['meeting_date'])
    print(f'{email}')
    try:
        insert_query = """
        INSERT INTO booked (email, first_name, last_name, name, text_reminder_number, 
                            timezone, company_id, created_at, updated_at,
                            business, website, meeting_date, publicist, referral, interested_id, event_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (email, row['first_name'], row['last_name'], row['name'],
                                       row['text_reminder_number'], row['timezone'], row['company_id'],
                                       row['created_at'], row['updated_at'], row['business'], row['website'],
                                       meeting_date, row['publicist'], row['referral'], row['interested_id'], row['event_name']))
        print(f"Inserted new record for email '{email}'")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print("CSV data successfully uploaded to MySQL database.")
