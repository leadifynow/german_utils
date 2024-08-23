import csv
import mysql.connector
from mysql.connector import Error

# MySQL database configuration
db_config = {
    'host': 'db-leadify-prod.c1kc0qesii6f.us-east-2.rds.amazonaws.com',
    'port': 3306,
    'user': 'admin',
    'password': 'Leadify1!',
    'database': 'leadifydb'
}

# CSV file path
csv_file_path = r"D:\malej\Downloads\Connections - Connections.csv.csv"

# Function to insert data into the database
def insert_data(cursor, data):
    insert_query = """
    INSERT INTO interested (firstName, lastName, companyName, title, workspace, linkedin_url)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, data)

try:
    # Establishing the connection to the database
    connection = mysql.connector.connect(**db_config)

    if connection.is_connected():
        cursor = connection.cursor()

        # Reading the CSV file
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                first_name = row['First Name']
                last_name = row['Last Name']
                company_name = row['Company']
                title = row['Position']
                workspace = 'ec247541-0aba-405c-9f35-2c6d98916961'
                linkedin_url = row['URL']
                
                data = (first_name, last_name, company_name, title, workspace, linkedin_url)
                insert_data(cursor, data)

        # Commit the transaction
        connection.commit()

        print("Data inserted successfully!")

except Error as e:
    print(f"Error: {e}")
    if connection.is_connected():
        connection.rollback()

finally:
    # Closing the connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
