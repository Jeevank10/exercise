import mysql.connector

def calculate_weather_stats():
    # Establish the connection to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        db='weather'
    )
    
    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Define the SQL command to calculate and insert weather statistics
    cursor.execute('''
    INSERT INTO WeatherStats (
        station_id,
        year,
        avg_max_temp,
        avg_min_temp,
        total_precipitation
    )
    SELECT 
        station_id,
        YEAR(date) AS year,
        AVG(max_temp / 10.0) AS avg_max_temp,    # Calculate average max temperature
        AVG(min_temp / 10.0) AS avg_min_temp,    # Calculate average min temperature
        SUM(precipitation / 100.0) AS total_precipitation  # Calculate total precipitation
    FROM WeatherData
    WHERE max_temp IS NOT NULL                  # Ensure max_temp is not null
    AND min_temp IS NOT NULL                    # Ensure min_temp is not null
    AND precipitation IS NOT NULL               # Ensure precipitation is not null
    GROUP BY station_id, YEAR(date)             # Group by station_id and year
    ON DUPLICATE KEY UPDATE 
        avg_max_temp=VALUES(avg_max_temp), 
        avg_min_temp=VALUES(avg_min_temp), 
        total_precipitation=VALUES(total_precipitation);
    ''')

    # Commit the changes to the database
    connection.commit()
    
    # Close the cursor and connection
    cursor.close()
    connection.close()

# Call the function to calculate and insert weather statistics
calculate_weather_stats()
