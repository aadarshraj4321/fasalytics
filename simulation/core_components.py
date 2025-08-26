# # simulation/core_components.py

# import numpy as np

# class Soil:
#     def __init__(self, soil_type: str, initial_moisture: float = None):
#         self.soil_type = soil_type
        
#         # ENHANCED: More realistic soil parameters
#         if soil_type == "Alluvial":
#             self.field_capacity = 0.8
#             self.wilting_point = 0.2
#             self.drainage_rate = 0.02  # Daily drainage coefficient
#             self.nutrient_retention = 0.95  # How well soil retains nutrients
#         elif soil_type == "Black":
#             self.field_capacity = 0.9
#             self.wilting_point = 0.22
#             self.drainage_rate = 0.015  # Better water retention
#             self.nutrient_retention = 0.97  # Excellent nutrient retention
#         else:  # Sandy or other
#             self.field_capacity = 0.75
#             self.wilting_point = 0.22
#             self.drainage_rate = 0.03  # Poor water retention
#             self.nutrient_retention = 0.92  # Poor nutrient retention
        
#         # ENHANCED: More sophisticated initialization
#         if initial_moisture is None:
#             # Start with varied but reasonable moisture levels
#             self.moisture_content = np.random.uniform(
#                 self.wilting_point + 0.1, 
#                 self.field_capacity - 0.1
#             )
#         else:
#             self.moisture_content = initial_moisture
            
#         # ENHANCED: More realistic nitrogen starting levels
#         self.nitrogen_level = np.random.uniform(0.15, 0.5)
        
#         # ENHANCED: Additional soil properties
#         self.ph_level = np.random.uniform(6.0, 7.5)  # Soil pH
#         self.organic_matter = np.random.uniform(0.2, 0.6)  # Organic matter content
#         self.compaction_level = np.random.uniform(0.1, 0.3)  # Soil compaction

#     def add_water(self, amount_mm: float):
#         """Enhanced water addition with drainage consideration."""
#         water_added = amount_mm / 1000.0
        
#         # ENHANCED: Consider soil compaction affecting water infiltration
#         infiltration_efficiency = 1.0 - (self.compaction_level * 0.3)
#         effective_water = water_added * infiltration_efficiency
        
#         self.moisture_content += effective_water
        
#         # ENHANCED: Natural drainage above field capacity
#         if self.moisture_content > self.field_capacity:
#             excess_water = self.moisture_content - self.field_capacity
#             drainage = excess_water * self.drainage_rate
#             self.moisture_content = self.field_capacity + (excess_water - drainage)

#     def daily_evaporation(self, temperature: float, humidity: float = 0.6):
#         """Enhanced evaporation model with humidity consideration."""
#         # ENHANCED: More sophisticated evaporation calculation
#         base_evaporation = (temperature - 10) / 400.0  # Base evaporation rate
#         humidity_factor = (1.0 - humidity) * 1.2  # Lower humidity = more evaporation
#         moisture_factor = min(1.0, self.moisture_content / (self.wilting_point + 0.1))
        
#         total_evaporation = base_evaporation * humidity_factor * moisture_factor
#         total_evaporation = max(0, total_evaporation)  # No negative evaporation
        
#         self.moisture_content -= total_evaporation
#         self.moisture_content = max(0, self.moisture_content)

#     def add_fertilizer(self, amount_kg_per_ha: float):
#         """Enhanced fertilization with efficiency consideration."""
#         # ENHANCED: Fertilizer efficiency depends on soil conditions
#         base_efficiency = 0.8  # 80% base efficiency
#         moisture_efficiency = 1.0
        
#         if self.moisture_content < self.wilting_point:
#             moisture_efficiency = 0.5  # Poor uptake in dry soil
#         elif self.moisture_content > self.field_capacity:
#             moisture_efficiency = 0.7  # Some leaching in waterlogged soil
            
#         ph_efficiency = 1.0
#         if not (6.0 <= self.ph_level <= 7.5):
#             ph_efficiency = 0.8  # Reduced efficiency outside optimal pH
            
#         total_efficiency = base_efficiency * moisture_efficiency * ph_efficiency
#         effective_fertilizer = (amount_kg_per_ha / 100.0) * total_efficiency
        
#         self.nitrogen_level += effective_fertilizer
#         self.nitrogen_level = min(1.0, self.nitrogen_level)

#     def daily_depletion(self):
#         """Enhanced nutrient depletion model."""
#         # ENHANCED: Depletion rate varies with soil type and conditions
#         base_depletion = 1.0 - (1.0 / 100.0)  # 1% base depletion
#         retention_factor = self.nutrient_retention
        
#         # Organic matter helps retain nutrients
#         organic_bonus = self.organic_matter * 0.05
#         final_retention = min(0.99, retention_factor + organic_bonus)
        
#         self.nitrogen_level *= final_retention

#     def get_stress_factors(self):
#         """Get current stress factors for the crop."""
#         water_stress = 0.0
#         nutrient_stress = 0.0
        
#         if self.moisture_content < self.wilting_point:
#             water_stress = (self.wilting_point - self.moisture_content) / self.wilting_point
#         elif self.moisture_content > self.field_capacity:
#             water_stress = (self.moisture_content - self.field_capacity) * 0.5
            
#         if self.nitrogen_level < 0.3:
#             nutrient_stress = (0.3 - self.nitrogen_level) / 0.3
#         elif self.nitrogen_level > 0.9:
#             nutrient_stress = (self.nitrogen_level - 0.9) * 2.0
            
#         return min(1.0, water_stress), min(1.0, nutrient_stress)


# class Crop:
#     def __init__(self, crop_type: str):
#         self.crop_type = crop_type
#         self.growth_stage = "Seed"
#         self.health = np.random.uniform(90, 100)  # Slight variation in initial health
#         self.age = 0
#         self.accumulated_growth = 0.0
#         self.max_potential_growth = 100.0

#         self.height = 0.0 # Height in meters
#         self.max_height = 1.2 # Max possible height for Wheat in meters
        
#         # --- NEW: pest/pesticide properties ---
#         self.rust_risk = 0.0
#         self.pesticide_active_days = 0
        
#         # ENHANCED: Crop-specific parameters for Wheat, Rice, and Sugarcane
#         if crop_type == "Wheat":
#             self.potential_yield_kg_per_ha = np.random.uniform(4500, 5500)
#             self.optimal_temp_min, self.optimal_temp_max = 15, 25
#             self.max_height = 1.2 # Meters
#             self.growth_stages = { "Seed": (0, 7), "Germination": (7, 15), "Vegetative": (15, 45), "Flowering": (45, 70), "Mature": (70, 90) }
#         elif crop_type == "Rice":
#             self.potential_yield_kg_per_ha = np.random.uniform(5000, 6500)
#             self.optimal_temp_min, self.optimal_temp_max = 21, 37
#             self.max_height = 1.0 # Meters
#             self.growth_stages = { "Seed": (0, 5), "Germination": (5, 15), "Vegetative": (15, 50), "Flowering": (50, 80), "Mature": (80, 110) }
#         elif crop_type == "Sugarcane":
#             self.potential_yield_kg_per_ha = np.random.uniform(60000, 80000)
#             self.optimal_temp_min, self.optimal_temp_max = 25, 35
#             self.max_height = 4.0 # Meters, Sugarcane is tall
#             self.growth_stages = { "Seed": (0, 20), "Germination": (20, 40), "Vegetative": (40, 150), "Flowering": (150, 250), "Mature": (250, 365) }
#         else:  # Default crop
#             self.potential_yield_kg_per_ha = np.random.uniform(4000, 6000)
#             self.optimal_temp_min, self.optimal_temp_max = 18, 28
#             self.growth_stages = { "Seed": (0, 5), "Germination": (5, 12), "Vegetative": (12, 40), "Flowering": (40, 65), "Mature": (65, 90) }
        
