import os
import email
from email import policy
from email.parser import BytesParser
import re
import csv

def extract_name_and_email(file_path):
    with open(file_path, "rb") as file:
        msg = BytesParser(policy=policy.default).parse(file)

        # Extract name and email from the "From" field using regex
        from_field = msg.get("From", "")
        match = re.match(r"(.+?) (.+?) <([^>]+)>", from_field)

        if match:
            first_name = match.group(1)
            last_name = match.group(2)
            email_address = match.group(3)

            # Check if email contains "@mindfulmediapr.com"
            if "@mindfulmediapr.com" not in email_address:
                return first_name, last_name, email_address

    return None, None, None

def process_eml_files(directory, output_csv):
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['File', 'First Name', 'Last Name', 'Email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for filename in os.listdir(directory):
            if filename.endswith(".eml"):
                file_path = os.path.join(directory, filename)
                first_name, last_name, email_address = extract_name_and_email(file_path)
                
                if first_name and last_name and email_address:
                    writer.writerow({'File': filename, 'First Name': first_name, 'Last Name': last_name, 'Email': email_address})

# Specify the directory containing your .eml files
directory_path = "D:/malej/Documents/emls"

# Specify the output CSV file with a filename
output_csv_path = "D:/malej/Documents/output.csv"

# Call the function
process_eml_files(directory_path, output_csv_path)