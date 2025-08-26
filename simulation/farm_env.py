# # # simulation/farm_env.py

# # import gymnasium as gym
# # from gymnasium import spaces
# # import numpy as np
# # import pandas as pd
# # import os
# # from .core_components import Soil, Crop
# # from .data_loader import get_weather_data
# # # Import the new stochastic forecaster
# # from .forecaster import StochasticWeatherForecaster

# # class FarmEnv(gym.Env):
# #     def __init__(self, crop_type="Wheat", soil_type="Alluvial", simulation_days=None, latitude=30.9010, longitude=75.8573):
# #         super(FarmEnv, self).__init__()

# #         self.crop_type = crop_type
# #         self.soil_type = soil_type
# #         self.latitude = latitude
# #         self.longitude = longitude
        
# #         self.crop = Crop(crop_type=self.crop_type)
# #         self.soil = Soil(soil_type=self.soil_type)

# #         if simulation_days is None:
# #             self.simulation_days = list(self.crop.growth_stages.values())[-1][-1]
# #         else:
# #             self.simulation_days = simulation_days
        
# #         self.current_day = 0

# #         # Initialize the Stochastic Weather Forecaster
# #         project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# #         model_dir = os.path.join(project_root_path, "models")
# #         scaler_path = os.path.join(project_root_path, "models", "weather_data_scaler.pkl")
# #         self.forecaster = StochasticWeatherForecaster(model_dir, scaler_path)

# #         # Load a long history of weather data for the specified location
# #         # Fetch 3 years + a 30-day buffer for the initial look-back period.
# #         historical_data = get_weather_data(latitude=self.latitude, longitude=self.longitude, 
# #                                          start_date="2019-12-01", end_date="2022-12-31")
# #         if historical_data is None:
# #             raise Exception("Could not fetch real weather data.")
# #         self.full_weather_data = historical_data
# #         self.weather_data_np = None
# #         self.start_index = 0

# #         # Action space includes pesticide
# #         self.action_space = spaces.Dict({
# #             "irrigation": spaces.Discrete(5),
# #             "fertilizer": spaces.Discrete(5),
# #             "pesticide": spaces.Discrete(2)
# #         })
# #         self.irrigation_map = {0: 0, 1: 5, 2: 10, 3: 15, 4: 20}
# #         self.fertilizer_map = {0: 0, 1: 5, 2: 10, 3: 15, 4: 20}
# #         self.pesticide_map = {0: 0, 1: 1}
        
# #         # Observation space is expanded for the stochastic forecast
# #         # 7 base + 7 days * (1 mean + 1 std) = 7 + 14 = 21 features. Wait, this is too large.
# #         # Let's simplify: 7 base + mean_temp + mean_rain + std_temp + std_rain = 11 features
# #         self.observation_space = spaces.Box(
# #             low=0.0,
# #             high=1.0,
# #             shape=(11,), # 7 base + 4 forecast stats
# #             dtype=np.float32
# #         )
        
# #         # ENHANCED: Track history for trend analysis
# #         self.moisture_history, self.nitrogen_history, self.health_history = [], [], []
        
# #         # ENHANCED: Cost tracking for economic optimization
# #         self.total_irrigation_cost, self.total_fertilizer_cost, self.total_pesticide_cost = 0.0, 0.0, 0.0
# #         self.irrigation_cost_per_mm = 0.1
# #         self.fertilizer_cost_per_kg = 0.5
# #         self.pesticide_cost_per_application = 50.0

# #     def _get_observation(self):
# #         """Observation space with stochastic forecast stats."""
# #         effective_day = min(self.current_day, self.simulation_days - 1)
        
# #         # Basic observations (7 items)
# #         base_obs = [
# #             self.soil.moisture_content, self.soil.nitrogen_level, self.crop.health / 100.0,
# #             self.current_day / self.simulation_days,
# #             np.clip((self.weather_data_np[effective_day, 0] - 5) / 35, 0, 1),
# #             np.clip(self.weather_data_np[effective_day, 1] / 50.0, 0, 1),
# #             self.crop.accumulated_growth / self.crop.max_potential_growth,
# #         ]
        
# #         # Get historical data for the forecaster
# #         current_data_index = self.start_index + self.current_day
# #         look_back_start_index = current_data_index - 30
# #         past_30_days = self.full_weather_data[['temperature', 'rainfall']].iloc[look_back_start_index:current_data_index].to_numpy()

# #         # Get the stochastic forecast (mean and std dev)
# #         mean_forecast, std_dev_forecast = self.forecaster.predict(past_30_days)
        
# #         # We will provide the agent with the average forecast and average uncertainty over the next 7 days
# #         avg_mean_temp = np.mean(mean_forecast[:, 0])
# #         avg_mean_rain = np.mean(mean_forecast[:, 1])
# #         avg_std_temp = np.mean(std_dev_forecast[:, 0])
# #         avg_std_rain = np.mean(std_dev_forecast[:, 1])
        
# #         # Normalize the forecast stats (4 items)
# #         norm_avg_mean_temp = np.clip((avg_mean_temp - 5) / 35, 0, 1)
# #         norm_avg_mean_rain = np.clip(avg_mean_rain / 50.0, 0, 1)
# #         norm_avg_std_temp = np.clip(avg_std_temp / 10.0, 0, 1) # Assume max std dev is 10
# #         norm_avg_std_rain = np.clip(avg_std_rain / 20.0, 0, 1) # Assume max std dev is 20

# #         # Combine all observations (7 base + 4 forecast stats = 11 items)
# #         final_obs = base_obs + [norm_avg_mean_temp, norm_avg_mean_rain, norm_avg_std_temp, norm_avg_std_rain]
        
# #         obs = np.array(final_obs, dtype=np.float32)
# #         return np.clip(obs, 0.0, 1.0)

# #     def reset(self, seed=None, options=None):
# #         super().reset(seed=seed)
# #         self.current_day = 0
# #         self.moisture_history, self.nitrogen_history, self.health_history = [], [], []
# #         self.total_irrigation_cost, self.total_fertilizer_cost, self.total_pesticide_cost = 0.0, 0.0, 0.0
# #         self.soil = Soil(soil_type=self.soil_type)
# #         self.crop = Crop(crop_type=self.crop_type)

# #         # Ensure we can always look back 30 days
# #         max_start_index = len(self.full_weather_data) - self.simulation_days
# #         self.start_index = self.np_random.integers(30, max_start_index)
# #         end_index = self.start_index + self.simulation_days
        
# #         self.weather_data_np = self.full_weather_data[['temperature', 'rainfall']].iloc[self.start_index:end_index].to_numpy()

# #         self.moisture_history.append(self.soil.moisture_content)
# #         self.nitrogen_history.append(self.soil.nitrogen_level)
# #         self.health_history.append(self.crop.health)

# #         observation = self._get_observation()
# #         info = {}
# #         return observation, info

# #     def step(self, action):
# #         """Enhanced reward function with economic considerations and intermediate rewards."""
# #         irrigation_action = int(action["irrigation"])
# #         fertilizer_action = int(action["fertilizer"])
# #         pesticide_action = int(action["pesticide"])
        
# #         irrigation_amount = self.irrigation_map[irrigation_action]
# #         fertilizer_amount = self.fertilizer_map[fertilizer_action]
        
# #         if self.pesticide_map[pesticide_action] == 1:
# #             self.crop.apply_pesticide()
# #             self.total_pesticide_cost += self.pesticide_cost_per_application

# #         self.total_irrigation_cost += irrigation_amount * self.irrigation_cost_per_mm
# #         self.total_fertilizer_cost += fertilizer_amount * self.fertilizer_cost_per_kg
        
# #         daily_reward = 0.0
# #         prev_health = self.crop.health
        
# #         self.soil.add_fertilizer(fertilizer_amount)
# #         self.soil.daily_depletion()
# #         today_rain = self.weather_data_np[self.current_day, 1]
# #         self.soil.add_water(today_rain + irrigation_amount)
# #         today_temp = self.weather_data_np[self.current_day, 0]
# #         self.crop.grow_one_day(soil=self.soil, temperature=today_temp)
# #         self.soil.daily_evaporation(temperature=today_temp)

# #         self.moisture_history.append(self.soil.moisture_content)
# #         self.nitrogen_history.append(self.soil.nitrogen_level)
# #         self.health_history.append(self.crop.health)
        