#         # ENHANCED: Additional crop properties
#         self.stress_resistance = np.random.uniform(0.7, 0.9)
#         self.disease_resistance = np.random.uniform(0.8, 0.95)
#         self.consecutive_stress_days = 0

#     def apply_pesticide(self):
#         """Activates pesticide effect for a few days."""
#         self.pesticide_active_days = 4 # Pesticide is effective for 4 days

#     def grow_one_day(self, soil: Soil, temperature: float, humidity: float = 0.6):
#         """Enhanced growth model with more realistic factors."""
#         self.age += 1

#         if self.pesticide_active_days > 0:
#             self.pesticide_active_days -= 1
        
#         # --- NEW: More Sophisticated Pest & Disease Model ---
#         # Calculate specific risk for Wheat Rust
#         self.rust_risk = 0.0
#         if self.crop_type == "Wheat":
#             # Rust thrives in cool, humid conditions
#             if 15 < temperature < 22 and soil.moisture_content > (soil.field_capacity - 0.1):
#                 risk_factor = ((temperature - 15) / 7.0) + (soil.moisture_content - (soil.field_capacity - 0.1))
#                 self.rust_risk = min(1.0, risk_factor * 0.6)

#         # Suppress risk if pesticide is active
#         if self.pesticide_active_days > 0:
#             self.rust_risk *= 0.1 # 90% reduction in risk
        
#         # Get stress factors from soil
#         water_stress, nutrient_stress = soil.get_stress_factors()
        
#         # ENHANCED: Temperature stress calculation
#         temp_stress = 0.0
#         if temperature < self.optimal_temp_min:
#             temp_stress = (self.optimal_temp_min - temperature) / 15.0
#         elif temperature > self.optimal_temp_max:
#             temp_stress = (temperature - self.optimal_temp_max) / 15.0
#         temp_stress = min(1.0, temp_stress)
        
#         # ENHANCED: Overall stress calculation
#         total_stress = (water_stress + nutrient_stress + temp_stress) / 3.0
        
#         # Track consecutive stress days
#         if total_stress > 0.3:
#             self.consecutive_stress_days += 1
#         else:
#             self.consecutive_stress_days = 0
            
#         # ENHANCED: Health changes based on stress and resistance
#         if total_stress > 0.5:
#             health_decline = total_stress * 8.0 * (1.0 - self.stress_resistance)
#             if self.consecutive_stress_days > 3:
#                 health_decline *= (1.0 + (self.consecutive_stress_days - 3) * 0.1)
#             self.health -= health_decline
#         elif total_stress < 0.2:
#             self.health += 1.5 * (1.0 - total_stress)

#         # --- NEW: Apply health penalty from Rust risk ---
#         if self.rust_risk > 0.2:
#             rust_damage = self.rust_risk * 5.0 * (1.0 - self.disease_resistance)
#             self.health -= rust_damage
            
#         self.health = max(0, min(100, self.health))
        
#         # ENHANCED: Growth factor calculation
#         growth_factor = 1.0 - total_stress
#         health_factor = self.health / 100.0
#         stage_modifier = self._get_stage_growth_modifier()
#         final_growth_factor = growth_factor * health_factor * stage_modifier
        
#         # Apply growth if in growing period
#         if self._is_growing_stage():
#             daily_potential_growth = self.max_potential_growth / 90
#             actual_growth = daily_potential_growth * final_growth_factor
#             self.accumulated_growth += actual_growth
        
#         self.height = (self.accumulated_growth / self.max_potential_growth) * self.max_height
        
#         # Update growth stage
#         self._update_growth_stage()

#     def _get_stage_growth_modifier(self):
#         """Get growth modifier based on current stage."""
#         stage_modifiers = {
#             "Seed": 0.1, "Germination": 0.3, "Vegetative": 1.2,
#             "Flowering": 0.8, "Mature": 0.2
#         }
#         return stage_modifiers.get(self.growth_stage, 1.0)

#     def _is_growing_stage(self):
#         """Check if crop is in a growing stage."""
#         return self.growth_stage in ["Germination", "Vegetative", "Flowering"]

#     def _update_growth_stage(self):
#         """Update growth stage based on age."""
#         max_age = list(self.growth_stages.values())[-1][-1]
#         for stage, (start_day, end_day) in self.growth_stages.items():
#             if start_day <= self.age < end_day:
#                 self.growth_stage = stage
#                 break
#         if self.age >= max_age:
#             self.growth_stage = "Mature"

#     def get_current_yield(self) -> float:
#         """Enhanced yield calculation with multiple factors."""
#         growth_ratio = min(1.0, self.accumulated_growth / self.max_potential_growth)
#         base_yield = self.potential_yield_kg_per_ha * growth_ratio
#         health_factor = (self.health / 100.0) ** 0.5
#         stage_bonus = 1.0
#         max_age = list(self.growth_stages.values())[-1][-1]
#         if self.growth_stage == "Mature" and self.age >= (max_age - 5):
#             stage_bonus = 1.1
#         final_yield = base_yield * health_factor * stage_bonus
#         return max(0, final_yield)

#     def get_growth_info(self):
#         """Get detailed growth information."""
#         return {
#             'stage': self.growth_stage, 'age': self.age, 'health': self.health,
#             'growth_progress': (self.accumulated_growth / self.max_potential_growth) * 100,
#             'stress_resistance': self.stress_resistance,
#             'consecutive_stress_days': self.consecutive_stress_days,
#             'potential_yield': self.potential_yield_kg_per_ha
#         }















# import numpy as np
# from .pest_database import PEST_DATABASE

# class Soil:
#     def __init__(self, soil_type: str, initial_moisture: float = None):
#         self.soil_type = soil_type
        
#         # ENHANCED: More realistic soil parameters
#         if soil_type == "Alluvial":
#             self.field_capacity = 0.8
#             self.wilting_point = 0.2
#             self.drainage_rate = 0.02  # Daily drainage coefficient
#             self.nutrient_retention = 0.95  # How well soil retains nutrients
#         elif soil_type == "Black":
#             self.field_capacity = 0.9
#             self.wilting_point = 0.22
#             self.drainage_rate = 0.015  # Better water retention
#             self.nutrient_retention = 0.97  # Excellent nutrient retention
#         else:  # Sandy or other
#             self.field_capacity = 0.75
#             self.wilting_point = 0.22
#             self.drainage_rate = 0.03  # Poor water retention
#             self.nutrient_retention = 0.92  # Poor nutrient retention
        
#         # ENHANCED: More sophisticated initialization
#         if initial_moisture is None:
#             # Start with varied but reasonable moisture levels
#             self.moisture_content = np.random.uniform(
#                 self.wilting_point + 0.1, 
#                 self.field_capacity - 0.1
#             )
#         else:
#             self.moisture_content = initial_moisture
            
#         # ENHANCED: More realistic nitrogen starting levels
#         self.nitrogen_level = np.random.uniform(0.15, 0.5)
        
#         # ENHANCED: Additional soil properties
#         self.ph_level = np.random.uniform(6.0, 7.5)  # Soil pH
#         self.organic_matter = np.random.uniform(0.2, 0.6)  # Organic matter content
#         self.compaction_level = np.random.uniform(0.1, 0.3)  # Soil compaction

#     def add_water(self, amount_mm: float):
#         """Enhanced water addition with drainage consideration."""
#         water_added = amount_mm / 1000.0
        
#         # ENHANCED: Consider soil compaction affecting water infiltration
#         infiltration_efficiency = 1.0 - (self.compaction_level * 0.3)
#         effective_water = water_added * infiltration_efficiency
        
#         self.moisture_content += effective_water
        
#         # ENHANCED: Natural drainage above field capacity
#         if self.moisture_content > self.field_capacity:
#             excess_water = self.moisture_content - self.field_capacity
#             drainage = excess_water * self.drainage_rate
#             self.moisture_content = self.field_capacity + (excess_water - drainage)

