# simulation/forecaster.py

import torch
import torch.nn as nn
import numpy as np
import pickle
import os

# --- 1. Re-define the ADVANCED LSTM Model Architecture ---
class AdvancedWeatherLSTM(nn.Module):
    def __init__(self, input_size=4, hidden_layer_size=128, output_size=4, num_layers=2, look_forward=7):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size
        self.num_layers = num_layers
        self.look_forward = look_forward
        self.lstm = nn.LSTM(input_size, hidden_layer_size, num_layers, batch_first=True, dropout=0.1)
        self.linear = nn.Linear(hidden_layer_size, output_size * look_forward)

    def forward(self, input_seq):
        # We don't need to manually initialize h0 and c0; LSTM does it by default
        lstm_out, _ = self.lstm(input_seq)
        predictions = self.linear(lstm_out[:, -1, :])
        return predictions.view(-1, self.look_forward, 4)

# --- 2. Create the LOCATION-AWARE Stochastic Forecaster Class ---
class StochasticWeatherForecaster:
    def __init__(self, model_dir, location_name, num_models=5, look_back=30):
        self.look_back = look_back
        self.num_models = num_models
        
        # --- THE FIX IS HERE: Load files based on location_name ---
        scaler_filename = f"advanced_weather_data_scaler_{location_name.lower()}.pkl"
        scaler_path = os.path.join(model_dir, scaler_filename)
        
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler file not found for location '{location_name}' at {scaler_path}")
            
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        self.models = []
        print(f"--- Loading ADVANCED Weather Forecaster Ensemble for {location_name.upper()} ---")
        for i in range(1, self.num_models + 1):
            model_filename = f"lstm_advanced_weather_forecaster_{location_name.lower()}_{i}.pth"
            model_path = os.path.join(model_dir, model_filename)
            
            if os.path.exists(model_path):
                model = AdvancedWeatherLSTM()
                model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
                model.eval()
                self.models.append(model)
                print(f"Loaded advanced model {i}/{self.num_models} for {location_name} successfully.")
            else:
                print(f"Warning: Advanced model file not found at {model_path}. It will be skipped.")
        
        if not self.models:
            raise RuntimeError(f"No advanced weather forecasting models were loaded for {location_name}.")
        print(f"Advanced stochastic weather forecaster for {location_name.upper()} loaded and ready.")

    def predict(self, past_weather_data):
        """
        Makes a 7-day probabilistic forecast for 4 features.
        Args:
            past_weather_data (np.ndarray): Shape (30, 4) for temp, rain, humidity, wind.
        """
        if past_weather_data.shape[0] < self.look_back:
            return np.zeros((7, 4)), np.ones((7, 4)) * 10 

        with torch.no_grad():
            scaled_input = self.scaler.transform(past_weather_data[-self.look_back:])
            input_tensor = torch.from_numpy(scaled_input).float().view(1, self.look_back, 4)
            
            all_predictions = []
            for model in self.models:
                prediction_scaled = model(input_tensor)
                prediction_reshaped = prediction_scaled.numpy().reshape(7, 4)
                prediction_unscaled = self.scaler.inverse_transform(prediction_reshaped)
                prediction_unscaled[:, 1] = np.maximum(0, prediction_unscaled[:, 1]) # Clip rainfall at 0
                all_predictions.append(prediction_unscaled)
            
            predictions_stack = np.stack(all_predictions, axis=0)
            mean_forecast = np.mean(predictions_stack, axis=0)
            std_dev_forecast = np.std(predictions_stack, axis=0)
            
            return mean_forecast, std_dev_forecast