# #         if len(self.moisture_history) > 5:
# #             self.moisture_history.pop(0)
# #             self.nitrogen_history.pop(0)
# #             self.health_history.pop(0)

# #         if self.crop.health > 85 and self.crop.health > prev_health:
# #             daily_reward += 1.0
# #         if self.crop.health < prev_health:
# #             daily_reward -= 0.5
            
# #         self.current_day += 1
# #         terminated = self.current_day >= self.simulation_days
# #         truncated = False

# #         profit = 0
# #         if terminated:
# #             final_yield = self.crop.get_current_yield()
# #             health_bonus = self.crop.health
# #             revenue = final_yield * 0.2
# #             total_costs = self.total_irrigation_cost + self.total_fertilizer_cost + self.total_pesticide_cost
# #             profit = revenue - total_costs
# #             economic_bonus = max(-500, profit)
# #             daily_reward += (economic_bonus / 100.0) + (health_bonus / 10.0)
            
# #         observation = self._get_observation()
        
# #         info = {
# #             'yield': self.crop.get_current_yield(),
# #             'health': self.crop.health,
# #             'moisture': self.soil.moisture_content,
# #             'nitrogen': self.soil.nitrogen_level,
# #             'profit': profit,
# #             'rust_risk': getattr(self.crop, 'rust_risk', 0.0)
# #         }

# #         return observation, daily_reward, terminated, truncated, info

















# import gymnasium as gym
# from gymnasium import spaces
# import numpy as np
# import pandas as pd
# import os
# from datetime import datetime, timedelta

# # Import all of our advanced simulation modules
# from .core_components import Soil, Crop
# from .data_loader import get_weather_data
# from .forecaster import StochasticWeatherForecaster
# from .extreme_weather import ExtremeWeatherDetector
# from .weather_thresholds import SEASONAL_ADJUSTMENTS

# class FarmEnv(gym.Env):
#     def __init__(self, crop_type="Wheat", soil_type="Alluvial", simulation_days=None, latitude=30.9010, longitude=75.8573):
#         super(FarmEnv, self).__init__()

#         self.crop_type = crop_type
#         self.soil_type = soil_type
#         self.latitude = latitude
#         self.longitude = longitude
        
#         # Initialize crop and soil to get their parameters
#         self.crop = Crop(crop_type=self.crop_type)
#         self.soil = Soil(soil_type=self.soil_type)

#         # Set simulation_days based on crop if not provided
#         if simulation_days is None:
#             self.simulation_days = list(self.crop.growth_stages.values())[-1][-1]
#         else:
#             self.simulation_days = simulation_days
        
#         self.current_day = 0

#         # --- Initialize All AI Brains and Data ---
#         project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
#         # 1. Load the Stochastic Forecaster with advanced models
#         model_dir = os.path.join(project_root_path, "models")
#         scaler_path = os.path.join(project_root_path, "models", "advanced_weather_data_scaler.pkl")
#         self.forecaster = StochasticWeatherForecaster(model_dir, scaler_path)
        
#         # 2. Load a long history of all 4 weather features
#         self.full_weather_data = get_weather_data(latitude=self.latitude, longitude=self.longitude, 
#                                                   start_date="2010-01-01", end_date="2022-12-31")
#         if self.full_weather_data is None:
#             raise Exception("Could not fetch real weather data.")
        
#         # 3. Initialize the Extreme Weather Detector with the historical data
#         hist_data_for_detector = self.full_weather_data.copy()
#         hist_data_for_detector['date'] = pd.to_datetime(hist_data_for_detector[['YEAR', 'MO', 'DY']].rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day'}))
#         hist_data_for_detector = hist_data_for_detector.set_index('date')
#         self.weather_detector = ExtremeWeatherDetector(latitude, longitude, crop_type)
#         # Manually assign the full dataframe to the detector
#         self.weather_detector.historical_data = hist_data_for_detector

#         # Action space includes all three actions
#         self.action_space = spaces.Dict({
#             "irrigation": spaces.Discrete(5),
#             "fertilizer": spaces.Discrete(5),
#             "pesticide": spaces.Discrete(2)
#         })
#         self.irrigation_map = {0: 0, 1: 5, 2: 10, 3: 15, 4: 20}
#         self.fertilizer_map = {0: 0, 1: 5, 2: 10, 3: 15, 4: 20}
#         self.pesticide_map = {0: 0, 1: 1}
        
#         # --- NEW: The Definitive, Richest Observation Space ---
#         # 7 base + 4 forecast stats + 5 specific risk scores = 16 observations
#         self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(16,), dtype=np.float32)
        
#         # Economic and history tracking
#         self.total_irrigation_cost = 0.0
#         self.total_fertilizer_cost = 0.0
#         self.total_pesticide_cost = 0.0
#         self.irrigation_cost_per_mm = 0.1
#         self.fertilizer_cost_per_kg = 0.5
#         self.pesticide_cost_per_application = 50.0

#     def _get_observation(self):
#         effective_day = min(self.current_day, self.simulation_days - 1)
        
#         # 1. Base observations (7 items)
#         base_obs = [
#             self.soil.moisture_content, self.soil.nitrogen_level,
#             self.crop.health / 100.0, self.current_day / self.simulation_days,
#             np.clip((self.weather_data_np[effective_day, 0] - 5) / 35, 0, 1), # Current Temp
#             np.clip(self.weather_data_np[effective_day, 1] / 50.0, 0, 1), # Current Rain
#             self.crop.accumulated_growth / self.crop.max_potential_growth
#         ]
        
#         # 2. Get Stochastic Forecast for all 4 features
#         current_data_index = self.start_index + self.current_day
#         past_30_days = self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[current_data_index - 30:current_data_index].to_numpy()
#         mean_forecast, std_dev_forecast = self.forecaster.predict(past_30_days)
        
#         # 3. Get Extreme Weather Risk Analysis from the new Detector
#         current_date = self.start_date_obj + timedelta(days=self.current_day)
#         current_season = self._get_season_from_date(current_date)
#         risks = self.weather_detector.calculate_risks(mean_forecast[:, :2], std_dev_forecast[:, :2], current_season)
        
#         # 4. Normalize and combine risk data (5 risk items)
#         risk_obs = [
#             risks["heat_wave_risk"], risks["cold_wave_risk"], risks["heavy_rain_risk"],
#             risks["drought_risk"], risks["crop_stress_risk"]
#         ]

#         # 5. Add simplified forecast stats (4 items)
#         avg_mean_temp = np.mean(mean_forecast[:, 0])
#         avg_mean_rain = np.mean(mean_forecast[:, 1])
#         avg_std_temp = np.mean(std_dev_forecast[:, 0])
#         avg_std_rain = np.mean(std_dev_forecast[:, 1])
#         forecast_stats = [
#             np.clip((avg_mean_temp - 5) / 35, 0, 1),
#             np.clip(avg_mean_rain / 50.0, 0, 1),
#             np.clip(avg_std_temp / 10.0, 0, 1),
#             np.clip(avg_std_rain / 20.0, 0, 1)
#         ]

#         # Combine all observations (7 base + 5 risks + 4 forecast stats = 16 items)
#         final_obs = base_obs + risk_obs + forecast_stats
        
#         return np.array(final_obs, dtype=np.float32)

#     def reset(self, seed=None, options=None):
#         super().reset(seed=seed)
#         self.current_day = 0
#         self.total_irrigation_cost, self.total_fertilizer_cost, self.total_pesticide_cost = 0.0, 0.0, 0.0
#         self.soil = Soil(soil_type=self.soil_type)
#         self.crop = Crop(crop_type=self.crop_type)

#         max_start_index = len(self.full_weather_data) - self.simulation_days - 30
#         self.start_index = self.np_random.integers(30, max_start_index)
#         end_index = self.start_index + self.simulation_days
        
#         # Store the full 4-feature weather data for the episode
#         self.weather_data_np = self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[self.start_index:end_index].to_numpy()
        
#         # Store the start date object for seasonal calculations
#         start_date_row = self.full_weather_data.iloc[self.start_index]
#         self.start_date_obj = datetime(year=int(start_date_row['YEAR']), month=int(start_date_row['MO']), day=int(start_date_row['DY']))

#         return self._get_observation(), {}

#     def step(self, action):
#         """Enhanced reward function with economic considerations and intermediate rewards."""
#         irrigation_action = int(action["irrigation"])
#         fertilizer_action = int(action["fertilizer"])
#         pesticide_action = int(action["pesticide"])
        
