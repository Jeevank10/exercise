#!pip install mysql-connector-python -This command needs to be executed only once at the beginning of code execution.
import mysql.connector

def create_table_weatherdata():
    # Establish the connection to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='weather'
    )
    
    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    
    # Define the SQL command to create the WeatherData table
    create_weather_data_table = '''
    CREATE TABLE IF NOT EXISTS WeatherData (
        id INT AUTO_INCREMENT PRIMARY KEY,       # Primary key with auto-increment
        station_id VARCHAR(100),                 # Weather station identifier
        date DATE,                               # Date of the weather data
        max_temp INT,                            # Maximum temperature
        min_temp INT,                            # Minimum temperature
        precipitation INT,                       # Precipitation amount
        UNIQUE(station_id, date)                 # Unique constraint on station_id and date
    );
    '''
    
    # Execute the SQL command to create the table
    cursor.execute(create_weather_data_table)
    
    # Commit the changes to the database
    connection.commit()
    
    # Close the cursor and connection
    cursor.close()
    connection.close()

# Call the function to create the WeatherData table
create_table_weatherdata()

