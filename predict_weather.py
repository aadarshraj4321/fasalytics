# predict_weather.py

import torch
import torch.nn as nn
import numpy as np
import pickle
import os
from datetime import datetime, timedelta

# We need to add the project root to the path to import our modules
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.data_loader import get_weather_data

# --- 1. Re-define the LSTM Model Architecture ---
class WeatherLSTM(nn.Module):
    def __init__(self, input_size=2, hidden_layer_size=100, output_size=2, num_layers=2, look_forward=7):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size
        self.num_layers = num_layers
        self.look_forward = look_forward
        self.lstm = nn.LSTM(input_size, hidden_layer_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_layer_size, output_size * look_forward)

    def forward(self, input_seq):
        h0 = torch.zeros(self.num_layers, input_seq.size(0), self.hidden_layer_size).to(input_seq.device)
        c0 = torch.zeros(self.num_layers, input_seq.size(0), self.hidden_layer_size).to(input_seq.device)
        lstm_out, _ = self.lstm(input_seq, (h0, c0))
        last_timestep_out = lstm_out[:, -1, :]
        predictions = self.linear(last_timestep_out)
        return predictions.view(-1, self.look_forward, 2)


def predict_future_weather(model, scaler, start_date, lat, lon, look_back=30):
    """
    Fetches the last 30 days of weather and predicts the next 7 days.
    """
    print("--- Preparing for Prediction ---")
    
    # 1. Calculate the required historical data range
    # --- THE FIX IS HERE ---
    # We fetch data up to the day *before* our "today" to get exactly 30 days.
    end_date_dt = start_date - timedelta(days=1)
    # -----------------------
    start_date_dt = end_date_dt - timedelta(days=look_back - 1) # look_back - 1 to make it inclusive
    
    start_date_str = start_date_dt.strftime('%Y-%m-%d')
    end_date_str = end_date_dt.strftime('%Y-%m-%d')

    print(f"Fetching historical data from {start_date_str} to {end_date_str}...")
    
    # 2. Fetch the historical data
    historical_data = get_weather_data(lat, lon, start_date_str, end_date_str)
    
    if historical_data is None or len(historical_data) != look_back:
        print(f"Error: Expected {look_back} days of data, but got {len(historical_data)}.")
        return None

    # 3. Prepare the data for the model
    input_values = historical_data[['temperature', 'rainfall']].values.astype(np.float32)
    
    with torch.no_grad():
        # 4. Scale the input data
        scaled_input = scaler.transform(input_values)
        
        # 5. Convert to a PyTorch tensor
        input_tensor = torch.from_numpy(scaled_input).float().view(1, look_back, 2)
        
        # 6. Get the model's prediction
        print("Model is making a prediction...")
        prediction_scaled = model(input_tensor)
        
        # 7. Reshape and un-scale the prediction
        prediction_reshaped = prediction_scaled.numpy().reshape(7, 2)
        prediction_unscaled = scaler.inverse_transform(prediction_reshaped)
        
        return prediction_unscaled


if __name__ == '__main__':
    # --- Configuration ---
    project_root = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(project_root, "models", "lstm_weather_forecaster.pth")
    scaler_path = os.path.join(project_root, "models", "weather_data_scaler.pkl")
    
    LAT_LUDHIANA = 30.9010
    LON_LUDHIANA = 75.8573
    
    # We will pretend "today" is a date from our historical dataset to test the model.
    today = datetime(2022, 12, 25)

    # --- Load Model and Scaler ---
    print("--- Loading Weather Forecasting AI ---")
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        print("Error: Model or scaler file not found. Please train the LSTM model first.")
        sys.exit(1)
    try:
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        model = WeatherLSTM()
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        model.eval()
        print("Model and scaler loaded successfully.")
    except Exception as e:
        print(f"Error loading model or scaler: {e}")
        sys.exit(1)

    # --- Make the Prediction ---
    predictions = predict_future_weather(model, scaler, start_date=today, lat=LAT_LUDHIANA, lon=LON_LUDHIANA)

    # --- Display the Results ---
    if predictions is not None:
        print("\n--- 7-Day Weather Forecast for Ludhiana ---")
        print(f"--- Starting from {today.strftime('%d %b, %Y')} ---") # Changed to start from "today"
        print("-" * 45)
        print(f"{'Date':<15} | {'Temperature (°C)':<20} | {'Rainfall (mm)':<15}")
        print("-" * 45)
        
        for i in range(7):
            future_date = today + timedelta(days=i) # Loop starts from today
            date_str = future_date.strftime('%d %b, %Y')
            temp = predictions[i, 0]
            rain = predictions[i, 1]
            rain = max(0, rain)
            print(f"{date_str:<15} | {temp:^20.1f} | {rain:^15.1f}")
        
        print("-" * 45)