#     def daily_evaporation(self, temperature: float, humidity: float = 0.6):
#         """Enhanced evaporation model with humidity consideration."""
#         # ENHANCED: More sophisticated evaporation calculation
#         base_evaporation = (temperature - 10) / 400.0  # Base evaporation rate
#         humidity_factor = (1.0 - humidity) * 1.2  # Lower humidity = more evaporation
#         moisture_factor = min(1.0, self.moisture_content / (self.wilting_point + 0.1))
        
#         total_evaporation = base_evaporation * humidity_factor * moisture_factor
#         total_evaporation = max(0, total_evaporation)  # No negative evaporation
        
#         self.moisture_content -= total_evaporation
#         self.moisture_content = max(0, self.moisture_content)

#     def add_fertilizer(self, amount_kg_per_ha: float):
#         """Enhanced fertilization with efficiency consideration."""
#         # ENHANCED: Fertilizer efficiency depends on soil conditions
#         base_efficiency = 0.8  # 80% base efficiency
#         moisture_efficiency = 1.0
        
#         if self.moisture_content < self.wilting_point:
#             moisture_efficiency = 0.5  # Poor uptake in dry soil
#         elif self.moisture_content > self.field_capacity:
#             moisture_efficiency = 0.7  # Some leaching in waterlogged soil
            
#         ph_efficiency = 1.0
#         if not (6.0 <= self.ph_level <= 7.5):
#             ph_efficiency = 0.8  # Reduced efficiency outside optimal pH
            
#         total_efficiency = base_efficiency * moisture_efficiency * ph_efficiency
#         effective_fertilizer = (amount_kg_per_ha / 100.0) * total_efficiency
        
#         self.nitrogen_level += effective_fertilizer
#         self.nitrogen_level = min(1.0, self.nitrogen_level)

#     def daily_depletion(self):
#         """Enhanced nutrient depletion model."""
#         # ENHANCED: Depletion rate varies with soil type and conditions
#         base_depletion = 1.0 - (1.0 / 100.0)  # 1% base depletion
#         retention_factor = self.nutrient_retention
        
#         # Organic matter helps retain nutrients
#         organic_bonus = self.organic_matter * 0.05
#         final_retention = min(0.99, retention_factor + organic_bonus)
        
#         self.nitrogen_level *= final_retention

#     def get_stress_factors(self):
#         """Get current stress factors for the crop."""
#         water_stress = 0.0
#         nutrient_stress = 0.0
        
#         if self.moisture_content < self.wilting_point:
#             water_stress = (self.wilting_point - self.moisture_content) / self.wilting_point
#         elif self.moisture_content > self.field_capacity:
#             water_stress = (self.moisture_content - self.field_capacity) * 0.5
            
#         if self.nitrogen_level < 0.3:
#             nutrient_stress = (0.3 - self.nitrogen_level) / 0.3
#         elif self.nitrogen_level > 0.9:
#             nutrient_stress = (self.nitrogen_level - 0.9) * 2.0
            
#         return min(1.0, water_stress), min(1.0, nutrient_stress)


# class Crop:
#     def __init__(self, crop_type: str):
#         self.crop_type = crop_type
#         self.growth_stage = "Seed"
#         self.health = np.random.uniform(90, 100)  # Slight variation in initial health
#         self.age = 0
#         self.accumulated_growth = 0.0
#         self.max_potential_growth = 100.0
#         self.height = 0.0
#         self.max_height = 1.2
        
#         # --- NEW: Properties for the advanced pest model ---
#         self.disease_risks = {}
#         self.pesticide_active_days = 0
        
#         # ENHANCED: Crop-specific parameters for Wheat, Rice, and Sugarcane
#         if crop_type == "Wheat":
#             self.potential_yield_kg_per_ha = np.random.uniform(4500, 5500)
#             self.optimal_temp_min, self.optimal_temp_max = 15, 25
#             self.max_height = 1.2
#             self.growth_stages = { "Seed": (0, 7), "Germination": (7, 15), "Vegetative": (15, 45), "Flowering": (45, 70), "Mature": (70, 90) }
#         elif crop_type == "Rice":
#             self.potential_yield_kg_per_ha = np.random.uniform(5000, 6500)
#             self.optimal_temp_min, self.optimal_temp_max = 21, 37
#             self.max_height = 1.0
#             self.growth_stages = { "Seed": (0, 5), "Germination": (5, 15), "Vegetative": (15, 50), "Flowering": (50, 80), "Mature": (80, 110) }
#         elif crop_type == "Sugarcane":
#             self.potential_yield_kg_per_ha = np.random.uniform(60000, 80000)
#             self.optimal_temp_min, self.optimal_temp_max = 25, 35
#             self.max_height = 4.0
#             self.growth_stages = { "Seed": (0, 20), "Germination": (20, 40), "Vegetative": (40, 150), "Flowering": (150, 250), "Mature": (250, 365) }
#         else:  # Default crop
#             self.potential_yield_kg_per_ha = np.random.uniform(4000, 6000)
#             self.optimal_temp_min, self.optimal_temp_max = 18, 28
#             self.growth_stages = { "Seed": (0, 5), "Germination": (5, 12), "Vegetative": (12, 40), "Flowering": (40, 65), "Mature": (65, 90) }
        
#         # ENHANCED: Additional crop properties
#         self.stress_resistance = np.random.uniform(0.7, 0.9)
#         self.disease_resistance = np.random.uniform(0.8, 0.95)
#         self.consecutive_stress_days = 0

#     def apply_pesticide(self):
#         """Activates pesticide effect for a few days."""
#         self.pesticide_active_days = 4

#     def _calculate_disease_risks(self, soil: Soil, temperature: float, humidity: float):
#         """Calculates daily risk for all relevant diseases for the crop."""
#         self.disease_risks = {}
#         possible_diseases = PEST_DATABASE.get(self.crop_type, [])
        
#         for disease in possible_diseases:
#             conditions = disease["trigger_conditions"]
#             risk = 0.0
#             temp_is_risky = conditions["min_temp"] <= temperature <= conditions["max_temp"]
#             humidity_is_risky = (humidity * 100) >= conditions["min_humidity_pct"]
#             if temp_is_risky and humidity_is_risky:
#                 temp_range = conditions["max_temp"] - conditions["min_temp"]
#                 temp_risk = 1.0 - (abs(temperature - (conditions["min_temp"] + temp_range / 2)) / (temp_range / 2))
#                 humidity_risk = ((humidity * 100) - conditions["min_humidity_pct"]) / (100 - conditions["min_humidity_pct"])
#                 risk = (temp_risk + humidity_risk) / 2.0
#             if self.pesticide_active_days > 0:
#                 risk *= 0.1
#             self.disease_risks[disease["name"]] = min(1.0, risk)

#     def grow_one_day(self, soil: Soil, temperature: float, humidity: float = 0.6):
#         """Enhanced growth model with more realistic factors."""
#         self.age += 1
        
#         if self.pesticide_active_days > 0:
#             self.pesticide_active_days -= 1
        
#         self._calculate_disease_risks(soil, temperature, humidity)
        
#         water_stress, nutrient_stress = soil.get_stress_factors()
        
#         # ENHANCED: Temperature stress calculation
#         temp_stress = 0.0
#         if temperature < self.optimal_temp_min:
#             temp_stress = (self.optimal_temp_min - temperature) / 15.0
#         elif temperature > self.optimal_temp_max:
#             temp_stress = (temperature - self.optimal_temp_max) / 15.0
#         temp_stress = min(1.0, temp_stress)
        
#         # ENHANCED: Overall stress calculation
#         total_stress = (water_stress + nutrient_stress + temp_stress) / 3.0
        
#         # Track consecutive stress days
#         if total_stress > 0.3:
#             self.consecutive_stress_days += 1
#         else:
#             self.consecutive_stress_days = 0
            