#         irrigation_amount = self.irrigation_map[irrigation_action]
#         fertilizer_amount = self.fertilizer_map[fertilizer_action]
        
#         if self.pesticide_map[pesticide_action] == 1:
#             self.crop.apply_pesticide()
#             self.total_pesticide_cost += self.pesticide_cost_per_application

#         self.total_irrigation_cost += irrigation_amount * self.irrigation_cost_per_mm
#         self.total_fertilizer_cost += fertilizer_amount * self.fertilizer_cost_per_kg
        
#         daily_reward = 0.0
#         prev_health = self.crop.health
        
#         self.soil.add_fertilizer(fertilizer_amount)
#         self.soil.daily_depletion()
#         today_rain = self.weather_data_np[self.current_day, 1]
#         self.soil.add_water(today_rain + irrigation_amount)
        
#         today_temp = self.weather_data_np[self.current_day, 0]
#         today_humidity = self.weather_data_np[self.current_day, 2] / 100.0 # Convert % to 0-1
        
#         self.crop.grow_one_day(soil=self.soil, temperature=today_temp, humidity=today_humidity)
#         self.soil.daily_evaporation(temperature=today_temp, humidity=today_humidity)
        
#         if self.crop.health > 85 and self.crop.health > prev_health:
#             daily_reward += 1.0
#         if self.crop.health < prev_health:
#             daily_reward -= 0.5
            
#         self.current_day += 1
#         terminated = self.current_day >= self.simulation_days
#         truncated = False

#         profit = 0
#         if terminated:
#             final_yield = self.crop.get_current_yield()
#             health_bonus = self.crop.health
#             revenue = final_yield * 0.2
#             total_costs = self.total_irrigation_cost + self.total_fertilizer_cost + self.total_pesticide_cost
#             profit = revenue - total_costs
#             economic_bonus = max(-500, profit)
#             daily_reward += (economic_bonus / 100.0) + (health_bonus / 10.0)
            
#         observation = self._get_observation()
        
#         # Get risk alerts for the info dictionary
#         mean_fc, std_fc = self.forecaster.predict(self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[self.start_index + self.current_day - 30:self.start_index + self.current_day].to_numpy())
#         current_date = self.start_date_obj + timedelta(days=self.current_day)
#         current_season = self._get_season_from_date(current_date)
#         risks = self.weather_detector.calculate_risks(mean_fc[:, :2], std_fc[:, :2], current_season)
#         alerts = self.weather_detector.get_risk_alerts(risks)
        
#         info = {
#             'yield': self.crop.get_current_yield(), 'health': self.crop.health,
#             'moisture': self.soil.moisture_content, 'nitrogen': self.soil.nitrogen_level,
#             'profit': profit, 'rust_risk': getattr(self.crop, 'rust_risk', 0.0),
#             'extreme_weather_alerts': alerts
#         }
#         return observation, daily_reward, terminated, truncated, info

#     def _get_season_from_date(self, date_obj):
#         month = date_obj.month
#         for season, data in SEASONAL_ADJUSTMENTS.items():
#             if month in data["months"]:
#                 return season
#         return "summer"





















# # simulation/farm_env.py

# import gymnasium as gym
# from gymnasium import spaces
# import numpy as np
# import pandas as pd
# import os
# from datetime import datetime, timedelta

# # Import all of our advanced simulation modules
# from .core_components import Soil, Crop
# from .data_loader import get_weather_data
# from .forecaster import StochasticWeatherForecaster
# from .extreme_weather import ExtremeWeatherDetector
# from .weather_thresholds import SEASONAL_ADJUSTMENTS

# # Helper function to map coordinates to a location name for model loading
# def get_location_name(latitude, longitude):
#     if 24.0 <= latitude <= 25.0 and 84.0 <= longitude <= 85.0: return "aurangabad"
#     if 30.0 <= latitude <= 31.0 and 75.0 <= longitude <= 76.0: return "ludhiana"
#     if 22.0 <= latitude <= 23.0 and 88.0 <= longitude <= 89.0: return "kolkata"
#     if 26.0 <= latitude <= 27.0 and 80.0 <= longitude <= 81.0: return "lucknow"
#     return "ludhiana" # Default fallback


# class FarmEnv(gym.Env):
#     def __init__(self, crop_type="Wheat", soil_type="Alluvial", simulation_days=None, latitude=30.9010, longitude=75.8573):
#         super(FarmEnv, self).__init__()

#         self.crop_type = crop_type
#         self.soil_type = soil_type
#         self.latitude = latitude
#         self.longitude = longitude
        
#         # Initialize crop and soil to get their parameters
#         self.crop = Crop(crop_type=self.crop_type)
#         self.soil = Soil(soil_type=self.soil_type)

#         # Set simulation_days based on crop if not provided
#         if simulation_days is None:
#             self.simulation_days = list(self.crop.growth_stages.values())[-1][-1]
#         else:
#             self.simulation_days = simulation_days
        
#         self.current_day = 0

#         # --- Initialize All AI Brains and Data ---
#         project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
#         # --- THE FIX IS HERE: Dynamic, Location-Aware Forecaster Loading ---
#         model_dir = os.path.join(project_root_path, "models")
#         # 1. Determine the location name from the provided coordinates
#         location_name = get_location_name(self.latitude, self.longitude)
        
#         # 2. Load the Stochastic Forecaster FOR THAT SPECIFIC LOCATION
#         self.forecaster = StochasticWeatherForecaster(model_dir, location_name=location_name)
        
#         # 2. Load a long history of all 4 weather features
#         # Fetch an extra 30-day buffer for the initial look-back period.
#         start_date_fetch = (datetime.strptime("2010-01-01", "%Y-%m-%d") - timedelta(days=30)).strftime("%Y-%m-%d")
#         self.full_weather_data = get_weather_data(latitude=self.latitude, longitude=self.longitude, 
#                                                   start_date=start_date_fetch, end_date="2022-12-31")
#         if self.full_weather_data is None:
#             raise Exception("Could not fetch real weather data.")
        
#         # 3. Initialize the Extreme Weather Detector with the historical data
#         hist_data_for_detector = self.full_weather_data.copy()
#         hist_data_for_detector['date'] = pd.to_datetime(hist_data_for_detector[['YEAR', 'MO', 'DY']].rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day'}))
#         hist_data_for_detector = hist_data_for_detector.set_index('date')
#         self.weather_detector = ExtremeWeatherDetector(latitude, longitude, crop_type)
#         self.weather_detector.historical_data = hist_data_for_detector # Manually assign the full dataframe

#         # Action space includes all three actions
#         self.action_space = spaces.Dict({
#             "irrigation": spaces.Discrete(5),
#             "fertilizer": spaces.Discrete(5),
#             "pesticide": spaces.Discrete(2)
#         })
#         self.irrigation_map = {0: 0, 1: 5, 2: 10, 3: 15, 4: 20}
#         self.fertilizer_map = {0: 0, 1: 5, 2: 10, 3: 15, 4: 20}
#         self.pesticide_map = {0: 0, 1: 1}
        
#         # --- NEW: The Definitive, Richest Observation Space ---
#         # 7 base + 4 forecast stats + 5 specific risk scores = 16 observations
#         self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(16,), dtype=np.float32)
        
#         # Economic and history tracking
#         self.total_irrigation_cost = 0.0
#         self.total_fertilizer_cost = 0.0
#         self.total_pesticide_cost = 0.0
#         self.irrigation_cost_per_mm = 0.1
#         self.fertilizer_cost_per_kg = 0.5
#         self.pesticide_cost_per_application = 50.0

#     def _get_observation(self):
#         effective_day = min(self.current_day, self.simulation_days - 1)
        
#         # 1. Base observations (7 items)
#         base_obs = [
#             self.soil.moisture_content, self.soil.nitrogen_level,
#             self.crop.health / 100.0, self.current_day / self.simulation_days,
#             np.clip((self.weather_data_np[effective_day, 0] - 5) / 35, 0, 1),
#             np.clip(self.weather_data_np[effective_day, 1] / 50.0, 0, 1),
#             self.crop.accumulated_growth / self.crop.max_potential_growth
#         ]
        
#         # 2. Get Stochastic Forecast for all 4 features
#         current_data_index = self.start_index + self.current_day
#         past_30_days = self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[current_data_index - 30:current_data_index].to_numpy()
#         mean_forecast, std_dev_forecast = self.forecaster.predict(past_30_days)
        
