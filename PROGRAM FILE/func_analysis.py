# func_analysis.py
import pandas as pd
import sqlite3

def analyze_weather(location='New York'):
    conn = sqlite3.connect('weather.db')

    # Average temperature & humidity
    df_avg = pd.read_sql_query(f'''
        SELECT AVG(temperature) AS avg_temp, AVG(humidity) AS avg_humidity
        FROM weather
        WHERE location='{location}'
    ''', conn)
    print("Average Metrics:")
    print(df_avg)

    # Rainy days
    df_rainy = pd.read_sql_query(f'''
        SELECT date, precipitation
        FROM weather
        WHERE location='{location}' AND precipitation > 1
        ORDER BY date
    ''', conn)
    print("\nRainy Days:")
    print(df_rainy)

    conn.close()