#         # ENHANCED: Health changes based on stress and resistance
#         if total_stress > 0.5:
#             health_decline = total_stress * 8.0 * (1.0 - self.stress_resistance)
#             if self.consecutive_stress_days > 3:
#                 health_decline *= (1.0 + (self.consecutive_stress_days - 3) * 0.1)
#             self.health -= health_decline
#         elif total_stress < 0.2:
#             self.health += 1.5 * (1.0 - total_stress)
            
#         # Apply health penalty from the highest disease risk
#         highest_risk_today = 0.0
#         if self.disease_risks:
#             highest_risk_today = max(self.disease_risks.values())
#         if highest_risk_today > 0.2:
#             pest_damage = highest_risk_today * 5.0 * (1.0 - self.disease_resistance)
#             self.health -= pest_damage
            
#         self.health = max(0, min(100, self.health))
        
#         # ENHANCED: Growth factor calculation
#         growth_factor = 1.0 - total_stress
#         health_factor = self.health / 100.0
#         stage_modifier = self._get_stage_growth_modifier()
#         final_growth_factor = growth_factor * health_factor * stage_modifier
        
#         # Apply growth if in growing period
#         if self._is_growing_stage():
#             daily_potential_growth = self.max_potential_growth / 90
#             actual_growth = daily_potential_growth * final_growth_factor
#             self.accumulated_growth += actual_growth
        
#         self.height = (self.accumulated_growth / self.max_potential_growth) * self.max_height
        
#         # Update growth stage
#         self._update_growth_stage()

#     def _get_stage_growth_modifier(self):
#         """Get growth modifier based on current stage."""
#         stage_modifiers = { "Seed": 0.1, "Germination": 0.3, "Vegetative": 1.2, "Flowering": 0.8, "Mature": 0.2 }
#         return stage_modifiers.get(self.growth_stage, 1.0)

#     def _is_growing_stage(self):
#         """Check if crop is in a growing stage."""
#         return self.growth_stage in ["Germination", "Vegetative", "Flowering"]

#     def _update_growth_stage(self):
#         """Update growth stage based on age."""
#         max_age = list(self.growth_stages.values())[-1][-1]
#         for stage, (start_day, end_day) in self.growth_stages.items():
#             if start_day <= self.age < end_day:
#                 self.growth_stage = stage
#                 break
#         if self.age >= max_age:
#             self.growth_stage = "Mature"

#     def get_current_yield(self) -> float:
#         """Enhanced yield calculation with multiple factors."""
#         growth_ratio = min(1.0, self.accumulated_growth / self.max_potential_growth)
#         base_yield = self.potential_yield_kg_per_ha * growth_ratio
#         health_factor = (self.health / 100.0) ** 0.5
#         stage_bonus = 1.0
#         max_age = list(self.growth_stages.values())[-1][-1]
#         if self.growth_stage == "Mature" and self.age >= (max_age - 5):
#             stage_bonus = 1.1
#         final_yield = base_yield * health_factor * stage_bonus
#         return max(0, final_yield)

#     def get_growth_info(self):
#         """Get detailed growth information."""
#         return {
#             'stage': self.growth_stage, 'age': self.age, 'health': self.health,
#             'growth_progress': (self.accumulated_growth / self.max_potential_growth) * 100,
#             'stress_resistance': self.stress_resistance,
#             'consecutive_stress_days': self.consecutive_stress_days,
#             'potential_yield': self.potential_yield_kg_per_ha
#         }










# import numpy as np
# from .pest_database import PEST_DATABASE

# class Soil:
#     def __init__(self, soil_type: str, initial_moisture: float = None, deterministic: bool = False):
#         self.soil_type = soil_type
#         self.deterministic = deterministic
        
#         # ENHANCED: More realistic soil parameters
#         if soil_type == "Alluvial":
#             self.field_capacity = 0.8
#             self.wilting_point = 0.2
#             self.drainage_rate = 0.02  # Daily drainage coefficient
#             self.nutrient_retention = 0.95  # How well soil retains nutrients
#         elif soil_type == "Black":
#             self.field_capacity = 0.9
#             self.wilting_point = 0.22
#             self.drainage_rate = 0.015  # Better water retention
#             self.nutrient_retention = 0.97  # Excellent nutrient retention
#         else:  # Sandy or other
#             self.field_capacity = 0.75
#             self.wilting_point = 0.22
#             self.drainage_rate = 0.03  # Poor water retention
#             self.nutrient_retention = 0.92  # Poor nutrient retention
        
#         # IMPROVED: Consistent initialization for deterministic behavior
#         if initial_moisture is None:
#             if self.deterministic:
#                 # Fixed reasonable starting values for consistency
#                 self.moisture_content = (self.wilting_point + self.field_capacity) / 2.5  # Slightly below optimal
#             else:
#                 # Random initialization for training variety
#                 self.moisture_content = np.random.uniform(
#                     self.wilting_point + 0.1, 
#                     self.field_capacity - 0.1
#                 )
#         else:
#             self.moisture_content = initial_moisture
            
#         # IMPROVED: More consistent nitrogen starting levels
#         if self.deterministic:
#             self.nitrogen_level = 0.35  # Fixed reasonable starting level
#         else:
#             self.nitrogen_level = np.random.uniform(0.2, 0.5)
        
#         # IMPROVED: More consistent additional soil properties
#         if self.deterministic:
#             self.ph_level = 6.8  # Optimal pH for most crops
#             self.organic_matter = 0.4  # Good organic matter content
#             self.compaction_level = 0.2  # Moderate compaction
#         else:
#             self.ph_level = np.random.uniform(6.0, 7.5)  # Soil pH
#             self.organic_matter = np.random.uniform(0.2, 0.6)  # Organic matter content
#             self.compaction_level = np.random.uniform(0.1, 0.3)  # Soil compaction

#     def add_water(self, amount_mm: float):
#         """Enhanced water addition with drainage consideration."""
#         water_added = amount_mm / 1000.0
        
#         # ENHANCED: Consider soil compaction affecting water infiltration
#         infiltration_efficiency = 1.0 - (self.compaction_level * 0.3)
#         effective_water = water_added * infiltration_efficiency
        
#         self.moisture_content += effective_water
        
#         # ENHANCED: Natural drainage above field capacity
#         if self.moisture_content > self.field_capacity:
#             excess_water = self.moisture_content - self.field_capacity
#             drainage = excess_water * self.drainage_rate
#             self.moisture_content = self.field_capacity + (excess_water - drainage)

#     def daily_evaporation(self, temperature: float, humidity: float = 0.6):
#         """Enhanced evaporation model with humidity consideration."""
#         # ENHANCED: More sophisticated evaporation calculation
#         base_evaporation = max(0, (temperature - 10) / 400.0)  # Base evaporation rate
#         humidity_factor = (1.0 - humidity) * 1.2  # Lower humidity = more evaporation
#         moisture_factor = min(1.0, self.moisture_content / max(0.01, (self.wilting_point + 0.1)))
        
#         total_evaporation = base_evaporation * humidity_factor * moisture_factor
#         total_evaporation = max(0, min(0.1, total_evaporation))  # Cap maximum evaporation
        
#         self.moisture_content -= total_evaporation
#         self.moisture_content = max(0, self.moisture_content)

#     def add_fertilizer(self, amount_kg_per_ha: float):
#         """Enhanced fertilization with efficiency consideration."""
#         if amount_kg_per_ha <= 0:
#             return
            
#         # ENHANCED: Fertilizer efficiency depends on soil conditions
#         base_efficiency = 0.8  # 80% base efficiency
#         moisture_efficiency = 1.0
        
#         if self.moisture_content < self.wilting_point:
#             moisture_efficiency = 0.5  # Poor uptake in dry soil
#         elif self.moisture_content > self.field_capacity:
#             moisture_efficiency = 0.7  # Some leaching in waterlogged soil
            
