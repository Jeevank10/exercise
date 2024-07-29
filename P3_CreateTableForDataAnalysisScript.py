import mysql.connector

def create_table_weatherstats():
    # Establish the connection to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='weather'
    )
    
    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    
    # Define the SQL command to create the WeatherStats table
    create_weather_stats_table = '''
    CREATE TABLE IF NOT EXISTS WeatherStats (
        station_id VARCHAR(100),                 # Weather station identifier
        year INT,                                # Year of the weather statistics
        avg_max_temp DECIMAL(10, 2),             # Average maximum temperature
        avg_min_temp DECIMAL(10, 2),             # Average minimum temperature
        total_precipitation DECIMAL(10, 2),      # Total precipitation amount
        PRIMARY KEY (station_id, year)           # Composite primary key on station_id and year
    );
    '''
    
    # Execute the SQL command to create the table
    cursor.execute(create_weather_stats_table)
    
    # Commit the changes to the database
    connection.commit()
    
    # Close the cursor and connection
    cursor.close()
    connection.close()

# Call the function to create the WeatherStats table
create_table_weatherstats()
