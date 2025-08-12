import pandas as pd
import numpy as np
import sqlite3
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

# Connect to your database
conn = sqlite3.connect('weather.db')

# Function for ML predictions
def predict_weather(location='New York'):
    # Load data from DB
    df = pd.read_sql_query(
        f"SELECT date, temperature FROM weather WHERE location='{location}'", conn
    )
    
    if df.empty:
        print(f"No data found for location: {location}")
        return

    # Prepare data
    df['date'] = pd.to_datetime(df['date'])
    df['day_number'] = (df['date'] - df['date'].min()).dt.days
    
    # --- Simple Linear Regression ---
    X = df[['day_number']].values
    y = df['temperature'].values
    if len(X) < 2:
        print("Not enough data for Linear Regression prediction.")
        return
    
    model = LinearRegression()
    model.fit(X, y)
    next_day = np.array([[df['day_number'].max() + 1]])
    predicted_temp_lr = model.predict(next_day)[0]
    print(f"Predicted temperature (Linear Regression): {predicted_temp_lr:.2f}°C")
    
    # --- LSTM (Only if we have at least 10 points) ---
    if len(df) >= 10:
        scaler = MinMaxScaler()
        df['scaled_temp'] = scaler.fit_transform(df[['temperature']])
        sequence_length = 5
        X_lstm, y_lstm = [], []
        for i in range(len(df) - sequence_length):
            X_lstm.append(df['scaled_temp'].iloc[i:i+sequence_length].values)
            y_lstm.append(df['scaled_temp'].iloc[i+sequence_length])
        X_lstm, y_lstm = np.array(X_lstm), np.array(y_lstm)
        
        model_lstm = tf.keras.Sequential([
            tf.keras.layers.LSTM(50, input_shape=(sequence_length, 1)),
            tf.keras.layers.Dense(1)
        ])
        model_lstm.compile(optimizer='adam', loss='mse')
        model_lstm.fit(X_lstm.reshape(-1, sequence_length, 1), y_lstm, epochs=10, batch_size=1, verbose=0)
        
        last_sequence = df['scaled_temp'].iloc[-sequence_length:].values.reshape(1, sequence_length, 1)
        predicted_scaled = model_lstm.predict(last_sequence)
        predicted_temp_lstm = scaler.inverse_transform(predicted_scaled)[0][0]
        print(f"Predicted temperature (LSTM): {predicted_temp_lstm:.2f}°C")
    else:
        print("Not enough data for LSTM prediction.")

# Call the function
predict_weather()

# Close DB connection
conn.close()