#         ph_efficiency = 1.0
#         if not (6.0 <= self.ph_level <= 7.5):
#             ph_efficiency = 0.8  # Reduced efficiency outside optimal pH
            
#         total_efficiency = base_efficiency * moisture_efficiency * ph_efficiency
#         effective_fertilizer = (amount_kg_per_ha / 100.0) * total_efficiency
        
#         self.nitrogen_level += effective_fertilizer
#         self.nitrogen_level = min(1.0, self.nitrogen_level)

#     def daily_depletion(self):
#         """Enhanced nutrient depletion model."""
#         # ENHANCED: Depletion rate varies with soil type and conditions
#         base_depletion_rate = 0.008  # 0.8% base depletion (more conservative)
#         retention_factor = self.nutrient_retention
        
#         # Organic matter helps retain nutrients
#         organic_bonus = self.organic_matter * 0.02
#         final_retention = min(0.99, retention_factor + organic_bonus)
        
#         self.nitrogen_level *= (1.0 - base_depletion_rate + (base_depletion_rate * final_retention))
#         self.nitrogen_level = max(0, self.nitrogen_level)

#     def get_stress_factors(self):
#         """Get current stress factors for the crop."""
#         water_stress = 0.0
#         nutrient_stress = 0.0
        
#         if self.moisture_content < self.wilting_point:
#             water_stress = (self.wilting_point - self.moisture_content) / max(0.01, self.wilting_point)
#         elif self.moisture_content > self.field_capacity * 1.1:  # More tolerance for excess water
#             water_stress = (self.moisture_content - self.field_capacity * 1.1) * 0.5
            
#         if self.nitrogen_level < 0.25:  # Lower threshold for nutrient stress
#             nutrient_stress = (0.25 - self.nitrogen_level) / 0.25
#         elif self.nitrogen_level > 0.95:  # Higher threshold for over-fertilization
#             nutrient_stress = (self.nitrogen_level - 0.95) * 2.0
            
#         return min(1.0, water_stress), min(1.0, nutrient_stress)


# class Crop:
#     def __init__(self, crop_type: str, deterministic: bool = False):
#         self.crop_type = crop_type
#         self.growth_stage = "Seed"
#         self.deterministic = deterministic
        
#         # IMPROVED: More consistent initialization
#         if self.deterministic:
#             self.health = 95.0  # Fixed good starting health
#         else:
#             self.health = np.random.uniform(90, 100)  # Slight variation in initial health
            
#         self.age = 0
#         self.accumulated_growth = 0.0
#         self.max_potential_growth = 100.0
#         self.height = 0.0
#         self.max_height = 1.2
        
#         # --- NEW: Properties for the advanced pest model ---
#         self.disease_risks = {}
#         self.pesticide_active_days = 0
        
#         # ENHANCED: Crop-specific parameters for Wheat, Rice, and Sugarcane
#         if crop_type == "Wheat":
#             if self.deterministic:
#                 self.potential_yield_kg_per_ha = 5000  # Fixed for consistency
#             else:
#                 self.potential_yield_kg_per_ha = np.random.uniform(4500, 5500)
#             self.optimal_temp_min, self.optimal_temp_max = 15, 25
#             self.max_height = 1.2
#             self.growth_stages = { "Seed": (0, 7), "Germination": (7, 15), "Vegetative": (15, 45), "Flowering": (45, 70), "Mature": (70, 90) }
#         elif crop_type == "Rice":
#             if self.deterministic:
#                 self.potential_yield_kg_per_ha = 5750  # Fixed for consistency
#             else:
#                 self.potential_yield_kg_per_ha = np.random.uniform(5000, 6500)
#             self.optimal_temp_min, self.optimal_temp_max = 21, 37
#             self.max_height = 1.0
#             self.growth_stages = { "Seed": (0, 5), "Germination": (5, 15), "Vegetative": (15, 50), "Flowering": (50, 80), "Mature": (80, 110) }
#         elif crop_type == "Sugarcane":
#             if self.deterministic:
#                 self.potential_yield_kg_per_ha = 70000  # Fixed for consistency
#             else:
#                 self.potential_yield_kg_per_ha = np.random.uniform(60000, 80000)
#             self.optimal_temp_min, self.optimal_temp_max = 25, 35
#             self.max_height = 4.0
#             self.growth_stages = { "Seed": (0, 20), "Germination": (20, 40), "Vegetative": (40, 150), "Flowering": (150, 250), "Mature": (250, 365) }
#         else:  # Default crop
#             if self.deterministic:
#                 self.potential_yield_kg_per_ha = 5000  # Fixed for consistency
#             else:
#                 self.potential_yield_kg_per_ha = np.random.uniform(4000, 6000)
#             self.optimal_temp_min, self.optimal_temp_max = 18, 28
#             self.growth_stages = { "Seed": (0, 5), "Germination": (5, 12), "Vegetative": (12, 40), "Flowering": (40, 65), "Mature": (65, 90) }
        
#         # IMPROVED: More consistent additional crop properties
#         if self.deterministic:
#             self.stress_resistance = 0.8  # Fixed good resistance
#             self.disease_resistance = 0.88  # Fixed good disease resistance
#         else:
#             self.stress_resistance = np.random.uniform(0.7, 0.9)
#             self.disease_resistance = np.random.uniform(0.8, 0.95)
            
#         self.consecutive_stress_days = 0

#     def apply_pesticide(self):
#         """Activates pesticide effect for a few days."""
#         self.pesticide_active_days = 5  # Increased duration for better effectiveness

#     def _calculate_disease_risks(self, soil: Soil, temperature: float, humidity: float):
#         """Calculates daily risk for all relevant diseases for the crop."""
#         self.disease_risks = {}
#         possible_diseases = PEST_DATABASE.get(self.crop_type, [])
        
#         for disease in possible_diseases:
#             conditions = disease["trigger_conditions"]
#             risk = 0.0
#             temp_is_risky = conditions["min_temp"] <= temperature <= conditions["max_temp"]
#             humidity_is_risky = (humidity * 100) >= conditions["min_humidity_pct"]
            
#             if temp_is_risky and humidity_is_risky:
#                 temp_range = max(1, conditions["max_temp"] - conditions["min_temp"])
#                 temp_midpoint = conditions["min_temp"] + temp_range / 2
#                 temp_risk = 1.0 - (abs(temperature - temp_midpoint) / (temp_range / 2))
#                 temp_risk = max(0, min(1, temp_risk))
                
#                 humidity_range = max(1, 100 - conditions["min_humidity_pct"])
#                 humidity_risk = ((humidity * 100) - conditions["min_humidity_pct"]) / humidity_range
#                 humidity_risk = max(0, min(1, humidity_risk))
                
#                 risk = (temp_risk + humidity_risk) / 2.0
                
#             # Pesticide effectiveness
#             if self.pesticide_active_days > 0:
#                 risk *= 0.15  # Reduced risk when pesticide is active
                
#             self.disease_risks[disease["name"]] = min(1.0, max(0.0, risk))

#     def grow_one_day(self, soil: Soil, temperature: float, humidity: float = 0.6):
#         """Enhanced growth model with more realistic factors."""
#         self.age += 1
        
#         if self.pesticide_active_days > 0:
#             self.pesticide_active_days -= 1
        
#         self._calculate_disease_risks(soil, temperature, humidity)
        
#         water_stress, nutrient_stress = soil.get_stress_factors()
        
#         # ENHANCED: Temperature stress calculation
#         temp_stress = 0.0
#         if temperature < self.optimal_temp_min:
#             temp_stress = (self.optimal_temp_min - temperature) / 15.0
#         elif temperature > self.optimal_temp_max:
#             temp_stress = (temperature - self.optimal_temp_max) / 15.0
#         temp_stress = min(1.0, max(0.0, temp_stress))
        
#         # ENHANCED: Overall stress calculation with better weighting
#         total_stress = (water_stress * 0.4 + nutrient_stress * 0.3 + temp_stress * 0.3)
        
