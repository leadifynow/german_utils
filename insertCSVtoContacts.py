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

# Function to insert data into the contacts table
def insert_data(data):
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Construct the SQL query based on column names
                columns = ', '.join([f"`{key}`" for key in data[0].keys()])
                placeholders = ', '.join(['%s'] * len(data[0]))
                sql = f"INSERT INTO contacts ({columns}) VALUES ({placeholders})"
                
                # Execute the query for each row of data
                for row in data:
                    cursor.execute(sql, tuple(row.values()))
                    
            # Commit changes to the database
            conn.commit()
            print("Data inserted successfully.")
        except pymysql.Error as e:
            print(f"Error inserting data into MySQL database: {e}")
        finally:
            # Close the database connection
            conn.close()

# Function to read data from the CSV file
def read_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

# Main function
def main():
    # Provide the path to your CSV file
    csv_filename = r"D:\malej\Downloads\Completed No reply 2 april 15.csv"  # Use raw string literal
    # Alternatively, you can use forward slashes
    # csv_filename = "D:/malej/Downloads/Not Interested.csv"
    data = read_csv(csv_filename)
    insert_data(data)

if __name__ == "__main__":
    main()

# IMPORTANTE remover columnas duplicadas o que no esten definidas en la bd