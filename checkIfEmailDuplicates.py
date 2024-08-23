import csv
import pymysql

# MySQL database connection details
HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWORD = 'admin'
DATABASE = 'instantlycontacts'

# Function to connect to the MySQL database
def connect_to_database():
    try:
        print("Connecting to MySQL database...")
        conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE)
        print("Connected to MySQL database.")
        return conn
    except pymysql.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Function to read data from the CSV file
def read_csv(filename):
    data = []
    print(f"Reading data from CSV file: {filename}")
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)  # Append entire row
    print(f"Data read successfully from CSV file: {filename}")
    return data

# Function to fetch all unique emails from the contacts table
def fetch_unique_emails():
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                print("Fetching unique emails from the database...")
                cursor.execute("SELECT DISTINCT email FROM contacts")
                result = cursor.fetchall()
                unique_emails = [row[0] for row in result]  # Extract emails from the result
                return unique_emails
        except pymysql.Error as e:
            print(f"Error fetching emails from database: {e}")
        finally:
            # Close the database connection
            conn.close()
            print("Closed database connection.")
    return []

# Main function
def main():
    # Provide the path to your CSV file
    csv_filename = "D:/malej/Downloads/Financial_Services_August.valids_Cleansed.csv"
    
    # Read data from the CSV file
    data = read_csv(csv_filename)
    
    # Fetch unique emails from the database
    unique_emails = fetch_unique_emails()
    
    # New data list to store unmatched data
    unmatched_data = []
    
    # Process each row from the CSV file
    for row in data:
        # Check if the email exists in the unique emails from the database
        if row['Email'] not in unique_emails:
            unmatched_data.append(row)
    
    # Write unmatched data to a new CSV file
    unmatched_filename = "D:/malej/Documents/CSVMatches/Financial_Services_August.valids_Cleansed_noduplcicates.csv"
    with open(unmatched_filename, 'w', newline='', encoding='utf-8') as file:
        if unmatched_data:  # Check if unmatched_data is not empty
            writer = csv.DictWriter(file, fieldnames=unmatched_data[0].keys())
            writer.writeheader()  # Write header row
            writer.writerows(unmatched_data)  # Write data rows
            print("New CSV file created with unmatched data.")
            print(f"File path: {unmatched_filename}")
        else:
            print("All emails matched. No unmatched data to write to CSV.")

if __name__ == "__main__":
    main()
