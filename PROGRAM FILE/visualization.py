# visualizations.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3

def visualize_weather(location='New York'):
    conn = sqlite3.connect('weather.db')
    df = pd.read_sql_query(
        f"SELECT date, temperature, humidity, precipitation FROM weather WHERE location='{location}'", 
        conn
    )
    conn.close()

    # Convert to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Temperature over time
    plt.figure(figsize=(8, 5))
    sns.lineplot(x='date', y='temperature', data=df, marker='o')
    plt.title(f'Temperature Over Time - {location}')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Correlation heatmap
    plt.figure(figsize=(5, 4))
    sns.heatmap(df[['temperature', 'humidity', 'precipitation']].corr(), annot=True, cmap='coolwarm')
    plt.title(f'Weather Correlations - {location}')
    plt.tight_layout()
    plt.show()