#         # 3. Get Extreme Weather Risk Analysis from the new Detector
#         current_date = self.start_date_obj + timedelta(days=self.current_day)
#         current_season = self._get_season_from_date(current_date)
#         risks = self.weather_detector.calculate_risks(mean_forecast[:, :2], std_dev_forecast[:, :2], current_season)
        
#         # 4. Normalize and combine risk data (5 risk items)
#         risk_obs = [
#             risks["heat_wave_risk"], risks["cold_wave_risk"], risks["heavy_rain_risk"],
#             risks["drought_risk"], risks["crop_stress_risk"]
#         ]

#         # 5. Add simplified forecast stats (4 items)
#         avg_mean_temp = np.mean(mean_forecast[:, 0])
#         avg_mean_rain = np.mean(mean_forecast[:, 1])
#         avg_std_temp = np.mean(std_dev_forecast[:, 0])
#         avg_std_rain = np.mean(std_dev_forecast[:, 1])
#         forecast_stats = [
#             np.clip((avg_mean_temp - 5) / 35, 0, 1),
#             np.clip(avg_mean_rain / 50.0, 0, 1),
#             np.clip(avg_std_temp / 10.0, 0, 1),
#             np.clip(avg_std_rain / 20.0, 0, 1)
#         ]

#         # Combine all observations (7 base + 5 risks + 4 forecast stats = 16 items)
#         final_obs = base_obs + risk_obs + forecast_stats
        
#         return np.array(final_obs, dtype=np.float32)

#     def reset(self, seed=None, options=None):
#         super().reset(seed=seed)
#         self.current_day = 0
#         self.total_irrigation_cost, self.total_fertilizer_cost, self.total_pesticide_cost = 0.0, 0.0, 0.0
#         self.soil = Soil(soil_type=self.soil_type)
#         self.crop = Crop(crop_type=self.crop_type)

#         max_start_index = len(self.full_weather_data) - self.simulation_days - 1
#         self.start_index = self.np_random.integers(30, max_start_index)
#         end_index = self.start_index + self.simulation_days
        
#         self.weather_data_np = self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[self.start_index:end_index].to_numpy()
        
#         start_date_row = self.full_weather_data.iloc[self.start_index]
#         self.start_date_obj = datetime(year=int(start_date_row['YEAR']), month=int(start_date_row['MO']), day=int(start_date_row['DY']))

#         return self._get_observation(), {}

#     def step(self, action):
#         """Enhanced reward function with economic considerations and intermediate rewards."""
#         irrigation_action = int(action["irrigation"])
#         fertilizer_action = int(action["fertilizer"])
#         pesticide_action = int(action["pesticide"])
        
#         irrigation_amount = self.irrigation_map[irrigation_action]
#         fertilizer_amount = self.fertilizer_map[fertilizer_action]
        
#         if self.pesticide_map[pesticide_action] == 1:
#             self.crop.apply_pesticide()
#             self.total_pesticide_cost += self.pesticide_cost_per_application

#         self.total_irrigation_cost += irrigation_amount * self.irrigation_cost_per_mm
#         self.total_fertilizer_cost += fertilizer_amount * self.fertilizer_cost_per_kg
        
#         daily_reward = 0.0
#         prev_health = self.crop.health
        
#         self.soil.add_fertilizer(fertilizer_amount)
#         self.soil.daily_depletion()
#         today_rain = self.weather_data_np[self.current_day, 1]
#         self.soil.add_water(today_rain + irrigation_amount)
        
#         today_temp = self.weather_data_np[self.current_day, 0]
#         today_humidity = self.weather_data_np[self.current_day, 2] / 100.0
        
#         self.crop.grow_one_day(soil=self.soil, temperature=today_temp, humidity=today_humidity)
#         self.soil.daily_evaporation(temperature=today_temp, humidity=today_humidity)
        
#         if self.crop.health > 85 and self.crop.health > prev_health:
#             daily_reward += 1.0
#         if self.crop.health < prev_health:
#             daily_reward -= 0.5
            
#         self.current_day += 1
#         terminated = self.current_day >= self.simulation_days
#         truncated = False

#         profit = 0
#         if terminated:
#             final_yield = self.crop.get_current_yield()
#             health_bonus = self.crop.health
#             revenue = final_yield * 0.2
#             total_costs = self.total_irrigation_cost + self.total_fertilizer_cost + self.total_pesticide_cost
#             profit = revenue - total_costs
#             economic_bonus = max(-500, profit)
#             daily_reward += (economic_bonus / 100.0) + (health_bonus / 10.0)
            
#         observation = self._get_observation()
        
#         # Get risk alerts for the info dictionary
#         mean_fc, std_fc = self.forecaster.predict(self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[self.start_index + self.current_day - 30:self.start_index + self.current_day].to_numpy())
#         current_date = self.start_date_obj + timedelta(days=self.current_day)
#         current_season = self._get_season_from_date(current_date)
#         risks = self.weather_detector.calculate_risks(mean_fc[:, :2], std_fc[:, :2], current_season)
#         alerts = self.weather_detector.get_risk_alerts(risks)
        
#         info = {
#             'yield': self.crop.get_current_yield(), 'health': self.crop.health,
#             'moisture': self.soil.moisture_content, 'nitrogen': self.soil.nitrogen_level,
#             'profit': profit, 'disease_risks': getattr(self.crop, 'disease_risks', {}),
#             'extreme_weather_alerts': alerts
#         }
#         return observation, daily_reward, terminated, truncated, info

#     def _get_season_from_date(self, date_obj):
#         month = date_obj.month
        
#         # Check for crop-specific seasonal adjustments first
#         if self.crop_type in SEASONAL_ADJUSTMENTS:
#             for season, data in SEASONAL_ADJUSTMENTS[self.crop_type].items():
#                 if month in data["months"]:
#                     return season
        
#         # Fallback to generic seasons if no crop-specific one is found
#         if 3 <= month <= 5: return "summer"
#         if 6 <= month <= 9: return "monsoon"
#         if 10 <= month <= 11: return "post-monsoon"
#         return "winter"


































# # simulation/farm_env.py

# import gymnasium as gym
# from gymnasium import spaces
# import numpy as np
# import pandas as pd
# import os
# from datetime import datetime, timedelta

# # Import all of our advanced simulation modules
# from .core_components import Soil, Crop
# from .data_loader import get_weather_data
# from .forecaster import StochasticWeatherForecaster
# from .extreme_weather import ExtremeWeatherDetector
# from .weather_thresholds import SEASONAL_ADJUSTMENTS

# # Helper function to map coordinates to a location name for model loading
# def get_location_name(latitude, longitude):
#     if 24.0 <= latitude <= 25.0 and 84.0 <= longitude <= 85.0: return "aurangabad"
#     if 30.0 <= latitude <= 31.0 and 75.0 <= longitude <= 76.0: return "ludhiana"
#     if 22.0 <= latitude <= 23.0 and 88.0 <= longitude <= 89.0: return "kolkata"
#     if 26.0 <= latitude <= 27.0 and 80.0 <= longitude <= 81.0: return "lucknow"
#     return "ludhiana" # Default fallback


# class FarmEnv(gym.Env):
#     def __init__(self, crop_type="Wheat", soil_type="Alluvial", simulation_days=None, latitude=30.9010, longitude=75.8573):
#         super(FarmEnv, self).__init__()

#         self.crop_type = crop_type
#         self.soil_type = soil_type
#         self.latitude = latitude
#         self.longitude = longitude
        
#         self.crop = Crop(crop_type=self.crop_type)
#         self.soil = Soil(soil_type=self.soil_type)

#         if simulation_days is None:
#             self.simulation_days = list(self.crop.growth_stages.values())[-1][-1]
#         else:
#             self.simulation_days = simulation_days
        
#         self.current_day = 0

#         # --- Initialize All AI Brains and Data ---
#         project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
#         model_dir = os.path.join(project_root_path, "models")
#         location_name = get_location_name(self.latitude, self.longitude)
#         scaler_path = os.path.join(model_dir, f"advanced_weather_data_scaler_{location_name}.pkl")
#         self.forecaster = StochasticWeatherForecaster(model_dir, location_name=location_name)
        
