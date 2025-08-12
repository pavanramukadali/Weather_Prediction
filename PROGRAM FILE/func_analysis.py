# func_analysis.py
import pandas as pd
import sqlite3

# Connect to the existing weather database
conn = sqlite3.connect('weather.db')

# Function for analysis
def analyze_weather(location='New York'):
    # SQL Query: Average temperature and humidity
    df_avg = pd.read_sql_query(f'''
        SELECT AVG(temperature) AS avg_temp, AVG(humidity) AS avg_humidity
        FROM weather
        WHERE location='{location}'
    ''', conn)
    print("Average Metrics:")
    print(df_avg)
    
    # SQL Query: Days with precipitation > 1mm
    df_rainy = pd.read_sql_query(f'''
        SELECT date, precipitation
        FROM weather
        WHERE location='{location}' AND precipitation > 1
        ORDER BY date
    ''', conn)
    print("\nRainy Days:")
    print(df_rainy)

# Call the function
analyze_weather()

# Close DB connection
conn.close()