#         # Track consecutive stress days
#         if total_stress > 0.3:
#             self.consecutive_stress_days += 1
#         else:
#             self.consecutive_stress_days = max(0, self.consecutive_stress_days - 1)
            
#         # ENHANCED: Health changes based on stress and resistance
#         if total_stress > 0.4:
#             health_decline = total_stress * 6.0 * (1.0 - self.stress_resistance)
#             if self.consecutive_stress_days > 3:
#                 health_decline *= (1.0 + (self.consecutive_stress_days - 3) * 0.1)
#             self.health -= health_decline
#         elif total_stress < 0.2:
#             # Health recovery when conditions are good
#             recovery_rate = 1.2 * (1.0 - total_stress)
#             self.health += recovery_rate
            
#         # Apply health penalty from the highest disease risk
#         highest_risk_today = 0.0
#         if self.disease_risks:
#             highest_risk_today = max(self.disease_risks.values())
#         if highest_risk_today > 0.2:
#             pest_damage = highest_risk_today * 4.0 * (1.0 - self.disease_resistance)
#             self.health -= pest_damage
            
#         # Ensure health stays within bounds
#         self.health = max(0, min(100, self.health))
        
#         # ENHANCED: Growth factor calculation
#         growth_factor = max(0.1, 1.0 - total_stress)  # Minimum growth factor
#         health_factor = max(0.5, self.health / 100.0)  # Minimum health factor
#         stage_modifier = self._get_stage_growth_modifier()
#         final_growth_factor = growth_factor * health_factor * stage_modifier
        
#         # Apply growth if in growing period
#         if self._is_growing_stage():
#             # More consistent growth calculation
#             stage_duration = self._get_current_stage_duration()
#             daily_potential_growth = self.max_potential_growth / max(1, stage_duration * 2)  # Spread growth over stage duration
#             actual_growth = daily_potential_growth * final_growth_factor
#             self.accumulated_growth += actual_growth
        
#         # Update height based on growth
#         self.height = (self.accumulated_growth / self.max_potential_growth) * self.max_height
        
#         # Update growth stage
#         self._update_growth_stage()

#     def _get_current_stage_duration(self):
#         """Get the duration of the current growth stage."""
#         if self.growth_stage in self.growth_stages:
#             start_day, end_day = self.growth_stages[self.growth_stage]
#             return max(1, end_day - start_day)
#         return 30  # Default duration

#     def _get_stage_growth_modifier(self):
#         """Get growth modifier based on current stage."""
#         stage_modifiers = { 
#             "Seed": 0.1, 
#             "Germination": 0.4, 
#             "Vegetative": 1.5,  # Peak growth stage
#             "Flowering": 1.0, 
#             "Mature": 0.3 
#         }
#         return stage_modifiers.get(self.growth_stage, 1.0)

#     def _is_growing_stage(self):
#         """Check if crop is in a growing stage."""
#         return self.growth_stage in ["Germination", "Vegetative", "Flowering"]

#     def _update_growth_stage(self):
#         """Update growth stage based on age."""
#         max_age = list(self.growth_stages.values())[-1][-1]
#         for stage, (start_day, end_day) in self.growth_stages.items():
#             if start_day <= self.age < end_day:
#                 self.growth_stage = stage
#                 break
#         if self.age >= max_age:
#             self.growth_stage = "Mature"

#     def get_current_yield(self) -> float:
#         """Enhanced yield calculation with multiple factors."""
#         # Base yield from growth progress
#         growth_ratio = min(1.0, self.accumulated_growth / self.max_potential_growth)
#         base_yield = self.potential_yield_kg_per_ha * growth_ratio
        
#         # Health factor with diminishing returns
#         health_factor = (self.health / 100.0) ** 0.7  # Less harsh penalty
        
#         # Stage bonus for completing growth cycle
#         stage_bonus = 1.0
#         max_age = list(self.growth_stages.values())[-1][-1]
#         if self.growth_stage == "Mature" and self.age >= (max_age - 10):
#             stage_bonus = 1.15  # Bonus for reaching full maturity
#         elif self.growth_stage in ["Flowering", "Mature"]:
#             stage_bonus = 1.05  # Small bonus for reaching reproductive stages
        
#         # Age completion bonus
#         age_completion = min(1.0, self.age / max_age)
#         age_bonus = 1.0 + (age_completion * 0.1)  # Up to 10% bonus for age completion
        
#         final_yield = base_yield * health_factor * stage_bonus * age_bonus
#         return max(0, final_yield)

#     def get_growth_info(self):
#         """Get detailed growth information."""
#         return {
#             'stage': self.growth_stage, 
#             'age': self.age, 
#             'health': self.health,
#             'growth_progress': (self.accumulated_growth / self.max_potential_growth) * 100,
#             'stress_resistance': self.stress_resistance,
#             'consecutive_stress_days': self.consecutive_stress_days,
#             'potential_yield': self.potential_yield_kg_per_ha,
#             'height': self.height,
#             'disease_resistance': self.disease_resistance
#         }
























import numpy as np
from .pest_database import PEST_DATABASE