#         start_date_fetch = (datetime.strptime("2010-01-01", "%Y-%m-%d") - timedelta(days=30)).strftime("%Y-%m-%d")
#         self.full_weather_data = get_weather_data(latitude=self.latitude, longitude=self.longitude, 
#                                                   start_date=start_date_fetch, end_date="2022-12-31")
#         if self.full_weather_data is None:
#             raise Exception("Could not fetch real weather data.")
        
#         hist_data_for_detector = self.full_weather_data.copy()
#         hist_data_for_detector['date'] = pd.to_datetime(hist_data_for_detector[['YEAR', 'MO', 'DY']].rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day'}))
#         hist_data_for_detector = hist_data_for_detector.set_index('date')
#         self.weather_detector = ExtremeWeatherDetector(latitude, longitude, crop_type)
#         self.weather_detector.historical_data = hist_data_for_detector

#         # Action space includes all three actions
#         self.action_space = spaces.Dict({
#             "irrigation": spaces.Discrete(5),
#             "fertilizer": spaces.Discrete(5),
#             "pesticide": spaces.Discrete(2)
#         })
#         self.irrigation_map = {0: 0, 1: 5, 2: 10, 3: 15, 4: 20}
#         self.fertilizer_map = {0: 0, 1: 5, 2: 10, 3: 15, 4: 20}
#         self.pesticide_map = {0: 0, 1: 1}
        
#         # The Definitive, Richest Observation Space
#         self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(16,), dtype=np.float32)
        
#         # Economic and history tracking
#         self.total_irrigation_cost = 0.0
#         self.total_fertilizer_cost = 0.0
#         self.total_pesticide_cost = 0.0
#         self.irrigation_cost_per_mm = 0.1
#         self.fertilizer_cost_per_kg = 0.5
#         self.pesticide_cost_per_application = 50.0

#     def _get_observation(self):
#         effective_day = min(self.current_day, self.simulation_days - 1)
        
#         base_obs = [
#             self.soil.moisture_content, self.soil.nitrogen_level,
#             self.crop.health / 100.0, self.current_day / self.simulation_days,
#             np.clip((self.weather_data_np[effective_day, 0] - 5) / 35, 0, 1),
#             np.clip(self.weather_data_np[effective_day, 1] / 50.0, 0, 1),
#             self.crop.accumulated_growth / self.crop.max_potential_growth
#         ]
        
#         current_data_index = self.start_index + self.current_day
#         past_30_days = self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[current_data_index - 30:current_data_index].to_numpy()
#         mean_forecast, std_dev_forecast = self.forecaster.predict(past_30_days)
        
#         current_date = self.start_date_obj + timedelta(days=self.current_day)
#         current_season = self._get_season_from_date(current_date)
#         risks = self.weather_detector.calculate_risks(mean_forecast[:, :2], std_dev_forecast[:, :2], current_season)
        
#         risk_obs = [
#             risks["heat_wave_risk"], risks["cold_wave_risk"], risks["heavy_rain_risk"],
#             risks["drought_risk"], risks["crop_stress_risk"]
#         ]

#         avg_mean_temp = np.mean(mean_forecast[:, 0])
#         avg_mean_rain = np.mean(mean_forecast[:, 1])
#         avg_std_temp = np.mean(std_dev_forecast[:, 0])
#         avg_std_rain = np.mean(std_dev_forecast[:, 1])
#         forecast_stats = [
#             np.clip((avg_mean_temp - 5) / 35, 0, 1),
#             np.clip(avg_mean_rain / 50.0, 0, 1),
#             np.clip(avg_std_temp / 10.0, 0, 1),
#             np.clip(avg_std_rain / 20.0, 0, 1)
#         ]

#         final_obs = base_obs + risk_obs + forecast_stats
        
#         return np.array(final_obs, dtype=np.float32)

#     def reset(self, seed=None, options=None):
#         super().reset(seed=seed)
#         self.current_day = 0
#         self.total_irrigation_cost, self.total_fertilizer_cost, self.total_pesticide_cost = 0.0, 0.0, 0.0
#         self.soil = Soil(soil_type=self.soil_type)
#         self.crop = Crop(crop_type=self.crop_type)

#         max_start_index = len(self.full_weather_data) - self.simulation_days - 1
#         self.start_index = self.np_random.integers(30, max_start_index)
#         end_index = self.start_index + self.simulation_days
        
#         self.weather_data_np = self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[self.start_index:end_index].to_numpy()
        
#         start_date_row = self.full_weather_data.iloc[self.start_index]
#         self.start_date_obj = datetime(year=int(start_date_row['YEAR']), month=int(start_date_row['MO']), day=int(start_date_row['DY']))

#         return self._get_observation(), {}

#     def step(self, action):
#         """Definitive Reward Function: Sparse rewards with a single, clear economic goal."""
#         irrigation_action = int(action["irrigation"])
#         fertilizer_action = int(action["fertilizer"])
#         pesticide_action = int(action["pesticide"])
        
#         irrigation_amount = self.irrigation_map[irrigation_action]
#         fertilizer_amount = self.fertilizer_map[fertilizer_action]
        
#         if self.pesticide_map[pesticide_action] == 1:
#             self.crop.apply_pesticide()
#             self.total_pesticide_cost += self.pesticide_cost_per_application

#         self.total_irrigation_cost += irrigation_amount * self.irrigation_cost_per_mm
#         self.total_fertilizer_cost += fertilizer_amount * self.fertilizer_cost_per_kg
        
#         # The reward for every intermediate day is ZERO.
#         daily_reward = 0.0
        
#         # Apply actions and run simulation physics
#         self.soil.add_fertilizer(fertilizer_amount)
#         self.soil.daily_depletion()
#         today_rain = self.weather_data_np[self.current_day, 1]
#         self.soil.add_water(today_rain + irrigation_amount)
#         today_temp = self.weather_data_np[self.current_day, 0]
#         today_humidity = self.weather_data_np[self.current_day, 2] / 100.0
#         self.crop.grow_one_day(soil=self.soil, temperature=today_temp, humidity=today_humidity)
#         self.soil.daily_evaporation(temperature=today_temp, humidity=today_humidity)
        
#         self.current_day += 1
#         terminated = self.current_day >= self.simulation_days
#         truncated = False

#         profit = 0
#         # The one and only reward signal is given on the final day.
#         if terminated:
#             final_yield = self.crop.get_current_yield()
#             health_bonus = self.crop.health
            
#             revenue = final_yield * 0.2
#             total_costs = self.total_irrigation_cost + self.total_fertilizer_cost + self.total_pesticide_cost
#             profit = revenue - total_costs
            
#             # The final reward is a combination of the scaled profit and final health
#             daily_reward = (profit / 10.0) + (health_bonus / 10.0)
            
#         observation = self._get_observation()
        
#         # Get risk alerts for the info dictionary to pass to the frontend
#         mean_fc, std_fc = self.forecaster.predict(self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[self.start_index + self.current_day - 30:self.start_index + self.current_day].to_numpy())
#         current_date = self.start_date_obj + timedelta(days=self.current_day)
#         current_season = self._get_season_from_date(current_date)
#         risks = self.weather_detector.calculate_risks(mean_fc[:, :2], std_fc[:, :2], current_season)
#         alerts = self.weather_detector.get_risk_alerts(risks)
        
#         info = {
#             'yield': self.crop.get_current_yield(), 'health': self.crop.health,
#             'moisture': self.soil.moisture_content, 'nitrogen': self.soil.nitrogen_level,
#             'profit': profit, 'disease_risks': getattr(self.crop, 'disease_risks', {}),
#             'extreme_weather_alerts': alerts
#         }
#         return observation, daily_reward, terminated, truncated, info

#     def _get_season_from_date(self, date_obj):
#         month = date_obj.month
        
#         if self.crop_type in SEASONAL_ADJUSTMENTS:
#             for season, data in SEASONAL_ADJUSTMENTS[self.crop_type].items():
#                 if month in data["months"]:
#                     return season
        
#         if 3 <= month <= 5: return "summer"
#         if 6 <= month <= 9: return "monsoon"
#         if 10 <= month <= 11: return "post-monsoon"
#         return "winter"

































# import gymnasium as gym
# from gymnasium import spaces
# import numpy as np
# import pandas as pd
# import os
# from datetime import datetime, timedelta

# # Import all of our advanced simulation modules
# from .core_components import Soil, Crop
# from .data_loader import get_weather_data
# from .forecaster import StochasticWeatherForecaster
# from .extreme_weather import ExtremeWeatherDetector
# from .weather_thresholds import SEASONAL_ADJUSTMENTS

