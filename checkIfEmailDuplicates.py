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

# Function to check if a contact exists in the database
def contact_exists(firstName, lastName):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                print(f"Checking if contact with first name '{firstName}' and last name '{lastName}' exists in the database...")
                # Check if contact exists in the contacts table
                cursor.execute("SELECT * FROM contacts WHERE firstName = %s AND lastName = %s", (firstName, lastName))
                result = cursor.fetchone()
                if result:
                    print("Contact found in the database.")
                else:
                    print("Contact not found in the database.")
                return result
        except pymysql.Error as e:
            print(f"Error checking contact in database: {e}")
        finally:
            # Close the database connection
            conn.close()
            print("Closed database connection.")
    return None

# Function to parse full name into first name and last name
def parse_full_name(full_name):
    parts = full_name.split()
    if len(parts) > 1:
        return parts[0], ' '.join(parts[1:])
    else:
        return parts[0], ''

# Main function
def main():
    # Provide the path to your CSV file
    csv_filename = "D:/malej/Downloads/UnMatched - Sheet2.csv"
    
    # Read data from the CSV file
    data = read_csv(csv_filename)
    
    # New data list to store matched data
    matched_data = []
    
    # Process each row from the CSV file
    for row in data:
        # Parse full name from the 'Name' column
        first_name, last_name = parse_full_name(row['Name'])
        
        # Check if the contact exists in the database
        contact = contact_exists(first_name, last_name)
        
        # If match found, add to matched data list
        if contact:
            matched_data.append({**row, **contact})  # Combine CSV and database data
    
    # Write matched data to a new CSV file
    matched_filename = "D:/malej/Documents/CSVMatches/matched.csv"
    with open(matched_filename, 'w', newline='', encoding='utf-8') as file:
        if matched_data:  # Check if matched_data is not empty
            writer = csv.DictWriter(file, fieldnames=matched_data[0].keys())
            writer.writeheader()  # Write header row
            writer.writerows(matched_data)  # Write data rows
            print("New CSV file created with matched data.")
            print(f"File path: {matched_filename}")
        else:
            print("No matches found. No CSV file created.")

if __name__ == "__main__":
    main()
