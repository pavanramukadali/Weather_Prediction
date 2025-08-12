import sqlite3
import pandas as pd
import requests
from datetime import datetime, timedelta

# Your API key
API_KEY = 'c7ed8760cfc640b8405dcb059e7e9d0c'

# Connect to SQLite database (or create if not exists)
conn = sqlite3.connect('weather.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS weather (
    date TEXT,
    temperature REAL,
    humidity INTEGER,
    precipitation REAL,
    location TEXT
)
''')
conn.commit()

def fetch_and_store_weather(api_key, location='New York', days=5):
    base_url = 'https://api.openweathermap.org/data/2.5/onecall/timemachine'
    today = datetime(2025, 8, 12)  # fixed date as per your example
    
    for i in range(1, days + 1):
        date = today - timedelta(days=i)
        timestamp = int(date.timestamp())
        url = f"{base_url}?lat=40.7128&lon=-74.0060&dt={timestamp}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url).json()
            if 'current' in response:
                data = response['current']
                weather_data = {
                    'date': date.strftime('%Y-%m-%d'),
                    'temperature': data['temp'],
                    'humidity': data['humidity'],
                    'precipitation': data.get('rain', {}).get('1h', 0),
                    'location': location
                }
                
                cursor.execute('''
                    INSERT INTO weather (date, temperature, humidity, precipitation, location)
                    VALUES (?, ?, ?, ?, ?)
                ''', (weather_data['date'], weather_data['temperature'], weather_data['humidity'],
                      weather_data['precipitation'], weather_data['location']))
                conn.commit()
                print(f"Data stored for {weather_data['date']}")
            else:
                print(f"No weather data available for {date.strftime('%Y-%m-%d')}")
        except Exception as e:
            print(f"Error fetching data for {date.strftime('%Y-%m-%d')}: {e}")

def load_mock_data():
    mock_data = [
        {'date': '2025-08-07', 'temperature': 25.5, 'humidity': 70, 'precipitation': 0.0, 'location': 'New York'},
        {'date': '2025-08-08', 'temperature': 26.2, 'humidity': 65, 'precipitation': 2.5, 'location': 'New York'},
        {'date': '2025-08-09', 'temperature': 24.8, 'humidity': 72, 'precipitation': 0.5, 'location': 'New York'},
        {'date': '2025-08-10', 'temperature': 27.1, 'humidity': 60, 'precipitation': 0.0, 'location': 'New York'},
        {'date': '2025-08-11', 'temperature': 26.5, 'humidity': 68, 'precipitation': 1.0, 'location': 'New York'},
    ]
    df = pd.DataFrame(mock_data)
    df.to_sql('weather', conn, if_exists='append', index=False)
    conn.commit()
    print("Mock data loaded.")

# Uncomment to fetch real data with your API key
# fetch_and_store_weather(API_KEY)

# Or use mock data for testing
load_mock_data()

# Close DB connection when done
conn.close()
