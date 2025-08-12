# main.py
from func_analysis import analyze_weather
from visualization import visualize_weather
from predict_weather import predict_weather

if __name__ == "__main__":
    location = "New York"

    print("=== Weather Analysis ===")
    analyze_weather(location)

    print("\n=== Weather Visualization ===")
    visualize_weather(location)

    print("\n=== Weather Prediction ===")
    predict_weather(location)
