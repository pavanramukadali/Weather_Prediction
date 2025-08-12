import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

# Connect to your database
conn = sqlite3.connect('weather.db')

# Function for visualization
def visualize_weather(location='New York'):
    # Read data from DB
    df = pd.read_sql_query(
        f"SELECT date, temperature, humidity, precipitation FROM weather WHERE location='{location}'", 
        conn
    )
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # --- Line plot: Temperature over time ---
    plt.figure(figsize=(8, 5))
    sns.lineplot(x='date', y='temperature', data=df, marker='o')
    plt.title(f'Temperature Over Time - {location}')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # --- Heatmap: Correlations ---
    plt.figure(figsize=(5, 4))
    sns.heatmap(df[['temperature', 'humidity', 'precipitation']].corr(), annot=True, cmap='coolwarm')
    plt.title(f'Weather Correlations - {location}')
    plt.tight_layout()
    plt.show()

# Call the function
visualize_weather('New York')

# Close connection
conn.close()
