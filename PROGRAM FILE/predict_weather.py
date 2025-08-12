# prediction_weather.py
import pandas as pd
import numpy as np
import sqlite3
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

def predict_weather(location='New York'):
    conn = sqlite3.connect('weather.db')
    df = pd.read_sql_query(
        f"SELECT date, temperature FROM weather WHERE location='{location}'", conn
    )
    conn.close()

    if df.empty:
        print(f"No data found for location: {location}")
        return

    # Prepare data
    df['date'] = pd.to_datetime(df['date'])
    df['day_number'] = (df['date'] - df['date'].min()).dt.days

    # Linear Regression
    X = df[['day_number']].values
    y = df['temperature'].values
    if len(X) < 2:
        print("Not enough data for Linear Regression prediction.")
        return
    
    lr_model = LinearRegression()
    lr_model.fit(X, y)
    next_day = np.array([[df['day_number'].max() + 1]])
    predicted_temp_lr = lr_model.predict(next_day)[0]
    print(f"Predicted temperature (Linear Regression): {predicted_temp_lr:.2f}°C")

    # LSTM prediction (if enough data)
    if len(df) >= 10:
        scaler = MinMaxScaler()
        df['scaled_temp'] = scaler.fit_transform(df[['temperature']])

        seq_len = 5
        X_lstm, y_lstm = [], []
        for i in range(len(df) - seq_len):
            X_lstm.append(df['scaled_temp'].iloc[i:i+seq_len].values)
            y_lstm.append(df['scaled_temp'].iloc[i+seq_len])

        X_lstm, y_lstm = np.array(X_lstm), np.array(y_lstm)

        lstm_model = tf.keras.Sequential([
            tf.keras.layers.LSTM(50, input_shape=(seq_len, 1)),
            tf.keras.layers.Dense(1)
        ])
        lstm_model.compile(optimizer='adam', loss='mse')
        lstm_model.fit(X_lstm.reshape(-1, seq_len, 1), y_lstm, epochs=10, batch_size=1, verbose=0)

        last_seq = df['scaled_temp'].iloc[-seq_len:].values.reshape(1, seq_len, 1)
        predicted_scaled = lstm_model.predict(last_seq)
        predicted_temp_lstm = scaler.inverse_transform(predicted_scaled)[0][0]
        print(f"Predicted temperature (LSTM): {predicted_temp_lstm:.2f}°C")
    else:
        print("Not enough data for LSTM prediction.")
