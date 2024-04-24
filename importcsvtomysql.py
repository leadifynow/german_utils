import pandas as pd
import mysql.connector
from datetime import datetime

# MySQL database configuration
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'admin',
    'database': 'leadifydb'
}

# CSV file path
csv_file = 'D:/malej/Downloads/Instantly.ai Report Tracking - Interested.csv'

# MySQL table name
table_name = 'interested'

# Read CSV file using pandas
df = pd.read_csv(csv_file)

# Print unique values in each column
for column in df.columns:
    unique_values = df[column].unique()
    print(f"Column '{column}': {unique_values}")

# Connect to MySQL database
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Iterate over rows in the DataFrame
for index, row in df.iterrows():
    # Replace 'nan' and 'Check Notes' values with None for each row
    row = [None if pd.isna(value) or value == 'Check Notes' else value for value in row]
    # Set event_type to 'lead_interested'
    row[0] = 'lead_interested'
    # Set default values for campaign_id and campaign_name if they are null
    if row[2] is None:
        row[2] = 'd90e6bbc-52cc-42da-baaf-59d77f8440d1'
    if row[3] is None:
        row[3] = 'No Longer Active'
    # Convert next_update to MySQL datetime format
    if row[20] is not None:
        try:
            row[20] = datetime.strptime(row[20], '%m/%d/%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            print(f"Invalid datetime format: {row[20]}")
            row[20] = None  # Set the value to None if conversion fails
    
    try:
        # Check if the lead_email already exists
        cursor.execute(f"SELECT * FROM {table_name} WHERE lead_email = %s", (row[4],))
        existing_row = cursor.fetchone()
        if existing_row:
            # If the lead_email exists, update the existing row
            update_query = f"""
            UPDATE {table_name} SET event_type = %s, workspace = %s, campaign_id = %s, campaign_name = %s,
            lead_email = %s, title = %s, email = %s, website = %s, industry = %s, lastName = %s, firstName = %s,
            number_of_employees = %s, companyName = %s, linkedin_url = %s, created_at = %s, updated_at = %s,
            stage_id = %s, notes = %s, booked = %s, manager = %s, next_update = %s WHERE lead_email = %s
            """
            cursor.execute(update_query, tuple(row[0:21] + [row[4]]))  # Ensure all placeholders are filled
        else:
            # If the lead_email does not exist, insert a new row
            insert_query = f"""
            INSERT INTO {table_name} (event_type, workspace, campaign_id, campaign_name, lead_email, title, email,
            website, industry, lastName, firstName, number_of_employees, companyName, linkedin_url, created_at,
            updated_at, stage_id, notes, booked, manager, next_update)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, tuple(row))
    except Exception as e:
        print(f"Error processing row: {row}")
        print(f"Error message: {e}")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()

print("CSV data successfully uploaded to MySQL database.")