# # Helper function to map coordinates to a location name for model loading
# def get_location_name(latitude, longitude):
#     if 24.0 <= latitude <= 25.0 and 84.0 <= longitude <= 85.0: return "aurangabad"
#     if 30.0 <= latitude <= 31.0 and 75.0 <= longitude <= 76.0: return "ludhiana"
#     if 22.0 <= latitude <= 23.0 and 88.0 <= longitude <= 89.0: return "kolkata"
#     if 26.0 <= latitude <= 27.0 and 80.0 <= longitude <= 81.0: return "lucknow"
#     return "ludhiana" # Default fallback


# class FarmEnv(gym.Env):
#     def __init__(self, crop_type="Wheat", soil_type="Alluvial", simulation_days=None, 
#                  latitude=30.9010, longitude=75.8573, deterministic_init=False):
#         super(FarmEnv, self).__init__()

#         self.crop_type = crop_type
#         self.soil_type = soil_type
#         self.latitude = latitude
#         self.longitude = longitude
#         self.deterministic_init = deterministic_init
        
#         # Initialize with fixed seed for deterministic behavior if requested
#         if self.deterministic_init:
#             np.random.seed(42)
        
#         self.crop = Crop(crop_type=self.crop_type, deterministic=deterministic_init)
#         self.soil = Soil(soil_type=self.soil_type, deterministic=deterministic_init)

#         if simulation_days is None:
#             self.simulation_days = list(self.crop.growth_stages.values())[-1][-1]
#         else:
#             self.simulation_days = simulation_days
        
#         self.current_day = 0

#         # --- Initialize All AI Brains and Data ---
#         project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
#         model_dir = os.path.join(project_root_path, "models")
#         location_name = get_location_name(self.latitude, self.longitude)
#         scaler_path = os.path.join(model_dir, f"advanced_weather_data_scaler_{location_name}.pkl")
#         self.forecaster = StochasticWeatherForecaster(model_dir, location_name=location_name)
        
#         start_date_fetch = (datetime.strptime("2010-01-01", "%Y-%m-%d") - timedelta(days=30)).strftime("%Y-%m-%d")
#         self.full_weather_data = get_weather_data(latitude=self.latitude, longitude=self.longitude, 
#                                                   start_date=start_date_fetch, end_date="2022-12-31")
#         if self.full_weather_data is None:
#             raise Exception("Could not fetch real weather data.")
        
#         hist_data_for_detector = self.full_weather_data.copy()
#         hist_data_for_detector['date'] = pd.to_datetime(hist_data_for_detector[['YEAR', 'MO', 'DY']].rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day'}))
#         hist_data_for_detector = hist_data_for_detector.set_index('date')
#         self.weather_detector = ExtremeWeatherDetector(latitude, longitude, crop_type)
#         self.weather_detector.historical_data = hist_data_for_detector

#         # IMPROVED: More reasonable action mappings
#         self.action_space = spaces.Dict({
#             "irrigation": spaces.Discrete(5),
#             "fertilizer": spaces.Discrete(5),
#             "pesticide": spaces.Discrete(2)
#         })
        
#         # More conservative and realistic action values
#         self.irrigation_map = {0: 0, 1: 2, 2: 5, 3: 8, 4: 12}  # Reduced from max 20 to 12
#         self.fertilizer_map = {0: 0, 1: 2, 2: 5, 3: 8, 4: 12}  # Reduced from max 20 to 12
#         self.pesticide_map = {0: 0, 1: 1}
        
#         # The Definitive, Richest Observation Space
#         self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(16,), dtype=np.float32)
        
#         # IMPROVED: More balanced economic parameters
#         self.total_irrigation_cost = 0.0
#         self.total_fertilizer_cost = 0.0
#         self.total_pesticide_cost = 0.0
#         self.irrigation_cost_per_mm = 0.05  # Reduced from 0.1
#         self.fertilizer_cost_per_kg = 0.3   # Reduced from 0.5
#         self.pesticide_cost_per_application = 25.0  # Reduced from 50.0
        
#         # IMPROVED: Better revenue calculation
#         self.crop_price_per_kg = 0.8  # Increased from 0.2

#     def _get_observation(self):
#         effective_day = min(self.current_day, self.simulation_days - 1)
        
#         base_obs = [
#             self.soil.moisture_content, self.soil.nitrogen_level,
#             self.crop.health / 100.0, self.current_day / self.simulation_days,
#             np.clip((self.weather_data_np[effective_day, 0] - 5) / 35, 0, 1),
#             np.clip(self.weather_data_np[effective_day, 1] / 50.0, 0, 1),
#             self.crop.accumulated_growth / self.crop.max_potential_growth
#         ]
        
#         current_data_index = self.start_index + self.current_day
#         past_30_days = self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[current_data_index - 30:current_data_index].to_numpy()
#         mean_forecast, std_dev_forecast = self.forecaster.predict(past_30_days)
        
#         current_date = self.start_date_obj + timedelta(days=self.current_day)
#         current_season = self._get_season_from_date(current_date)
#         risks = self.weather_detector.calculate_risks(mean_forecast[:, :2], std_dev_forecast[:, :2], current_season)
        
#         risk_obs = [
#             risks["heat_wave_risk"], risks["cold_wave_risk"], risks["heavy_rain_risk"],
#             risks["drought_risk"], risks["crop_stress_risk"]
#         ]

#         avg_mean_temp = np.mean(mean_forecast[:, 0])
#         avg_mean_rain = np.mean(mean_forecast[:, 1])
#         avg_std_temp = np.mean(std_dev_forecast[:, 0])
#         avg_std_rain = np.mean(std_dev_forecast[:, 1])
#         forecast_stats = [
#             np.clip((avg_mean_temp - 5) / 35, 0, 1),
#             np.clip(avg_mean_rain / 50.0, 0, 1),
#             np.clip(avg_std_temp / 10.0, 0, 1),
#             np.clip(avg_std_rain / 20.0, 0, 1)
#         ]

#         final_obs = base_obs + risk_obs + forecast_stats
        
#         return np.array(final_obs, dtype=np.float32)

#     def reset(self, seed=None, options=None):
#         super().reset(seed=seed)
#         self.current_day = 0
#         self.total_irrigation_cost, self.total_fertilizer_cost, self.total_pesticide_cost = 0.0, 0.0, 0.0
        
#         # IMPROVED: More consistent initialization
#         if self.deterministic_init:
#             np.random.seed(42)
        
#         self.soil = Soil(soil_type=self.soil_type, deterministic=self.deterministic_init)
#         self.crop = Crop(crop_type=self.crop_type, deterministic=self.deterministic_init)

#         max_start_index = len(self.full_weather_data) - self.simulation_days - 1
        
#         # IMPROVED: More consistent start index selection
#         if self.deterministic_init:
#             # Use a fixed reasonable start index
#             self.start_index = 365 * 3  # Start from 3rd year for consistency
#         else:
#             self.start_index = self.np_random.integers(30, max_start_index)
            
#         end_index = self.start_index + self.simulation_days
        
#         self.weather_data_np = self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[self.start_index:end_index].to_numpy()
        
#         start_date_row = self.full_weather_data.iloc[self.start_index]
#         self.start_date_obj = datetime(year=int(start_date_row['YEAR']), month=int(start_date_row['MO']), day=int(start_date_row['DY']))

#         return self._get_observation(), {}

#     def step(self, action):
#         """IMPROVED: Better balanced reward function with intermediate feedback."""
#         irrigation_action = int(action["irrigation"])
#         fertilizer_action = int(action["fertilizer"])
#         pesticide_action = int(action["pesticide"])
        
#         irrigation_amount = self.irrigation_map[irrigation_action]
#         fertilizer_amount = self.fertilizer_map[fertilizer_action]
        
#         if self.pesticide_map[pesticide_action] == 1:
#             self.crop.apply_pesticide()
#             self.total_pesticide_cost += self.pesticide_cost_per_application

#         self.total_irrigation_cost += irrigation_amount * self.irrigation_cost_per_mm
#         self.total_fertilizer_cost += fertilizer_amount * self.fertilizer_cost_per_kg
        
#         # Apply actions and run simulation physics
#         self.soil.add_fertilizer(fertilizer_amount)
#         self.soil.daily_depletion()
#         today_rain = self.weather_data_np[self.current_day, 1]
#         self.soil.add_water(today_rain + irrigation_amount)
#         today_temp = self.weather_data_np[self.current_day, 0]
#         today_humidity = self.weather_data_np[self.current_day, 2] / 100.0
        
