import pandas as pd
import mysql.connector

# MySQL database configuration
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'admin',
    'database': 'leadifydb'
}

# CSV file path
csv_file = 'D:/malej/Downloads/Instantly.ai Report Tracking - Booked - Instantly.ai Report Tracking - Booked.csv'

# Read CSV file using pandas
df = pd.read_csv(csv_file)

# Replace NaN values with None
df = df.where(pd.notna(df), None)

# Reverse the DataFrame to read from end to start
df = df[::-1]

# Connect to MySQL database
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(buffered=True)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        email = row['email']
        event_name = row['event_name']

        # Check if email exists in the booked table
        cursor.execute("SELECT email FROM booked WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            # Email exists, update the event_name
            cursor.execute("UPDATE booked SET event_name = %s WHERE email = %s", (event_name, email))
            conn.commit()  # Commit the update
            print(f"Updated event_name for email '{email}': {event_name}")
        else:
            # Email does not exist in booked table
            print(f"No record found for email '{email}'")

        # Create a separate cursor to fetch all results and clear the main cursor
        clear_cursor = conn.cursor()
        clear_cursor.execute("SELECT * FROM booked")
        clear_cursor.fetchall()
        clear_cursor.close()

    print("Script execution completed.")

except mysql.connector.Error as e:
    print(f"Error connecting to MySQL database: {e}")

finally:
    # Close main cursor and connection
    cursor.close()
    conn.close()
