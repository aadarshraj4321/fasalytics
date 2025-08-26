# simulation/weather_thresholds.py

"""
Extreme Weather Thresholds for Indian Agricultural Conditions
Based on IMD standards and regional agricultural practices
"""

# Temperature thresholds (Celsius)
TEMPERATURE_THRESHOLDS = {
    "heat_wave": {
        "plains": 40.0,      # Plains regions (Punjab, UP, Bihar)
        "coastal": 37.0,     # Coastal areas (West Bengal coastal)
        "hilly": 30.0        # Hilly regions
    },
    "severe_heat_wave": {
        "plains": 45.0,
        "coastal": 40.0,
        "hilly": 35.0
    },
    "cold_wave": {
        "northern": 4.0,     # Punjab, UP northern parts
        "central": 6.0,      # Central regions
        "eastern": 8.0       # West Bengal, Bihar
    }
}

# Rainfall thresholds (mm)
RAINFALL_THRESHOLDS = {
    "heavy_rain": 64.5,          # Heavy rain in 24 hours (IMD standard)
    "very_heavy_rain": 115.6,    # Very heavy rain in 24 hours
    "extremely_heavy_rain": 204.4, # Extremely heavy rain in 24 hours
    "drought_daily": 2.0,        # Less than 2mm daily indicates drought risk
    "excess_weekly": 200.0       # More than 200mm in a week
}

# State-specific thresholds for major agricultural states
STATE_THRESHOLDS = {
    "Punjab": {
        "heat_wave_temp": 42.0,
        "cold_wave_temp": 2.0,
        "heavy_rain": 75.0,
        "drought_threshold": 1.5,
        "region_type": "plains"
    },
    "Uttar Pradesh": {
        "heat_wave_temp": 41.0,
        "cold_wave_temp": 4.0,
        "heavy_rain": 70.0,
        "drought_threshold": 2.0,
        "region_type": "plains"
    },
    "Bihar": {
        "heat_wave_temp": 40.0,
        "cold_wave_temp": 6.0,
        "heavy_rain": 80.0,
        "drought_threshold": 2.5,
        "region_type": "eastern"
    },
    "West Bengal": {
        "heat_wave_temp": 37.0,
        "cold_wave_temp": 8.0,
        "heavy_rain": 100.0,
        "drought_threshold": 3.0,
        "region_type": "coastal"
    }
}

# Crop-specific vulnerability to extreme weather
CROP_VULNERABILITY = {
    "Wheat": {
        "heat_wave_critical_temp": 35.0,    # Above this, severe yield loss
        "cold_tolerance": 5.0,              # Can tolerate cold better
        "waterlogging_tolerance": 2,        # Days of waterlogging tolerable
        "drought_stress_days": 7            # Days without water before stress
    },
    "Rice": {
        "heat_wave_critical_temp": 38.0,
        "cold_tolerance": 15.0,             # More sensitive to cold
        "waterlogging_tolerance": 30,       # Very tolerant to waterlogging
        "drought_stress_days": 3            # Needs regular water
    },
    "Sugarcane": {
        "heat_wave_critical_temp": 42.0,    # More heat tolerant
        "cold_tolerance": 10.0,
        "waterlogging_tolerance": 15,
        "drought_stress_days": 10           # More drought tolerant
    }
}

# Duration requirements for extreme weather classification
DURATION_THRESHOLDS = {
    "heat_wave_min_days": 2,           # Minimum 2 consecutive days
    "cold_wave_min_days": 2,           # Minimum 2 consecutive days
    "heavy_rain_max_duration": 1,      # Single day event
    "drought_min_days": 7,             # Minimum 7 days of low rainfall
    "excess_rain_period": 7            # Weekly accumulation check
}

# Risk severity levels
RISK_LEVELS = {
    "low": {"min": 0.0, "max": 0.3, "color": "green"},
    "moderate": {"min": 0.3, "max": 0.6, "color": "yellow"},
    "high": {"min": 0.6, "max": 0.8, "color": "orange"},
    "severe": {"min": 0.8, "max": 1.0, "color": "red"}
}

# Regional climate patterns (monsoon, post-monsoon, winter, summer)
SEASONAL_ADJUSTMENTS = {
    "monsoon": {
        "months": [6, 7, 8, 9],  # June to September
        "rain_expectation_multiplier": 1.5,
        "heat_tolerance_increase": 2.0
    },
    "post_monsoon": {
        "months": [10, 11],
        "rain_expectation_multiplier": 0.3,
        "heat_tolerance_increase": 0.0
    },
    "winter": {
        "months": [12, 1, 2],
        "rain_expectation_multiplier": 0.2,
        "cold_sensitivity_increase": 1.5
    },
    "summer": {
        "months": [3, 4, 5],
        "rain_expectation_multiplier": 0.1,
        "heat_sensitivity_increase": 1.2
    }
}

def get_threshold_for_location(latitude, longitude, parameter):
    """
    Get location-specific threshold based on coordinates
    Simplified mapping for major agricultural regions
    """
    # Punjab region
    if 30.0 <= latitude <= 32.0 and 74.0 <= longitude <= 77.0:
        return STATE_THRESHOLDS["Punjab"]
    
    # UP region
    elif 24.0 <= latitude <= 30.0 and 77.0 <= longitude <= 84.0:
        return STATE_THRESHOLDS["Uttar Pradesh"]
    
    # Bihar region  
    elif 24.0 <= latitude <= 27.5 and 83.0 <= longitude <= 88.0:
        return STATE_THRESHOLDS["Bihar"]
    
    # West Bengal region
    elif 21.5 <= latitude <= 27.0 and 85.0 <= longitude <= 90.0:
        return STATE_THRESHOLDS["West Bengal"]
    
    # Default fallback
    else:
        return STATE_THRESHOLDS["Uttar Pradesh"]  # Use UP as default