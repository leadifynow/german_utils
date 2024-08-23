import pandas as pd
import mysql.connector
from mysql.connector import Error

def update_prices_and_tat_from_csv(csv_file, db_config):
    try:
        # Read the CSV file
        data = pd.read_csv(csv_file)

        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host=db_config["host"],
            port=3306,
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"]
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Filter rows where "NEW UPDATE" is "Raised" or "Lowered" and update prices
            price_update_data = data[data["NEW UPDATE"].isin(["Raised", "Lowered"])]
            for index, row in price_update_data.iterrows():
                publication = row["Publication"]
                # Remove dollar sign and commas, then convert to float
                new_price = float(row["Price"].replace('$', '').replace(',', ''))

                update_price_query = """
                UPDATE offer
                SET price = %s
                WHERE publication = %s
                """
                cursor.execute(update_price_query, (new_price, publication))

            # Filter rows where "NEW UPDATE" is "Updated TAT" and update TAT
            updated_tat_data = data[data["NEW UPDATE"] == "Updated TAT"]
            for index, row in updated_tat_data.iterrows():
                publication = row["Publication"]
                new_tat = row["TAT"]

                update_tat_query = """
                UPDATE offer
                SET tat = %s
                WHERE publication = %s
                """
                cursor.execute(update_tat_query, (new_tat, publication))

            # Commit the updates
            connection.commit()
            print("Prices and TATs updated successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    # Path to your CSV file
    csv_file = r'D:\malej\Downloads\June - June.csv'

    # Database configuration
    db_config = {
        "host": "mediablitz-prod.c1kc0qesii6f.us-east-2.rds.amazonaws.com",
        "user": "admin",
        "password": "germanMedia",
        "database": "mediablitzdb"
    }

    update_prices_and_tat_from_csv(csv_file, db_config)