class Soil:
    def __init__(self, soil_type: str, initial_moisture: float = None, deterministic: bool = False):
        self.soil_type = soil_type
        self.deterministic = deterministic
        
        # ENHANCED: More realistic soil parameters
        if soil_type == "Alluvial":
            self.field_capacity = 0.8
            self.wilting_point = 0.2
            self.drainage_rate = 0.02  # Daily drainage coefficient
            self.nutrient_retention = 0.95  # How well soil retains nutrients
        elif soil_type == "Black":
            self.field_capacity = 0.9
            self.wilting_point = 0.22
            self.drainage_rate = 0.015  # Better water retention
            self.nutrient_retention = 0.97  # Excellent nutrient retention
        else:  # Sandy or other
            self.field_capacity = 0.75
            self.wilting_point = 0.22
            self.drainage_rate = 0.03  # Poor water retention
            self.nutrient_retention = 0.92  # Poor nutrient retention
        
        # IMPROVED: Consistent initialization for deterministic behavior
        if initial_moisture is None:
            if self.deterministic:
                # Fixed reasonable starting values for consistency
                self.moisture_content = (self.wilting_point + self.field_capacity) / 2.5  # Slightly below optimal
            else:
                # Random initialization for training variety
                self.moisture_content = np.random.uniform(
                    self.wilting_point + 0.1, 
                    self.field_capacity - 0.1
                )
        else:
            self.moisture_content = initial_moisture
            
        # IMPROVED: More realistic nitrogen starting levels (depleted soil)
        if self.deterministic:
            self.nitrogen_level = 0.15  # Fixed realistic depleted soil level
        else:
            self.nitrogen_level = np.random.uniform(0.12, 0.18)  # Realistic range for depleted soils
        
        # IMPROVED: More consistent additional soil properties
        if self.deterministic:
            self.ph_level = 6.8  # Optimal pH for most crops
            self.organic_matter = 0.4  # Good organic matter content
            self.compaction_level = 0.2  # Moderate compaction
        else:
            self.ph_level = np.random.uniform(6.0, 7.5)  # Soil pH
            self.organic_matter = np.random.uniform(0.2, 0.6)  # Organic matter content
            self.compaction_level = np.random.uniform(0.1, 0.3)  # Soil compaction

    def add_water(self, amount_mm: float):
        """Enhanced water addition with drainage consideration."""
        water_added = amount_mm / 1000.0
        
        # ENHANCED: Consider soil compaction affecting water infiltration
        infiltration_efficiency = 1.0 - (self.compaction_level * 0.3)
        effective_water = water_added * infiltration_efficiency
        
        self.moisture_content += effective_water
        
        # ENHANCED: Natural drainage above field capacity
        if self.moisture_content > self.field_capacity:
            excess_water = self.moisture_content - self.field_capacity
            drainage = excess_water * self.drainage_rate
            self.moisture_content = self.field_capacity + (excess_water - drainage)

    def daily_evaporation(self, temperature: float, humidity: float = 0.6):
        """Enhanced evaporation model with humidity consideration."""
        # ENHANCED: More sophisticated evaporation calculation
        base_evaporation = max(0, (temperature - 10) / 400.0)  # Base evaporation rate
        humidity_factor = (1.0 - humidity) * 1.2  # Lower humidity = more evaporation
        moisture_factor = min(1.0, self.moisture_content / max(0.01, (self.wilting_point + 0.1)))
        
        total_evaporation = base_evaporation * humidity_factor * moisture_factor
        total_evaporation = max(0, min(0.1, total_evaporation))  # Cap maximum evaporation
        
        self.moisture_content -= total_evaporation
        self.moisture_content = max(0, self.moisture_content)

    def add_fertilizer(self, amount_kg_per_ha: float):
        """Enhanced fertilization with efficiency consideration."""
        if amount_kg_per_ha <= 0:
            return
            
        # ENHANCED: Fertilizer efficiency depends on soil conditions
        base_efficiency = 0.8  # 80% base efficiency
        moisture_efficiency = 1.0
        
        if self.moisture_content < self.wilting_point:
            moisture_efficiency = 0.5  # Poor uptake in dry soil
        elif self.moisture_content > self.field_capacity:
            moisture_efficiency = 0.7  # Some leaching in waterlogged soil
            
        ph_efficiency = 1.0
        if not (6.0 <= self.ph_level <= 7.5):
            ph_efficiency = 0.8  # Reduced efficiency outside optimal pH
            
        total_efficiency = base_efficiency * moisture_efficiency * ph_efficiency
        effective_fertilizer = (amount_kg_per_ha / 100.0) * total_efficiency
        
        self.nitrogen_level += effective_fertilizer
        self.nitrogen_level = min(1.0, self.nitrogen_level)

    def daily_depletion(self, crop_stage="Vegetative"):
        """Enhanced nutrient depletion model with stage-specific rates."""
        # Stage-specific depletion rates (more realistic)
        stage_depletion_rates = {
            "Seed": 0.005,         # 0.5% - minimal depletion
            "Germination": 0.008,  # 0.8% - moderate depletion  
            "Vegetative": 0.015,   # 1.5% - high depletion during growth
            "Flowering": 0.012,    # 1.2% - high depletion during reproduction
            "Mature": 0.003        # 0.3% - minimal depletion at maturity
        }
        
        base_depletion_rate = stage_depletion_rates.get(crop_stage, 0.01)
        retention_factor = self.nutrient_retention
        
        # Organic matter helps retain nutrients
        organic_bonus = self.organic_matter * 0.02
        final_retention = min(0.99, retention_factor + organic_bonus)
        
        self.nitrogen_level *= (1.0 - base_depletion_rate + (base_depletion_rate * final_retention))
        self.nitrogen_level = max(0, self.nitrogen_level)

    def get_stress_factors(self):
        """Get current stress factors for the crop."""
        water_stress = 0.0
        nutrient_stress = 0.0
        
        if self.moisture_content < self.wilting_point:
            water_stress = (self.wilting_point - self.moisture_content) / max(0.01, self.wilting_point)
        elif self.moisture_content > self.field_capacity * 1.1:  # More tolerance for excess water
            water_stress = (self.moisture_content - self.field_capacity * 1.1) * 0.5
            
        if self.nitrogen_level < 0.25:  # Lower threshold for nutrient stress
            nutrient_stress = (0.25 - self.nitrogen_level) / 0.25
        elif self.nitrogen_level > 0.95:  # Higher threshold for over-fertilization
            nutrient_stress = (self.nitrogen_level - 0.95) * 2.0
            
        return min(1.0, water_stress), min(1.0, nutrient_stress)


