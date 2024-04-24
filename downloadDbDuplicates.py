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

# Function to execute SQL query and write results to CSV file
def export_duplicates_to_csv():
    conn = connect_to_database()
    if conn:
        try:
            with conn.cursor() as cursor:
                # SQL query to select duplicate email and Campaign Name combinations
                sql = """
                SELECT email, `Campaign Name`, COUNT(*) AS num_duplicates
                FROM contacts
                GROUP BY email, `Campaign Name`
                HAVING COUNT(*) > 1
                """

                # Execute the query
                cursor.execute(sql)

                # Fetch all rows
                rows = cursor.fetchall()

                # Write results to CSV file
                with open('duplicates.csv', 'w', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(['Email', 'Campaign Name', 'Num Duplicates'])
                    csvwriter.writerows(rows)

                print("Results exported to duplicates.csv")
        except pymysql.Error as e:
            print(f"Error exporting duplicates to CSV: {e}")
        finally:
            # Close the database connection
            conn.close()

# Main function
def main():
    export_duplicates_to_csv()

if __name__ == "__main__":
    main()