#         # Store previous health for intermediate rewards
#         prev_health = self.crop.health
#         prev_growth = self.crop.accumulated_growth
        
#         self.crop.grow_one_day(soil=self.soil, temperature=today_temp, humidity=today_humidity)
#         self.soil.daily_evaporation(temperature=today_temp, humidity=today_humidity)
        
#         self.current_day += 1
#         terminated = self.current_day >= self.simulation_days
#         truncated = False

#         # IMPROVED: Balanced reward system with intermediate feedback
#         daily_reward = 0.0
        
#         # Small intermediate rewards for maintaining health and growth
#         if not terminated:
#             health_change = self.crop.health - prev_health
#             growth_change = self.crop.accumulated_growth - prev_growth
            
#             # Reward health maintenance and growth progress
#             daily_reward += health_change * 0.01  # Small health bonus/penalty
#             daily_reward += growth_change * 0.02  # Small growth progress reward
            
#             # Penalty for excessive resource use when not needed
#             if self.soil.moisture_content > 0.8 and irrigation_amount > 0:
#                 daily_reward -= 0.5  # Penalty for over-irrigation
#             if self.soil.nitrogen_level > 0.8 and fertilizer_amount > 0:
#                 daily_reward -= 0.3  # Penalty for over-fertilization

#         profit = 0
#         # The main reward signal is still given on the final day
#         if terminated:
#             final_yield = self.crop.get_current_yield()
#             health_bonus = self.crop.health
            
#             # IMPROVED: Better revenue calculation
#             revenue = final_yield * self.crop_price_per_kg
#             total_costs = self.total_irrigation_cost + self.total_fertilizer_cost + self.total_pesticide_cost
#             profit = revenue - total_costs
            
#             # IMPROVED: More balanced final reward
#             final_reward = (profit / 1000.0) + (health_bonus / 200.0) + (final_yield / 10000.0)
#             daily_reward += final_reward
            
#         observation = self._get_observation()
        
#         # Get risk alerts for the info dictionary to pass to the frontend
#         mean_fc, std_fc = self.forecaster.predict(self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[self.start_index + self.current_day - 30:self.start_index + self.current_day].to_numpy())
#         current_date = self.start_date_obj + timedelta(days=self.current_day)
#         current_season = self._get_season_from_date(current_date)
#         risks = self.weather_detector.calculate_risks(mean_fc[:, :2], std_fc[:, :2], current_season)
#         alerts = self.weather_detector.get_risk_alerts(risks)
        
#         info = {
#             'yield': self.crop.get_current_yield(), 
#             'health': self.crop.health,
#             'moisture': self.soil.moisture_content, 
#             'nitrogen': self.soil.nitrogen_level,
#             'profit': profit, 
#             'disease_risks': getattr(self.crop, 'disease_risks', {}),
#             'extreme_weather_alerts': alerts,
#             'total_costs': self.total_irrigation_cost + self.total_fertilizer_cost + self.total_pesticide_cost,
#             'revenue': final_yield * self.crop_price_per_kg if terminated else 0
#         }
#         return observation, daily_reward, terminated, truncated, info

#     def _get_season_from_date(self, date_obj):
#         month = date_obj.month
        
#         if self.crop_type in SEASONAL_ADJUSTMENTS:
#             for season, data in SEASONAL_ADJUSTMENTS[self.crop_type].items():
#                 if month in data["months"]:
#                     return season
        
#         if 3 <= month <= 5: return "summer"
#         if 6 <= month <= 9: return "monsoon"
#         if 10 <= month <= 11: return "post-monsoon"
#         return "winter"















import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta

# Import all of our advanced simulation modules
from .core_components import Soil, Crop
from .data_loader import get_weather_data
from .forecaster import StochasticWeatherForecaster
from .extreme_weather import ExtremeWeatherDetector
from .weather_thresholds import SEASONAL_ADJUSTMENTS

# Helper function to map coordinates to a location name for model loading
def get_location_name(latitude, longitude):
    if 24.0 <= latitude <= 25.0 and 84.0 <= longitude <= 85.0: return "aurangabad"
    if 30.0 <= latitude <= 31.0 and 75.0 <= longitude <= 76.0: return "ludhiana"
    if 22.0 <= latitude <= 23.0 and 88.0 <= longitude <= 89.0: return "kolkata"
    if 26.0 <= latitude <= 27.0 and 80.0 <= longitude <= 81.0: return "lucknow"
    return "ludhiana" # Default fallback


