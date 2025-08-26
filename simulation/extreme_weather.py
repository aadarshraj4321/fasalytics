# simulation/extreme_weather.py

import numpy as np
from datetime import datetime
from .weather_thresholds import (
    TEMPERATURE_THRESHOLDS, RAINFALL_THRESHOLDS, STATE_THRESHOLDS,
    CROP_VULNERABILITY, DURATION_THRESHOLDS, RISK_LEVELS,
    SEASONAL_ADJUSTMENTS, get_threshold_for_location
)

class ExtremeWeatherDetector:
    """
    Detects extreme weather conditions and calculates risk levels
    for Indian agricultural conditions
    """
    
    def __init__(self, latitude=30.9010, longitude=75.8573, crop_type="Wheat"):
        self.latitude = latitude
        self.longitude = longitude
        self.crop_type = crop_type
        
        # Get location-specific thresholds
        self.location_thresholds = get_threshold_for_location(latitude, longitude, None)
        self.crop_vulnerability = CROP_VULNERABILITY.get(crop_type, CROP_VULNERABILITY["Wheat"])
        
        # Track consecutive days for duration-based events
        self.consecutive_hot_days = 0
        self.consecutive_cold_days = 0
        self.consecutive_dry_days = 0
        self.weekly_rainfall = []
        
    def calculate_risks(self, mean_forecast, std_dev_forecast, current_season=None):
        """
        Calculate extreme weather risks based on 7-day forecast
        
        Args:
            mean_forecast: numpy array (7, 2) - [temp, rainfall] means
            std_dev_forecast: numpy array (7, 2) - [temp, rainfall] std devs
            current_season: string - current season for adjustments
            
        Returns:
            dict: Risk scores for different extreme weather events
        """
        if current_season is None:
            current_season = self._get_current_season()
            
        risks = {
            "heat_wave_risk": 0.0,
            "cold_wave_risk": 0.0, 
            "heavy_rain_risk": 0.0,
            "drought_risk": 0.0,
            "crop_stress_risk": 0.0,
            "overall_risk": 0.0
        }
        
        # Calculate individual risk components
        risks["heat_wave_risk"] = self._calculate_heat_wave_risk(mean_forecast, std_dev_forecast, current_season)
        risks["cold_wave_risk"] = self._calculate_cold_wave_risk(mean_forecast, std_dev_forecast, current_season)
        risks["heavy_rain_risk"] = self._calculate_heavy_rain_risk(mean_forecast, std_dev_forecast, current_season)
        risks["drought_risk"] = self._calculate_drought_risk(mean_forecast, std_dev_forecast, current_season)
        risks["crop_stress_risk"] = self._calculate_crop_stress_risk(mean_forecast, std_dev_forecast)
        
        # Calculate overall risk (weighted average)
        risks["overall_risk"] = self._calculate_overall_risk(risks)
        
        return risks
    
    def _calculate_heat_wave_risk(self, mean_forecast, std_dev_forecast, season):
        """Calculate heat wave risk based on temperature forecast"""
        heat_threshold = self.location_thresholds["heat_wave_temp"]
        
        # Seasonal adjustment
        if season in SEASONAL_ADJUSTMENTS:
            seasonal_factor = SEASONAL_ADJUSTMENTS[season].get("heat_sensitivity_increase", 1.0)
            heat_threshold = heat_threshold / seasonal_factor
        
        risk = 0.0
        consecutive_hot_days = 0
        
        for day in range(len(mean_forecast)):
            temp_mean = mean_forecast[day, 0]
            temp_std = std_dev_forecast[day, 0]
            
            # Probability that temperature exceeds threshold
            prob_exceed = self._calculate_exceedance_probability(temp_mean, temp_std, heat_threshold)
            
            if prob_exceed > 0.5:  # More than 50% chance
                consecutive_hot_days += 1
                day_risk = min(1.0, prob_exceed * (temp_mean - heat_threshold) / 10.0)
                risk = max(risk, day_risk)
            else:
                consecutive_hot_days = 0
        
        # Duration bonus - heat waves need consecutive days
        if consecutive_hot_days >= DURATION_THRESHOLDS["heat_wave_min_days"]:
            risk *= (1.0 + (consecutive_hot_days - 2) * 0.2)
        else:
            risk *= 0.5  # Reduce risk if not consecutive
            
        return min(1.0, risk)
    
    def _calculate_cold_wave_risk(self, mean_forecast, std_dev_forecast, season):
        """Calculate cold wave risk"""
        cold_threshold = self.location_thresholds["cold_wave_temp"]
        
        # Cold waves more likely in winter
        if season == "winter":
            cold_threshold += 2.0  # More sensitive in winter
        
        risk = 0.0
        consecutive_cold_days = 0
        
        for day in range(len(mean_forecast)):
            temp_mean = mean_forecast[day, 0]
            temp_std = std_dev_forecast[day, 0]
            
            # Probability that temperature goes below threshold
            prob_below = self._calculate_exceedance_probability(-temp_mean, temp_std, -cold_threshold)
            
            if prob_below > 0.5:
                consecutive_cold_days += 1
                day_risk = min(1.0, prob_below * (cold_threshold - temp_mean) / 10.0)
                risk = max(risk, day_risk)
            else:
                consecutive_cold_days = 0
        
        # Duration factor
        if consecutive_cold_days >= DURATION_THRESHOLDS["cold_wave_min_days"]:
            risk *= (1.0 + (consecutive_cold_days - 2) * 0.15)
        else:
            risk *= 0.3
            
        return min(1.0, risk)
    
    def _calculate_heavy_rain_risk(self, mean_forecast, std_dev_forecast, season):
        """Calculate heavy rainfall risk"""
        rain_threshold = self.location_thresholds["heavy_rain"]
        
        # Monsoon season adjustment
        if season == "monsoon":
            rain_threshold *= 1.3  # Higher threshold during monsoon
        
        risk = 0.0
        
        for day in range(len(mean_forecast)):
            rain_mean = mean_forecast[day, 1]
            rain_std = std_dev_forecast[day, 1]
            
            # Probability of heavy rain
            prob_heavy_rain = self._calculate_exceedance_probability(rain_mean, rain_std, rain_threshold)
            
            if prob_heavy_rain > 0.3:  # 30% chance threshold
                day_risk = min(1.0, prob_heavy_rain * (rain_mean / rain_threshold))
                risk = max(risk, day_risk)
        
        # Check for weekly accumulation risk
        weekly_total = np.sum(mean_forecast[:, 1])
        if weekly_total > RAINFALL_THRESHOLDS["excess_weekly"]:
            weekly_risk = min(1.0, weekly_total / RAINFALL_THRESHOLDS["excess_weekly"] - 1.0)
            risk = max(risk, weekly_risk)
            
        return min(1.0, risk)
    
    def _calculate_drought_risk(self, mean_forecast, std_dev_forecast, season):
        """Calculate drought risk based on low rainfall"""
        drought_threshold = self.location_thresholds["drought_threshold"]
        
        # Seasonal adjustment
        if season in ["winter", "summer"]:
            drought_threshold *= 0.5  # Lower expectations in dry seasons
        
        risk = 0.0
        consecutive_dry_days = 0
        
        for day in range(len(mean_forecast)):
            rain_mean = mean_forecast[day, 1]
            rain_std = std_dev_forecast[day, 1]
            
            # Probability of very low rainfall
            prob_dry = self._calculate_exceedance_probability(-rain_mean, rain_std, -drought_threshold)
            
            if prob_dry > 0.7:  # High probability of dry day
                consecutive_dry_days += 1
            else:
                consecutive_dry_days = 0
        
        # Drought risk increases with consecutive dry days
        if consecutive_dry_days >= DURATION_THRESHOLDS["drought_min_days"]:
            risk = min(1.0, consecutive_dry_days / 14.0)  # Max risk after 14 dry days
        elif consecutive_dry_days >= 3:
            risk = consecutive_dry_days / 10.0
            
        return min(1.0, risk)
    
    def _calculate_crop_stress_risk(self, mean_forecast, std_dev_forecast):
        """Calculate crop-specific stress risk"""
        stress_risk = 0.0
        
        for day in range(len(mean_forecast)):
            temp_mean = mean_forecast[day, 0]
            rain_mean = mean_forecast[day, 1]
            
            # Temperature stress
            critical_temp = self.crop_vulnerability["heat_wave_critical_temp"]
            if temp_mean > critical_temp:
                temp_stress = min(1.0, (temp_mean - critical_temp) / 10.0)
                stress_risk = max(stress_risk, temp_stress)
            
            # Cold stress
            cold_tolerance = self.crop_vulnerability["cold_tolerance"]
            if temp_mean < cold_tolerance:
                cold_stress = min(1.0, (cold_tolerance - temp_mean) / 10.0)
                stress_risk = max(stress_risk, cold_stress)
        
        # Water stress
        total_weekly_rain = np.sum(mean_forecast[:, 1])
        drought_days = self.crop_vulnerability["drought_stress_days"]
        if total_weekly_rain < (drought_days * 2.0):  # Less than 2mm per critical day
            water_stress = min(1.0, 1.0 - (total_weekly_rain / (drought_days * 2.0)))
            stress_risk = max(stress_risk, water_stress)
            
        return min(1.0, stress_risk)
    
    def _calculate_overall_risk(self, risks):
        """Calculate weighted overall risk"""
        weights = {
            "heat_wave_risk": 0.25,
            "cold_wave_risk": 0.15,
            "heavy_rain_risk": 0.20,
            "drought_risk": 0.25,
            "crop_stress_risk": 0.15
        }
        
        overall = 0.0
        for risk_type, weight in weights.items():
            overall += risks[risk_type] * weight
            
        return min(1.0, overall)
    
    def _calculate_exceedance_probability(self, mean, std, threshold):
        """Calculate probability that value exceeds threshold using normal distribution"""
        if std <= 0:
            return 1.0 if mean > threshold else 0.0
        
        # Z-score calculation
        z_score = (threshold - mean) / std
        
        # Using complementary error function approximation
        # P(X > threshold) = 1 - P(X <= threshold)
        if z_score > 3:
            return 0.0
        elif z_score < -3:
            return 1.0
        else:
            # Simple approximation for normal distribution
            prob = 0.5 * (1.0 + np.tanh(z_score * 0.7978845))  # Approximation
            return 1.0 - prob
    
    def _get_current_season(self):
        """Determine current season based on month"""
        current_month = datetime.now().month
        
        for season, data in SEASONAL_ADJUSTMENTS.items():
            if current_month in data["months"]:
                return season
        
        return "summer"  # Default fallback
    
    def get_risk_severity_level(self, risk_value):
        """Convert risk value to severity level"""
        for level, data in RISK_LEVELS.items():
            if data["min"] <= risk_value <= data["max"]:
                return level
        return "low"
    
    def get_risk_alerts(self, risks):
        """Generate human-readable alerts based on risk levels"""
        alerts = []
        
        for risk_type, risk_value in risks.items():
            if risk_value > 0.6:  # High risk threshold
                severity = self.get_risk_severity_level(risk_value)
                
                if risk_type == "heat_wave_risk":
                    alerts.append(f"{severity.upper()} heat wave risk - protect crops from heat stress")
                elif risk_type == "heavy_rain_risk":
                    alerts.append(f"{severity.upper()} heavy rainfall risk - ensure proper drainage")
                elif risk_type == "drought_risk":
                    alerts.append(f"{severity.upper()} drought risk - arrange irrigation immediately")
                elif risk_type == "cold_wave_risk":
                    alerts.append(f"{severity.upper()} cold wave risk - protect sensitive crops")
                elif risk_type == "crop_stress_risk":
                    alerts.append(f"{severity.upper()} crop stress risk - monitor crop health closely")
        
        return alerts