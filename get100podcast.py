import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup
import requests
import csv
import os

def is_english(text):
    return all(ord(char) < 128 for char in text)

def make_request(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    return response

def scrape_and_export():
    url = url_entry.get()
    output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

    # Make the request with retry mechanism
    response = make_request(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <div> elements with the specified class
        target_class = "title f3"
        target_divs = soup.find_all('div', class_=target_class)

        # Extract text from each matching div
        extracted_texts = [div.get_text(strip=True) for div in target_divs if is_english(div.get_text(strip=True))]

        # Export to CSV
        with open(output_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Society & Culture"])  # Header row

            # Write each extracted text as a new row in a single column
            for text in extracted_texts:
                writer.writerow([text])

        result_label.config(text=f"Data exported to {output_path}")
        
        # Clear the URL entry
        url_entry.delete(0, tk.END)
    else:
        result_label.config(text=f"Failed to retrieve the webpage. Status code: {response.status_code}")

# Create the main window
app = tk.Tk()
app.title("Web Scraper App")

# Create and place widgets
url_label = tk.Label(app, text="Enter URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=10)

scrape_button = tk.Button(app, text="Scrape and Export", command=scrape_and_export)
scrape_button.pack(pady=20)

result_label = tk.Label(app, text="")
result_label.pack()

# Start the GUI event loop
app.mainloop()