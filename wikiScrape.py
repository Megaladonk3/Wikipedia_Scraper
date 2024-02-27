'''
# Import necessary libraries
from bs4 import BeautifulSoup
import requests

# Function to retrieve and print data from Wikipedia based on the user's query
def get_data(query):
    # Construct the Wikipedia URL for the given query
    url = f"https://en.wikipedia.org/wiki/{query}"

    # Use a session to make HTTP requests (can be more efficient for multiple requests)
    with requests.Session() as session:
        try:
            # Send a GET request to the Wikipedia URL
            response = session.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad requests

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Check if the page contains valid data (not a disambiguation page or error message)
            if "Wikipedia does not have an article with this exact name." not in str(response.text) and "Bad title" not in str(response.text):
                # Extract and print the heading of the Wikipedia page
                heading = soup.find(id="firstHeading").text
                print(f"------[+]{heading}[+]--------")

                # Extract and print the first two paragraphs from the Wikipedia page
                paragraphs = soup.select(".mw-parser-output p")[:2]
                if paragraphs:
                    for paragraph in paragraphs:
                        print(paragraph.text)
                    print("-----------------------")
                else:
                    print("[-] No valid data found :(")
            else:
                print("[-] No entry found in Wikipedia.")
        except requests.RequestException as e:
            # Handle exceptions related to the HTTP request
            print(f"Error: {e}")

# Main function to get user input and call the get_data function
def main():
    # Prompt the user to enter a query
    query = input("Enter query - ")
    
    # Get data for the entered query
    get_data(query=query)

# Entry point to the script; execute the main function if this script is run directly
if __name__ == "__main__":
    main()
'''

import csv
from bs4 import BeautifulSoup
import requests
import html2text

# Function to retrieve and print data from Wikipedia based on the user's query
def get_data(query, output_file):
    # Construct the Wikipedia URL for the given query
    url = f"https://en.wikipedia.org/wiki/{query}"

    # Use a session to make HTTP requests (can be more efficient for multiple requests)
    with requests.Session() as session:
        try:
            # Send a GET request to the Wikipedia URL
            response = session.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad requests

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")

            # Check if the page contains valid data (not a disambiguation page or error message)
            if "Wikipedia does not have an article with this exact name." not in str(response.text) and "Bad title" not in str(response.text):
                # Open a CSV file for writing
                with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                    csv_writer = csv.writer(csvfile, delimiter = '>') #the separator between fields

                    # Write headers to the CSV file
                    csv_writer.writerow(['Heading', 'Paragraph'])

                    # Extract and write all the headings and paragraphs to the CSV file
                    headings = soup.select(".mw-headline")
                    for heading in headings:
                        heading_text = heading.text
                        current_heading = soup.find(id=heading.get("id"))
                        next_paragraph = current_heading.find_next("p")
                        paragraph_text = next_paragraph.text if next_paragraph else "No paragraph found"

                        # Convert HTML content to plain text
                        heading_text = html2text.html2text(heading_text)
                        paragraph_text = html2text.html2text(paragraph_text)

                        # Write heading and paragraph to the CSV file
                        csv_writer.writerow([heading_text, paragraph_text])

                        print(f"------[+]{heading_text}[+]--------")
                        print(paragraph_text)
                        print("-----------------------")

                print(f"Data written to {output_file}")
            else:
                print("[-] No entry found in Wikipedia.")
        except requests.RequestException as e:
            # Handle exceptions related to the HTTP request
            print(f"Error: {e}")

# Main function to get user input and call the get_data function
def main():
    # Prompt the user to enter a query and the output file name
    query = input("Enter query - ")
    output_file = input("Enter output file name (including .csv extension) - ")

    # Get data for the entered query and write to CSV file
    get_data(query=query, output_file=output_file)

# Entry point to the script; execute the main function if this script is run directly
if __name__ == "__main__":
    main()