class FarmEnv(gym.Env):
    def __init__(self, crop_type="Wheat", soil_type="Alluvial", simulation_days=None, 
                 latitude=30.9010, longitude=75.8573, deterministic_init=False):
        super(FarmEnv, self).__init__()

        self.crop_type = crop_type
        self.soil_type = soil_type
        self.latitude = latitude
        self.longitude = longitude
        self.deterministic_init = deterministic_init
        
        # Initialize with fixed seed for deterministic behavior if requested
        if self.deterministic_init:
            np.random.seed(42)
        
        self.crop = Crop(crop_type=self.crop_type, deterministic=deterministic_init)
        self.soil = Soil(soil_type=self.soil_type, deterministic=deterministic_init)

        if simulation_days is None:
            self.simulation_days = list(self.crop.growth_stages.values())[-1][-1]
        else:
            self.simulation_days = simulation_days
        
        self.current_day = 0

        # --- Initialize All AI Brains and Data ---
        project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        model_dir = os.path.join(project_root_path, "models")
        location_name = get_location_name(self.latitude, self.longitude)
        scaler_path = os.path.join(model_dir, f"advanced_weather_data_scaler_{location_name}.pkl")
        self.forecaster = StochasticWeatherForecaster(model_dir, location_name=location_name)
        
        start_date_fetch = (datetime.strptime("2010-01-01", "%Y-%m-%d") - timedelta(days=30)).strftime("%Y-%m-%d")
        self.full_weather_data = get_weather_data(latitude=self.latitude, longitude=self.longitude, 
                                                  start_date=start_date_fetch, end_date="2022-12-31")
        if self.full_weather_data is None:
            raise Exception("Could not fetch real weather data.")
        
        hist_data_for_detector = self.full_weather_data.copy()
        hist_data_for_detector['date'] = pd.to_datetime(hist_data_for_detector[['YEAR', 'MO', 'DY']].rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day'}))
        hist_data_for_detector = hist_data_for_detector.set_index('date')
        self.weather_detector = ExtremeWeatherDetector(latitude, longitude, crop_type)
        self.weather_detector.historical_data = hist_data_for_detector

        # IMPROVED: More reasonable action mappings
        self.action_space = spaces.Dict({
            "irrigation": spaces.Discrete(5),
            "fertilizer": spaces.Discrete(5),
            "pesticide": spaces.Discrete(2)
        })
        
        # More conservative and realistic action values
        self.irrigation_map = {0: 0, 1: 2, 2: 5, 3: 8, 4: 12}  # Reduced from max 20 to 12
        self.fertilizer_map = {0: 0, 1: 2, 2: 5, 3: 8, 4: 12}  # Reduced from max 20 to 12
        self.pesticide_map = {0: 0, 1: 1}
        
        # The Definitive, Richest Observation Space
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(16,), dtype=np.float32)
        
        # IMPROVED: More balanced economic parameters with fixed costs
        self.total_irrigation_cost = 0.0
        self.total_fertilizer_cost = 0.0
        self.total_pesticide_cost = 0.0
        self.total_fertilizer_applied = 0.0  # Track total fertilizer for yield calculation
        
        # Variable costs
        self.irrigation_cost_per_mm = 0.05  # Reduced from 0.1
        self.fertilizer_cost_per_kg = 0.3   # Reduced from 0.5
        self.pesticide_cost_per_application = 25.0  # Reduced from 50.0
        
        # REALISTIC: Fixed costs per season
        self.seed_cost = 3000      # ₹3000/ha for seeds
        self.labor_cost = 15000    # ₹15000/ha for labor
        self.machinery_cost = 8000 # ₹8000/ha for machinery/equipment
        
        # IMPROVED: Better revenue calculation
        self.crop_price_per_kg = 0.8  # Increased from 0.2

    def _get_observation(self):
        effective_day = min(self.current_day, self.simulation_days - 1)
        
        base_obs = [
            self.soil.moisture_content, self.soil.nitrogen_level,
            self.crop.health / 100.0, self.current_day / self.simulation_days,
            np.clip((self.weather_data_np[effective_day, 0] - 5) / 35, 0, 1),
            np.clip(self.weather_data_np[effective_day, 1] / 50.0, 0, 1),
            self.crop.accumulated_growth / self.crop.max_potential_growth
        ]
        
        current_data_index = self.start_index + self.current_day
        past_30_days = self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[current_data_index - 30:current_data_index].to_numpy()
        mean_forecast, std_dev_forecast = self.forecaster.predict(past_30_days)
        
        current_date = self.start_date_obj + timedelta(days=self.current_day)
        current_season = self._get_season_from_date(current_date)
        risks = self.weather_detector.calculate_risks(mean_forecast[:, :2], std_dev_forecast[:, :2], current_season)
        
        risk_obs = [
            risks["heat_wave_risk"], risks["cold_wave_risk"], risks["heavy_rain_risk"],
            risks["drought_risk"], risks["crop_stress_risk"]
        ]

        avg_mean_temp = np.mean(mean_forecast[:, 0])
        avg_mean_rain = np.mean(mean_forecast[:, 1])
        avg_std_temp = np.mean(std_dev_forecast[:, 0])
        avg_std_rain = np.mean(std_dev_forecast[:, 1])
        forecast_stats = [
            np.clip((avg_mean_temp - 5) / 35, 0, 1),
            np.clip(avg_mean_rain / 50.0, 0, 1),
            np.clip(avg_std_temp / 10.0, 0, 1),
            np.clip(avg_std_rain / 20.0, 0, 1)
        ]

        final_obs = base_obs + risk_obs + forecast_stats
        
        return np.array(final_obs, dtype=np.float32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_day = 0
        self.total_irrigation_cost, self.total_fertilizer_cost, self.total_pesticide_cost = 0.0, 0.0, 0.0
        self.total_fertilizer_applied = 0.0  # Reset fertilizer tracking
        
        # IMPROVED: More consistent initialization
        if self.deterministic_init:
            np.random.seed(42)
        
        self.soil = Soil(soil_type=self.soil_type, deterministic=self.deterministic_init)
        self.crop = Crop(crop_type=self.crop_type, deterministic=self.deterministic_init)

        max_start_index = len(self.full_weather_data) - self.simulation_days - 1
        
        # IMPROVED: More consistent start index selection
        if self.deterministic_init:
            # Use a fixed reasonable start index
            self.start_index = 365 * 3  # Start from 3rd year for consistency
        else:
            self.start_index = self.np_random.integers(30, max_start_index)
            
        end_index = self.start_index + self.simulation_days
        
        self.weather_data_np = self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[self.start_index:end_index].to_numpy()
        
        start_date_row = self.full_weather_data.iloc[self.start_index]
        self.start_date_obj = datetime(year=int(start_date_row['YEAR']), month=int(start_date_row['MO']), day=int(start_date_row['DY']))

        return self._get_observation(), {}

    def step(self, action):
        """IMPROVED: Better balanced reward function with intermediate feedback."""
        irrigation_action = int(action["irrigation"])
        fertilizer_action = int(action["fertilizer"])
        pesticide_action = int(action["pesticide"])
        
        irrigation_amount = self.irrigation_map[irrigation_action]
        fertilizer_amount = self.fertilizer_map[fertilizer_action]
        
        if self.pesticide_map[pesticide_action] == 1:
            self.crop.apply_pesticide()
            self.total_pesticide_cost += self.pesticide_cost_per_application

        self.total_irrigation_cost += irrigation_amount * self.irrigation_cost_per_mm
        self.total_fertilizer_cost += fertilizer_amount * self.fertilizer_cost_per_kg
        self.total_fertilizer_applied += fertilizer_amount  # Track total fertilizer for yield calculation
        
        # Apply actions and run simulation physics
        self.soil.add_fertilizer(fertilizer_amount)
        self.soil.daily_depletion()
        today_rain = self.weather_data_np[self.current_day, 1]
        self.soil.add_water(today_rain + irrigation_amount)
        today_temp = self.weather_data_np[self.current_day, 0]
        today_humidity = self.weather_data_np[self.current_day, 2] / 100.0
        
        # Store previous health for intermediate rewards
        prev_health = self.crop.health
        prev_growth = self.crop.accumulated_growth
        
        self.crop.grow_one_day(soil=self.soil, temperature=today_temp, humidity=today_humidity)
        self.soil.daily_evaporation(temperature=today_temp, humidity=today_humidity)
        
        self.current_day += 1
        terminated = self.current_day >= self.simulation_days
        truncated = False

        # IMPROVED: Balanced reward system with intermediate feedback
        daily_reward = 0.0
        
        # Small intermediate rewards for maintaining health and growth
        if not terminated:
            health_change = self.crop.health - prev_health
            growth_change = self.crop.accumulated_growth - prev_growth
            
            # Reward health maintenance and growth progress
            daily_reward += health_change * 0.01  # Small health bonus/penalty
            daily_reward += growth_change * 0.02  # Small growth progress reward
            
            # Penalty for excessive resource use when not needed
            if self.soil.moisture_content > 0.8 and irrigation_amount > 0:
                daily_reward -= 0.5  # Penalty for over-irrigation
            if self.soil.nitrogen_level > 0.8 and fertilizer_amount > 0:
                daily_reward -= 0.3  # Penalty for over-fertilization

        profit = 0
        # The main reward signal is still given on the final day
        if terminated:
            final_yield = self.crop.get_current_yield(total_season_fertilizer=self.total_fertilizer_applied)
            health_bonus = self.crop.health
            
            # IMPROVED: Realistic cost structure with fixed costs
            revenue = final_yield * self.crop_price_per_kg
            variable_costs = self.total_irrigation_cost + self.total_fertilizer_cost + self.total_pesticide_cost
            fixed_costs = self.seed_cost + self.labor_cost + self.machinery_cost
            total_costs = variable_costs + fixed_costs
            profit = revenue - total_costs
            
            # IMPROVED: More balanced final reward
            final_reward = (profit / 1000.0) + (health_bonus / 200.0) + (final_yield / 10000.0)
            daily_reward += final_reward
            
        observation = self._get_observation()
        
        # Get risk alerts for the info dictionary to pass to the frontend
        mean_fc, std_fc = self.forecaster.predict(self.full_weather_data[['temperature', 'rainfall', 'humidity', 'wind_speed']].iloc[self.start_index + self.current_day - 30:self.start_index + self.current_day].to_numpy())
        current_date = self.start_date_obj + timedelta(days=self.current_day)
        current_season = self._get_season_from_date(current_date)
        risks = self.weather_detector.calculate_risks(mean_fc[:, :2], std_fc[:, :2], current_season)
        alerts = self.weather_detector.get_risk_alerts(risks)
        
        info = {
            'yield': self.crop.get_current_yield(total_season_fertilizer=self.total_fertilizer_applied) if terminated else self.crop.get_current_yield(), 
            'health': self.crop.health,
            'moisture': self.soil.moisture_content, 
            'nitrogen': self.soil.nitrogen_level,
            'profit': profit, 
            'disease_risks': getattr(self.crop, 'disease_risks', {}),
            'extreme_weather_alerts': alerts,
            'total_costs': (self.total_irrigation_cost + self.total_fertilizer_cost + self.total_pesticide_cost + 
                          (self.seed_cost + self.labor_cost + self.machinery_cost if terminated else 0)),
            'revenue': final_yield * self.crop_price_per_kg if terminated else 0,
            'total_fertilizer_applied': self.total_fertilizer_applied,
            'fixed_costs': self.seed_cost + self.labor_cost + self.machinery_cost if terminated else 0,
            'variable_costs': self.total_irrigation_cost + self.total_fertilizer_cost + self.total_pesticide_cost
        }
        return observation, daily_reward, terminated, truncated, info

    def _get_season_from_date(self, date_obj):
        month = date_obj.month
        
        if self.crop_type in SEASONAL_ADJUSTMENTS:
            for season, data in SEASONAL_ADJUSTMENTS[self.crop_type].items():
                if month in data["months"]:
                    return season
        
        if 3 <= month <= 5: return "summer"
        if 6 <= month <= 9: return "monsoon"
        if 10 <= month <= 11: return "post-monsoon"
        return "winter"