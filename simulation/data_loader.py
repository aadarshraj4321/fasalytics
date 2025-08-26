# simulation/data_loader.py

import requests
import pandas as pd
from io import StringIO
import numpy as np

def get_weather_data(latitude, longitude, start_date, end_date):
    print(f"Fetching ADVANCED weather data for Lat: {latitude}, Long: {longitude} from Open-Meteo...")

    api_url = "https://archive-api.open-meteo.com/v1/archive"
    
    # The 'daily' parameters are passed as a Python list of strings.
    # 'relativehumidity_2m_mean' is corrected to 'relative_humidity_2m_mean'.
    params = {
        "latitude": latitude, 
        "longitude": longitude,
        "start_date": start_date, 
        "end_date": end_date,
        "daily": [
            "temperature_2m_mean", 
            "precipitation_sum", 
            "relative_humidity_2m_mean", # CORRECTED VARIABLE NAME
            "windspeed_10m_mean"
        ],
        "timezone": "auto"
    }

    try:
        response = requests.get(api_url, params=params)
        
        # Check the response content first to see the error message if any
        if response.status_code != 200:
            print("Error from API:", response.json())
        
        response.raise_for_status()
        data = response.json()

        if "daily" not in data or "time" not in data["daily"]:
            print("Error: API response does not contain 'daily' data.")
            return None
        
        daily_df = pd.DataFrame(data["daily"])

        # The column name in the response will now also have the underscore.
        daily_df = daily_df.rename(columns={
            "time": "date",
            "temperature_2m_mean": "temperature",
            "precipitation_sum": "rainfall",
            "relative_humidity_2m_mean": "humidity", # CORRECTED COLUMN NAME
            "windspeed_10m_mean": "wind_speed"
        })

        # Clean all potential missing values
        for col in ['temperature', 'rainfall', 'humidity', 'wind_speed']:
            if col in daily_df.columns:
                daily_df[col] = pd.to_numeric(daily_df[col], errors='coerce').ffill().bfill()

        daily_df["date"] = pd.to_datetime(daily_df["date"])
        daily_df["YEAR"] = daily_df["date"].dt.year
        daily_df["MO"] = daily_df["date"].dt.month
        daily_df["DY"] = daily_df["date"].dt.day

        # Return the new columns
        final_df = daily_df[["YEAR", "MO", "DY", "temperature", "rainfall", "humidity", "wind_speed"]]
        print("Successfully fetched and processed advanced weather data.")
        return final_df
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Open-Meteo API: {e}")
        return None

# The test block at the end
if __name__ == '__main__':
    lat_ludhiana = 30.9010
    lon_ludhiana = 75.8573
    weather_df = get_weather_data(lat_ludhiana, lon_ludhiana, "2022-01-01", "2022-12-31")
    if weather_df is not None:
        print("\nSample Data from Ludhiana, 2022 from Open-Meteo:")
        print(weather_df.head())