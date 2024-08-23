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
        conn = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE)
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
def contact_exists(email):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Check if contact exists in the contacts table
                cursor.execute("SELECT `Interest status`, `Instantly status` FROM contacts WHERE email = %s", (email,))
                result = cursor.fetchone()
                if result:
                    print("Contact found in the database.")
                return result
        except pymysql.Error as e:
            print(f"Error checking contact in database: {e}")
        finally:
            # Close the database connection
            conn.close()
    return None

# Main function
def main():
    # Provide the path to your CSV file
    csv_filename = "D:/malej/Downloads/Management.valids.csv"
    
    # Read data from the CSV file
    data = read_csv(csv_filename)
    
    # New data list to store valid data
    valid_data = []
    
    # Process each row from the CSV file
    for row in data:
        email = row['Email']
        
        # Check if the contact exists in the database
        contact = contact_exists(email)
        
        # If contact found, check the conditions
        if contact:
            interest_status, instantly_status = contact
            if interest_status != "Wrong person" and instantly_status != "Bounced":
                valid_data.append(row)  # Add row to valid data if conditions are not met
        else:
            valid_data.append(row)  # Add row to valid data if contact not found in the database
    
    # Write valid data to a new CSV file
    valid_filename = "D:/malej/Documents/CSVMatches/5FilterStatus.csv"
    with open(valid_filename, 'w', newline='', encoding='utf-8') as file:
        if valid_data:  # Check if valid_data is not empty
            writer = csv.DictWriter(file, fieldnames=valid_data[0].keys())
            writer.writeheader()  # Write header row
            writer.writerows(valid_data)  # Write data rows
            print("New CSV file created with valid data.")
            print(f"File path: {valid_filename}")
        else:
            print("No valid data found. No CSV file created.")

if __name__ == "__main__":
    main()
