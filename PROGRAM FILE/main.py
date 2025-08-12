import sqlite3
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf
from datetime import datetime
import time
 
API_KEY = "c7ed8760cfc640b8405dcb059e7e9d0c"  
DB_FILE = "weather.db"

def get_my_location():
    try:
        response = requests.get("https://ipinfo.io/json").json()
        city = response.get("city", "Unknown")
        loc = response.get("loc", "0,0").split(",")
        lat, lon = float(loc[0]), float(loc[1])
        print(f"Detected location: {city} ({lat}, {lon})")
        return city, lat, lon
    except Exception as e:
        print("Could not detect location:", e)
        return "Unknown", 0.0, 0.0