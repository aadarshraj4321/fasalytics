# simulation/weather_events.py

import pandas as pd

class WeatherEventManager:
    def __init__(self, historical_weather_df):
        """
        Initializes the manager with a long-term historical weather DataFrame.
        """
        if historical_weather_df is None or historical_weather_df.empty:
            raise ValueError("Historical weather data cannot be empty.")
        
        self.historical_data = historical_weather_df
        print("WeatherEventManager initialized with historical data.")

    def get_daily_heat_wave_prob(self, current_day_of_year: int, current_temp: float) -> float:
        """
        Calculates the probability of a heat wave for a given day.
        
        This is a simple model based on historical averages.
        """
        # A simple model: heat wave risk is highest in May/June (days 120-180)
        if not (120 <= current_day_of_year <= 180):
            return 0.0 # No risk outside of peak summer months

        # Get the average temperature for this specific day of the year from all historical data
        # Day of year is 1-366
        avg_temp_for_this_day = self.historical_data[
            self.historical_data.index.dayofyear == current_day_of_year
        ]['temperature'].mean()

        # If today's temperature is significantly higher than the historical average, risk increases
        temp_difference = current_temp - avg_temp_for_this_day
        
        if temp_difference < 5: # If temp is less than 5°C above average, risk is low
            return 0.05
        
        # The probability increases as the temperature difference grows
        # A very simple linear model for probability
        probability = 0.05 + (temp_difference - 5) * 0.05
        
        return min(1.0, probability) # Cap probability at 1.0 (100%)

    def get_monsoon_forecast(self):
        """
        Analyzes historical data to predict monsoon onset/withdrawal.
        (This is a complex placeholder for now).
        """
        # Placeholder logic: Find the average day of the year when rainfall starts to pick up
        # We define "monsoon start" as the first day after day 150 (end of May)
        # where the 7-day rolling average of rain exceeds 5mm.
        
        # This is a very complex task. For now, we will return a simple placeholder.
        # A full implementation would require deep climatological analysis.
        
        return {
            "onset_prediction": "Normal", # Could be "Early", "Normal", "Late"
            "intensity_prediction": "Moderate", # Could be "Weak", "Moderate", "Strong"
            "confidence": 0.75 # Confidence in the prediction
        }

# Example of how to use this class
if __name__ == '__main__':
    # This requires the updated data_loader
    from data_loader import get_weather_data
    
    # Load 10 years of data for analysis
    hist_data = get_weather_data(30.9010, 75.8573, "2013-01-01", "2022-12-31")
    
    if hist_data is not None:
        # Convert date columns to a proper datetime index for easier analysis
        hist_data['date'] = pd.to_datetime(hist_data[['YEAR', 'MO', 'DY']].rename(columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day'}))
        hist_data = hist_data.set_index('date')

        # Create the manager
        event_manager = WeatherEventManager(hist_data)
        
        # Test the heat wave probability function
        # A hot day in June (day 166)
        day_of_year_june = 166
        current_temp_hot = 42.0 # A very hot day
        prob_hot = event_manager.get_daily_heat_wave_prob(day_of_year_june, current_temp_hot)
        print(f"Probability of heat wave on a {current_temp_hot}°C day in June: {prob_hot*100:.1f}%")
        
        # A normal day in June
        current_temp_normal = 36.0
        prob_normal = event_manager.get_daily_heat_wave_prob(day_of_year_june, current_temp_normal)
        print(f"Probability of heat wave on a {current_temp_normal}°C day in June: {prob_normal*100:.1f}%")

        # A day in December
        day_of_year_dec = 350
        prob_dec = event_manager.get_daily_heat_wave_prob(day_of_year_dec, 20.0)
        print(f"Probability of heat wave in December: {prob_dec*100:.1f}%")

        # Test monsoon forecast (will return placeholder for now)
        monsoon_pred = event_manager.get_monsoon_forecast()
        print(f"\nMonsoon Forecast: {monsoon_pred}")