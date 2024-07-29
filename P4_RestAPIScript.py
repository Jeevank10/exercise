#!pip install Flask
#!pip install Flask-SQLAlchemy - The above 2 commands needs to be executed only once at the beginning of code execution.


from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

# Initialize the Flask application
app = Flask(__name__)

# Database configuration dictionary
db_config = {
    'host': 'localhost',
    'user': 'root',      
    'password': 'root',  
    'database': 'weather'  
}

# Function to establish a connection to the MySQL database
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Route to get weather data
@app.route('/api/weather', methods=['GET'])
def get_weather_data():
    # Get query parameters for station_id and date
    station_id = request.args.get('station_id')
    date = request.args.get('date')

    # Get a connection to the database
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM WeatherData WHERE 1=1"
    params = []

    # Append conditions to the query based on the presence of query parameters
    if station_id:
        query += " AND station_id = %s"
        params.append(station_id)
    if date:
        query += " AND date = %s"
        params.append(date)

    # Execute the query with parameters
    cursor.execute(query, params)
    results = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Return the results as a JSON response
    return jsonify(results)

# Route to get weather statistics
@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    # Get query parameters for station_id and year
    station_id = request.args.get('station_id')
    year = request.args.get('year')

    # Get a connection to the database
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM WeatherStats WHERE 1=1"
    params = []

    # Append conditions to the query based on the presence of query parameters
    if station_id:
        query += " AND station_id = %s"
        params.append(station_id)
    if year:
        query += " AND year = %s"
        params.append(year)

    # Execute the query with parameters
    cursor.execute(query, params)
    results = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Return the results as a JSON response
    return jsonify(results)

# Main block to run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