class Crop:
    def __init__(self, crop_type: str, deterministic: bool = False):
        self.crop_type = crop_type
        self.growth_stage = "Seed"
        self.deterministic = deterministic
        
        # IMPROVED: More consistent initialization
        if self.deterministic:
            self.health = 95.0  # Fixed good starting health
        else:
            self.health = np.random.uniform(90, 100)  # Slight variation in initial health
            
        self.age = 0
        self.accumulated_growth = 0.0
        self.max_potential_growth = 100.0
        self.height = 0.0
        self.max_height = 1.2
        
        # --- NEW: Properties for the advanced pest model ---
        self.disease_risks = {}
        self.pesticide_active_days = 0
        
        # ENHANCED: Crop-specific parameters for Wheat, Rice, and Sugarcane
        if crop_type == "Wheat":
            if self.deterministic:
                self.potential_yield_kg_per_ha = 5000  # Fixed for consistency
            else:
                self.potential_yield_kg_per_ha = np.random.uniform(4500, 5500)
            self.optimal_temp_min, self.optimal_temp_max = 15, 25
            self.max_height = 1.2
            self.growth_stages = { "Seed": (0, 7), "Germination": (7, 15), "Vegetative": (15, 45), "Flowering": (45, 70), "Mature": (70, 90) }
        elif crop_type == "Rice":
            if self.deterministic:
                self.potential_yield_kg_per_ha = 5750  # Fixed for consistency
            else:
                self.potential_yield_kg_per_ha = np.random.uniform(5000, 6500)
            self.optimal_temp_min, self.optimal_temp_max = 21, 37
            self.max_height = 1.0
            self.growth_stages = { "Seed": (0, 5), "Germination": (5, 15), "Vegetative": (15, 50), "Flowering": (50, 80), "Mature": (80, 110) }
        elif crop_type == "Sugarcane":
            if self.deterministic:
                self.potential_yield_kg_per_ha = 70000  # Fixed for consistency
            else:
                self.potential_yield_kg_per_ha = np.random.uniform(60000, 80000)
            self.optimal_temp_min, self.optimal_temp_max = 25, 35
            self.max_height = 4.0
            self.growth_stages = { "Seed": (0, 20), "Germination": (20, 40), "Vegetative": (40, 150), "Flowering": (150, 250), "Mature": (250, 365) }
        else:  # Default crop
            if self.deterministic:
                self.potential_yield_kg_per_ha = 5000  # Fixed for consistency
            else:
                self.potential_yield_kg_per_ha = np.random.uniform(4000, 6000)
            self.optimal_temp_min, self.optimal_temp_max = 18, 28
            self.growth_stages = { "Seed": (0, 5), "Germination": (5, 12), "Vegetative": (12, 40), "Flowering": (40, 65), "Mature": (65, 90) }
        
        # IMPROVED: More consistent additional crop properties
        if self.deterministic:
            self.stress_resistance = 0.8  # Fixed good resistance
            self.disease_resistance = 0.88  # Fixed good disease resistance
        else:
            self.stress_resistance = np.random.uniform(0.7, 0.9)
            self.disease_resistance = np.random.uniform(0.8, 0.95)
            
        self.consecutive_stress_days = 0

    def apply_pesticide(self):
        """Activates pesticide effect for a few days."""
        self.pesticide_active_days = 5  # Increased duration for better effectiveness

    def _calculate_disease_risks(self, soil: Soil, temperature: float, humidity: float):
        """Calculates daily risk for all relevant diseases for the crop."""
        self.disease_risks = {}
        possible_diseases = PEST_DATABASE.get(self.crop_type, [])
        
        # REALISTIC: Baseline disease risk always present (fungi/bacteria in environment)
        baseline_risk = 0.008  # 0.8% minimum risk
        
        for disease in possible_diseases:
            conditions = disease["trigger_conditions"]
            risk = baseline_risk  # Start with baseline
            temp_is_risky = conditions["min_temp"] <= temperature <= conditions["max_temp"]
            humidity_is_risky = (humidity * 100) >= conditions["min_humidity_pct"]
            
            if temp_is_risky and humidity_is_risky:
                temp_range = max(1, conditions["max_temp"] - conditions["min_temp"])
                temp_midpoint = conditions["min_temp"] + temp_range / 2
                temp_risk = 1.0 - (abs(temperature - temp_midpoint) / (temp_range / 2))
                temp_risk = max(0, min(1, temp_risk))
                
                humidity_range = max(1, 100 - conditions["min_humidity_pct"])
                humidity_risk = ((humidity * 100) - conditions["min_humidity_pct"]) / humidity_range
                humidity_risk = max(0, min(1, humidity_risk))
                
                calculated_risk = (temp_risk + humidity_risk) / 2.0
                risk = max(baseline_risk, calculated_risk)
                
            # Pesticide effectiveness (but never eliminates all risk)
            if self.pesticide_active_days > 0:
                risk = max(baseline_risk * 0.3, risk * 0.15)  # Minimum 0.24% even with pesticide
                
            self.disease_risks[disease["name"]] = min(1.0, max(baseline_risk, risk))

    def grow_one_day(self, soil: Soil, temperature: float, humidity: float = 0.6):
        """Enhanced growth model with more realistic factors."""
        self.age += 1
        
        if self.pesticide_active_days > 0:
            self.pesticide_active_days -= 1
        
        self._calculate_disease_risks(soil, temperature, humidity)
        
        water_stress, nutrient_stress = soil.get_stress_factors()
        
        # ENHANCED: Temperature stress calculation
        temp_stress = 0.0
        if temperature < self.optimal_temp_min:
            temp_stress = (self.optimal_temp_min - temperature) / 15.0
        elif temperature > self.optimal_temp_max:
            temp_stress = (temperature - self.optimal_temp_max) / 15.0
        temp_stress = min(1.0, max(0.0, temp_stress))
        
        # ENHANCED: Overall stress calculation with better weighting
        total_stress = (water_stress * 0.4 + nutrient_stress * 0.3 + temp_stress * 0.3)
        
        # Track consecutive stress days
        if total_stress > 0.3:
            self.consecutive_stress_days += 1
        else:
            self.consecutive_stress_days = max(0, self.consecutive_stress_days - 1)
            
        # ENHANCED: Health changes based on stress and resistance
        if total_stress > 0.4:
            health_decline = total_stress * 6.0 * (1.0 - self.stress_resistance)
            if self.consecutive_stress_days > 3:
                health_decline *= (1.0 + (self.consecutive_stress_days - 3) * 0.1)
            self.health -= health_decline
        elif total_stress < 0.2:
            # Health recovery when conditions are good
            recovery_rate = 1.2 * (1.0 - total_stress)
            self.health += recovery_rate
            
        # Apply health penalty from the highest disease risk
        highest_risk_today = 0.0
        if self.disease_risks:
            highest_risk_today = max(self.disease_risks.values())
        if highest_risk_today > 0.2:
            pest_damage = highest_risk_today * 4.0 * (1.0 - self.disease_resistance)
            self.health -= pest_damage
            
        # Ensure health stays within bounds
        self.health = max(0, min(100, self.health))
        
        # ENHANCED: Growth factor calculation
        growth_factor = max(0.1, 1.0 - total_stress)  # Minimum growth factor
        health_factor = max(0.5, self.health / 100.0)  # Minimum health factor
        stage_modifier = self._get_stage_growth_modifier()
        final_growth_factor = growth_factor * health_factor * stage_modifier
        
        # Apply growth if in growing period
        if self._is_growing_stage():
            # More consistent growth calculation
            stage_duration = self._get_current_stage_duration()
            daily_potential_growth = self.max_potential_growth / max(1, stage_duration * 2)  # Spread growth over stage duration
            actual_growth = daily_potential_growth * final_growth_factor
            self.accumulated_growth += actual_growth
        
        # Update height based on growth
        self.height = (self.accumulated_growth / self.max_potential_growth) * self.max_height
        
        # Update growth stage
        self._update_growth_stage()

    def _get_current_stage_duration(self):
        """Get the duration of the current growth stage."""
        if self.growth_stage in self.growth_stages:
            start_day, end_day = self.growth_stages[self.growth_stage]
            return max(1, end_day - start_day)
        return 30  # Default duration

    def _get_stage_growth_modifier(self):
        """Get growth modifier based on current stage."""
        stage_modifiers = { 
            "Seed": 0.1, 
            "Germination": 0.4, 
            "Vegetative": 1.5,  # Peak growth stage
            "Flowering": 1.0, 
            "Mature": 0.3 
        }
        return stage_modifiers.get(self.growth_stage, 1.0)

    def _is_growing_stage(self):
        """Check if crop is in a growing stage."""
        return self.growth_stage in ["Germination", "Vegetative", "Flowering"]

    def _update_growth_stage(self):
        """Update growth stage based on age."""
        max_age = list(self.growth_stages.values())[-1][-1]
        for stage, (start_day, end_day) in self.growth_stages.items():
            if start_day <= self.age < end_day:
                self.growth_stage = stage
                break
        if self.age >= max_age:
            self.growth_stage = "Mature"

    def get_current_yield(self, total_season_fertilizer: float = 0) -> float:
        """Enhanced yield calculation with fertilizer requirements."""
        # Base yield from growth progress
        growth_ratio = min(1.0, self.accumulated_growth / self.max_potential_growth)
        base_yield = self.potential_yield_kg_per_ha * growth_ratio
        
        # Health factor with diminishing returns
        health_factor = (self.health / 100.0) ** 0.7  # Less harsh penalty
        
        # REALISTIC: Fertilizer requirement for high yields
        fertilizer_factor = 1.0
        if total_season_fertilizer < 40:
            # Severe penalty for very low fertilizer
            fertilizer_factor = 0.4 + (total_season_fertilizer / 40.0) * 0.35  # 40-75% of potential
        elif total_season_fertilizer < 80:
            # Moderate penalty for low fertilizer  
            fertilizer_factor = 0.75 + ((total_season_fertilizer - 40) / 40.0) * 0.15  # 75-90% of potential
        elif total_season_fertilizer < 120:
            # Good fertilizer range
            fertilizer_factor = 0.90 + ((total_season_fertilizer - 80) / 40.0) * 0.10  # 90-100% of potential
        else:
            # Diminishing returns for excessive fertilizer
            excess = total_season_fertilizer - 120
            fertilizer_factor = 1.0 - (excess / 200.0) * 0.1  # Slight penalty for over-fertilization
            fertilizer_factor = max(0.9, fertilizer_factor)
        
        # Stage bonus for completing growth cycle
        stage_bonus = 1.0
        max_age = list(self.growth_stages.values())[-1][-1]
        if self.growth_stage == "Mature" and self.age >= (max_age - 10):
            stage_bonus = 1.15  # Bonus for reaching full maturity
        elif self.growth_stage in ["Flowering", "Mature"]:
            stage_bonus = 1.05  # Small bonus for reaching reproductive stages
        
        # Age completion bonus
        age_completion = min(1.0, self.age / max_age)
        age_bonus = 1.0 + (age_completion * 0.1)  # Up to 10% bonus for age completion
        
        # REALISTIC: Always some yield loss from unavoidable stresses (weather, minor pests)
        unavoidable_loss_factor = np.random.uniform(0.95, 0.98) if not self.deterministic else 0.97
        
        final_yield = base_yield * health_factor * fertilizer_factor * stage_bonus * age_bonus * unavoidable_loss_factor
        return max(0, final_yield)

    def get_growth_info(self):
        """Get detailed growth information."""
        return {
            'stage': self.growth_stage, 
            'age': self.age, 
            'health': self.health,
            'growth_progress': (self.accumulated_growth / self.max_potential_growth) * 100,
            'stress_resistance': self.stress_resistance,
            'consecutive_stress_days': self.consecutive_stress_days,
            'potential_yield': self.potential_yield_kg_per_ha,
            'height': self.height,
            'disease_resistance': self.disease_resistance
        }