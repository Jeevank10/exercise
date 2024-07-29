#!pip install requests
#!pip install datetime -The above 2 commands needs to be executed only once at the beginning of code execution.


import mysql.connector
import requests
from datetime import datetime

# Define the GitHub repository API URL
repo_api_url = "https://api.github.com/repos/corteva/code-challenge-template/contents/wx_data"

def get_file_list(api_url):
    # Send a GET request to the GitHub API to retrieve the list of files
    response = requests.get(api_url)
    if response.status_code == 200:
        files = response.json()
        # Filter the list to include only .txt files
        file_list = [file['name'] for file in files if file['name'].endswith('.txt')]
        return file_list
    else:
        print("Failed to retrieve file list from GitHub.")
        return []

def fetch_and_ingest_data(file_list):
    # Define the base URL for raw file access on GitHub
    base_url = "https://raw.githubusercontent.com/corteva/code-challenge-template/main/wx_data/"

    # Establish the connection to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='weather'
    )
    cursor = connection.cursor()

    # Loop through each file in the file list
    for file_name in file_list:
        # Send a GET request to fetch the raw file content
        response = requests.get(base_url + file_name)
        if response.status_code == 200:
            station_id = file_name.split('.')[0]
            # Process each line in the file
            for line in response.text.split('\n'):
                if line:
                    # Split the line into individual data elements
                    date, max_temp, min_temp, precipitation = line.strip().split('\t')
                    
                    # Handle missing data indicated by '-9999'
                    if max_temp == '-9999':
                        max_temp = None
                    if min_temp == '-9999':
                        min_temp = None
                    if precipitation == '-9999':
                        precipitation = None

                    # Insert data into the WeatherData table, updating if the record already exists
                    cursor.execute('''
                        INSERT INTO WeatherData (station_id, date, max_temp, min_temp, precipitation) 
                        VALUES (%s, %s, %s, %s, %s) 
                        ON DUPLICATE KEY UPDATE max_temp=VALUES(max_temp), min_temp=VALUES(min_temp), precipitation=VALUES(precipitation)
                    ''', (station_id, date, max_temp, min_temp, precipitation))

    # Commit the changes to the database
    connection.commit()
    
    # Close the cursor and connection
    cursor.close()
    connection.close()

# Record the start time of the data ingestion process
start_time = datetime.now()

# Get the list of files to process from the GitHub repository
file_list = get_file_list(repo_api_url)
if file_list:
    # Fetch and ingest the data from the files
    fetch_and_ingest_data(file_list)

# Record the end time of the data ingestion process
end_time = datetime.now()

# Print the start and end times of the data ingestion process
print(f"Data ingestion started at: {start_time} and ended at: {end_time}")
