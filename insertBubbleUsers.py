import csv
import mysql.connector

# Define database connection parameters
db_config = {
    'user': 'admin',
    'password': 'germanMedia',
    'host': 'mediablitz-prod.c1kc0qesii6f.us-east-2.rds.amazonaws.com',
    'port': 3306,
    'database': 'mediablitzdb'
}

# Connect to the MySQL database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Path to the CSV file
csv_file_path = r'D:\malej\Downloads\Previous Clients - MediaBlitz - Sheet1.csv'

# Read data from CSV and insert into the database
with open(csv_file_path, newline='') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    for row in csvreader:
        first_name = row['firstName']
        last_name = row['lastName']
        phone_number = row['phoneNumber']
        email = row['email']
        
        # Define the SQL query for insertion
        insert_query = """
        INSERT INTO user (first_name, last_name, phone_number, email, referrer_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        data = (first_name, last_name, phone_number, email, 3)
        
        # Execute the query
        cursor.execute(insert_query, data)
        
    # Commit the transaction
    connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()

print("Data inserted successfully.")